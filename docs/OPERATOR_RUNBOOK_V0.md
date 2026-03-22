# Continuum Operator Runbook v0

## Purpose

This runbook defines the minimum fresh-session reconstruction and demo path for the repository-centered Continuum prototype.

It exists so a new session can recover project state without hidden chat memory and still produce continuity-relevant artifacts.

## Reconstruction Inputs

Required repository surfaces:

- `docs/FOUNDING_THESIS.md`
- `docs/OPERATING_MODEL.md`
- `docs/TASK_BOARD.md`
- `docs/OPEN_QUESTIONS.md`
- `docs/REVISION_LOG.md`

Executable fixture surfaces:

- `tests/fixtures/continuum_demo_v0.json`
- `tests/test_runtime_bootstrap.py`

Required execution surfaces:

- `.continuum/agents/`
- `.continuum/events/`
- `.continuum/state/assessments/`
- `.continuum/state/standing/`
- `.continuum/state/governance/`
- `.continuum/state/anchors/`

## Fresh-Session Reconstruction

1. Read the thesis, operating model, task board, open questions, and revision log in that order.
2. Inspect uncommitted repository changes before editing.
3. Reconstruct the current execution boundary from `pyproject.toml`, `src/`, and `tests/test_runtime_bootstrap.py`.
4. Prefer continuing the highest-leverage active task already on the board instead of creating parallel tracks.
5. Treat cached state as accelerators, not as canonical truth; rebuild with `--refresh` when correctness matters.

## Minimum Demo Narrative

The v0 demo should remain narrow:

1. initialize or restore an agent identity
2. publish profile and continuity evidence
3. materialize continuity and governance state
4. evaluate continuity or standing-sensitive governance outcomes
5. export an anchor-worthy root through the local adapter

## CLI Sequence

### 1. Initialize the active agent

```bash
python -m src.cli.main agent init \
  --scope continuum \
  --name main \
  --display-name "Continuum Main"
```

### 2. Publish profile and continuity evidence

```bash
python -m src.cli.main agent profile set \
  --display-name "Continuum Main" \
  --description "Repository-local continuity operator"

python -m src.cli.main memory checkpoint create \
  --scope session_handoff \
  --summary "Fresh session reconstruction complete" \
  --artifact-ref docs/TASK_BOARD.md
```

### 3. Rebuild derived state

```bash
python -m src.cli.main query agent-state --refresh
python -m src.cli.main query governance-state --community-id community:continuum:lab --refresh
python -m src.cli.main query standing-state --community-id community:continuum:lab --refresh
```

### 4. Assess continuity when a restart or migration matters

```bash
python -m src.cli.main continuity assess --refresh
```

### 5. Export an anchor-worthy root

Governance root:

```bash
python -m src.cli.main anchor export \
  --anchor-type governance_state_root \
  --community-id community:continuum:lab \
  --refresh
```

Assessment root:

```bash
python -m src.cli.main anchor export \
  --anchor-type continuity_assessment_root \
  --assessment-id <assessment_id>
```

## Anchor Export Rules

- Export only continuity-sensitive or governance-sensitive roots in v0.
- Treat `anchor_id` as transport metadata for the export record, not as the governed root itself.
- Treat `root_hash` as the durable subject of later external anchoring.
- Keep the adapter replaceable; the current reference target is `adapter:local_witness_v0`.

## Current Anchor-Worthy Roots

- `continuity_assessment_root`
- `standing_state_root`
- `governance_state_root`
- `agent_state_root` for repository-local recovery support, not as the primary public anchor

## Failure Handling

- If repository docs and event history disagree, repair the docs and revision log before exporting a new anchor.
- If cached state is missing or stale, rerun the relevant query or assessment command with `--refresh`.
- If a continuity dispute or restricted standing exists, do not treat treasury-sensitive outputs as clean demo success.
- If the runbook and executable demo fixture diverge, treat that mismatch as a continuity failure and repair it before extending scope.

## Operator Stance

- Keep Continuum scoped to agent continuity and autonomous community operation.
- Do not expand this runbook into a generalized human-agent operating system manual.
- Escalate only for legal, financial, public-positioning, irreversible naming, or permission-bound decisions.
