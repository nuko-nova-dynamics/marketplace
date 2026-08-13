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
EXPECTED_MARKETPLACE_VERSION = "1.4.0"
EXPECTED_CODEX = ["cld", "nuko-nova-legal", "nuko-nova-unslop"]
EXPECTED_CLAUDE = ["claude-goal", "cdx", "nuko-nova-legal", "nuko-nova-unslop"]
EXPECTED_CODEX_VERSIONS = {
    "cld": "0.2.2",
    "nuko-nova-legal": "0.1.1",
    "nuko-nova-unslop": "0.2.1",
}
EXPECTED_CLAUDE_VERSIONS = {
    "claude-goal": "0.3.0",
    "cdx": "0.1.4",
    "nuko-nova-legal": "0.1.1",
    "nuko-nova-unslop": "0.2.1",
}
DUAL_CLIENT_DISPLAY_NAMES = {
    "nuko-nova-legal": "Nuko Nova Legal",
    "nuko-nova-unslop": "Nuko Nova Unslop",
}
LEGAL_ARTWORK = {
    "composerIcon": "./assets/icon.png",
    "logo": "./assets/logo.png",
    "logoDark": "./assets/logo-dark.png",
}


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
    claude_manifest = load(CLAUDE_PATH)
    if claude_manifest.get("version") != EXPECTED_MARKETPLACE_VERSION:
        fail("Claude: marketplace version mismatch")
    claude = plugin_map(claude_manifest, EXPECTED_CLAUDE, "Claude")

    for name, plugin in codex.items():
        check_source(plugin, f"Codex {name}")
        if plugin.get("version") != EXPECTED_CODEX_VERSIONS[name]:
            fail(f"Codex {name}: version mismatch")
        policy = plugin.get("policy")
        if policy != {"installation": "AVAILABLE", "authentication": "ON_INSTALL"}:
            fail(f"Codex {name}: policy mismatch")
        if not isinstance(plugin.get("category"), str) or not plugin["category"].strip():
            fail(f"Codex {name}: category is required")

    for name, plugin in claude.items():
        check_source(plugin, f"Claude {name}")
        if plugin.get("version") != EXPECTED_CLAUDE_VERSIONS[name]:
            fail(f"Claude {name}: version mismatch")

    for name, display_name in DUAL_CLIENT_DISPLAY_NAMES.items():
        if codex[name]["source"] != claude[name]["source"]:
            fail(f"{display_name} source pin differs between clients")
        interface = codex[name].get("interface")
        if not isinstance(interface, dict):
            fail(f"Codex {display_name}: interface metadata is required")
        if interface.get("displayName") != display_name:
            fail(f"Codex {display_name}: display name mismatch")
        if claude[name].get("displayName") != display_name:
            fail(f"Claude {display_name}: display name mismatch")

    unslop = codex["nuko-nova-unslop"]
    if "all human-facing writing" not in unslop.get("description", ""):
        fail("Nuko Nova Unslop: default writing standard is missing")
    if unslop.get("keywords", [])[-1:] != ["always-on"]:
        fail("Nuko Nova Unslop: always-on keyword is missing")

    legal_interface = codex["nuko-nova-legal"].get("interface")
    for field, expected_path in LEGAL_ARTWORK.items():
        if legal_interface.get(field) != expected_path:
            fail(f"Codex Nuko Nova Legal: {field} path mismatch")

    print("PASS: dual-client Nuko Nova marketplace manifests and immutable pins verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
