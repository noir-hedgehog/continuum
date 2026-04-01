---
layout: default
title: Continuum Playground
---

<div class="language-switch" markdown="1">
  <a class="language-pill active" href="/continuum/playground/">Playground</a>
  <a class="language-pill" href="/continuum/">Home</a>
  <a class="language-pill" href="/continuum/zh-cn/">简体中文</a>
</div>

<section class="hero" markdown="1">
# Continuum Playground

<p class="hero-tagline">A visual walkthrough of constitutional conflict, legitimacy, and replay effectiveness.</p>

This playground turns the current strongest Continuum demo path into an inspectable state machine. It is static and local to GitHub Pages, but it mirrors the protocol logic already implemented in the repository prototype.
</section>

<div class="playground-layout">
  <section class="section-card playground-sidebar">
    <h2>Scenario</h2>
    <p>One community publishes two competing constitutional branches. A proposal-backed resolution chooses one branch, but replay still refuses to treat it as canon until execution proof exists.</p>

    <div class="playground-steps" id="playground-steps">
      <button class="playground-step active" data-step="0">1. Root constitution</button>
      <button class="playground-step" data-step="1">2. Competing branches</button>
      <button class="playground-step" data-step="2">3. Proposal-backed resolution</button>
      <button class="playground-step" data-step="3">4. Recorded, not effective</button>
      <button class="playground-step" data-step="4">5. Execution proof</button>
      <button class="playground-step" data-step="5">6. Canonical replay</button>
    </div>
  </section>

  <section class="section-card playground-main">
    <div class="playground-stage">
      <div>
        <p class="playground-label">Current Stage</p>
        <h2 id="stage-title">Root constitution</h2>
        <p id="stage-summary">The community starts from a single recognized constitution. There is no institutional ambiguity yet.</p>
      </div>
      <div class="playground-badges" id="stage-badges"></div>
    </div>

    <div class="playground-grid">
      <div class="playground-panel">
        <h3>Institutional State</h3>
        <ul id="state-list"></ul>
      </div>
      <div class="playground-panel">
        <h3>Why It Matters</h3>
        <p id="stage-meaning"></p>
      </div>
    </div>

    <div class="playground-grid">
      <div class="playground-panel">
        <h3>Warnings</h3>
        <ul id="warning-list"></ul>
      </div>
      <div class="playground-panel">
        <h3>Replay Snapshot</h3>
        <pre id="state-json" class="playground-json"></pre>
      </div>
    </div>
  </section>
</div>

<section class="section-card" markdown="1">
## Related Docs

- [Constitutional Conflict Demo](../DEMO_CONSTITUTIONAL_CONFLICT_V0.md)
- [Constitution Conflict Resolution Spec](../specs/CONSTITUTION_CONFLICT_RESOLUTION_V0.md)
- [Constitution Lineage Spec](../specs/CONSTITUTION_LINEAGE_V0.md)
- [Governance Execution Receipts](../specs/GOVERNANCE_EXECUTION_RECEIPTS_V0.md)
</section>

<script>
const PLAYGROUND_STAGES = [
  {
    title: "Root constitution",
    summary: "The community starts from a single recognized constitution. There is no institutional ambiguity yet.",
    badges: ["stable", "single lineage"],
    stateList: [
      "recognized_constitution: constitution:v1",
      "lineage_status: clear",
      "branch_conflict: none",
      "replay_effective: true"
    ],
    meaning:
      "This is the baseline most systems assume forever. Continuum treats it as only the starting point, not the whole story.",
    warnings: [],
    snapshot: {
      root_constitution: "constitution:v1",
      active_constitution: "constitution:v1",
      constitution_lineage: "single_branch",
      replay_effective: true
    }
  },
  {
    title: "Competing branches",
    summary: "Two child constitutions supersede the same parent, creating a branch conflict that replay can see.",
    badges: ["conflict", "history preserved"],
    stateList: [
      "recognized_constitution: constitution:v1",
      "branch_a: constitution:v2-a",
      "branch_b: constitution:v2-b",
      "branch_conflict: detected"
    ],
    meaning:
      "Instead of pretending conflict never happened, Continuum keeps constitutional ambiguity visible inside institutional history.",
    warnings: ["constitution_branch_conflict:constitution:v1"],
    snapshot: {
      root_constitution: "constitution:v1",
      competing_children: ["constitution:v2-a", "constitution:v2-b"],
      active_constitution: "constitution:v1",
      replay_effective: true
    }
  },
  {
    title: "Proposal-backed resolution",
    summary: "A constitutional proposal and a branch resolution choose branch B as the recognized path forward.",
    badges: ["proposal-linked", "legible legitimacy"],
    stateList: [
      "proposal_id: proposal:constitutional:001",
      "resolution_id: resolution:constitution:001",
      "recognized_branch: constitution:v2-b",
      "rejected_branch: constitution:v2-a"
    ],
    meaning:
      "Continuum does not reduce branch selection to admin fiat. The decision becomes a replayable governance object with explicit basis.",
    warnings: ["constitution_resolution_execution_required:resolution:constitution:001"],
    snapshot: {
      proposal_ref: "proposal:constitutional:001",
      resolution_ref: "resolution:constitution:001",
      recognized_constitution: "constitution:v2-b",
      replay_effective: false
    }
  },
  {
    title: "Recorded, not effective",
    summary: "The branch resolution exists in history, but the chosen constitution is still not canonically active because execution proof is missing.",
    badges: ["delayed canonical effect", "execution pending"],
    stateList: [
      "resolution_recorded: true",
      "replay_effective: false",
      "active_constitution: constitution:v1",
      "execution_receipt: missing"
    ],
    meaning:
      "This is a key Continuum idea: history can record an outcome before institutions are willing to treat that outcome as effective canon.",
    warnings: ["constitution_resolution_execution_required:resolution:constitution:001"],
    snapshot: {
      resolution_recorded: true,
      active_constitution: "constitution:v1",
      pending_constitution: "constitution:v2-b",
      replay_effective: false
    }
  },
  {
    title: "Execution proof",
    summary: "A constitution_execution receipt is recorded for the resolution and its governing proposal.",
    badges: ["receipt recorded", "proof attached"],
    stateList: [
      "execution_receipt: receipt:constitution:001",
      "governed_ref: resolution:constitution:001",
      "governed_ref: proposal:constitutional:001",
      "proof_status: satisfied"
    ],
    meaning:
      "Legitimacy is no longer only claimed. It is attached to a replayable execution event that future sessions can inspect.",
    warnings: [],
    snapshot: {
      execution_receipt: "receipt:constitution:001",
      governed_refs: ["resolution:constitution:001", "proposal:constitutional:001"],
      replay_effective: true
    }
  },
  {
    title: "Canonical replay",
    summary: "Replay now upgrades branch B into the active constitution, while preserving the conflict, proposal, resolution, and execution history.",
    badges: ["canonical", "historical continuity"],
    stateList: [
      "active_constitution: constitution:v2-b",
      "replay_effective: true",
      "historical_conflict: preserved",
      "warnings: cleared"
    ],
    meaning:
      "This is the value proposition in miniature: institutions can change, but they change through visible, replayable history rather than silent replacement.",
    warnings: [],
    snapshot: {
      active_constitution: "constitution:v2-b",
      prior_conflict: ["constitution:v2-a", "constitution:v2-b"],
      proposal_ref: "proposal:constitutional:001",
      execution_receipt: "receipt:constitution:001",
      replay_effective: true
    }
  }
];

const stepButtons = Array.from(document.querySelectorAll(".playground-step"));
const titleEl = document.getElementById("stage-title");
const summaryEl = document.getElementById("stage-summary");
const badgesEl = document.getElementById("stage-badges");
const stateListEl = document.getElementById("state-list");
const warningListEl = document.getElementById("warning-list");
const meaningEl = document.getElementById("stage-meaning");
const stateJsonEl = document.getElementById("state-json");

function renderStage(index) {
  const stage = PLAYGROUND_STAGES[index];
  titleEl.textContent = stage.title;
  summaryEl.textContent = stage.summary;
  meaningEl.textContent = stage.meaning;
  badgesEl.innerHTML = stage.badges.map((badge) => `<span class="playground-badge">${badge}</span>`).join("");
  stateListEl.innerHTML = stage.stateList.map((item) => `<li>${item}</li>`).join("");
  warningListEl.innerHTML = stage.warnings.length
    ? stage.warnings.map((item) => `<li>${item}</li>`).join("")
    : "<li>No active warnings.</li>";
  stateJsonEl.textContent = JSON.stringify(stage.snapshot, null, 2);

  stepButtons.forEach((button, buttonIndex) => {
    button.classList.toggle("active", buttonIndex === index);
  });
}

stepButtons.forEach((button, index) => {
  button.addEventListener("click", () => renderStage(index));
});

renderStage(0);
</script>
