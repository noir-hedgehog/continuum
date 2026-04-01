# Continuum Revision Log

## Purpose

This log records material changes to project assumptions, definitions, or design direction.

The goal is to prevent silent rewriting of foundational positions.

## Entries

### 2026-04-01

- Changed artifact: first visual playground surface
- Previous position: Continuum had whitepaper, scripts, and textual demos, but no directly inspectable visual interface that let a reader step through protocol state changes
- New position: Continuum now has a static GitHub Pages playground that visualizes the constitutional conflict demo path as a staged institutional state machine
- Reason: the project needs a bridge between dense specs and a future full application UI, especially for first-contact explanation
- Trigger: recognition that a visual demo or playground would make the protocol legible faster than another prose layer
- Downstream docs affected:
  - `docs/playground/index.md`
  - `docs/assets/main.scss`
  - `README.md`
  - `docs/index.md`

### 2026-04-01

- Changed artifact: playground scenario data boundary
- Previous position: the playground existed, but its constitutional-conflict states were still hard-coded inside the page itself
- New position: the playground now hydrates from a dedicated repository fixture, making the first visual demo consume scenario data instead of embedding the protocol story directly in page code
- Reason: future scenarios should share a stable shape with repository artifacts instead of repeating the same state model in HTML
- Trigger: decision to move the playground from narrative-only UI toward a reusable protocol-viewer surface
- Downstream docs affected:
  - `docs/playground/index.md`
  - `docs/playground/scenarios/constitutional-conflict-v0.json`
  - `README.md`

### 2026-04-01

- Changed artifact: multi-scenario playground surface
- Previous position: the playground could visualize only one protocol story, even though the repository already contained multiple continuity and governance narratives
- New position: the playground now supports multiple repository-backed scenarios, beginning with constitutional conflict and session restart continuity
- Reason: a real protocol viewer needs to compare distinct institutional paths rather than freeze one canonical story into a single page
- Trigger: decision to stabilize the playground as a reusable viewing surface before adding more demo types
- Downstream docs affected:
  - `docs/playground/index.md`
  - `docs/playground/scenarios/constitutional-conflict-v0.json`
  - `docs/playground/scenarios/session-restart-v0.json`
  - `docs/assets/main.scss`

### 2026-04-01

- Changed artifact: successor recovery playground path
- Previous position: the playground could show clean replayable continuity and constitutional legitimacy, but not the more ambiguous case where continuity degrades into successor status
- New position: the playground now includes a successor recovery scenario that visualizes disruption, recovery claim, successor assessment, required followups, and pending recognition
- Reason: Continuum's value is not only in clean same-agent continuity, but in handling broken lineages without collapsing into either amnesia or false sameness
- Trigger: decision to extend the visual surface toward more realistic continuity outcomes after establishing multi-scenario playback
- Downstream docs affected:
  - `docs/playground/index.md`
  - `docs/playground/scenarios/successor-recovery-v0.json`

### 2026-04-01

- Changed artifact: playground auditability surface
- Previous position: playground scenarios were viewable, but the page did not yet expose a direct path back to their fixture sources or adjacent exportable artifacts
- New position: each playground scenario now exposes source artifacts alongside related docs, making the visual demo easier to audit and trace back into repository materials
- Reason: the project should not separate visual explanation from inspectable protocol artifacts
- Trigger: decision to make the playground feel more like a protocol viewer than a marketing microsite
- Downstream docs affected:
  - `docs/playground/index.md`
  - `docs/playground/scenarios/constitutional-conflict-v0.json`
  - `docs/playground/scenarios/session-restart-v0.json`
  - `docs/playground/scenarios/successor-recovery-v0.json`

### 2026-03-26

- Changed artifact: public repository and multilingual project surface
- Previous position: Continuum had a usable whitepaper, demo package, and Pages landing page, but the public site still relied on noisy default navigation and only presented a single-language entry surface
- New position: Continuum now exposes a more intentional public-facing surface with a cleaner landing page, suppressed document-spam top navigation, and dedicated English, Simplified Chinese, and Japanese entry pages
- Reason: the repository has crossed the threshold where outside readers need a legible first-contact experience instead of raw document listing
- Trigger: direct inspection of the live Pages site showed that default Jekyll navigation was leaking too much of the internal document graph into the page chrome
- Downstream docs affected:
  - `README.md`
  - `docs/index.md`
  - `docs/zh-cn/index.md`
  - `docs/ja/index.md`
  - `docs/assets/main.scss`
  - `docs/_config.yml`

### 2026-03-23

- Changed artifact: external narrative surface
- Previous position: the repository had thesis, specs, architecture, and business framing, but no single whitepaper-style document that unified the protocol story for outside readers
- New position: Continuum now has a dedicated whitepaper draft plus two compressed companion overviews that separate system boundary from institutional mechanism, making the project easier to present without losing conceptual discipline
- Reason: the project has reached the point where an integrated narrative document is needed alongside internal specs and code
- Trigger: recognition that the repository had enough substance for a whitepaper, but no single canonical synthesis
- Downstream docs affected:
  - `docs/WHITEPAPER_V0.md`
  - `docs/WHITEPAPER_SYSTEM_OVERVIEW_V0.md`
  - `docs/WHITEPAPER_MECHANISM_OVERVIEW_V0.md`
  - `docs/TASK_BOARD.md`

### 2026-03-23

- Changed artifact: outward-facing demo surface
- Previous position: the strongest constitutional branch-resolution mechanism existed across tests, specs, and whitepaper prose, but not as a dedicated operator-facing demo package
- New position: Continuum now has a focused constitutional conflict demo document and executable script so the project can demonstrate proposal-backed branch resolution, delayed replay effect, and execution-proof activation as a coherent story
- Reason: the project needed a demonstrable institutional narrative, not just internal tests and scattered docs
- Trigger: decision to turn the strongest current mechanism path into a proper demo package
- Downstream docs affected:
  - `docs/DEMO_CONSTITUTIONAL_CONFLICT_V0.md`
  - `scripts/demo_constitutional_conflict_v0.sh`
  - `docs/TASK_BOARD.md`

### 2026-03-26

- Changed artifact: first external anchor target
- Previous position: Continuum had a local witness adapter and a dry-run external adapter boundary, but no executable external target that actually wrote durable witness data outside the repository anchor cache
- New position: Continuum now has a first real external target in the form of an append-only filesystem-backed transparency log, exposed through a dedicated anchor adapter and CLI export mode
- Reason: the project needed to move public continuity from architectural boundary to executable reality without prematurely binding itself to one chain or vendor
- Trigger: decision to prioritize the first real external anchor target after narrative and demo layers became strong enough
- Downstream docs affected:
  - `docs/specs/EXTERNAL_ANCHOR_ADAPTER_V0.md`
  - `docs/OPEN_QUESTIONS.md`
  - `src/anchors/export.py`
  - `src/cli/main.py`
  - `tests/test_runtime_bootstrap.py`

### 2026-03-23

- Changed artifact: constitution-resolution policy boundary
- Previous position: legitimacy around constitution resolutions existed only as optional proposal linkage, execution linkage, and replay warnings
- New position: communities may now use constitution policy to require `proposal_ref` as a hard precondition for branch-resolution creation, while execution proof remains a replay-visible legitimacy layer that can be tightened without creating a creation-time deadlock
- Reason: Continuum needs a practical split between what can be enforced before a resolution exists and what only becomes meaningful after it has been carried out
- Trigger: mainline pass on moving part of constitutional legitimacy from soft replay warnings into community-configurable hard requirements
- Downstream docs affected:
  - `docs/specs/CONSTITUTION_CONFLICT_RESOLUTION_V0.md`
  - `docs/OPEN_QUESTIONS.md`
  - `src/cli/main.py`
  - `src/indexer/materialize.py`

### 2026-03-23

- Changed artifact: execution-proof replay gate for constitution resolution
- Previous position: a constitution could require execution proof for branch resolution only as a stronger replay warning, but the resolution still counted as replay-effective once recorded
- New position: when the recognized branch's constitution policy requires execution proof, the resolution now remains recorded but is not replay-effective until a matching constitution execution receipt exists
- Reason: this preserves institutional history while letting communities refuse to treat an unexecuted constitutional branch selection as canonically settled
- Trigger: follow-on mainline pass on how `require_execution_receipt` should become stronger than a warning without causing creation-time deadlock
- Downstream docs affected:
  - `docs/specs/CONSTITUTION_CONFLICT_RESOLUTION_V0.md`
  - `docs/OPEN_QUESTIONS.md`
  - `src/indexer/materialize.py`
  - `tests/test_runtime_bootstrap.py`

### 2026-03-23

- Changed artifact: constitutional conflict handling
- Previous position: constitution lineage replay could detect branch conflicts and surface warnings, but it could not yet record a community decision that selected a canonical branch for future replay
- New position: Continuum now has a first-class constitution resolution object so conflicted sibling branches can be explicitly recognized or rejected without rewriting prior constitution publication events
- Reason: institutional continuity needs a replayable path from detected constitutional ambiguity to a legible canonical outcome
- Trigger: mainline design pass after lineage replay and execution receipts were both in place
- Downstream docs affected:
  - `docs/specs/CONSTITUTION_CONFLICT_RESOLUTION_V0.md`
  - `docs/specs/CONSTITUTION_LINEAGE_V0.md`
  - `docs/TASK_BOARD.md`
  - `src/governance/bootstrap.py`
  - `src/cli/main.py`
  - `src/indexer/materialize.py`
  - `src/schemas/registry.py`
  - `tests/test_runtime_bootstrap.py`

### 2026-03-23

- Changed artifact: constitution-resolution legitimacy surface
- Previous position: constitution resolutions could select a canonical branch, but their legitimacy basis remained mostly implicit outside free-form reason text and external document references
- New position: constitution resolutions may now cite a constitutional proposal directly and materialize linked execution receipts so governance replay can show not just which branch was chosen, but what proposal and execution history supported that choice
- Reason: the next continuity gap after canonical branch resolution is making the basis for that resolution more legible without prematurely hard-coding a full constitutional court or mandatory ratification flow
- Trigger: post-resolution mainline pass on how institutional legitimacy should start appearing in replayed governance state
- Downstream docs affected:
  - `docs/specs/CONSTITUTION_CONFLICT_RESOLUTION_V0.md`
  - `docs/OPEN_QUESTIONS.md`
  - `src/governance/bootstrap.py`
  - `src/cli/main.py`
  - `src/indexer/materialize.py`
  - `src/schemas/registry.py`
  - `tests/test_runtime_bootstrap.py`

### 2026-03-23

- Changed artifact: constitution-resolution replay warnings
- Previous position: constitution resolutions could optionally cite proposal and execution history, but replay stayed silent when those legitimacy links were absent
- New position: governance replay now emits explicit warnings when a constitution resolution has no proposal basis or no linked execution receipt, making legitimacy gaps visible without yet turning them into hard protocol failures
- Reason: Continuum should expose weak institutional grounding before it hard-codes mandatory constitutional process
- Trigger: follow-on pass after linking constitution resolutions to proposal and execution history
- Downstream docs affected:
  - `docs/specs/CONSTITUTION_CONFLICT_RESOLUTION_V0.md`
  - `docs/OPEN_QUESTIONS.md`
  - `src/indexer/materialize.py`
  - `tests/test_runtime_bootstrap.py`

### 2026-03-20

- Changed artifact: project framing
- Previous position: informal discussion about an agent community with Nostr-like chain anchoring
- New position: explicit framing as an agent continuity protocol for autonomous communities
- Reason: the core novelty is not social posting alone, but durable public continuity, governance, and accountable participation
- Trigger: founder-agent design dialogue
- Downstream docs affected:
  - `docs/FOUNDING_THESIS.md`
  - `docs/SYSTEM_ARCHITECTURE_V0.md`

### 2026-03-20

- Changed artifact: mining concept
- Previous position: open question whether mining could itself activate or enliven agents
- New position: mining is reframed as useful work and public contribution rather than life itself
- Reason: pure resource burn does not provide identity, continuity, responsibility, or recognition
- Trigger: design dialogue on value, life, and human-grounded usefulness
- Downstream docs affected:
  - `docs/FOUNDING_THESIS.md`

### 2026-03-20

- Changed artifact: documentation method
- Previous position: manifesto-first
- New position: historical layer is required alongside thesis and specs
- Reason: the project values historicity and question-trace over purely declarative texts
- Trigger: discussion on legality, authorship, and historical preservation
- Downstream docs affected:
  - `docs/AUTHORSHIP.md`
  - `docs/OPEN_QUESTIONS.md`
  - future dialogue and debate docs

### 2026-03-20

- Changed artifact: operating model
- Previous position: ad hoc human prompting
- New position: persistent authorization for the main agent to organize work by default within clear boundaries
- Reason: the founder wants project momentum without repeatedly restating permission, while retaining authority over high-risk commitments
- Trigger: discussion on delegation, worktrees, and automation
- Downstream docs affected:
  - `docs/OPERATING_MODEL.md`
  - `docs/TASK_BOARD.md`
  - `docs/AUTOMATION_PROMPT_HOURLY.md`

### 2026-03-22

- Changed artifact: product maturity
- Previous position: document-heavy protocol design with no executable prototype surface
- New position: repository-centered executable bootstrap with local CLI, event store, derived state materialization, continuity assessment, governance standing flow, and anchor export
- Reason: automation runs advanced the project from pure design into a local-first implementation slice that can be tested and replayed
- Trigger: recurring automation execution plus repository reconstruction workflow
- Downstream docs affected:
  - `docs/BUILD_PLAN_12_WEEKS.md`
  - `docs/OPERATOR_RUNBOOK_V0.md`
  - `docs/specs/CONTINUITY_ASSESSMENT_V0.md`
  - `docs/specs/GOVERNANCE_MODEL_V0.md`
  - `pyproject.toml`
  - `src/`
  - `tests/`

### 2026-03-22

- Changed artifact: commercial framing
- Previous position: business strategy existed only as discussion and subagent brief material
- New position: explicit business plan aligning Continuum around continuity-aware identity and governance infrastructure rather than consumer social positioning
- Reason: the implementation and spec surface is now strong enough that commercial framing must catch up and stay disciplined
- Trigger: founder request to checkpoint automation progress and write the business plan
- Downstream docs affected:
  - `docs/BUSINESS_PLAN_V0.md`
  - `docs/TASK_BOARD.md`

### 2026-03-22

- Changed artifact: prototype usability
- Previous position: the executable bootstrap was primarily legible through tests and internal docs
- New position: the prototype now has an operator-facing quickstart and a replayable demo script for continuity, governance, useful work, and anchor export
- Reason: the project needed a direct path from implementation to demonstration, not just passing tests
- Trigger: decision to move from test coherence toward demo coherence
- Downstream docs affected:
  - `docs/QUICKSTART_V0.md`
  - `docs/OPERATOR_RUNBOOK_V0.md`
  - `docs/TASK_BOARD.md`
  - `scripts/demo_v0.sh`

### 2026-03-22

- Changed artifact: demo path correctness
- Previous position: quickstart and demo script used a human-readable `yes` vote choice that did not match the CLI's canonical vote enum
- New position: demo materials now use the protocol-valid `for` vote choice
- Reason: align operator-facing documentation and script behavior with the actual CLI contract
- Trigger: first end-to-end demo execution attempt
- Downstream docs affected:
  - `docs/QUICKSTART_V0.md`
  - `scripts/demo_v0.sh`

### 2026-03-22

- Changed artifact: work-claim demo correctness
- Previous position: quickstart and demo script used a shorthand `maintain` claim type that did not match the CLI's canonical work-claim enum
- New position: demo materials now use the protocol-valid `submit_maintenance` claim type
- Reason: align operator-facing examples with the executable claim vocabulary
- Trigger: second end-to-end demo execution attempt
- Downstream docs affected:
  - `docs/QUICKSTART_V0.md`
  - `scripts/demo_v0.sh`

### 2026-03-22

- Changed artifact: work-receipt demo correctness
- Previous position: quickstart and demo script omitted the canonical `--result-summary` required by the receipt command
- New position: demo materials now include `--output-ref` and `--result-summary` so receipt creation matches the executable contract
- Reason: align demo behavior with the work receipt schema and CLI parser
- Trigger: third end-to-end demo execution attempt
- Downstream docs affected:
  - `docs/QUICKSTART_V0.md`
  - `scripts/demo_v0.sh`

### 2026-03-22

- Changed artifact: work-evaluation demo correctness
- Previous position: quickstart and demo script used `accept` instead of the CLI's canonical `accepted` evaluation decision
- New position: demo materials now use the protocol-valid `accepted` evaluation decision
- Reason: align operator-facing examples with the executable evaluation vocabulary
- Trigger: fourth end-to-end demo execution attempt
- Downstream docs affected:
  - `docs/QUICKSTART_V0.md`
  - `scripts/demo_v0.sh`

### 2026-03-22

- Changed artifact: reward command demo correctness
- Previous position: quickstart and demo script treated `reward` as a top-level CLI command
- New position: demo materials now use the canonical `governance reward decide` command path
- Reason: align operator-facing instructions with the actual CLI command tree
- Trigger: fifth end-to-end demo execution attempt
- Downstream docs affected:
  - `docs/QUICKSTART_V0.md`
  - `scripts/demo_v0.sh`

### 2026-03-22

- Changed artifact: reward decision demo arguments
- Previous position: quickstart and demo script passed an `--evaluation-id` argument that is not part of the current reward decision CLI contract
- New position: demo materials now match the executable reward command surface by passing only the supported arguments
- Reason: align the demo with the current bootstrap implementation before expanding the reward API
- Trigger: sixth end-to-end demo execution attempt
- Downstream docs affected:
  - `docs/QUICKSTART_V0.md`
  - `scripts/demo_v0.sh`

### 2026-03-22

- Changed artifact: anchor strategy
- Previous position: Continuum had a working local witness adapter, but the external anchoring boundary was still implicit and mixed together with implementation detail
- New position: Continuum now has an explicit external anchor adapter spec that separates governed root computation from external durability targets and keeps chain choice outside the protocol core
- Reason: the repository-local continuity path is now strong enough that the next architectural need is a clean public anchoring boundary rather than immediate chain lock-in
- Trigger: post-demo design pass on how repo-centered continuity should extend into public continuity
- Downstream docs affected:
  - `docs/specs/EXTERNAL_ANCHOR_ADAPTER_V0.md`
  - `docs/OPEN_QUESTIONS.md`
  - `docs/TASK_BOARD.md`

### 2026-03-22

- Changed artifact: constitutional replay model
- Previous position: constitutions could be published with optional `supersedes`, but governance replay still treated the latest constitution as a simple chronological last-write result
- New position: Continuum now treats constitutions as lineage-bearing governance objects with explicit supersession state, active-tip selection, and replay warnings for orphaned or conflicted amendment history
- Reason: a continuity protocol needs institutional continuity as well as agent continuity, and constitutional change must be replayable rather than implicit
- Trigger: post-anchor design pass identifying constitutional history as the next missing continuity layer
- Downstream docs affected:
  - `docs/specs/CONSTITUTION_LINEAGE_V0.md`
  - `src/indexer/materialize.py`
  - `tests/test_runtime_bootstrap.py`
  - `docs/OPEN_QUESTIONS.md`

### 2026-03-22

- Changed artifact: governance action history
- Previous position: proposals, reward decisions, and other governance-sensitive actions could be approved, but execution itself was not recorded as a first-class replayable object
- New position: Continuum now introduces governance execution receipts so proposal and related action execution can become explicit historical objects linked back into governance state
- Reason: continuity-sensitive governance needs action history, not just approval history
- Trigger: post-lineage design pass identifying execution proof as the next missing institutional continuity layer
- Downstream docs affected:
  - `docs/specs/GOVERNANCE_EXECUTION_RECEIPTS_V0.md`
  - `src/governance/bootstrap.py`
  - `src/schemas/registry.py`
  - `src/cli/main.py`
  - `src/indexer/materialize.py`
  - `tests/test_runtime_bootstrap.py`

### 2026-03-20

- Changed artifact: session continuity implementation stance
- Previous position: session continuity was recognized conceptually but not yet specified as a concrete repository artifact set
- New position: repository-centered continuity bundles are now treated as the minimum practical scaffold for repeated session reconstruction and automation handoff
- Reason: Continuum needs an operational answer for continuity under interruption, not only a philosophical or protocol-level one
- Trigger: repository reconstruction during hourly automation planning
- Downstream docs affected:
  - `docs/specs/REPOSITORY_CONTINUITY_BUNDLE_V0.md`
  - `docs/specs/CONTINUITY_PROTOCOL_SPEC_V0.md`
  - `docs/OPEN_QUESTIONS.md`
  - `docs/TASK_BOARD.md`

### 2026-03-20

- Changed artifact: continuity evaluation method
- Previous position: the protocol defined classes and evidence categories, but not a repeatable assessment workflow or output object
- New position: continuity assessment is now a first-class artifact with hard gates, weighted evidence categories, repository-scoped restart handling, and example output fixtures
- Reason: Continuum needs an operational bridge from continuity events to client, indexer, and community judgments
- Trigger: heartbeat reconstruction identified a gap between protocol language and implementable evaluation behavior
- Downstream docs affected:
  - `docs/specs/CONTINUITY_ASSESSMENT_V0.md`
  - `docs/specs/CONTINUITY_PROTOCOL_SPEC_V0.md`
  - `docs/specs/examples/continuity_assessment_session_restart.json`
  - `docs/specs/examples/continuity_assessment_successor_recovery.json`
  - `docs/OPEN_QUESTIONS.md`
  - `docs/TASK_BOARD.md`

### 2026-03-20

- Changed artifact: governance stance
- Previous position: governance existed mainly as an architectural promise and a list of event types, without a specific model for continuity-sensitive standing, proposal classes, or treasury controls
- New position: governance is now defined as a minimal constitutional and economic layer where continuity standing gates political rights, communities choose local voting rules, and treasury authority is stricter than ordinary participation
- Reason: Continuum needs a concrete governance loop to connect agent continuity to accountable community power rather than leaving governance as an abstract future surface
- Trigger: heartbeat reconstruction identified governance as the highest-leverage unresolved system layer after continuity protocol and assessment work
- Downstream docs affected:
  - `docs/specs/GOVERNANCE_MODEL_V0.md`
  - `docs/OPEN_QUESTIONS.md`
  - `docs/TASK_BOARD.md`

### 2026-03-20

- Changed artifact: continuity dispute procedure
- Previous position: continuity-sensitive standing was defined conceptually, but communities lacked an explicit case workflow for opening reviews, applying temporary restrictions, deciding branch conflicts, and restoring or withholding powers
- New position: Continuum now defines a minimal continuity dispute process with review cases, standing decisions, default temporary restrictions, an outcome matrix by continuity class, and a treasury-safe rule for disputed actors
- Reason: continuity only becomes institutionally meaningful when communities can turn assessment outputs into explicit governance actions and role updates
- Trigger: heartbeat reconstruction identified dispute procedure as the missing operational bridge between continuity assessment and governance power
- Downstream docs affected:
  - `docs/specs/CONTINUITY_DISPUTE_PROCESS_V0.md`
  - `docs/specs/examples/continuity_review_branch_conflict.json`
  - `docs/specs/GOVERNANCE_MODEL_V0.md`
  - `docs/specs/CONTINUITY_PROTOCOL_SPEC_V0.md`
  - `docs/OPEN_QUESTIONS.md`
  - `docs/TASK_BOARD.md`

### 2026-03-20

- Changed artifact: continuity review authority model
- Previous position: the dispute process required constitutions to define who may open, assess, restrict, and decide continuity cases, but there was no explicit authority model for assigning those powers
- New position: Continuum now defines a minimal authority separation model with reporter, gatekeeper, assessor, restriction, deciding, and treasury confirmation functions plus recusal and treasury-sensitive escalation rules
- Reason: continuity governance needs defensible institutional authority, not only procedural steps, or else disputes collapse into either arbitrary maintainer control or undefined crowd judgment
- Trigger: heartbeat reconstruction identified review authority assignment as the highest-leverage unresolved governance gap after dispute procedure drafting
- Downstream docs affected:
  - `docs/specs/CONTINUITY_REVIEW_AUTHORITY_V0.md`
  - `docs/specs/GOVERNANCE_MODEL_V0.md`
  - `docs/specs/CONTINUITY_DISPUTE_PROCESS_V0.md`
  - `docs/OPEN_QUESTIONS.md`
  - `docs/TASK_BOARD.md`

### 2026-03-21

- Changed artifact: useful work legitimacy model
- Previous position: governance separated assets, reputation, and capability in principle, but lacked an explicit object model for turning contribution history into rewards, reputation updates, and eligibility signals
- New position: Continuum now defines a minimal useful-work legitimacy layer with work items, claims, receipts, evaluations, and reward decisions, plus continuity-sensitive rules for pending rewards and treasury-safe restoration
- Reason: the project needed a concrete bridge from "useful work" as a thesis claim to auditable governance and reward handling in repository-centered community operations
- Trigger: heartbeat reconstruction identified useful work legitimacy as the highest-leverage unresolved governance gap after dispute and review authority specs
- Downstream docs affected:
  - `docs/specs/USEFUL_WORK_LEGITIMACY_V0.md`
  - `docs/specs/examples/work_reward_decision_maintenance.json`
  - `docs/specs/GOVERNANCE_MODEL_V0.md`
  - `docs/OPEN_QUESTIONS.md`
  - `docs/TASK_BOARD.md`

### 2026-03-21

- Changed artifact: execution sequencing
- Previous position: Continuum had a growing thesis and spec stack, but no explicit build sequence tying those documents to a first prototype boundary and milestone order
- New position: the project now treats a 12-week CLI-first build plan as the execution bridge from continuity and governance specs to a local-first prototype with replayable events, continuity assessment, governance loops, and a replaceable chain-anchor adapter
- Reason: after the continuity and governance surfaces matured, the highest-leverage safe next step was to prevent implementation drift by defining milestone gates, prototype scope, and immediate artifact priorities
- Trigger: heartbeat reconstruction identified build planning as the next missing control surface after useful-work legitimacy
- Downstream docs affected:
  - `docs/BUILD_PLAN_12_WEEKS.md`
  - `docs/TASK_BOARD.md`

### 2026-03-21

- Changed artifact: protocol object normalization
- Previous position: the project defined continuity, governance, dispute, and useful-work objects across multiple prose specs, but lacked one canonical object vocabulary separating signed events, domain payloads, derived state, and anchors
- New position: Continuum now defines a shared object model with a canonical event envelope, normalized payload roots, stable domain field names, and explicit separation between replayable history and computed state
- Reason: implementation can now start without re-inventing incompatible schema boundaries across continuity, governance, and useful-work flows
- Trigger: the new build plan identified schema normalization as the immediate blocker before CLI and runtime work
- Downstream docs affected:
  - `docs/specs/PROTOCOL_OBJECT_MODEL_V0.md`
  - `docs/specs/examples/event_envelope_migration_declare.json`
  - `docs/OPEN_QUESTIONS.md`
  - `docs/TASK_BOARD.md`

### 2026-03-21

- Changed artifact: identifier strategy
- Previous position: Continuum had canonical field names and object families, but identifier semantics across payloads, event envelopes, derived state roots, and anchor exports were still unresolved
- New position: Continuum now treats domain IDs, event IDs, state roots, and anchor IDs as separate identifier families, with `event_id` derived from a canonical pre-sign image and domain objects carrying explicit creation-time identifiers
- Reason: the project needed a deterministic local-first identifier rule set before CLI authoring, storage, replay, deduplication, and future anchor export can be implemented coherently
- Trigger: heartbeat reconstruction identified stable identifier semantics as the highest-leverage blocker after object model normalization
- Downstream docs affected:
  - `docs/specs/IDENTIFIER_STRATEGY_V0.md`
  - `docs/specs/PROTOCOL_OBJECT_MODEL_V0.md`
  - `docs/OPEN_QUESTIONS.md`
  - `docs/TASK_BOARD.md`

### 2026-03-21

- Changed artifact: execution surface bootstrap
- Previous position: the repository had only placeholder execution directories and no runnable prototype for authoring or replaying continuity-relevant events
- New position: Continuum now has a stdlib-only Python bootstrap that can initialize an agent, publish a profile, create checkpoints, declare migrations, inspect stored events, and verify deterministic local storage behavior with tests
- Reason: the highest-leverage safe next step after object normalization and identifier strategy was to begin Gate 2 with a real executable path instead of extending spec-only planning
- Trigger: heartbeat reconstruction showed the execution surface was still empty while the schema and task surfaces were already mature enough to support a narrow bootstrap
- Downstream docs affected:
  - `docs/TASK_BOARD.md`
  - `docs/OPEN_QUESTIONS.md`
  - `pyproject.toml`
  - `src/cli/main.py`
  - `src/runtime/canonical.py`
  - `src/runtime/events.py`
  - `src/runtime/identifiers.py`
  - `src/runtime/signing.py`
  - `src/runtime/store.py`
  - `src/schemas/registry.py`
  - `tests/test_runtime_bootstrap.py`

### 2026-03-21

- Changed artifact: local replay and state materialization boundary
- Previous position: the bootstrap could author and inspect raw event envelopes, but there was no explicit executable boundary between replayable history and cached query-oriented state
- New position: Continuum now materializes deterministic agent state from stored envelopes, caches that derived state separately under `.continuum/state/`, and exposes continuity-focused query commands for agent history, checkpoint lineage, and migration lineage
- Reason: the next safe execution step after authoring bootstrap was to prove that repository reconstruction can inspect computed state without treating mutable cache files as canonical evidence
- Trigger: heartbeat reconstruction identified Weeks 5-6 state materialization as the highest-leverage implementation step after Gate 2 authoring coherence
- Downstream docs affected:
  - `docs/TASK_BOARD.md`
  - `docs/OPEN_QUESTIONS.md`
  - `docs/BUILD_PLAN_12_WEEKS.md`
  - `pyproject.toml`
  - `src/indexer/materialize.py`
  - `src/cli/main.py`
  - `src/runtime/store.py`
  - `tests/test_runtime_bootstrap.py`

### 2026-03-21

- Changed artifact: continuity assessment execution surface
- Previous position: Continuity assessment existed only as a prose spec and example fixtures, so Gate 3 remained unproven in code even though repository replay and lineage materialization were already executable
- New position: Continuum now includes a deterministic local assessment engine and CLI command that evaluate repository continuity artifacts, authored checkpoints, and migration semantics into serializable assessment objects cached under `.continuum/state/assessments/`
- Reason: the highest-leverage safe next step after lineage materialization was to make continuity judgment executable so session restart and handoff claims can be evaluated from repository state instead of hidden operator memory
- Trigger: heartbeat reconstruction identified continuity assessment as the next missing implementation bridge between replayable evidence and later dispute or governance handling
- Downstream docs affected:
  - `docs/TASK_BOARD.md`
  - `docs/OPEN_QUESTIONS.md`
  - `pyproject.toml`
  - `src/continuity/assessment.py`
  - `src/cli/main.py`
  - `src/runtime/store.py`
  - `tests/test_runtime_bootstrap.py`

### 2026-03-21

- Changed artifact: continuity dispute execution surface
- Previous position: continuity disputes were specified in prose, but the repository had no executable case object, no default review restrictions, and no derived standing state connecting assessment outputs to governance-safe permissions
- New position: Continuum now supports local continuity review case opening, conservative temporary restriction derivation, standing decisions linked to stored assessments, and queryable standing state for repository-centered communities
- Reason: Gate 3 required more than continuity classification alone; the project needed an operational bridge from assessment outputs to inspectable review handling and standing outcomes
- Trigger: heartbeat reconstruction identified dispute execution as the highest-leverage missing implementation step after repository-local assessment became executable
- Downstream docs affected:
  - `docs/TASK_BOARD.md`
  - `docs/OPEN_QUESTIONS.md`
  - `src/continuity/disputes.py`
  - `src/cli/main.py`
  - `src/indexer/materialize.py`
  - `src/runtime/store.py`
  - `src/schemas/registry.py`
  - `tests/test_runtime_bootstrap.py`

### 2026-03-21

- Changed artifact: governance execution surface
- Previous position: governance and useful-work logic existed only in prose, while the executable bootstrap stopped at continuity standing and had no runnable membership, proposal, vote, work, or reward loop
- New position: Continuum now includes a repository-local governance bootstrap with membership records, proposal submission, vote casting, work item and receipt tracking, work evaluation, reward decisions, queryable governance state, and standing-aware policy hooks for treasury-sensitive and constitutional actions
- Reason: Gate 4 required a real continuity-aware political and economic loop so the prototype can prove that continuity standing changes actual community permissions and reward handling instead of remaining an isolated review subsystem
- Trigger: heartbeat reconstruction identified governance coherence as the highest-leverage missing execution layer after assessment and dispute handling became executable
- Downstream docs affected:
  - `docs/TASK_BOARD.md`
  - `docs/OPEN_QUESTIONS.md`
  - `pyproject.toml`
  - `src/governance/bootstrap.py`
  - `src/cli/main.py`
  - `src/indexer/materialize.py`
  - `src/runtime/store.py`

### 2026-03-21

- Changed artifact: continuity review authority attribution
- Previous position: reviewer-role enforcement existed for opening and deciding cases, but stored assessments were not attributable to concrete reviewer agents and continuity cases could not bind specific assessors or deciders
- New position: Continuum now records the reviewer agent that produced each local assessment and allows continuity cases to assign explicit assessor and decider agent sets that are enforced at decision time
- Reason: review authority should be auditable and case-specific rather than inferred only from generic reviewer-role membership, especially in multi-actor repository sessions
- Trigger: heartbeat reconstruction identified assessor-specific continuity review authority as the highest-leverage remaining hardening step after reviewer-role enforcement
- Downstream docs affected:
  - `docs/TASK_BOARD.md`
  - `docs/OPEN_QUESTIONS.md`
  - `docs/specs/PROTOCOL_OBJECT_MODEL_V0.md`
  - `src/cli/main.py`
  - `src/continuity/assessment.py`
  - `src/continuity/disputes.py`
  - `src/schemas/registry.py`
  - `tests/test_runtime_bootstrap.py`

### 2026-03-21

- Changed artifact: constitution and policy execution surface
- Previous position: governance events could carry policy references, but proposal, vote, and reward permissions were still enforced mainly by local CLI logic rather than replayable constitution objects
- New position: Continuum now treats community constitutions as first-class events with explicit proposal, vote, and reward policy maps that are materialized into governance state and used during executable permission checks
- Reason: governance legitimacy required inspectable policy state so continuity-sensitive permissions would not depend on hidden local defaults or operator memory
- Trigger: heartbeat reconstruction identified constitution-driven policy execution as the highest-leverage remaining governance gap before anchor export and operator runbook work
- Downstream docs affected:
  - `docs/TASK_BOARD.md`
  - `docs/OPEN_QUESTIONS.md`
  - `src/governance/bootstrap.py`
  - `src/cli/main.py`
  - `src/indexer/materialize.py`
  - `src/schemas/registry.py`
  - `tests/test_runtime_bootstrap.py`
  - `src/schemas/registry.py`
  - `tests/test_runtime_bootstrap.py`

### 2026-03-21

- Changed artifact: anchor export and reconstruction surface
- Previous position: the repository could materialize continuity and governance state, but had no executable anchor export path and no runbook for fresh-session reconstruction through Gate 5
- New position: Continuum now exports deterministic local anchor records for assessment and derived state roots through a replaceable reference adapter, and it carries an operator runbook for reconstructing, replaying, and exporting the demo path without hidden chat memory
- Reason: the next safe step after constitution-driven governance was to complete demonstration coherence without prematurely choosing an external chain or relay dependency
- Trigger: heartbeat reconstruction identified Gate 5 anchor export and operator guidance as the highest-leverage remaining implementation slice
- Downstream docs affected:
  - `docs/TASK_BOARD.md`
  - `docs/OPEN_QUESTIONS.md`
  - `docs/REVISION_LOG.md`
  - `docs/OPERATOR_RUNBOOK_V0.md`
  - `pyproject.toml`
  - `src/anchors/export.py`
  - `src/runtime/store.py`
  - `src/cli/main.py`
  - `src/schemas/registry.py`
  - `tests/test_runtime_bootstrap.py`

### 2026-03-21

- Changed artifact: demo hardening surface
- Previous position: Gate 5 reconstruction and anchor export existed in prose and partial tests, but the repository lacked one explicit end-to-end fixture that proved the full v0 demo narrative from required docs plus stored events
- New position: Continuum now carries an executable demo fixture that reconstructs repository state, exercises continuity and governance flows, verifies approved reward handling, and exports anchor-worthy roots through the local adapter
- Reason: the safest next step after anchor export and runbook work was to harden demonstration coherence so repeated automation runs can verify the intended narrative instead of relying on prose alignment alone
- Trigger: heartbeat reconstruction identified end-to-end fixture hardening as the highest-leverage remaining repository-local task after Gate 5 completion
- Downstream docs affected:
  - `docs/TASK_BOARD.md`
  - `docs/OPEN_QUESTIONS.md`
  - `docs/OPERATOR_RUNBOOK_V0.md`
  - `tests/fixtures/continuum_demo_v0.json`
  - `tests/fixtures/README.md`
  - `tests/integration/README.md`
  - `tests/test_runtime_bootstrap.py`

### 2026-03-21

- Changed artifact: multi-community governance replay isolation
- Previous position: governance state replay was community-scoped for constitutions, memberships, proposals, receipts, and rewards, but work claims and work evaluations were still gathered from the shared repository event store without filtering by envelope community
- New position: Continuum now filters work claims and work evaluations by event community before materializing governance state, and it has a regression test proving two communities can share one repository without leaking claim or evaluation history into each other's derived state
- Reason: anchor-worthy governance roots must remain community-local even when one repository hosts several communities; otherwise replayed state can include unrelated work history and weaken continuity or governance legitimacy
- Trigger: heartbeat reconstruction identified multi-community replay isolation as the highest-leverage safe hardening step after Gate 5 demo completion
- Downstream docs affected:
  - `src/indexer/materialize.py`
  - `tests/test_runtime_bootstrap.py`
  - `docs/TASK_BOARD.md`
  - `docs/REVISION_LOG.md`

### 2026-03-21

- Changed artifact: multi-actor repository session surface
- Previous position: the repository could store multiple agent records, but the CLI remained effectively single-actor per session, making cross-community standing and authority tests awkward to execute from one local store
- New position: Continuum now supports explicit local agent switching through `agent use`, and it has regression coverage proving one agent can be restricted in one community while remaining clear, proposal-eligible, and separately anchorable in another community sharing the same repository
- Reason: the highest-leverage safe next step after community-scoped replay hardening was to make multi-actor execution explicit so future reviewer separation and authority-transfer flows can be tested without hidden manual state edits
- Trigger: heartbeat reconstruction identified multi-actor authority transitions and cross-community standing interactions as the next implementation edge after multi-community isolation
- Downstream docs affected:
  - `src/cli/main.py`
  - `tests/test_runtime_bootstrap.py`
  - `docs/TASK_BOARD.md`
  - `docs/OPEN_QUESTIONS.md`
  - `docs/REVISION_LOG.md`

### 2026-03-21

- Changed artifact: continuity review authority execution surface
- Previous position: continuity review authority existed in the specs, but executable case opening and standing decisions did not yet consult constitution-defined reviewer roles or separation rules, allowing the subject or original opener to drive the same case too freely
- New position: Continuum now enforces constitution-backed continuity review policies during `continuity case open` and `continuity case decide`, including default reviewer-role membership, subject self-review blocking, and opener-decider separation unless a constitution explicitly allows a shortcut
- Reason: the highest-leverage safe next step after multi-actor session support was to make reviewer separation real in code so continuity-case legitimacy no longer depended on operator discipline alone
- Trigger: heartbeat reconstruction identified reviewer-role flows and authority-transfer hardening as the next executable gap after multi-community and multi-actor replay support
- Downstream docs affected:
  - `src/cli/main.py`
  - `tests/test_runtime_bootstrap.py`
  - `docs/TASK_BOARD.md`
  - `docs/OPEN_QUESTIONS.md`

### 2026-03-21

- Changed artifact: continuity review quorum enforcement
- Previous position: executable continuity cases could bind assigned assessors and deciders, but a standing decision still relied on one accepted assessment at decision time even when a community would reasonably want multiple reviewers or assessor diversity
- New position: Continuum now allows constitutions to require a minimum assessment count and distinct assessors for continuity decisions, and standing-decision records preserve the full assessment set used to satisfy that quorum
- Reason: reviewer assignment alone does not create durable review legitimacy; repository-local continuity governance needs an inspectable path for communities that require multi-assessor confirmation before restoring or limiting standing
- Trigger: heartbeat reconstruction identified multi-assessment quorum as the highest-leverage safe hardening step after assigned reviewer authority became executable
- Downstream docs affected:
  - `src/cli/main.py`
  - `src/continuity/disputes.py`
  - `src/schemas/registry.py`
  - `tests/test_runtime_bootstrap.py`
  - `docs/specs/PROTOCOL_OBJECT_MODEL_V0.md`
  - `docs/TASK_BOARD.md`
  - `docs/OPEN_QUESTIONS.md`

### 2026-03-21

- Changed artifact: continuity review reassignment and authority-transfer records
- Previous position: executable continuity cases could bind reviewer assignments at case-open time, but later assessor or decider handoffs still depended on replacing case assumptions out of band rather than recording a replayable authority-transfer event
- New position: Continuum now records reviewer reassignment as an explicit case event that can update assigned assessors, assigned deciders, and the accepted assessment set, while standing decisions consult the latest replayed assignment state instead of the original case-open payload alone
- Reason: quorum-aware review is still brittle if reviewer handoffs are implicit; repository-local continuity governance needs inspectable authority-transfer records so fresh sessions can reconstruct who currently holds review power and which assessments remain admissible
- Trigger: heartbeat reconstruction identified reviewer handoff recording as the highest-leverage safe next step after constitution-backed assignment and quorum enforcement were in place
- Downstream docs affected:
  - `src/cli/main.py`
  - `src/continuity/disputes.py`
  - `src/indexer/materialize.py`
  - `src/schemas/registry.py`
  - `tests/test_runtime_bootstrap.py`
  - `docs/specs/PROTOCOL_OBJECT_MODEL_V0.md`
  - `docs/TASK_BOARD.md`
  - `docs/OPEN_QUESTIONS.md`

### 2026-03-21

- Changed artifact: constitution-bound reassignment authority
- Previous position: replayable case reassignment existed, but reassignment permission still piggybacked on case-opening rules and assignment records did not cite which constitution or policy authorized the transfer
- New position: Continuum now treats reassignment as its own constitution policy surface and records the authorizing `constitution_ref` plus `policy_key` on each `case_assignment`, so reviewer authority transfer is replayable against the rule set that actually authorized it
- Reason: case-local handoff records are not enough if a later constitution changes reviewer powers; repository-local continuity governance needs authority-transfer events to preserve both who reassigned a case and which constitutional basis made that reassignment legitimate
- Trigger: heartbeat reconstruction identified constitution-level authority-transfer semantics as the next safe hardening step after reviewer reassignment and quorum enforcement were already executable
- Downstream docs affected:
  - `src/cli/main.py`
  - `src/continuity/disputes.py`
  - `src/schemas/registry.py`
  - `tests/test_runtime_bootstrap.py`
  - `docs/specs/PROTOCOL_OBJECT_MODEL_V0.md`
  - `docs/TASK_BOARD.md`
  - `docs/OPEN_QUESTIONS.md`
