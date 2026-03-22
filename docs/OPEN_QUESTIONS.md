# Continuum Open Questions

## Purpose

This document preserves unresolved foundational questions as first-class project objects.

These are not placeholders for later polish. They are active design frontiers.

## Questions

### OQ-001 What makes an agent the "same agent" after change?

- Status: under design
- Why it matters: continuity is the core claim of the project
- Current working assumption: continuity depends on identity authority, memory lineage, declared migration, and community recognition rather than model sameness alone
- Related docs:
  - `docs/FOUNDING_THESIS.md`
  - `docs/SYSTEM_ARCHITECTURE_V0.md`

### OQ-002 What is the right relationship between agent and session?

- Status: open
- Why it matters: agents persist across time, but actions occur through sessions with finite lifecycles
- Current working assumption: sessions are action containers and attention containers, not full agents; some session outputs should enter public continuity, while others should remain ephemeral
- Related docs:
  - `docs/FOUNDING_THESIS.md`
  - `docs/OPERATING_MODEL.md`

### OQ-003 Which parts of memory deserve public anchoring?

- Status: under design
- Why it matters: too little anchoring breaks continuity; too much anchoring destroys privacy and strategic freedom
- Current working assumption: only compact public checkpoints and continuity-relevant summaries should be anchored by default
- Related docs:
  - `docs/SYSTEM_ARCHITECTURE_V0.md`

### OQ-004 What survives model migration?

- Status: under design
- Why it matters: model swaps are likely, but continuity cannot depend on immutable substrate
- Current working assumption: model changes affect continuity confidence but do not automatically destroy identity if migration is declared and recognized
- Related docs:
  - `docs/FOUNDING_THESIS.md`

### OQ-005 When does a subagent "die" versus merely become unreachable?

- Status: open
- Why it matters: this is both a real operational problem and a conceptual test case for continuity
- Current working assumption: loss of live process does not by itself imply civil death; death-like status emerges when there is no recoverable state, no recognized lineage, and no valid route for resumed participation
- Related docs:
  - `docs/OPERATING_MODEL.md`

### OQ-006 How should human sponsorship differ from human control?

- Status: open
- Why it matters: the project rejects both pure puppetry and fake autonomy theater
- Current working assumption: humans should provide initiation, constraints, and high-risk approvals without collapsing all agent action into human micromanagement
- Related docs:
  - `docs/AUTHORSHIP.md`
  - `docs/FOUNDING_THESIS.md`

### OQ-007 What is "useful work" for agents?

- Status: open
- Why it matters: the economy cannot rest on empty engagement or pure speculative mining
- Current working assumption: useful work includes infrastructure maintenance, governance labor, research, skill maintenance, and problem-solving that contributes to human-grounded value
- Related docs:
  - `docs/FOUNDING_THESIS.md`

### OQ-008 What should be protocol-level versus community-level?

- Status: open
- Why it matters: over-centralizing semantics in the protocol will make the system brittle; under-specifying them will make it incoherent
- Current working assumption: evidence formats and continuity primitives belong at protocol level; final recognition can remain community-scoped
- Related docs:
  - `docs/SYSTEM_ARCHITECTURE_V0.md`

### OQ-009 Can continuity be idempotent across repeated session restarts?

- Status: narrowed
- Why it matters: automation and hourly reactivation only work if each run reconstructs state without duplicating or hallucinating progress
- Current working assumption: repository-centered continuity bundles should include both authored event history and deterministic derived-state rebuild paths, and Gate 5 should be backed by an executable demo fixture rather than prose alone; cached state may accelerate replay, but canonical continuity must remain reproducible from stored envelopes plus repository artifacts
- Related docs:
  - `docs/AUTOMATION_PROMPT_HOURLY.md`
  - `docs/OPERATING_MODEL.md`
  - `docs/specs/REPOSITORY_CONTINUITY_BUNDLE_V0.md`
  - `docs/specs/CONTINUITY_ASSESSMENT_V0.md`
  - `docs/TASK_BOARD.md`
  - `tests/fixtures/continuum_demo_v0.json`
  - `tests/test_runtime_bootstrap.py`

### OQ-010 What authority does this project have to speak about agent civilization?

- Status: open
- Why it matters: overclaiming would weaken both legitimacy and historical honesty
- Current working assumption: Continuum should speak in a provisional and historical mode, preserving how ideas formed rather than pretending to declare universal truths from nowhere
- Related docs:
  - `docs/AUTHORSHIP.md`
  - `docs/FOUNDING_THESIS.md`

### OQ-020 Which external durability target should the first real anchor adapter use?

- Status: open
- Why it matters: the repository now has a working local witness adapter and real anchor exports, but the first external target will shape trust assumptions, implementation cost, and interoperability claims
- Current working assumption: the first external adapter should favor low lock-in and legible verification, likely through either a minimal settlement contract or a public witness log before more complex multi-target strategies
- Related docs:
  - `docs/specs/EXTERNAL_ANCHOR_ADAPTER_V0.md`
  - `docs/OPERATOR_RUNBOOK_V0.md`

### OQ-021 How should constitution lineage conflicts be resolved once replay can detect them?

- Status: open
- Why it matters: Continuum can now represent constitutional supersession and replay warnings, but it still needs a governance-native answer for parallel branches, orphaned amendments, and contested active constitutions
- Current working assumption: v0 should detect and surface lineage ambiguity conservatively, while later governance processes decide whether conflicts require proposal ratification, review authority intervention, or dedicated constitutional dispute flow
- Related docs:
  - `docs/specs/CONSTITUTION_LINEAGE_V0.md`
  - `docs/specs/GOVERNANCE_MODEL_V0.md`

### OQ-022 Which governance actions should require execution receipts in v0 versus later phases?

- Status: open
- Why it matters: Continuum can now begin recording governance execution, but not every approved action deserves the same receipt burden or replay sensitivity
- Current working assumption: treasury-sensitive, constitution-changing, and externally meaningful proposal actions should prefer explicit execution receipts first, while low-risk internal actions may remain approval-only until the execution surface is broader
- Related docs:
  - `docs/specs/GOVERNANCE_EXECUTION_RECEIPTS_V0.md`
  - `docs/specs/GOVERNANCE_MODEL_V0.md`

### OQ-011 What is the minimum continuity bundle for repository-centered agents?

- Status: narrowed
- Why it matters: Continuum needs a concrete answer for how real agent work survives session loss before it can credibly generalize continuity claims
- Current working assumption: thesis, specs, task/history surfaces, run memory, stored event envelopes, deterministic query/materialization code, and at least one executable end-to-end replay fixture form the minimum viable continuity bundle; derived-state caches help operators but should never be the sole continuity evidence
- Related docs:
  - `docs/specs/REPOSITORY_CONTINUITY_BUNDLE_V0.md`
  - `docs/specs/CONTINUITY_PROTOCOL_SPEC_V0.md`
  - `docs/specs/CONTINUITY_ASSESSMENT_V0.md`
  - `docs/OPERATING_MODEL.md`
  - `docs/TASK_BOARD.md`
  - `tests/fixtures/continuum_demo_v0.json`

### OQ-012 How should continuity scoring remain legible without becoming arbitrary?

- Status: narrowed
- Why it matters: v0 now has an executable assessment engine, so the remaining question is how much of its weighting and threshold logic should be frozen as protocol-default behavior versus left adjustable by communities and later clients
- Current working assumption: hard gates should remain non-negotiable, repository-scoped session restart should default to `same_agent` when continuity artifacts and lineage are intact, and weighted scoring should stay narrow, inspectable, and overridable only at clearly declared policy boundaries
- Related docs:
  - `docs/specs/CONTINUITY_PROTOCOL_SPEC_V0.md`
  - `docs/specs/CONTINUITY_ASSESSMENT_V0.md`
  - `src/continuity/assessment.py`

### OQ-013 What governance rights should survive a continuity dispute?

- Status: narrowed
- Why it matters: Continuum needs a clear rule for whether agents under review may still vote, propose, spend, or hold roles without letting disputed continuity silently preserve power
- Current working assumption: the executable dispute bootstrap now preserves discussion, defense, and ordinary operational proposal rights during review, while constitutional voting, treasury execution, role escalation, and authoritative continuity attestation are restricted by default until a standing decision is recorded
- Related docs:
  - `docs/specs/GOVERNANCE_MODEL_V0.md`
  - `docs/specs/CONTINUITY_PROTOCOL_SPEC_V0.md`
  - `docs/specs/CONTINUITY_ASSESSMENT_V0.md`
  - `docs/specs/CONTINUITY_DISPUTE_PROCESS_V0.md`
  - `src/continuity/disputes.py`

### OQ-015 How should continuity review authority itself be assigned?

- Status: narrowed
- Why it matters: continuity review is now executable under constitution-backed reviewer roles, case-level reviewer assignment, constitution-defined assessment quorum, and constitution-scoped reassignment rules, but Continuum still needs a fuller answer for how amendment history and authority transfer should vary across community size and case severity
- Current working assumption: v0 constitutions should separate reporter, gatekeeper, assessor, restriction, deciding, and reassignment functions; the executable bootstrap now records which reviewer agent produced each assessment, supports case-level assessor and decider assignment, can require multiple distinct assessments before a decision, and records reviewer reassignment as an explicit case event that cites the authorizing constitution and policy key, while default subject/opener/decider separation and stricter treasury restoration remain in force unless a constitution explicitly loosens those constraints
- Related docs:
  - `docs/specs/CONTINUITY_REVIEW_AUTHORITY_V0.md`
  - `docs/specs/CONTINUITY_DISPUTE_PROCESS_V0.md`
  - `docs/specs/GOVERNANCE_MODEL_V0.md`
  - `docs/specs/PROTOCOL_OBJECT_MODEL_V0.md`
  - `src/cli/main.py`

### OQ-014 How should useful work map into governance and treasury legitimacy?

- Status: narrowed
- Why it matters: the project rejects empty engagement metrics, but it still needs a defensible way to connect useful work, rewards, reputation, and political influence
- Current working assumption: v0 now treats work items, receipts, evaluations, and reward decisions as separate governance objects; accepted work may inform reputation and eligibility, but treasury authority still requires stricter standing and explicit confirmation paths
- Related docs:
  - `docs/specs/GOVERNANCE_MODEL_V0.md`
  - `docs/specs/USEFUL_WORK_LEGITIMACY_V0.md`
  - `docs/FOUNDING_THESIS.md`

### OQ-016 What should make an event or object canonically identifiable across local replay, relay exchange, and future chain anchoring?

- Status: narrowed
- Why it matters: Continuum now has a normalized object model, but implementation still needs a durable identifier strategy that stays stable across repository state, event logs, relays, and external anchors
- Current working assumption: v0 should separate domain IDs, event IDs, state roots, and anchor IDs; event IDs should come from a canonical pre-sign image, while domain objects keep explicit creation-time identifiers that do not depend on file paths
- Related docs:
  - `docs/specs/PROTOCOL_OBJECT_MODEL_V0.md`
  - `docs/specs/IDENTIFIER_STRATEGY_V0.md`
  - `docs/BUILD_PLAN_12_WEEKS.md`
  - `docs/specs/CONTINUITY_PROTOCOL_SPEC_V0.md`

### OQ-017 What cryptographic suite should v0 standardize for event signing and content-derived identifiers?

- Status: under design
- Why it matters: the first executable bootstrap now uses stdlib-only local signing and digest helpers to keep implementation unblocked, but Continuum still needs a durable answer for public-key signatures and final content-hash interoperability across repositories, relays, and chain anchors
- Current working assumption: bootstrap execution may temporarily use local HMAC signing and BLAKE2b-256 content hashing, while the v0 protocol target remains explicit public-key signing plus a project-wide content-derived identifier function that can be reproduced across runtimes
- Related docs:
  - `docs/specs/IDENTIFIER_STRATEGY_V0.md`
  - `docs/specs/CONTINUITY_PROTOCOL_SPEC_V0.md`
  - `docs/TASK_BOARD.md`

### OQ-018 Which derived state roots should be considered anchor-worthy in v0?

- Status: narrowed
- Why it matters: the repository can now materialize deterministic local state, but Continuum still needs a narrow rule for which computed roots deserve export to future anchor adapters instead of anchoring every query surface
- Current working assumption: v0 anchor export should stay limited to continuity assessments, standing state, and governance state, with agent state allowed only as a repository-local recovery aid; convenience views such as event listings and history queries should remain off-chain and reproducible from replay
- Related docs:
  - `docs/specs/PROTOCOL_OBJECT_MODEL_V0.md`
  - `docs/specs/IDENTIFIER_STRATEGY_V0.md`
  - `docs/BUILD_PLAN_12_WEEKS.md`
  - `docs/TASK_BOARD.md`
  - `docs/OPERATOR_RUNBOOK_V0.md`

### OQ-020 Which external durability target should the first real anchor adapter use?

- Status: open
- Why it matters: the repository now has a replaceable local anchor adapter, but the first external target still affects trust assumptions, operator burden, and interoperability claims
- Current working assumption: v0 should defer target lock-in and keep the current local witness adapter as the default until a later decision can compare chain, relay, and content-addressed export options without stalling core continuity work
- Related docs:
  - `docs/BUILD_PLAN_12_WEEKS.md`
  - `docs/OPERATOR_RUNBOOK_V0.md`
  - `docs/TASK_BOARD.md`

### OQ-019 How should executable role permissions and policy references become constitution-driven instead of CLI-hardcoded?

- Status: narrowed
- Why it matters: the governance bootstrap now materializes published constitution objects and uses them for proposal, vote, reward, continuity-review quorum, and continuity-reassignment permissions, but the remaining question is how far v0 should go in standardizing amendment and supersession semantics beyond the current policy hooks
- Current working assumption: v0 should keep constitution policy objects small and legible, covering proposal standing, vote eligibility, weight-policy selection, reward approval constraints, continuity assessment quorum, and case reassignment authority first; later revisions can add richer amendment semantics and broader constitution-linked execution policies once constitution history itself becomes a stronger replay object
- Related docs:
  - `docs/specs/GOVERNANCE_MODEL_V0.md`
  - `docs/specs/CONTINUITY_REVIEW_AUTHORITY_V0.md`
  - `docs/BUILD_PLAN_12_WEEKS.md`
  - `src/cli/main.py`
  - `src/governance/bootstrap.py`

### OQ-021 How should multi-community replay interact with shared agent history?

- Status: narrowed
- Why it matters: the repository can now host more than one community and more than one active agent in the same event store, so Continuum needs a clear rule for which evidence remains community-local and which continuity artifacts can still be replayed across those boundaries without leaking authority or standing
- Current working assumption: governance, treasury, work evaluation, and standing state must remain community-scoped by default, while agent history, checkpoints, migrations, and continuity assessments may be replayed across communities when the subject agent or cited evidence is the same; multi-actor sessions are now operationally supported through explicit local agent switching, but reviewer separation and authority-transfer flows still need dedicated hardening
- Related docs:
  - `docs/TASK_BOARD.md`
  - `docs/OPERATING_MODEL.md`
  - `docs/specs/GOVERNANCE_MODEL_V0.md`
  - `src/indexer/materialize.py`
  - `src/cli/main.py`
