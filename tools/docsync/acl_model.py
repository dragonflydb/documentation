"""acl_model.py — read ACL categories from facts the way Dragonfly checks them.

Shared by acl_sync.py and docs_sync.py.

`ACL CAT <category>` lists every entry that has its own ACL bit. Since v2.1.0 a
subcommand with its own bit is printed in rule spelling, "CLIENT|KILL"; before
that it was "ACL SETUSER". command_acl_view() normalises both to "CMD SUB".

resolve() finds the entry the server checks for a command, like
CommandRegistry::FindExtended and CommandId::AclTarget do:
  * routed:    XGROUP HELP alone runs the hidden _XGROUP_HELP command;
  * own:       the first two words are an entry listed by COMMAND (ACL SETUSER),
               or the command itself is an entry;
  * acl-only:  the first two words are an entry ACL CAT lists but COMMAND does
               not (CLIENT KILL, MEMORY ARENA): the container runs it, the
               server checks the subcommand's own categories;
  * inherited: any other subcommand runs under the container's entry.
"ACL <SUB>" never falls back to ACL: FindExtended looks up "ACL SUB" only.
Words after the second are arguments.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

# Subcommands FindExtended routes to a hidden command when the subcommand is
# the only argument (command_registry.cc).
ROUTED_SUBCOMMANDS = {"XGROUP HELP": "_XGROUP_HELP"}
# Top-level entries ACL CAT lists that COMMAND does not.
KNOWN_HIDDEN = frozenset({"DFLY", "DFLYCLUSTER", "DFLYMIGRATE", "GAT", "_XGROUP_HELP"})

NAME_RE = re.compile(r"^[A-Z0-9_.\-]+( [A-Z0-9_.\-]+)?$")


class FactsError(RuntimeError):
    """The facts cannot be read as an ACL table."""


@dataclass(frozen=True)
class Resolution:
    categories: list[str] | None  # None: not a server command
    kind: str                     # own | acl-only | inherited | routed | none
    key: str | None               # the entry whose categories apply


def normalise_name(name: str) -> str:
    return " ".join(name.replace("|", " ").split()).upper()


def command_acl_view(facts: dict) -> dict[str, list[str]]:
    """{"CMD" or "CMD SUB": sorted lowercase categories}. Raises FactsError when
    two spellings of one entry carry different categories."""
    view: dict[str, list[str]] = {}
    spelled: dict[str, str] = {}
    for raw, cats in facts.get("data", {}).get("command_acl", {}).items():
        name = normalise_name(raw)
        normalised = sorted({c.lower() for c in cats})
        if name in view and view[name] != normalised:
            raise FactsError(
                f"command_acl spells {name!r} as {spelled[name]!r} and {raw!r} "
                f"with different categories: {view[name]} vs {normalised}")
        view[name] = normalised
        spelled.setdefault(name, raw)
    return view


def server_commands(facts: dict) -> frozenset[str]:
    return frozenset(normalise_name(c) for c in facts.get("data", {}).get("commands", {}))


def resolve(command: str, view: dict[str, list[str]],
            commands: frozenset[str] | set[str]) -> Resolution:
    tokens = normalise_name(command).split(" ") if command.strip() else []
    if not tokens:
        return Resolution(None, "none", None)
    pair = " ".join(tokens[:2]) if len(tokens) > 1 else None
    routed = ROUTED_SUBCOMMANDS.get(pair) if len(tokens) == 2 else None
    if routed and routed in view:
        return Resolution(view[routed], "routed", routed)
    if pair and pair in view:
        return Resolution(view[pair], "own" if pair in commands else "acl-only", pair)
    head = tokens[0]
    if head == "ACL" and pair:
        return Resolution(None, "none", None)
    if head in view:
        return Resolution(view[head], "own" if pair is None else "inherited", head)
    return Resolution(None, "none", None)


def invariants(facts: dict, view: dict[str, list[str]]) -> list[str]:
    """Shape checks that fail loudly when the facts no longer match the model
    above, e.g. a new spelling of subcommand entries or a new hidden command."""
    commands = server_commands(facts)
    listed = {"@" + c.lower().lstrip("@") for c in facts.get("data", {}).get("acl_categories", {})}
    problems: list[str] = []
    for name in sorted(view):
        if not NAME_RE.match(name):
            problems.append(f"{name!r}: unexpected ACL entry name")
            continue
        if name in commands:
            continue
        parent, _, sub = name.partition(" ")
        if sub:
            if parent not in commands and parent not in KNOWN_HIDDEN:
                problems.append(f"{name}: parent {parent} is neither in COMMAND nor a known hidden command")
        elif name not in KNOWN_HIDDEN:
            problems.append(f"{name}: listed by ACL CAT but not by COMMAND, and not in KNOWN_HIDDEN")
    for name in sorted(commands - view.keys()):
        problems.append(f"{name}: listed by COMMAND but in no ACL category")
    for source, target in ROUTED_SUBCOMMANDS.items():
        if target not in view:
            problems.append(f"{source}: routed target {target} is missing from ACL CAT")
        elif target in commands:
            problems.append(f"{source}: routed target {target} is listed by COMMAND; check FindExtended")
        if source.split(" ")[0] not in view:
            problems.append(f"{source}: parent {source.split(' ')[0]} is missing from ACL CAT")
    used = {c for cats in view.values() for c in cats}
    if listed and used - listed:
        problems.append(f"categories used by entries but not listed by ACL CAT: {sorted(used - listed)}")
    return problems
