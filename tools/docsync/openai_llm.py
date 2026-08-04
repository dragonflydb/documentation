"""Shared OpenAI Responses API helpers for docsync scripts.

The docsync tools are intentionally one-shot: each request receives all of its
grounding in ``instructions`` and ``input`` and returns one strict JSON object.
Keeping the provider-specific code here makes the sync logic and its validators
independent from the OpenAI SDK response shape.
"""

from __future__ import annotations

import json
import os
from typing import Any


DEFAULT_QUALITY_MODEL = "gpt-5.6-sol"
DEFAULT_BALANCED_MODEL = "gpt-5.6-terra"
DEFAULT_REASONING_EFFORT = "medium"

_REASONING_EFFORTS = {
    "none", "low", "medium", "high", "xhigh", "max",
}
_OMIT_REASONING_VALUES = {"default", "omit"}
_RETRYABLE_RESPONSE_CODES = {
    "server_error", "rate_limit_exceeded", "vector_store_timeout",
}


class OpenAIResponseError(RuntimeError):
    """A completed API exchange that cannot produce the requested JSON output."""


def configured_model(default: str = DEFAULT_QUALITY_MODEL) -> str:
    """Return the global model override or the workflow's recommended default."""
    return os.getenv("OPENAI_MODEL", "").strip() or default


def configured_reasoning_effort(model: str) -> str | None:
    """Return the requested effort, or ``None`` to use the model default.

    ``OPENAI_REASONING_EFFORT=default`` (or ``omit``) leaves the parameter out,
    which is useful when ``OPENAI_MODEL`` points at a model without configurable
    reasoning.
    """
    configured = os.getenv("OPENAI_REASONING_EFFORT")
    if configured is None:
        # The bundled defaults are GPT-5.6-family models. For an arbitrary
        # OPENAI_MODEL override, omitting the field is safer than assuming the
        # model accepts GPT-5.6's effort values.
        is_gpt_5_6 = model == "gpt-5.6" or model.startswith("gpt-5.6-")
        return DEFAULT_REASONING_EFFORT if is_gpt_5_6 else None
    value = configured.strip().lower()
    if value in _OMIT_REASONING_VALUES:
        return None
    if value not in _REASONING_EFFORTS:
        allowed = ", ".join(sorted(_REASONING_EFFORTS | _OMIT_REASONING_VALUES))
        raise ValueError(
            f"invalid OPENAI_REASONING_EFFORT={value!r}; expected one of {allowed}"
        )
    return value


def create_client():
    """Create an OpenAI client without importing the optional SDK at startup."""
    try:
        from openai import OpenAI
    except ImportError as exc:
        raise RuntimeError(
            "openai SDK not installed (pip install -r tools/docsync/requirements.txt)"
        ) from exc
    return OpenAI()


def strict_object_schema(properties: dict[str, Any]) -> dict[str, Any]:
    """Build the strict top-level object schema used by Responses."""
    return {
        "type": "object",
        "properties": properties,
        "required": list(properties),
        "additionalProperties": False,
    }


def _request_args(
    *,
    system_prompt: str,
    user_text: str,
    schema_name: str,
    schema: dict[str, Any],
    max_output_tokens: int,
    model: str,
) -> dict[str, Any]:
    args: dict[str, Any] = {
        "model": model,
        "instructions": system_prompt,
        "input": user_text,
        "max_output_tokens": max_output_tokens,
        "text": {
            "format": {
                "type": "json_schema",
                "name": schema_name,
                "strict": True,
                "schema": schema,
            },
        },
        # Every docsync call is self-contained; server-side conversation state is
        # unnecessary and may contain repository/source excerpts.
        "store": False,
    }
    reasoning_effort = configured_reasoning_effort(model)
    if reasoning_effort is not None:
        args["reasoning"] = {"effort": reasoning_effort}
    return args


def _response_text(response: Any) -> str:
    status = getattr(response, "status", None)
    if status != "completed":
        details = getattr(response, "incomplete_details", None)
        reason = getattr(details, "reason", None)
        error = getattr(response, "error", None)
        error_code = getattr(error, "code", None)
        error_message = getattr(error, "message", None)
        diagnostics = [value for value in (reason, error_code, error_message) if value]
        suffix = f": {'; '.join(diagnostics)}" if diagnostics else ""
        error_type = (
            RuntimeError if error_code in _RETRYABLE_RESPONSE_CODES
            else OpenAIResponseError
        )
        raise error_type(f"OpenAI response ended with status {status!r}{suffix}")

    text = (getattr(response, "output_text", "") or "").strip()
    if not text:
        refusals: list[str] = []
        for output in getattr(response, "output", []) or []:
            for content in getattr(output, "content", []) or []:
                if getattr(content, "type", None) == "refusal":
                    refusals.append(getattr(content, "refusal", "") or "")
        refusal = " ".join(value.strip() for value in refusals if value.strip())
        if refusal:
            raise OpenAIResponseError(f"OpenAI response refused the request: {refusal}")
        raise OpenAIResponseError("OpenAI response contained no output text")
    return text


def _usage(response: Any) -> dict[str, Any]:
    usage = getattr(response, "usage", None)
    output_details = getattr(usage, "output_tokens_details", None)
    return {
        "input_tokens": getattr(usage, "input_tokens", 0) or 0,
        "output_tokens": getattr(usage, "output_tokens", 0) or 0,
        "reasoning_tokens": getattr(output_details, "reasoning_tokens", 0) or 0,
        "response_status": getattr(response, "status", None) or "unknown",
    }


def _create_response(client: Any, args: dict[str, Any], stream: bool) -> Any:
    if not stream:
        return client.responses.create(**args)

    chars = 0
    terminal_response = None
    stream_error_code = None
    stream_error_message = None
    print("  streaming response", end="", flush=True)
    with client.responses.stream(**args) as response_stream:
        for event in response_stream:
            event_type = getattr(event, "type", None)
            if event_type == "response.output_text.delta":
                delta = getattr(event, "delta", "") or ""
                chars += len(delta)
                if chars % 4000 < len(delta):
                    print(".", end="", flush=True)
            elif event_type in {"response.incomplete", "response.failed"}:
                terminal_response = getattr(event, "response", None)
            elif event_type == "error":
                stream_error_code = getattr(event, "code", None)
                stream_error_message = getattr(event, "message", None)
        try:
            response = response_stream.get_final_response()
        except RuntimeError as exc:
            if terminal_response is not None:
                response = terminal_response
            elif stream_error_message:
                error_type = (
                    RuntimeError
                    if stream_error_code in _RETRYABLE_RESPONSE_CODES
                    else OpenAIResponseError
                )
                details = ": ".join(
                    value for value in (stream_error_code, stream_error_message)
                    if value
                )
                raise error_type(
                    f"OpenAI stream ended with an error: {details}"
                ) from exc
            else:
                raise
    print(f" done ({chars} chars)")
    return response


def call_json(
    client: Any,
    *,
    system_prompt: str,
    user_text: str,
    schema_name: str,
    schema: dict[str, Any],
    max_output_tokens: int,
    model: str,
    stream: bool = False,
    retries: int = 1,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Call Responses with strict Structured Outputs and parse one JSON object."""
    if retries < 1:
        raise ValueError("retries must be at least 1")

    args = _request_args(
        system_prompt=system_prompt,
        user_text=user_text,
        schema_name=schema_name,
        schema=schema,
        max_output_tokens=max_output_tokens,
        model=model,
    )
    last_error: Exception | None = None
    for _attempt in range(1, retries + 1):
        try:
            response = _create_response(client, args, stream)
            text = _response_text(response)
            parsed = json.loads(text)
            if not isinstance(parsed, dict):
                raise RuntimeError("OpenAI response was valid JSON but not an object")
            return parsed, _usage(response)
        except OpenAIResponseError:
            # Retrying truncation, refusal, or another terminal model response
            # with the identical request only repeats cost without changing it.
            raise
        except Exception as exc:  # The SDK already retries transient HTTP errors.
            last_error = exc

    raise RuntimeError(
        f"OpenAI request failed after {retries} attempt(s): {last_error}"
    ) from last_error
