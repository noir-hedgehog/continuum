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

<p class="hero-tagline">A visual walkthrough of continuity, governance, legitimacy, and replay.</p>

This playground turns current Continuum demo paths into inspectable state machines. It is static and local to GitHub Pages, but it mirrors the protocol logic already implemented in the repository prototype.
</section>

<div class="playground-layout">
  <section class="section-card playground-sidebar">
    <h2>Scenario</h2>
    <div class="playground-scenario-switch" id="scenario-switch"></div>
    <div class="playground-scenario-meta" id="scenario-meta"></div>
    <p id="scenario-summary">Loading scenario...</p>

    <div class="playground-steps" id="playground-steps"></div>
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

<ul id="related-docs-list">
  <li>Loading related documents...</li>
</ul>
</section>

<script>
const SCENARIOS = [
  {
    id: "constitutional_conflict_v0",
    label: "Constitutional conflict",
    lens: "Institutional legitimacy",
    bestFor: "Why constitutions need replayable conflict resolution",
    path: "/continuum/playground/scenarios/constitutional-conflict-v0.json"
  },
  {
    id: "session_restart_v0",
    label: "Session restart continuity",
    lens: "Same-agent continuity",
    bestFor: "Why session death does not have to break public identity",
    path: "/continuum/playground/scenarios/session-restart-v0.json"
  },
  {
    id: "successor_recovery_v0",
    label: "Successor recovery",
    lens: "Broken-lineage recovery",
    bestFor: "Why recovery is not the same as perfect sameness",
    path: "/continuum/playground/scenarios/successor-recovery-v0.json"
  }
];

let PLAYGROUND_STAGES = [];
let stepButtons = [];
let scenarioButtons = [];
let activeScenarioIndex = 0;
const scenarioSwitchEl = document.getElementById("scenario-switch");
const scenarioMetaEl = document.getElementById("scenario-meta");
const scenarioSummaryEl = document.getElementById("scenario-summary");
const stepContainerEl = document.getElementById("playground-steps");
const titleEl = document.getElementById("stage-title");
const summaryEl = document.getElementById("stage-summary");
const badgesEl = document.getElementById("stage-badges");
const stateListEl = document.getElementById("state-list");
const warningListEl = document.getElementById("warning-list");
const meaningEl = document.getElementById("stage-meaning");
const stateJsonEl = document.getElementById("state-json");
const relatedDocsEl = document.getElementById("related-docs-list");

function renderScenarioButtons() {
  scenarioSwitchEl.innerHTML = SCENARIOS
    .map(
      (scenario, index) =>
        `<button class="playground-scenario-pill${index === activeScenarioIndex ? " active" : ""}" data-scenario="${index}">${scenario.label}</button>`
    )
    .join("");

  scenarioButtons = Array.from(document.querySelectorAll(".playground-scenario-pill"));
  scenarioButtons.forEach((button, index) => {
    button.addEventListener("click", () => loadScenario(index));
  });

  const activeScenario = SCENARIOS[activeScenarioIndex];
  scenarioMetaEl.innerHTML = `
    <div class="playground-scenario-card">
      <p class="playground-label">Lens</p>
      <p class="playground-scenario-value">${activeScenario.lens}</p>
      <p class="playground-label">Best for</p>
      <p class="playground-scenario-caption">${activeScenario.bestFor}</p>
    </div>
  `;
}

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

function installScenario(scenario) {
  PLAYGROUND_STAGES = scenario.stages.map((stage) => ({
    title: stage.title,
    summary: stage.summary,
    badges: stage.badges,
    stateList: stage.state_list,
    meaning: stage.meaning,
    warnings: stage.warnings,
    snapshot: stage.snapshot
  }));

  scenarioSummaryEl.textContent = scenario.summary;
  relatedDocsEl.innerHTML = (scenario.related_docs || [])
    .map((docPath) => {
      const parts = docPath.split("/");
      const label = parts[parts.length - 1]
        .replace(".md", "")
        .replace(/[-_]/g, " ");
      return `<li><a href="${docPath}">${label}</a></li>`;
    })
    .join("");
  stepContainerEl.innerHTML = scenario.stages
    .map(
      (stage, index) =>
        `<button class="playground-step${index === 0 ? " active" : ""}" data-step="${index}">${stage.button_label}</button>`
    )
    .join("");

  stepButtons = Array.from(document.querySelectorAll(".playground-step"));
  stepButtons.forEach((button, index) => {
    button.addEventListener("click", () => renderStage(index));
  });

  renderStage(0);
}

function loadScenario(index) {
  const scenarioMeta = SCENARIOS[index];
  activeScenarioIndex = index;
  renderScenarioButtons();
  scenarioSummaryEl.textContent = "Loading scenario...";
  relatedDocsEl.innerHTML = "<li>Loading related documents...</li>";
  stepContainerEl.innerHTML = "";
  titleEl.textContent = scenarioMeta.label;
  summaryEl.textContent = "Loading stage data...";
  meaningEl.textContent = "Fetching repository-backed scenario fixture.";
  warningListEl.innerHTML = "<li>loading</li>";
  stateListEl.innerHTML = "<li>scenario fixture requested</li>";
  stateJsonEl.textContent = JSON.stringify({ path: scenarioMeta.path }, null, 2);

  fetch(scenarioMeta.path)
    .then((response) => {
    if (!response.ok) {
      throw new Error(`Failed to load scenario: ${response.status}`);
    }
    return response.json();
  })
    .then((scenario) => installScenario(scenario))
    .catch((error) => {
      scenarioSummaryEl.textContent = "Scenario fixture failed to load.";
      titleEl.textContent = "Playground load error";
      summaryEl.textContent = error.message;
      meaningEl.textContent =
        "The visual playground expects repository-backed scenario fixtures. Once the JSON is available, the page will hydrate from repository data instead of hard-coded stage objects.";
      relatedDocsEl.innerHTML = "<li>Related documents unavailable.</li>";
      warningListEl.innerHTML = "<li>fixture_load_failed</li>";
      stateListEl.innerHTML = "<li>scenario_fixture: unavailable</li>";
      stateJsonEl.textContent = JSON.stringify({ error: error.message, path: scenarioMeta.path }, null, 2);
    });
}

renderScenarioButtons();
loadScenario(0);
</script>
