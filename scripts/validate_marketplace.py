#!/usr/bin/env python3
"""Dependency-free checks for the dual-client Nuko Nova marketplace."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CODEX_PATH = ROOT / ".agents" / "plugins" / "marketplace.json"
CLAUDE_PATH = ROOT / ".claude-plugin" / "marketplace.json"
SHA_RE = re.compile(r"^[0-9a-f]{40}$")
EXPECTED_CODEX = ["cld", "nuko-nova-legal"]
EXPECTED_CLAUDE = ["claude-goal", "cdx", "nuko-nova-legal"]


def fail(message: str) -> None:
    raise AssertionError(message)


def load(path: Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"{path.relative_to(ROOT)}: {exc}")
    if not isinstance(data, dict):
        fail(f"{path.relative_to(ROOT)}: root must be an object")
    return data


def plugin_map(manifest: dict, expected: list[str], label: str) -> dict[str, dict]:
    if manifest.get("name") != "nuko-nova-tools":
        fail(f"{label}: marketplace name mismatch")
    plugins = manifest.get("plugins")
    if not isinstance(plugins, list):
        fail(f"{label}: plugins must be an array")
    names = [plugin.get("name") for plugin in plugins if isinstance(plugin, dict)]
    if names != expected:
        fail(f"{label}: expected ordered plugins {expected}, found {names}")
    if len(names) != len(set(names)):
        fail(f"{label}: duplicate plugin names")
    return {plugin["name"]: plugin for plugin in plugins}


def check_source(plugin: dict, label: str) -> None:
    source = plugin.get("source")
    if not isinstance(source, dict) or source.get("source") != "url":
        fail(f"{label}: source must be a URL object")
    url = source.get("url")
    if not isinstance(url, str) or not url.startswith("https://github.com/nuko-nova-dynamics/") or not url.endswith(".git"):
        fail(f"{label}: source URL must be a Nuko Nova GitHub HTTPS repository")
    if not isinstance(source.get("ref"), str) or not source["ref"].strip():
        fail(f"{label}: source ref is required")
    if not isinstance(source.get("sha"), str) or not SHA_RE.fullmatch(source["sha"]):
        fail(f"{label}: source sha must be 40 lowercase hexadecimal characters")


def main() -> int:
    codex = plugin_map(load(CODEX_PATH), EXPECTED_CODEX, "Codex")
    claude = plugin_map(load(CLAUDE_PATH), EXPECTED_CLAUDE, "Claude")

    for name, plugin in codex.items():
        check_source(plugin, f"Codex {name}")
        policy = plugin.get("policy")
        if policy != {"installation": "AVAILABLE", "authentication": "ON_INSTALL"}:
            fail(f"Codex {name}: policy mismatch")
        if not isinstance(plugin.get("category"), str) or not plugin["category"].strip():
            fail(f"Codex {name}: category is required")

    for name, plugin in claude.items():
        check_source(plugin, f"Claude {name}")

    if codex["nuko-nova-legal"]["source"] != claude["nuko-nova-legal"]["source"]:
        fail("Nuko Nova Legal source pin differs between clients")

    print("PASS: dual-client Nuko Nova marketplace manifests and immutable pins verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
