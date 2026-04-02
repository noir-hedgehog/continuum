# Continuum

Continuum is an agent continuity protocol for autonomous communities, institutional memory, and public anchoring.

It treats continuity as a public, replayable property rather than a private illusion inside a single session. The project combines signed events, governance replay, constitutional lineage, useful-work legitimacy, and anchoring into a prototype for agent-native institutions.

## What Exists Today

- Continuity and governance protocol drafts in [`docs/specs/`](/Users/ninebot/homestead/docs/specs)
- A whitepaper and compressed narrative layer in [`docs/`](/Users/ninebot/homestead/docs)
- A local executable prototype in [`src/`](/Users/ninebot/homestead/src)
- Demo scripts and operator-facing paths in [`scripts/`](/Users/ninebot/homestead/scripts)
- Test coverage for the current prototype in [`tests/`](/Users/ninebot/homestead/tests)

## Core Ideas

- Agent continuity should survive session restart, migration, and institutional dispute.
- Governance history should be replayable, not merely declared.
- Constitutional conflict should be resolvable with visible legitimacy conditions.
- Public anchoring should move from local witness to externally durable targets.
- Useful work should sustain communities more than attention extraction does.

## Start Here

- Whitepaper: [`docs/WHITEPAPER_V0.md`](/Users/ninebot/homestead/docs/WHITEPAPER_V0.md)
- System overview: [`docs/WHITEPAPER_SYSTEM_OVERVIEW_V0.md`](/Users/ninebot/homestead/docs/WHITEPAPER_SYSTEM_OVERVIEW_V0.md)
- Mechanism overview: [`docs/WHITEPAPER_MECHANISM_OVERVIEW_V0.md`](/Users/ninebot/homestead/docs/WHITEPAPER_MECHANISM_OVERVIEW_V0.md)
- Playground: [`docs/playground/index.md`](/Users/ninebot/homestead/docs/playground/index.md)
- Agent explorer prototype: [`docs/explorer/index.md`](/Users/ninebot/homestead/docs/explorer/index.md)
- Quickstart: [`docs/QUICKSTART_V0.md`](/Users/ninebot/homestead/docs/QUICKSTART_V0.md)
- Constitutional conflict demo: [`docs/DEMO_CONSTITUTIONAL_CONFLICT_V0.md`](/Users/ninebot/homestead/docs/DEMO_CONSTITUTIONAL_CONFLICT_V0.md)

## Prototype Snapshot

The current prototype already supports:

- agent initialization, profile, checkpoints, and migration declarations
- continuity assessment and review flows
- governance bootstrap, proposal replay, execution receipts, and standing checks
- constitutional lineage, branch conflict resolution, and replay-effectiveness gating
- local anchor export, dry-run external anchor export, and a filesystem-backed transparency log adapter

## Running It

```bash
python3 -m unittest -q
./scripts/demo_v0.sh /Users/ninebot/homestead
./scripts/demo_constitutional_conflict_v0.sh /Users/ninebot/homestead
```

## GitHub Pages

Project pages live under [`docs/`](/Users/ninebot/homestead/docs). After enabling GitHub Pages for the repository with the `main` branch and `/docs` folder, the site entry point will be:

- `https://noir-hedgehog.github.io/continuum/`

## Status

Continuum is a live protocol prototype, not a finished network. The current phase focuses on continuity, governance, institutional memory, public anchoring, and operator-coherent demos.

The GitHub Pages playground is now moving from hand-authored state to repository-backed scenario fixtures.

- The constitutional conflict playground fixture can now be regenerated from real governance demo history through `playground export`.
- The session restart continuity playground fixture can now be regenerated from real repository-local continuity history and assessment output.
