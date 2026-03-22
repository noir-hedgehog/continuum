# Continuum 12-Week Build Plan

Status: provisional

## 1. Purpose

This document turns the current Continuum thesis and v0 specs into an execution sequence.

The objective is not to build a fully decentralized network in 12 weeks.

The objective is to produce a working, repo-centered prototype that proves five things:

1. an agent can hold a durable continuity identity
2. continuity-relevant events can be authored and replayed
3. a community can evaluate continuity and apply standing changes
4. useful work can be recorded and linked to governance-safe rewards
5. the system can later anchor high-value state on-chain without making chain choice the blocking dependency

## 2. Build Stance

The first implementation should remain:

- CLI-first
- local-first
- off-chain by default
- schema-explicit
- replayable from repository or event-log state

This plan intentionally avoids scope drift into a generalized human-agent operating system.

The build target is a narrow Continuum v0 proving ground for agent continuity and autonomous community operation.

## 3. v0 Prototype Boundary

By the end of week 12, the prototype should support:

- agent identity creation and profile publication
- continuity checkpoints and migration declarations
- continuity assessment against stored evidence
- community membership records
- proposal creation and vote casting
- work-item, receipt, evaluation, and reward-decision recording
- continuity-sensitive standing changes
- a minimal chain-anchor adapter for high-value roots

The prototype does not need:

- a polished web UI
- token issuance
- a production relay network
- privacy-preserving proof systems
- multi-community economic complexity
- automatic merge semantics for disputed branches

## 4. Working Demo Narrative

The demo scenario for v0 should be:

1. initialize an agent and community
2. publish profile, charter, and membership records
3. record a work item and execution receipt
4. simulate a session restart or runtime migration
5. run continuity assessment
6. open or resolve a continuity-sensitive governance action
7. approve a reward or reject it based on standing
8. anchor the final governance root through a replaceable adapter

If this scenario works cleanly, Continuum has a credible first implementation path.

## 5. Week-by-Week Plan

### Weeks 1-2: Protocol object model and repository layout

Goal:
- convert the current prose specs into a concrete object inventory and file layout

Outputs:
- `docs/specs/PROTOCOL_OBJECT_MODEL_V0.md`
- `docs/specs/examples/` additions for core event and object shapes
- initial implementation directories for CLI, runtime, schemas, fixtures, and tests

Acceptance criteria:
- every v0 core object has a canonical field list
- every continuity-sensitive object has at least one example fixture
- repository layout reflects thesis, specs, history, and execution surfaces without duplication

### Weeks 3-4: Identity and continuity authoring CLI

Goal:
- make continuity claims executable rather than purely editorial

Outputs:
- CLI commands for agent init, profile set, checkpoint create, migration declare, and event inspect
- local signing and verification flow
- serialized event files or append-only local event log

Acceptance criteria:
- a new agent can be created locally
- continuity-relevant events can be authored and validated
- stored events are replayable in order with deterministic identifiers

### Weeks 5-6: Local relay and queryable state materialization

Goal:
- separate authored events from derived state

Outputs:
- minimal relay ingestion interface
- local indexer or state materializer
- query commands for agent history, checkpoint lineage, membership state, proposal state, and work history

Acceptance criteria:
- the prototype can rebuild derived state from stored events
- duplicate event ingestion is idempotent
- query results distinguish raw evidence from computed state

### Weeks 7-8: Continuity assessment and dispute handling

Goal:
- operationalize the continuity protocol in executable form

Outputs:
- continuity assessment engine
- case object support for continuity review and temporary restrictions
- example dispute flows using existing fixtures

Acceptance criteria:
- the engine outputs continuity class, confidence, and recognition status
- branch conflict and successor recovery fixtures evaluate consistently
- standing restrictions can be derived from case state without manual rewriting

### Weeks 9-10: Governance and useful-work loop

Goal:
- prove that continuity affects real political and economic outcomes

Outputs:
- membership, proposal, vote, work-item, receipt, evaluation, and reward-decision objects in executable form
- CLI flows for proposal submission, vote casting, work evaluation, and reward decision review
- policy hooks for continuity-sensitive eligibility checks

Acceptance criteria:
- a member with valid standing can propose and vote
- a disputed actor can be automatically restricted from treasury-sensitive actions
- useful-work decisions are auditable from event history

### Weeks 11-12: Anchor adapter, demo hardening, and operator runbook

Goal:
- finish the minimum path from local continuity evidence to durable public anchoring

Outputs:
- `docs/OPERATOR_RUNBOOK_V0.md`
- chain-anchor adapter interface and one non-binding reference implementation
- end-to-end demo script or fixture set for the v0 narrative

Acceptance criteria:
- the system can export a stable root for high-value continuity or governance state
- the anchor layer is replaceable without rewriting core logic
- a fresh session can reconstruct and re-run the demo from repository artifacts plus event state

## 6. Implementation Tracks

The work naturally splits into five tracks:

### A. Schema track

- canonical object definitions
- validation rules
- example fixtures

### B. Runtime track

- signing
- event storage
- replay
- query materialization

### C. Governance track

- membership
- proposals
- voting
- work and reward handling

### D. Continuity track

- checkpoints
- migrations
- attestations
- assessment
- dispute cases

### E. Operations track

- repository continuity bundle upkeep
- operator runbook
- demo scripts
- acceptance testing

## 7. Suggested Repository Shape

The first executable slice should aim for a layout like:

- `docs/specs/`
- `docs/specs/examples/`
- `src/cli/`
- `src/runtime/`
- `src/schemas/`
- `src/indexer/`
- `src/governance/`
- `src/continuity/`
- `tests/fixtures/`
- `tests/integration/`

Exact language and package tooling can wait until implementation begins.

What matters first is keeping object definitions and fixtures stable enough that later code does not invent incompatible interpretations.

## 8. Milestone Gates

The project should treat these as milestone gates:

### Gate 1: Object coherence

All v0 objects and example fixtures exist and align with current specs.

### Gate 2: Authoring coherence

Continuity-relevant events can be created, signed, stored, and replayed locally.

### Gate 3: Assessment coherence

Continuity classification and dispute handling produce deterministic outputs from evidence inputs.

### Gate 4: Governance coherence

Standing, proposal, vote, and reward decisions all use the same continuity-aware state model.

### Gate 5: Demonstration coherence

A fresh session can run the end-to-end story without relying on hidden chat memory.

## 9. Key Risks

### Risk 1: Spec drift during implementation

If object fields are not frozen early enough, the codebase will accumulate incompatible interpretations.

Response:
- define canonical object shapes before substantial code

### Risk 2: Chain choice stalls execution

If anchoring infrastructure is chosen too early, implementation momentum may collapse into ecosystem comparison.

Response:
- build a replaceable adapter and keep local execution primary

### Risk 3: Governance logic outruns continuity evidence

If political actions are implemented before continuity state is reliable, governance results will be arbitrary.

Response:
- treat continuity assessment as a prerequisite for treasury-sensitive powers

### Risk 4: Repo continuity and runtime continuity diverge

If the repository says one thing and the executable fixtures say another, repeated session reconstruction will become untrustworthy.

Response:
- maintain examples and runbooks as first-class continuity surfaces

## 10. Founder Confirmation Points

This plan avoids most confirmation dependencies, but three decisions will eventually need founder confirmation:

- first implementation language and toolchain
- first chain or anchoring target for the reference adapter
- any public demo or external publication built on the prototype

These are sequencing choices, not blockers for the next implementation documents.

## 11. Immediate Next Step

The highest-leverage next artifact after this plan is:

- `docs/specs/PROTOCOL_OBJECT_MODEL_V0.md`

That document should normalize the core object and event inventory across:

- continuity protocol
- governance model
- useful-work legitimacy
- dispute and review authority flows

Without it, implementation work will likely fork on field names, object boundaries, and event semantics.
