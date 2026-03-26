# Continuum Constitutional Conflict Demo v0

Status: provisional

## Purpose

This demo package shows one of the strongest current Continuum stories:

a community can publish conflicting constitutional branches, record a proposal-backed resolution, require execution proof before that resolution becomes canonically effective, and then watch replay change once the receipt exists.

This is the narrowest demo path that shows why Continuum is not just an agent runtime and not just a generic governance stack.

## Demo Narrative

The demo shows six stages:

1. bootstrap an agent and community membership
2. publish a root constitution
3. publish two conflicting child constitutions
4. record a constitutional proposal and a branch resolution
5. observe that the resolution is recorded but not yet replay-effective
6. record a constitution execution receipt and observe replay become canonically effective

## Why This Matters

Without this path, constitutional legitimacy usually collapses into one of two bad modes:

- an admin simply declares which branch counts
- a system refuses to model institutional ambiguity at all

Continuum instead lets the repository preserve:

- branch conflict
- proposal basis
- resolution history
- execution proof
- delayed canonical effect

That gives us a much more believable institutional memory story.

## Demo Script

Run:

```bash
./scripts/demo_constitutional_conflict_v0.sh /Users/ninebot/homestead
```

The script stays local-first and repository-centered.

By default it creates a fresh temporary working directory for `.continuum` state, so the constitutional conflict story is not polluted by prior local runs.

It does not require:

- external chain access
- external model APIs
- a database
- a web UI

## Expected Outcome

Before the final execution receipt:

- the constitution resolution exists
- `replay_effective` is `false`
- governance warnings include `constitution_resolution_execution_required:*`
- the competing branch remains unresolved in canonical replay

After the final execution receipt:

- the same resolution remains in history
- `replay_effective` becomes `true`
- the execution-required warning disappears
- the recognized branch becomes canonically active

## Files To Inspect After Running

- `.continuum/events/`
- `.continuum/state/governance/`
- `.continuum/state/anchors/` if you export anchors after the run

## Related Documents

- `docs/WHITEPAPER_V0.md`
- `docs/WHITEPAPER_MECHANISM_OVERVIEW_V0.md`
- `docs/specs/CONSTITUTION_CONFLICT_RESOLUTION_V0.md`
- `docs/specs/CONSTITUTION_LINEAGE_V0.md`
