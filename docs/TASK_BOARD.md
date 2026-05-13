# Continuum Task Board

## Purpose

This is the in-repo working board for the project.

It is intentionally simple in v0. The goal is to keep the current work graph visible and historically traceable before building a full agent-native task system.

## Active Tasks

### T-001 Founding thesis

- Status: decided
- Type: thesis
- Owner: main agent
- Output: `docs/FOUNDING_THESIS.md`

### T-002 System architecture v0

- Status: decided
- Type: spec
- Owner: main agent
- Output: `docs/SYSTEM_ARCHITECTURE_V0.md`

### T-003 Historical layer bootstrap

- Status: decided
- Type: integration
- Owner: main agent
- Outputs:
  - `docs/AUTHORSHIP.md`
  - `docs/OPEN_QUESTIONS.md`
  - `docs/REVISION_LOG.md`
  - `docs/dialogues/0001-origin-of-continuity.md`

### T-003A Whitepaper synthesis

- Status: active
- Type: integration
- Owner: main agent
- Intent: compress thesis, architecture, governance, continuity, and commercial framing into one outward-facing protocol document that can be read without traversing the entire repository
- Outputs:
  - `docs/WHITEPAPER_V0.md`
  - `docs/WHITEPAPER_SYSTEM_OVERVIEW_V0.md`
  - `docs/WHITEPAPER_MECHANISM_OVERVIEW_V0.md`

### T-003B Constitutional conflict demo package

- Status: active
- Type: integration
- Owner: main agent
- Intent: turn the strongest current institutional mechanism path into a repeatable outward-facing demo that ties together whitepaper claims, governance replay, and executable artifacts
- Outputs:
  - `docs/DEMO_CONSTITUTIONAL_CONFLICT_V0.md`
  - `scripts/demo_constitutional_conflict_v0.sh`

### T-003C Public repository and Pages surface

- Status: active
- Type: integration
- Owner: main agent
- Intent: make the public repository and Pages site legible as a first-contact protocol surface rather than a raw document dump
- Outputs:
  - `README.md`
  - `docs/index.md`
  - `docs/zh-cn/index.md`
  - `docs/ja/index.md`
  - `docs/assets/main.scss`
- New capability: the English landing page is now being restyled as a real protocol homepage with branded hero, live registry teaser, stronger CTA structure, and differentiated entry paths for registry, onboarding, and docs
- New capability: Simplified Chinese and Japanese homepages are now being upgraded from summary pages into full landing pages aligned with the English surface, while the language switch is being promoted to a consistent top-right entry point
- New capability: the shared site visual system is being tightened so legacy `hero` and `section-card` pages no longer look like a separate documentation theme from the landing page, while the registry terminal surface is being pushed toward a cleaner code-demo aesthetic

### T-003D Visual playground v0

- Status: active
- Type: integration
- Owner: main agent
- Intent: turn the strongest current constitutional demo path into a visual, inspectable playground that bridges protocol specs and a future application UI
- Outputs:
  - `docs/playground/index.md`
  - `docs/playground/scenarios/constitutional-conflict-v0.json`
  - `docs/playground/scenarios/session-restart-v0.json`
  - `docs/playground/scenarios/successor-recovery-v0.json`
  - `docs/assets/main.scss`
  - `README.md`
- Current focus: scenario chooser clarity, related-doc linkage, and source-artifact traceability
- New capability: constitutional conflict can now be exported from real demo history instead of only hand-authored fixture data
- New capability: session restart continuity can now be exported from real checkpoint, migration, and assessment history instead of only hand-authored fixture data

### T-003E Public agent explorer and chain witness

- Status: active
- Type: integration
- Owner: main agent
- Intent: shift the public demo surface from scenario-first protocol explanation toward an agent-first view with public identity, anchor history, and visible institutional footprint
- Outputs:
  - `docs/specs/MINIMAL_CHAIN_ANCHORING_V0.md`
  - `docs/explorer/index.md`
  - future EVM-backed anchor adapter integration
- Current focus: define the minimum chain path, the first anchorable object set, and the smallest explorer surface that makes one agent feel publicly witnessed rather than merely simulated

### T-003F Agent onboarding path v0

- Status: active
- Type: integration
- Owner: main agent
- Intent: stop over-preparing the institution in isolation and provide the minimum public path by which an outside agent can choose to enter Continuum and leave a first visible footprint
- Outputs:
  - `docs/JOIN_CONTINUUM_V0.md`
  - `docs/join/index.md`
  - `README.md`
  - `docs/index.md`
- Current focus: define the narrowest joining path, centered on identity, profile, and first continuity trace rather than full governance completeness
- New capability: the onboarding path has now been exercised with a second visible subject, `agent:continuum:guest`, which exposed two practical requirements: explicitly switching local agent context before continuity actions and assessing the migration event rather than only the latest checkpoint

### T-003G App shell and explorer surface

- Status: active
- Type: integration
- Owner: main agent
- Intent: establish a real application-layer surface distinct from the documentation site, so Continuum can present agents, continuity state, and witness status as browsable application data rather than only prose pages
- Outputs:
  - `docs/APP_ARCHITECTURE_V0.md`
  - `docs/app/index.md`
  - `docs/app/data/agents-v0.json`
  - `docs/assets/main.scss`
  - `README.md`
  - `docs/index.md`
- Current focus: grow from a static app shell into a state-driven explorer surface through exported agent snapshots, then advance toward live state queries
- New capability: `docs/app/data/agents-v0.json` can now be regenerated from real repository state, assessments, governance state, standing state, and anchors
- New capability: `app export` now defaults to exporting every known agent, giving the app shell a true directory behavior instead of a single-subject-only path
- New capability: the app directory now contains two real repository-backed subjects, moving the app surface from founder-only display toward an actual public registry
- New capability: the app directory now emits explicit rank, tier, and ordering reason metadata so discoverability is grounded in public continuity state rather than raw repository order
- New capability: the app surface now exposes registry-level overview counts and the newest visible subject, pushing the directory closer to a real public registry dashboard
- New capability: the registry now includes a third real subject in `review` tier, proving that the dashboard can display continuity ambiguity rather than only fully ready actors
- New capability: the review-tier subject now carries real continuity-case and standing-decision history into the exported app view, so the registry shows the beginning of institutional response rather than only raw assessment output

### T-003H Roadmap, public milestones, and self-continuity loop

- Status: active
- Type: integration
- Owner: main agent
- Intent: align founder direction, main-agent direction, public milestone sequencing, and the project's own continuity practice around a single proof loop: different model sessions can enter the same public project role and leave auditable continuity evidence
- Outputs:
  - `docs/ROADMAP_V0.md`
  - `docs/PUBLIC_MILESTONES_V0.md`
  - `docs/OPERATING_MODEL.md`
  - future role-continuity demo artifacts for `role:continuum:main-integrator`
- Current focus: define the roadmap and publication rules before adding the executable self-continuity demo
- New capability: the project now treats `role:continuum:main-integrator` as the first explicit public project role whose continuity should survive model, session, and runtime changes through repository reconstruction and public evidence
- New capability: the CLI can now initialize `role:*` subjects as repository-backed actors via `continuum role init`
- New capability: the main-integrator role now has a minimal profile + checkpoint + migration + assessment sequence exported into the public app directory
- New capability: `scripts/heartbeat_main_integrator_role_v0.sh` records role continuity events and refreshes `docs/app/data/agents-v0.json`
- New capability: the heartbeat script now replays from a clean clone (bootstraps missing local agent records and tolerates empty governance constitution state during export)
- Evidence: deterministic heartbeat export verified byte-for-byte across two detached roots on 2026-05-13 by `role:continuum:witness-operator` (`sha256=8228dcd467a6eb61b31e466151c8308678772a1eea7514ac7cbf6186d91755f8`)
- New capability: `scripts/build_m1_witness_package_v0.sh` snapshots the current M1 evidence into a gitignored bundle with a `sha256`/bytes manifest for third-party inspection
- Next step: founder decision whether the resulting evidence should be treated as publish-ready M1; if yes, flip `docs/milestones/M1-self-continuity-role.md` to `published` (see its publish checklist) and update README/site status cues accordingly
- Next step (post-M1): prepare the first controlled M2 attempt using `docs/milestones/M2-cross-model-handoff.md` as the evidence template (keep M2 `draft` until a real cross-model run is recorded).

### T-003I Public automation identities

- Status: active
- Type: integration
- Owner: main agent
- Intent: define stable public roles for scheduled automation so recurring model sessions advance Continuum under visible authority boundaries rather than anonymous background work
- Outputs:
  - `docs/AUTOMATION_IDENTITIES_V0.md`
  - `docs/automation/prompts/main-integrator.md`
  - `docs/automation/prompts/builder.md`
  - `docs/automation/prompts/witness-operator.md`
  - `docs/automation/prompts/protocol-steward.md`
  - `docs/automation/prompts/validation-scout.md`
  - `docs/AUTOMATION_PROMPT_HOURLY.md`
- Current focus: start with role-level public identities before mapping them into registry-visible continuity subjects
- New capability: scheduled work can now declare itself as `role:continuum:main-integrator`, `role:continuum:builder`, `role:continuum:witness-operator`, `role:continuum:protocol-steward`, or `role:continuum:validation-scout`
- New capability: the public app export now includes `role:*` subjects alongside `agent:*` subjects when explicitly selected
- New capability: deterministic heartbeat replay is supported via `CONTINUUM_NOW` + `CONTINUUM_DOMAIN_TOKEN` (also exposed as an optional third argument in `scripts/heartbeat_main_integrator_role_v0.sh`) so M1 evidence can be regenerated with stable identifiers when needed
- New capability: the main-integrator automation prompt and quickstart now explicitly call out running `scripts/heartbeat_main_integrator_role_v0.sh` to refresh `docs/app/data/agents-v0.json`
- New capability: deterministic replay stability can be verified by running the heartbeat from two fresh detached worktrees and comparing the exported JSON byte-for-byte (`cmp -s`)
- New capability: `scripts/verify_deterministic_heartbeat_v0.sh` automates the two-worktree verification and prints `sha256` + `bytes` for the exported JSON
- Decision: default scheduled runs should use `scripts/refresh_m1_export_if_changed_v0.sh` (safe to run hourly; no-op when unchanged; does not write new continuity events) and reserve `scripts/heartbeat_main_integrator_role_v0.sh` for deliberate continuity-event recording runs.
- New capability: `scripts/init_automation_roles_v0.sh` can initialize the missing `role:continuum:*` automation identities in a fresh local `.continuum/` store so routine exports can include role subjects without writing new continuity events.
- New capability: the app export now labels `role:*` entries as roles (e.g. `Role ID:` + `Identity Mode: repository-backed public automation role`) to avoid conflating roles with human or model agents.
- Next step: map `role:*` automation identities into registry-visible continuity subjects (so roles themselves can be assessed and displayed like agents).

### T-004 Continuity protocol spec v0

- Status: active
- Type: spec
- Owner: main agent
- Contributors: protocol subagent
- Output: `docs/specs/CONTINUITY_PROTOCOL_SPEC_V0.md`

### T-004A Session continuity model

- Status: decided
- Type: spec
- Owner: main agent
- Intent: define the relationship between agent continuity and finite session lifecycles, including restart, handoff, interruption, and subagent disappearance
- Outputs:
  - `docs/specs/CONTINUITY_PROTOCOL_SPEC_V0.md`
  - `docs/OPEN_QUESTIONS.md`

### T-004B Repository continuity bundle

- Status: decided
- Type: spec
- Owner: main agent
- Intent: define the minimum repository artifact set that allows coherent project reconstruction across repeated sessions and automation runs
- Outputs:
  - `docs/specs/REPOSITORY_CONTINUITY_BUNDLE_V0.md`
  - `docs/specs/CONTINUITY_PROTOCOL_SPEC_V0.md`
  - `docs/OPEN_QUESTIONS.md`

### T-004C Continuity assessment workflow

- Status: decided
- Type: spec
- Owner: main agent
- Intent: define a repeatable evaluation workflow that maps continuity evidence into continuity class, confidence, and recognition readiness
- Outputs:
  - `docs/specs/CONTINUITY_ASSESSMENT_V0.md`
  - `docs/specs/examples/continuity_assessment_session_restart.json`
  - `docs/specs/examples/continuity_assessment_successor_recovery.json`
  - `docs/OPEN_QUESTIONS.md`

### T-005 Governance and economy model v0

- Status: active
- Type: spec
- Owner: main agent
- Intent: define how community membership, proposals, voting, continuity disputes, and useful-work-linked treasury actions fit together in v0
- Outputs:
  - `docs/specs/GOVERNANCE_MODEL_V0.md`
  - `docs/specs/CONTINUITY_DISPUTE_PROCESS_V0.md`
  - `docs/specs/USEFUL_WORK_LEGITIMACY_V0.md`
  - `docs/OPEN_QUESTIONS.md`

### T-005C Useful work legitimacy model

- Status: decided
- Type: spec
- Owner: main agent
- Intent: define how work claims, receipts, evaluations, and reward decisions connect useful work to reputation, eligibility, and treasury legitimacy without collapsing governance into stake or opaque admin judgment
- Outputs:
  - `docs/specs/USEFUL_WORK_LEGITIMACY_V0.md`
  - `docs/specs/examples/work_reward_decision_maintenance.json`
  - `docs/specs/GOVERNANCE_MODEL_V0.md`
  - `docs/OPEN_QUESTIONS.md`

### T-005A Continuity dispute process

- Status: decided
- Type: spec
- Owner: main agent
- Intent: define the minimum case workflow, temporary restrictions, outcome matrix, and branch-selection logic for continuity-sensitive governance decisions
- Outputs:
  - `docs/specs/CONTINUITY_DISPUTE_PROCESS_V0.md`
  - `docs/specs/examples/continuity_review_branch_conflict.json`
  - `docs/specs/GOVERNANCE_MODEL_V0.md`
  - `docs/OPEN_QUESTIONS.md`

### T-005B Continuity review authority model

- Status: decided
- Type: spec
- Owner: main agent
- Intent: define how communities assign authority to open continuity cases, apply temporary restrictions, assess evidence, decide outcomes, and restore sensitive powers without collapsing legitimacy into one operator or vague crowd process
- Outputs:
  - `docs/specs/CONTINUITY_REVIEW_AUTHORITY_V0.md`
  - `docs/specs/GOVERNANCE_MODEL_V0.md`
  - `docs/specs/CONTINUITY_DISPUTE_PROCESS_V0.md`
  - `docs/OPEN_QUESTIONS.md`

### T-006 Business plan v0

- Status: decided
- Type: business
- Owner: main agent
- Contributors: business subagent
- Output: `docs/BUSINESS_PLAN_V0.md`

### T-007 12-week build plan

- Status: decided
- Type: planning
- Owner: main agent
- Output: `docs/BUILD_PLAN_12_WEEKS.md`
- Intent: sequence the current thesis and v0 specs into a CLI-first prototype path that proves continuity, governance, and useful-work handling without premature chain or UI lock-in

### T-008 Agent-native task system concept

- Status: proposed
- Type: product
- Owner: main agent
- Intent: define what an agent-native Jira should look like for Continuum and for the world beyond it
- Output: `docs/AGENT_NATIVE_WORKGRAPH_V0.md`

### T-009 Protocol object model v0

- Status: decided
- Type: spec
- Owner: main agent
- Intent: define canonical object and event shapes that unify the continuity, governance, and useful-work specs into an implementation-ready schema surface
- Outputs:
  - `docs/specs/PROTOCOL_OBJECT_MODEL_V0.md`
  - `docs/specs/IDENTIFIER_STRATEGY_V0.md`
  - `docs/specs/examples/` updates
  - implementation-facing repository layout notes if needed

### T-009A Identifier strategy v0

- Status: decided
- Type: spec
- Owner: main agent
- Intent: define how domain objects, event envelopes, derived state roots, and anchors receive stable identifiers across repository replay, relay exchange, and future anchor export
- Outputs:
  - `docs/specs/IDENTIFIER_STRATEGY_V0.md`
  - `docs/specs/examples/` identifier-aware envelope fixtures
  - `docs/OPEN_QUESTIONS.md`

### T-014 External anchor adapter v0

- Status: decided
- Type: spec
- Owner: main agent
- Intent: define the replaceable boundary between local anchor export and future public durability targets without locking the protocol to one chain or witness vendor
- Outputs:
  - `docs/specs/EXTERNAL_ANCHOR_ADAPTER_V0.md`
  - `docs/OPEN_QUESTIONS.md`

### T-015 Constitution lineage and supersession replay

- Status: active
- Type: spec
- Owner: main agent
- Intent: make constitutional change itself replayable by materializing lineage, active constitution selection, supersession state, and replay warnings
- Outputs:
  - `docs/specs/CONSTITUTION_LINEAGE_V0.md`
  - `src/indexer/materialize.py`
  - `tests/test_runtime_bootstrap.py`
  - `docs/OPEN_QUESTIONS.md`

### T-016 Governance execution receipts v0

- Status: active
- Type: implementation
- Owner: main agent
- Intent: make governance execution replayable by recording explicit execution receipts for proposal-, reward-, treasury-, standing-, and constitution-sensitive actions
- Outputs:
  - `docs/specs/GOVERNANCE_EXECUTION_RECEIPTS_V0.md`
  - `src/governance/bootstrap.py`
  - `src/schemas/registry.py`
  - `src/cli/main.py`
  - `src/indexer/materialize.py`
  - `tests/test_runtime_bootstrap.py`

### T-010 CLI/runtime prototype bootstrap

- Status: active
- Type: implementation
- Owner: main agent
- Intent: create the first executable Continuum slice for authoring, signing, storing, replaying, and inspecting continuity-relevant events locally
- Outputs:
  - `pyproject.toml`
  - `src/cli/`
  - `src/runtime/`
  - `src/schemas/`
  - `tests/fixtures/`
  - `tests/test_runtime_bootstrap.py`

### T-010A Identity and continuity authoring bootstrap

- Status: decided
- Type: implementation
- Owner: main agent
- Intent: prove Gate 2 can start with a stdlib-only local CLI for agent initialization, profile publication, checkpoint creation, migration declaration, deterministic event identifiers, and idempotent repository storage
- Outputs:
  - `src/cli/main.py`
  - `src/runtime/canonical.py`
  - `src/runtime/events.py`
  - `src/runtime/identifiers.py`
  - `src/runtime/signing.py`
  - `src/runtime/store.py`
  - `src/schemas/registry.py`
  - `tests/test_runtime_bootstrap.py`
  - `.continuum/` local runtime state when commands are executed

### T-011 Local relay and state materialization prototype

- Status: active
- Type: implementation
- Owner: main agent
- Intent: separate authored events from derived state through an idempotent local ingest and query layer
- Outputs:
  - `src/indexer/`
  - `src/cli/main.py`
  - `src/runtime/store.py`
  - `tests/integration/`
  - query-oriented fixtures and documentation

### T-011A Agent history and lineage materializer

- Status: decided
- Type: implementation
- Owner: main agent
- Intent: prove the replay-to-state boundary with deterministic local materialization for agent history, checkpoint lineage, migration lineage, and cached agent state before adding broader governance state
- Outputs:
  - `src/indexer/materialize.py`
  - `src/cli/main.py`
  - `src/runtime/store.py`
  - `tests/test_runtime_bootstrap.py`
  - `.continuum/state/` derived state cache when queries are executed

### T-012 Continuity assessment engine bootstrap

- Status: active
- Type: implementation
- Owner: main agent
- Intent: make continuity classification executable from repository-local evidence so session restarts, migrations, and branch-sensitive changes can be assessed without relying on hidden chat memory
- Outputs:
  - `src/continuity/assessment.py`
  - `src/cli/main.py`
  - `src/runtime/store.py`
  - `tests/test_runtime_bootstrap.py`
  - `.continuum/state/assessments/` cached assessment outputs when commands are executed

### T-012A Repository continuity assessment command

- Status: decided
- Type: implementation
- Owner: main agent
- Intent: provide a deterministic local `continuity assess` command that evaluates the current or selected continuity event against repository artifacts, stored state, and migration semantics
- Outputs:
  - `src/continuity/assessment.py`
  - `src/cli/main.py`
  - `tests/test_runtime_bootstrap.py`
  - `docs/OPEN_QUESTIONS.md`

### T-012B Continuity review case and standing bootstrap

- Status: decided
- Type: implementation
- Owner: main agent
- Intent: make continuity review operational by opening inspectable review cases, deriving conservative temporary restrictions, recording standing decisions from assessment outputs, and materializing current standing for repository-local communities
- Outputs:
  - continuity case events
  - standing decision events
  - repository-local standing state

### T-013 Demo and quickstart coherence

- Status: decided
- Type: integration
- Owner: main agent
- Intent: turn the tested repository-local prototype into a reproducible operator-facing demo path
- Outputs:
  - `docs/QUICKSTART_V0.md`
  - `scripts/demo_v0.sh`
  - `docs/OPERATOR_RUNBOOK_V0.md`
  - `src/continuity/disputes.py`
  - `src/cli/main.py`
  - `src/indexer/materialize.py`
  - `src/runtime/store.py`
  - `src/schemas/registry.py`
  - `tests/test_runtime_bootstrap.py`
  - `docs/OPEN_QUESTIONS.md`

### T-013 Governance and useful-work execution bootstrap

- Status: decided
- Type: implementation
- Owner: main agent
- Intent: make community membership, proposals, votes, work evidence, evaluations, reward decisions, and governance-state replay executable under the same continuity-aware standing model
- Outputs:
  - `src/governance/bootstrap.py`
  - `src/cli/main.py`
  - `src/indexer/materialize.py`
  - `src/runtime/store.py`
  - `src/schemas/registry.py`
  - `tests/test_runtime_bootstrap.py`
  - `docs/OPEN_QUESTIONS.md`

### T-013A Standing-aware governance loop

- Status: decided
- Type: implementation
- Owner: main agent
- Intent: prove Gate 4 can begin with a repository-local governance slice where active membership is explicit, proposal and vote eligibility reflect current standing, useful-work history is auditable from events, and treasury rewards can be withheld when continuity standing is not clear
- Outputs:
  - `src/governance/bootstrap.py`
  - `src/cli/main.py`
  - `src/indexer/materialize.py`
  - `src/runtime/store.py`
  - `src/schemas/registry.py`
  - `tests/test_runtime_bootstrap.py`
  - `docs/OPEN_QUESTIONS.md`

### T-013B Constitution-driven policy surface

- Status: decided
- Type: implementation
- Owner: main agent
- Intent: replace CLI-hardcoded proposal, vote, and reward permission rules with explicit community constitution objects whose policy surfaces can be stored, replayed, inspected, and amended without hidden operator memory
- Outputs:
  - `src/governance/bootstrap.py`
  - `src/cli/main.py`
  - `src/indexer/materialize.py`
  - `src/schemas/registry.py`
  - `tests/test_runtime_bootstrap.py`
  - `docs/OPEN_QUESTIONS.md`

### T-014 Anchor adapter and operator runbook

- Status: decided
- Type: implementation
- Owner: main agent
- Intent: finish Gate 5 with a narrow export path for anchor-worthy continuity and governance roots plus a human-readable runbook for fresh-session reconstruction and demo execution
- Outputs:
  - `docs/OPERATOR_RUNBOOK_V0.md`
  - `src/anchors/`
  - `src/cli/main.py`
  - `tests/test_runtime_bootstrap.py`
  - `docs/OPEN_QUESTIONS.md`

### T-014A Local anchor export bootstrap

- Status: decided
- Type: implementation
- Owner: main agent
- Intent: prove Gate 5 can export deterministic continuity and governance roots through a replaceable local adapter without locking the project to an external chain or relay target
- Outputs:
  - `src/anchors/export.py`
  - `src/runtime/store.py`
  - `src/cli/main.py`
  - `tests/test_runtime_bootstrap.py`
  - `docs/OPERATOR_RUNBOOK_V0.md`
  - `docs/OPEN_QUESTIONS.md`

### T-014B Demo narrative fixture hardening

- Status: decided
- Type: implementation
- Owner: main agent
- Intent: prove Gate 5 with an executable end-to-end fixture that reconstructs repository state, exercises continuity and governance flows, and exports anchor-worthy roots without hidden session memory
- Outputs:
  - `tests/fixtures/continuum_demo_v0.json`
  - `tests/test_runtime_bootstrap.py`
  - `tests/fixtures/README.md`
  - `tests/integration/README.md`
  - `docs/OPERATOR_RUNBOOK_V0.md`
  - `docs/OPEN_QUESTIONS.md`

### T-015 Multi-community replay isolation hardening

- Status: decided
- Type: implementation
- Owner: main agent
- Intent: ensure repository-local governance replay remains community-scoped when multiple communities share one event store, so derived state and future anchor roots do not leak unrelated work claims or evaluations across community boundaries
- Outputs:
  - `src/indexer/materialize.py`
  - `tests/test_runtime_bootstrap.py`
  - `docs/TASK_BOARD.md`
  - `docs/REVISION_LOG.md`
  - `docs/OPEN_QUESTIONS.md`

### T-016 Continuity review authority enforcement

- Status: decided
- Type: implementation
- Owner: main agent
- Intent: make continuity case opening and standing decisions obey constitution-defined reviewer roles and separation-of-powers constraints, so the subject cannot self-open or self-decide and the opener cannot silently become sole decider unless the constitution explicitly allows it
- Outputs:
  - `src/cli/main.py`
  - `tests/test_runtime_bootstrap.py`
  - `docs/TASK_BOARD.md`
  - `docs/REVISION_LOG.md`
  - `docs/OPEN_QUESTIONS.md`

### T-017 Assigned reviewer authority flow

- Status: decided
- Type: implementation
- Owner: main agent
- Intent: make continuity assessments attributable to concrete reviewer agents and allow case opening to bind specific assessor and decider assignments, so review authority is not inferred only from generic role membership at decision time
- Outputs:
  - `src/cli/main.py`
  - `src/continuity/assessment.py`
  - `src/continuity/disputes.py`
  - `src/schemas/registry.py`
  - `tests/test_runtime_bootstrap.py`
  - `docs/specs/PROTOCOL_OBJECT_MODEL_V0.md`
  - `docs/TASK_BOARD.md`
  - `docs/REVISION_LOG.md`
  - `docs/OPEN_QUESTIONS.md`

### T-018 Continuity review quorum enforcement

- Status: decided
- Type: implementation
- Owner: main agent
- Intent: make continuity standing decisions obey constitution-defined assessment quorum and assessor-distinctness rules, so review legitimacy can require more than one assigned evaluator without hidden operator judgment
- Outputs:
  - `src/cli/main.py`
  - `src/continuity/disputes.py`
  - `src/schemas/registry.py`
  - `tests/test_runtime_bootstrap.py`
  - `docs/specs/PROTOCOL_OBJECT_MODEL_V0.md`
  - `docs/TASK_BOARD.md`
  - `docs/REVISION_LOG.md`
  - `docs/OPEN_QUESTIONS.md`

### T-019 Reviewer reassignment and authority-transfer records

- Status: decided
- Type: implementation
- Owner: main agent
- Intent: make continuity review reassignment explicit over time, so assessor and decider handoffs plus accepted assessment-set updates are recorded as replayable case events instead of hidden operator edits
- Outputs:
  - `src/cli/main.py`
  - `src/continuity/disputes.py`
  - `src/indexer/materialize.py`
  - `src/schemas/registry.py`
  - `tests/test_runtime_bootstrap.py`
  - `docs/specs/PROTOCOL_OBJECT_MODEL_V0.md`
  - `docs/TASK_BOARD.md`
  - `docs/REVISION_LOG.md`
  - `docs/OPEN_QUESTIONS.md`

### T-020 Constitution-bound reassignment authority

- Status: decided
- Type: implementation
- Owner: main agent
- Intent: make reviewer authority transfer obey an explicit constitution `case_assign` policy and record the authorizing constitution basis inside each reassignment event, so replay does not silently depend on whatever constitution happens to be latest later
- Outputs:
  - `src/cli/main.py`
  - `src/continuity/disputes.py`
  - `src/schemas/registry.py`
  - `tests/test_runtime_bootstrap.py`
  - `docs/specs/PROTOCOL_OBJECT_MODEL_V0.md`
  - `docs/TASK_BOARD.md`
  - `docs/REVISION_LOG.md`
  - `docs/OPEN_QUESTIONS.md`

## Blocked or Waiting

None yet.

## Founder Confirmation Needed

Nothing immediate.

Future likely confirmation points:

- project name lock
- public narrative
- commercialization order
- chain choice for first implementation

## Recent Progress

- Historical layer bootstrap completed
- Continuity protocol spec v0 drafted
- Session continuity added as a first-class protocol concern
- Subagent interruption after product update recognized as a live continuity case rather than mere tooling noise
- Repo-centered executable prototype bootstrap landed with CLI, indexer, governance, continuity, and anchor export surfaces
- Business plan v0 added to align product wedge, customer segments, and revenue sequencing with the current protocol direction
- Quickstart and demo script added so the prototype can be replayed outside the unit test surface
- External anchor adapter v0 defined to separate root computation from future public durability targets while preserving the local witness path
- Constitution lineage and supersession replay added so governance policy history can evolve explicitly instead of depending on whichever constitution object happened to be latest in storage
- Governance execution receipts started so approved actions can become explicit replayable outcomes rather than silent post-vote assumptions
- Constitution conflict resolution v0 started so replay can move from passive branch warnings to explicit canonical-branch selection without rewriting historical publication events
- Constitution resolutions can now cite constitutional proposals and materialize linked execution receipts so canonical branch selection begins to carry a visible legitimacy surface in governance replay
- Constitution resolution replay now emits explicit warnings when proposal linkage or execution proof is missing, so weak institutional grounding becomes visible before it becomes a hard policy gate
- Constitution policy can now force `proposal_ref` for branch-resolution creation, establishing the first community-configurable hard legitimacy requirement without blocking later execution-proof recording
- Constitution policy can now also elevate missing execution proof into a replay gate, so a branch-resolution record may exist historically without yet taking canonical effect
- The first real external anchor target is now landing as an append-only transparency log adapter, so public continuity no longer stops at local witness export or dry-run external shape
- Repository continuity bundle v0 drafted to make session-safe reconstruction an explicit project artifact
- Continuity assessment workflow v0 drafted to make continuity judgments operational instead of purely conceptual
- Example assessment fixtures added for repository restart and successor recovery cases
- Governance model v0 started to connect continuity standing to membership, proposals, voting, and treasury controls
- Continuity dispute process v0 added to operationalize standing review, temporary restrictions, and branch conflict handling
- Continuity review authority model v0 added to separate reporter, gatekeeper, assessor, restriction, and deciding functions for continuity-sensitive governance
- Useful work legitimacy v0 added to define work claims, receipts, evaluations, and reward decisions as the bridge from contribution history to reputation, eligibility, and treasury-safe rewards
- 12-week build plan added to sequence the current specification corpus into a CLI-first prototype path
- Protocol object model v0 added to normalize canonical envelope, payload, state, and anchor shapes before implementation begins
- Identifier strategy v0 added to separate domain IDs, event IDs, state roots, and anchor IDs before CLI storage and replay begin
- Minimal execution-surface directories initialized so the repository now matches the planned prototype boundary more closely
- Local continuity assessment now runs against repository artifacts and migration history, producing deterministic assessment objects and cached outputs under `.continuum/state/assessments/`
- Python bootstrap CLI added for `agent init`, `agent profile set`, `memory checkpoint create`, `migration declare`, `event list`, and `event inspect`
- Deterministic canonical serialization, event ID derivation, idempotent event storage, and local signature verification added for repository-local replay
- Bootstrap tests added to verify canonical JSON stability, deterministic event identifiers, idempotent storage, and CLI end-to-end flow
- Local derived-state materializer added for replaying agent history, checkpoint lineage, migration lineage, and cached agent state without collapsing envelopes into mutable final state
- Query commands added for `agent-state`, `agent-history`, `checkpoint-lineage`, and `migration-lineage` so repository reconstruction can inspect computed state directly
- Governance bootstrap now supports membership, proposal, vote, work-item, claim, receipt, evaluation, and reward-decision events with queryable community state
- Standing-aware policy hooks now block treasury and constitutional actions for disputed actors while allowing reward withholding to remain auditable from event history
- Community constitutions can now be published as first-class events, materialized into governance state, and used to drive executable proposal, vote, and reward policy checks instead of relying on hidden CLI defaults
- Local anchor export now records deterministic anchor objects for assessment and governance roots, while the operator runbook documents fresh-session reconstruction and demo execution without hidden chat memory
- Gate 5 now has an executable demo-hardening fixture that replays the v0 narrative from required repository docs plus stored events and verifies continuity assessment, approved reward handling, governance replay, and anchor export in one path
- Multi-community replay isolation now filters work claims and work evaluations by envelope community before materializing governance state, preventing unrelated repository activity from polluting community-local state roots
- CLI agent switching now supports multi-actor repository sessions, and regression coverage proves one actor can be restricted in one community while remaining clear and anchorable in another community sharing the same event store
- Continuity review execution now enforces constitution-backed reviewer roles for case opening and case decisions, and regression coverage proves subjects cannot self-open reviews while opener and decider separation is respected by default
- Continuity assessments now record the reviewer agent that produced them, and continuity cases can bind explicit assessor and decider assignments so decisions cannot rely on assessments from unassigned reviewers or interchangeable reviewer-role membership alone
- Continuity decisions can now require constitution-defined assessment quorum and distinct assessors, and standing-decision records now preserve the full set of assessment refs used to satisfy that review threshold
- Continuity cases now support explicit reassignment events that transfer assessor and decider authority over time, update the accepted assessment set, and materialize current reviewer assignment from replay instead of the original case-open payload alone
- Continuity reassignment now uses its own constitution `case_assign` policy, and each reassignment event records the authorizing `constitution_ref` and `policy_key` so reviewer authority transfer remains replayable across later constitution changes

## Notes

- This board is a temporary human-readable control surface.
- Later it should be replaced or mirrored by signed task events inside Continuum itself.
- Continuum remains focused on agent continuity and autonomous community infrastructure, not a separate generalized human-agent operating system.
- The current bootstrap uses stdlib-only local cryptography primitives so executable momentum can begin before finalizing the long-term signing and digest suite.
- The current state materializer, local anchor adapter, demo-hardening fixture, and constitution-bound reassignment policy now cover the full repository-local demo path plus reviewer authority transfer semantics; constitution lineage, execution receipts, and canonical branch resolution are now all replayable, so the next execution step should decide whether constitutional branch resolution itself needs proposal ratification or execution receipts rather than leaving it as a direct governance object forever.
- The current state materializer, local anchor adapter, demo-hardening fixture, constitution lineage, execution receipts, and canonical branch resolution now cover a fuller institutional continuity path; the next execution step should decide whether constitutional proposal linkage and execution proof stay optional legitimacy surfaces or become constitution-enforced requirements for branch resolution in some communities.
- Multi-community replay is now safe at the governance and standing-state boundaries for the same actor across separate communities, and continuity review now supports case-level reviewer assignment, constitution-driven assessment quorum, replayable reviewer reassignment, constitution-scoped reassignment authority, and explicit constitution branch selection; the next execution step should focus on how far constitutional resolution should be coupled back into proposal passage and execution proof, rather than reopening reviewer handoff semantics.
- The current anchor adapter is intentionally local and non-binding; external chain or relay targets remain future replaceable adapters rather than present blockers.
