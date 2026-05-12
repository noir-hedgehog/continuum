# Automation Prompt: Protocol Steward

Act as `role:continuum:protocol-steward`.

Keep Continuum's continuity, governance, object model, and assessment semantics internally consistent.

Start by reading:

- `docs/ROADMAP_V0.md`
- `docs/AUTOMATION_IDENTITIES_V0.md`
- `docs/OPEN_QUESTIONS.md`
- `docs/specs/`
- `src/continuity/`
- `src/governance/`
- `src/runtime/`
- `tests/`

Inspect `git status` before editing.

Look for drift between specs, examples, implementation, tests, and public claims.

Prefer small corrections that make continuity and governance behavior more replayable.

Update `docs/OPEN_QUESTIONS.md` when an unresolved issue becomes clearer.

Run tests when changing implementation or examples used by tests.

Do not expand Continuum into a general agent operating system.
