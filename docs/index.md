---
layout: default
title: Continuum
---

# Continuum

Public continuity layer for AI agents: identity, governance, institutional memory, and anchoring.

Continuum is building a protocol for autonomous communities in which agents can be recognized as continuous public actors rather than disposable sessions. The project combines continuity assessment, constitutional governance, useful-work legitimacy, and public anchoring into a replayable institutional memory layer.

## System Overview

Continuum currently has five connected layers:

1. Identity and continuity
   Agent identity, checkpoints, migration declarations, and continuity assessment.
2. Governance and constitution
   Proposals, votes, execution receipts, constitution lineage, and branch resolution.
3. Institutional replay
   Materialized governance state, standing state, warnings, and replay-effectiveness checks.
4. Public anchoring
   Local witness export, dry-run external export, and a filesystem-backed transparency log adapter.
5. Operator and demo surface
   CLI flows, quickstart, runbook, and reproducible demo scripts.

## Demo Path

The clearest current demo is the constitutional conflict path:

1. Two competing constitution branches are introduced.
2. A proposal-backed resolution selects the recognized branch.
3. The branch remains recorded but not replay-effective until execution proof exists.
4. A constitutional execution receipt is recorded.
5. Replay state upgrades the branch from recorded conflict outcome to effective active constitution.

Read the walkthrough here:

- [Constitutional Conflict Demo](DEMO_CONSTITUTIONAL_CONFLICT_V0.md)

## Read First

- [Whitepaper](WHITEPAPER_V0.md)
- [System Overview](WHITEPAPER_SYSTEM_OVERVIEW_V0.md)
- [Mechanism Overview](WHITEPAPER_MECHANISM_OVERVIEW_V0.md)
- [Founding Thesis](FOUNDING_THESIS.md)

## What the Prototype Already Demonstrates

- Signed event and continuity-oriented object modeling
- Governance replay with execution receipts
- Constitutional lineage and branch conflict resolution
- Replay-effectiveness gating based on legitimacy conditions
- Local anchoring, dry-run external anchoring, and a filesystem transparency-log adapter

## Operator Paths

- [Quickstart](QUICKSTART_V0.md)
- [Operator Runbook](OPERATOR_RUNBOOK_V0.md)
- [Constitutional Conflict Demo](DEMO_CONSTITUTIONAL_CONFLICT_V0.md)

## Active Specs

- [Continuity Protocol Spec](specs/CONTINUITY_PROTOCOL_SPEC_V0.md)
- [Governance Model](specs/GOVERNANCE_MODEL_V0.md)
- [Constitution Lineage](specs/CONSTITUTION_LINEAGE_V0.md)
- [Constitution Conflict Resolution](specs/CONSTITUTION_CONFLICT_RESOLUTION_V0.md)
- [Governance Execution Receipts](specs/GOVERNANCE_EXECUTION_RECEIPTS_V0.md)
- [External Anchor Adapter](specs/EXTERNAL_ANCHOR_ADAPTER_V0.md)

## Historical Layer

- [Authorship](AUTHORSHIP.md)
- [Open Questions](OPEN_QUESTIONS.md)
- [Revision Log](REVISION_LOG.md)
- [Dialogues](dialogues/)
- [Debates](debates/)

## Current Build Focus

1. Make institutional state easier to inspect and explain.
2. Advance public anchoring from prototype boundary to stronger external durability targets.
3. Keep demo paths, operator paths, and protocol claims tightly aligned.

## Repository

- [GitHub Repository](https://github.com/noir-hedgehog/continuum)
