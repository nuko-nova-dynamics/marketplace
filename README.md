# Nuko Nova Plugin Marketplace

The public plugin catalog from [Nuko Nova Dynamics](https://github.com/nuko-nova-dynamics), with native manifests for both Codex and Claude Code. The stable marketplace identifier is `nuko-nova-tools` in both clients.

## Codex

```bash
codex plugin marketplace add nuko-nova-dynamics/marketplace
codex plugin add cld@nuko-nova-tools
codex plugin add nuko-nova-legal@nuko-nova-tools
codex plugin add nuko-nova-unslop@nuko-nova-tools
```

### Codex plugins

- [`cld`](https://github.com/nuko-nova-dynamics/cld): delegate tasks, reviews, and parallel work from Codex to Claude Code.
- [`nuko-nova-legal`](https://github.com/nuko-nova-dynamics/nuko-nova-legal): evidence-first legal drafting, review, research, diligence, compliance, and quality-control skills.
- [`nuko-nova-unslop`](https://github.com/nuko-nova-dynamics/nuko-nova-unslop): human writing with no slop or cringe across every human-facing response and prose artifact, with facts and owned voice preserved. Type `$unslop` and select **Unslop** for explicit use, or use `$tighten` to run the full standard followed by its strictest useful removal pass.

## Claude Code

```bash
/plugin marketplace add nuko-nova-dynamics/marketplace
/plugin install cdx@nuko-nova-tools
/plugin install nuko-nova-legal@nuko-nova-tools
/plugin install nuko-nova-unslop@nuko-nova-tools
/plugin install docs-first@nuko-nova-tools
/plugin install lightbox@nuko-nova-tools
```

### Claude Code plugins

- [`cdx`](https://github.com/nuko-nova-dynamics/cdx): delegate tasks, reviews, and parallel work from Claude Code to Codex.
- [`nuko-nova-legal`](https://github.com/nuko-nova-dynamics/nuko-nova-legal): the same shared legal-skill bundle distributed to Codex.
- [`nuko-nova-unslop`](https://github.com/nuko-nova-dynamics/nuko-nova-unslop): the same human-writing skill and local checks available in Codex, without lifecycle hooks or final-output interception. Invoke it with `/unslop`, or use `/nuko-nova-unslop:tighten` to run the full standard followed by its strictest useful removal pass.
- [`docs-first`](https://github.com/nuko-nova-dynamics/docs-first): a mod that holds back dependency changes, new imports and sensitive-file edits until the session has checked the registry or the official docs. Requires Claude Code 2.1.287 or later.
- [`lightbox`](https://github.com/nuko-nova-dynamics/lightbox): a mod that shows the images you paste and the ones Claude reads, receives or creates in a small strip above the prompt, including HEIC. Requires Claude Code 2.1.288 or later.

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
