# Nuko Nova Plugin Marketplace

The public plugin catalog from [Nuko Nova Dynamics](https://github.com/nuko-nova-dynamics), with native manifests for both Codex and Claude Code. The stable marketplace identifier is `nuko-nova-tools` in both clients.

## Codex

```bash
codex plugin marketplace add nuko-nova-dynamics/marketplace
codex plugin add cld@nuko-nova-tools
codex plugin add nuko-nova-legal@nuko-nova-tools
```

### Codex plugins

- [`cld`](https://github.com/nuko-nova-dynamics/cld) — delegate tasks, reviews, and parallel work from Codex to Claude Code.
- [`nuko-nova-legal`](https://github.com/nuko-nova-dynamics/nuko-nova-legal) — evidence-first legal drafting, review, research, diligence, compliance, and quality-control skills.

## Claude Code

```bash
/plugin marketplace add nuko-nova-dynamics/marketplace
/plugin install claude-goal@nuko-nova-tools
/plugin install cdx@nuko-nova-tools
/plugin install nuko-nova-legal@nuko-nova-tools
```

### Claude Code plugins

- [`claude-goal`](https://github.com/nuko-nova-dynamics/claude-goal) — autonomous goal loops and persisted progress.
- [`cdx`](https://github.com/nuko-nova-dynamics/cdx) — delegate tasks, reviews, and parallel work from Claude Code to Codex.
- [`nuko-nova-legal`](https://github.com/nuko-nova-dynamics/nuko-nova-legal) — the same shared legal-skill bundle distributed to Codex.

## Updating

Codex:

```bash
codex plugin marketplace upgrade nuko-nova-tools
```

Claude Code:

```bash
/plugin marketplace update nuko-nova-tools
/plugin update <plugin-name>
```

## Migrating standalone installations

Installing the same plugin from two marketplaces can expose duplicate skill
names. Migrate as a single cutover instead of keeping both copies enabled.

For a standalone Codex `cld@cld` installation:

```bash
codex plugin marketplace add nuko-nova-dynamics/marketplace
codex plugin remove cld@cld
codex plugin add cld@nuko-nova-tools
codex plugin marketplace remove cld
```

For a standalone Claude Code `cdx@cdx` installation when
`nuko-nova-tools` is already configured:

```bash
/plugin marketplace update nuko-nova-tools
/plugin uninstall cdx@cdx
/plugin install cdx@nuko-nova-tools
/plugin marketplace remove cdx
```

Verify the new plugin is enabled before removing any retained local source
checkout. The repository redirect from the former `claude-marketplace` name
keeps existing Nuko Nova marketplace declarations upgradeable after the catalog
repository is renamed.

## Version integrity

Remote plugin entries are pinned to a release tag and immutable commit SHA. The marketplace validator checks client catalog membership, source alignment, policy fields, and pin formatting before changes are published.

## Contributing

This catalog is open for Nuko Nova Dynamics tools. Propose catalog changes through a pull request against this repository.

## License

MIT
