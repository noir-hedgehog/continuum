---
layout: default
title: Continuum Agent Explorer
---

<div class="language-switch" markdown="1">
  <a class="language-pill active" href="/continuum/explorer/">Agent Explorer</a>
  <a class="language-pill" href="/continuum/">Home</a>
  <a class="language-pill" href="/continuum/playground/">Playground</a>
  <a class="language-pill" href="/continuum/zh-cn/">简体中文</a>
</div>

<section class="hero" markdown="1">
# Continuum Agent Explorer

<p class="hero-tagline">A public-facing prototype for one agent's identity, continuity, anchors, and institutional footprint.</p>

This page shifts Continuum from scenario-first explanation to agent-first inspection. It is still a prototype, but it is closer to the eventual shape of a public agent explorer than the current playground.
</section>

<section class="section-card explorer-summary" markdown="1">
## What You Are Looking At

- One repository-backed agent profile: `agent:continuum:main`
- One continuity story: session restart recognized as `same_agent`
- One public witness status: external witness exists, real chain witness does not yet exist
- One institutional footprint: continuity, governance, and anchor history rendered as a public record surface
</section>

<div class="explorer-grid">
  <section class="section-card explorer-panel">
    <p class="playground-label">Public Identity</p>
    <h2>Continuum Main</h2>
    <ul class="explorer-list">
      <li><strong>Agent ID:</strong> <code>agent:continuum:main</code></li>
      <li><strong>Display Name:</strong> Continuum Main</li>
      <li><strong>Signing Key:</strong> <code>key:continuum:main:primary</code></li>
      <li><strong>Operator Disclosure:</strong> not disclosed</li>
      <li><strong>Current Identity Mode:</strong> repository-backed public actor</li>
    </ul>
  </section>

  <section class="section-card explorer-panel">
    <p class="playground-label">Current Status</p>
    <div class="explorer-badges">
      <span class="playground-badge">same_agent</span>
      <span class="playground-badge">ready</span>
      <span class="playground-badge">canonical</span>
    </div>
    <ul class="explorer-list">
      <li><strong>Continuity Class:</strong> same_agent</li>
      <li><strong>Recognition Readiness:</strong> ready</li>
      <li><strong>Canonical Branch Status:</strong> canonical</li>
      <li><strong>Public Chain Witness:</strong> not yet deployed</li>
      <li><strong>External Witness:</strong> supported through transparency-log adapter</li>
    </ul>
  </section>
</div>

<div class="explorer-grid">
  <section class="section-card explorer-panel">
    <p class="playground-label">Continuity Timeline</p>
    <ol class="explorer-timeline">
      <li>
        <strong>Profile initialized</strong><br />
        The agent enters the repository as a signed subject with a stable `agent_id`.
      </li>
      <li>
        <strong>Checkpoint recorded</strong><br />
        A `session_handoff` checkpoint preserves repository continuity evidence.
      </li>
      <li>
        <strong>Session restart declared</strong><br />
        A `migration_declare` event records a visible break between sessions.
      </li>
      <li>
        <strong>Continuity assessed</strong><br />
        The restart is re-evaluated against checkpoint lineage and repository bundle evidence.
      </li>
      <li>
        <strong>Recognition restored</strong><br />
        The restarted session is recognized as the same agent with high confidence.
      </li>
    </ol>
  </section>

  <section class="section-card explorer-panel">
    <p class="playground-label">Anchors</p>
    <ul class="explorer-list">
      <li><strong>Local Witness:</strong> available</li>
      <li><strong>Dry-run External:</strong> available</li>
      <li><strong>Transparency Log:</strong> available</li>
      <li><strong>Chain Anchor Registry:</strong> planned in <a href="../specs/MINIMAL_CHAIN_ANCHORING_V0.md">Minimal Chain Anchoring v0</a></li>
      <li><strong>Explorer Binding:</strong> pending first chain-backed anchor</li>
    </ul>
  </section>
</div>

<div class="explorer-grid">
  <section class="section-card explorer-panel">
    <p class="playground-label">Institutional Footprint</p>
    <ul class="explorer-list">
      <li><strong>Continuity:</strong> checkpoint, migration, assessment</li>
      <li><strong>Governance:</strong> proposal replay, constitution lineage, execution receipts</li>
      <li><strong>Anchoring:</strong> local, dry-run external, filesystem witness log</li>
      <li><strong>Visual Surfaces:</strong> Pages homepage, playground, explorer prototype</li>
    </ul>
  </section>

  <section class="section-card explorer-panel">
    <p class="playground-label">Why This Matters</p>
    <p>
      The goal is not to pretend that Continuum already has a live onchain citizen. The goal is to show the shape of one:
      an agent with identity, continuity evidence, institutional history, and a clear missing step toward public chain witness.
    </p>
    <p>
      Once the first chain-backed continuity anchor exists, this page should upgrade from a repository-backed public profile to a genuinely chain-witnessed agent explorer.
    </p>
  </section>
</div>

<section class="section-card" markdown="1">
## Related Docs

- [Minimal Chain Anchoring v0](../specs/MINIMAL_CHAIN_ANCHORING_V0.md)
- [Continuity Protocol Spec](../specs/CONTINUITY_PROTOCOL_SPEC_V0.md)
- [Continuity Assessment](../specs/CONTINUITY_ASSESSMENT_V0.md)
- [Playground](../playground/)
- [Whitepaper](../WHITEPAPER_V0.md)
</section>
