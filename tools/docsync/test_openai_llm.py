from __future__ import annotations

import importlib
import io
import json
import os
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from tools.docsync import openai_llm

DOCSYNC_DIR = Path(__file__).resolve().parent
if str(DOCSYNC_DIR) not in sys.path:
    sys.path.insert(0, str(DOCSYNC_DIR))


def fake_response(payload: dict, *, status: str = "completed"):
    return SimpleNamespace(
        status=status,
        incomplete_details=None,
        output_text=json.dumps(payload),
        usage=SimpleNamespace(
            input_tokens=11,
            output_tokens=7,
            output_tokens_details=SimpleNamespace(reasoning_tokens=3),
        ),
    )


class FakeResponses:
    def __init__(self, responses):
        self._responses = iter(responses)
        self.create_calls: list[dict] = []
        self.stream_calls: list[dict] = []

    def create(self, **kwargs):
        self.create_calls.append(kwargs)
        result = next(self._responses)
        if isinstance(result, Exception):
            raise result
        return result

    def stream(self, **kwargs):
        self.stream_calls.append(kwargs)
        response = next(self._responses)
        return FakeStream(response)


class FakeStream:
    def __init__(self, response):
        self.response = response

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return None

    def __iter__(self):
        yield SimpleNamespace(type="response.output_text.delta", delta='{"ok"')
        yield SimpleNamespace(type="response.output_text.delta", delta=": true}")

    def get_final_response(self):
        return self.response


class FakeIncompleteStream(FakeStream):
    def __iter__(self):
        yield SimpleNamespace(type="response.incomplete", response=self.response)

    def get_final_response(self):
        raise RuntimeError("Didn't receive a response.completed event.")


class FakeIncompleteResponses(FakeResponses):
    def stream(self, **kwargs):
        self.stream_calls.append(kwargs)
        return FakeIncompleteStream(next(self._responses))


class FakeClient:
    def __init__(self, responses):
        self.responses = FakeResponses(responses)


class OpenAILLMTests(unittest.TestCase):
    schema = openai_llm.strict_object_schema({"ok": {"type": "boolean"}})

    def call(self, client, **overrides):
        args = {
            "system_prompt": "system",
            "user_text": "user",
            "schema_name": "test_output",
            "schema": self.schema,
            "max_output_tokens": 100,
            "model": "gpt-5.6-sol",
        }
        args.update(overrides)
        return openai_llm.call_json(client, **args)

    def test_non_streaming_request_uses_responses_and_strict_schema(self):
        client = FakeClient([fake_response({"ok": True})])
        with patch.dict(os.environ, {"OPENAI_REASONING_EFFORT": "high"}):
            parsed, usage = self.call(client)

        self.assertEqual(parsed, {"ok": True})
        self.assertEqual(usage["reasoning_tokens"], 3)
        self.assertEqual(usage["response_status"], "completed")
        request = client.responses.create_calls[0]
        self.assertEqual(request["model"], "gpt-5.6-sol")
        self.assertEqual(request["instructions"], "system")
        self.assertEqual(request["input"], "user")
        self.assertEqual(request["reasoning"], {"effort": "high"})
        self.assertFalse(request["store"])
        self.assertEqual(request["text"]["format"]["type"], "json_schema")
        self.assertTrue(request["text"]["format"]["strict"])
        self.assertEqual(request["text"]["format"]["schema"], self.schema)

    def test_installed_openai_sdk_serializes_responses_request(self):
        import httpx
        from openai import OpenAI

        captured = {}

        def handle(request):
            captured.update(json.loads(request.content))
            return httpx.Response(
                200,
                json={
                    "id": "resp_test",
                    "object": "response",
                    "created_at": 0,
                    "status": "completed",
                    "model": "gpt-5.6-sol",
                    "output": [{
                        "id": "msg_test",
                        "type": "message",
                        "role": "assistant",
                        "status": "completed",
                        "content": [{
                            "type": "output_text",
                            "text": '{"ok": true}',
                            "annotations": [],
                        }],
                    }],
                    "parallel_tool_calls": True,
                    "tool_choice": "auto",
                    "tools": [],
                    "usage": {
                        "input_tokens": 1,
                        "input_tokens_details": {"cached_tokens": 0},
                        "output_tokens": 1,
                        "output_tokens_details": {"reasoning_tokens": 0},
                        "total_tokens": 2,
                    },
                },
            )

        http_client = httpx.Client(transport=httpx.MockTransport(handle))
        client = OpenAI(
            api_key="test",
            base_url="https://openai.invalid/v1",
            http_client=http_client,
        )
        try:
            with patch.dict(os.environ, {"OPENAI_REASONING_EFFORT": "max"}):
                parsed, _usage = self.call(client)
        finally:
            client.close()

        self.assertEqual(parsed, {"ok": True})
        self.assertEqual(captured["reasoning"], {"effort": "max"})
        self.assertEqual(captured["text"]["format"]["type"], "json_schema")
        self.assertFalse(captured["store"])

    def test_non_gpt_model_omits_default_reasoning_parameter(self):
        client = FakeClient([fake_response({"ok": True})])
        with patch.dict(os.environ, {}, clear=True):
            self.call(client, model="gpt-4.1")
        self.assertNotIn("reasoning", client.responses.create_calls[0])

    def test_arbitrary_gpt_5_override_omits_default_reasoning_parameter(self):
        client = FakeClient([fake_response({"ok": True})])
        with patch.dict(os.environ, {}, clear=True):
            self.call(client, model="gpt-5.4")
        self.assertNotIn("reasoning", client.responses.create_calls[0])

    def test_explicit_default_omits_reasoning_parameter(self):
        client = FakeClient([fake_response({"ok": True})])
        with patch.dict(os.environ, {"OPENAI_REASONING_EFFORT": "default"}):
            self.call(client)
        self.assertNotIn("reasoning", client.responses.create_calls[0])

    def test_invalid_reasoning_effort_fails_before_request(self):
        client = FakeClient([fake_response({"ok": True})])
        with patch.dict(os.environ, {"OPENAI_REASONING_EFFORT": "extreme"}):
            with self.assertRaisesRegex(ValueError, "invalid OPENAI_REASONING_EFFORT"):
                self.call(client)
        self.assertEqual(client.responses.create_calls, [])

    def test_retries_then_returns_structured_output(self):
        client = FakeClient([RuntimeError("temporary"), fake_response({"ok": True})])
        with patch.dict(os.environ, {}, clear=True):
            parsed, _usage = self.call(client, retries=2)
        self.assertEqual(parsed, {"ok": True})
        self.assertEqual(len(client.responses.create_calls), 2)

    def test_incomplete_response_is_rejected(self):
        response = fake_response({"ok": True}, status="incomplete")
        response.incomplete_details = SimpleNamespace(reason="max_output_tokens")
        client = FakeClient([response, fake_response({"ok": True})])
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaisesRegex(RuntimeError, "max_output_tokens"):
                self.call(client, retries=2)
        self.assertEqual(len(client.responses.create_calls), 1)

    def test_retryable_terminal_response_is_retried(self):
        failed = fake_response({"ok": True}, status="failed")
        failed.error = SimpleNamespace(code="server_error", message="try again")
        client = FakeClient([failed, fake_response({"ok": True})])
        with patch.dict(os.environ, {}, clear=True):
            parsed, _usage = self.call(client, retries=2)
        self.assertEqual(parsed, {"ok": True})
        self.assertEqual(len(client.responses.create_calls), 2)

    def test_streaming_incomplete_response_keeps_diagnostic(self):
        response = fake_response({"ok": True}, status="incomplete")
        response.incomplete_details = SimpleNamespace(reason="max_output_tokens")
        client = FakeClient([])
        client.responses = FakeIncompleteResponses([response])
        with patch.dict(os.environ, {}, clear=True), redirect_stdout(io.StringIO()):
            with self.assertRaisesRegex(RuntimeError, "max_output_tokens"):
                self.call(client, stream=True)

    def test_refusal_text_is_reported(self):
        response = fake_response({"ok": True})
        response.output_text = ""
        refusal = SimpleNamespace(type="refusal", refusal="policy blocked")
        response.output = [SimpleNamespace(content=[refusal])]
        client = FakeClient([response])
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaisesRegex(RuntimeError, "policy blocked"):
                self.call(client)

    def test_streaming_uses_final_response(self):
        client = FakeClient([fake_response({"ok": True})])
        output = io.StringIO()
        with patch.dict(os.environ, {}, clear=True), redirect_stdout(output):
            parsed, _usage = self.call(client, stream=True)
        self.assertEqual(parsed, {"ok": True})
        self.assertEqual(len(client.responses.stream_calls), 1)
        self.assertIn("12 chars", output.getvalue())

    def test_all_workflow_output_schemas_are_strict(self):
        import acl_sync
        import compat_sync
        import docs_sync
        import flags_sync

        schemas = [
            acl_sync.LLM_REPAIR_SCHEMA,
            compat_sync.REVIEW_SCHEMA,
            docs_sync.DISCOVER_SCHEMA,
            docs_sync.UPDATE_SCHEMA,
            flags_sync.POLISH_SCHEMA,
        ]

        def check(schema):
            if schema.get("type") == "object":
                properties = schema.get("properties", {})
                self.assertFalse(schema.get("additionalProperties", True))
                self.assertEqual(set(schema.get("required", [])), set(properties))
                for value in properties.values():
                    check(value)
            if schema.get("type") == "array":
                check(schema["items"])
            for option in schema.get("anyOf", []):
                check(option)

        for schema in schemas:
            check(schema)

    def test_workflows_support_package_imports(self):
        from tools.docsync import acl_sync
        from tools.docsync import compat_sync
        from tools.docsync import docs_sync
        from tools.docsync import flags_sync

        self.assertTrue(acl_sync.LLM_REPAIR_SCHEMA)
        self.assertTrue(compat_sync.REVIEW_SCHEMA)
        self.assertTrue(docs_sync.DISCOVER_SCHEMA)
        self.assertTrue(flags_sync.POLISH_SCHEMA)

    def test_workflow_model_defaults_preserve_quality_and_bulk_roles(self):
        import acl_sync
        import compat_sync
        import docs_sync
        import flags_sync

        with patch.dict(os.environ, {}, clear=True):
            acl_sync = importlib.reload(acl_sync)
            compat_sync = importlib.reload(compat_sync)
            docs_sync = importlib.reload(docs_sync)
            flags_sync = importlib.reload(flags_sync)

            self.assertEqual(flags_sync.MODEL, "gpt-5.6-sol")
            self.assertEqual(docs_sync.UPDATE_MODEL, "gpt-5.6-sol")
            self.assertEqual(docs_sync.DISCOVER_MODEL, "gpt-5.6-terra")
            self.assertEqual(acl_sync.LLM_REPAIR_MODEL, "gpt-5.6-terra")
            args = compat_sync.add_cli_args().parse_args([])
            self.assertEqual(args.review_model, "gpt-5.6-terra")

    def test_compat_review_fails_fast_without_api_key(self):
        import compat_sync

        stderr = io.StringIO()
        argv = ["compat_sync.py", "--review"]
        with (
            patch.dict(os.environ, {}, clear=True),
            patch.object(sys, "argv", argv),
            redirect_stdout(io.StringIO()),
            patch("sys.stderr", stderr),
        ):
            self.assertEqual(compat_sync.main(), 2)
        self.assertIn("--review requires OPENAI_API_KEY", stderr.getvalue())

    def test_compat_review_records_api_failure_without_treating_it_as_agreement(self):
        import compat_sync

        row = compat_sync.CompatRow("String", "GET", "supported")
        assessment = compat_sync.Assessment(row, "supported", "")
        dragonfly_source = SimpleNamespace(handler_impl=lambda _command: "")
        with (
            patch.object(
                compat_sync, "_call_openai_json", side_effect=RuntimeError("boom"),
            ),
            redirect_stdout(io.StringIO()),
        ):
            flags, errors = compat_sync.review_assessments(
                [assessment], {}, dragonfly_source, "gpt-5.6-terra", 1, 0,
            )

        self.assertEqual(flags, [])
        self.assertEqual(assessment.review, {"error": "boom"})
        self.assertEqual(errors, [{
            "type": "review-error",
            "command": "GET",
            "family": "String",
            "status": "supported",
            "message": "boom",
        }])

    def test_compat_review_keeps_flags_when_another_call_fails(self):
        import compat_sync

        assessments = [
            compat_sync.Assessment(
                compat_sync.CompatRow("String", command, "supported"), "supported", "",
            )
            for command in ("GET", "SET")
        ]
        dragonfly_source = SimpleNamespace(handler_impl=lambda _command: "")

        def review_response(_system, user, _model):
            if json.loads(user)["command"] == "SET":
                raise RuntimeError("temporary failure")
            return {
                "agree": False,
                "concern": "GET implementation needs human verification.",
                "suggested_status": "partial",
            }

        with (
            patch.object(compat_sync, "_call_openai_json", side_effect=review_response),
            redirect_stdout(io.StringIO()),
        ):
            flags, errors = compat_sync.review_assessments(
                assessments, {}, dragonfly_source, "gpt-5.6-terra", 2, 0,
            )

        self.assertEqual([flag["command"] for flag in flags], ["GET"])
        self.assertEqual([error["command"] for error in errors], ["SET"])
        self.assertFalse(assessments[0].review["agree"])
        self.assertEqual(assessments[1].review, {"error": "temporary failure"})

    def test_compat_review_reports_empty_exception_message(self):
        import compat_sync

        assessment = compat_sync.Assessment(
            compat_sync.CompatRow("String", "GET", "supported"), "supported", "",
        )
        with (
            patch.object(compat_sync, "_call_openai_json", side_effect=Exception()),
            redirect_stdout(io.StringIO()),
        ):
            _flags, errors = compat_sync.review_assessments(
                [assessment], {}, SimpleNamespace(handler_impl=lambda _command: ""),
                "gpt-5.6-terra", 1, 0,
            )

        self.assertEqual(errors[0]["message"], "Exception")

    def test_compat_review_rejects_disagreement_without_concern(self):
        import compat_sync

        assessment = compat_sync.Assessment(
            compat_sync.CompatRow("String", "GET", "supported"), "supported", "",
        )
        response = {"agree": False, "concern": "", "suggested_status": "partial"}
        with (
            patch.object(compat_sync, "_call_openai_json", return_value=response),
            redirect_stdout(io.StringIO()),
        ):
            flags, errors = compat_sync.review_assessments(
                [assessment], {}, SimpleNamespace(handler_impl=lambda _command: ""),
                "gpt-5.6-terra", 1, 0,
            )

        self.assertEqual(flags, [])
        self.assertEqual(
            errors[0]["message"], "Model returned agree=false without a concern.",
        )


if __name__ == "__main__":
    unittest.main()
