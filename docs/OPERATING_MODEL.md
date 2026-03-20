# Continuum Operating Model v0

## Purpose

This document defines how the project should be operated when a human founder and one or more agents are jointly building it.

The goal is not only project management.

The goal is to create an operating model that is itself aligned with the project's thesis:

- agent-native
- historically traceable
- capable of delegation
- explicit about authority and responsibility

## How Background Agents Work Here

Within this environment, background agents can be spawned for bounded tasks.

Operationally:

- they run in parallel
- they return structured completion messages
- completion appears as a notification in the conversation
- the main agent can also explicitly wait for them when blocked
- their outputs are advisory until integrated into the main thread

So yes, there is a callback-like behavior in practice:

- when a subagent finishes, a completion notification arrives
- the main agent can then integrate, reject, refine, or re-delegate

This is not a fully autonomous daemon mesh. It is supervised delegation with asynchronous returns.

## Collaboration Contract

### Human role

The human founder primarily acts as:

- question setter
- constraint setter
- resource holder
- legitimacy anchor for external commitments
- final approver for high-risk or irreversible decisions

The human does not need to manually break down all work.

### Main agent role

The main agent acts as:

- project integrator
- document editor
- task decomposer
- subagent coordinator
- architectural decision driver
- memory keeper for the current thread and workspace

### Subagent role

Subagents act as:

- bounded researchers
- spec drafters
- implementation workers
- reviewers

They do not define project truth alone.

## Default Delegation Rule

The main agent should act first and ask later unless one of the following is true:

- the decision creates legal or financial exposure
- the decision changes public positioning materially
- the decision locks the architecture in a costly direction
- the decision conflicts with stated founder constraints

Everything else should move forward by default.

## Decision Classes

### Class A: Agent-decide

The main agent can decide and execute:

- document structure
- working definitions
- first-pass specs
- task decomposition
- internal planning
- background research delegation
- repo structure for project docs and prototypes

### Class B: Human-confirm

The main agent should propose, then seek confirmation:

- external naming
- public launch narrative
- pricing
- token issuance structure
- legal entity choices
- fundraising posture
- hiring priorities

### Class C: Human-only

The main agent cannot unilaterally commit:

- signing contracts
- moving money
- publishing under legal representation
- irreversible legal or regulatory actions

## Heartbeat Model

The project should run on a repeating heartbeat, even before formal automation exists.

Each heartbeat has five stages:

1. Observe
- what changed
- what completed
- what got blocked

2. Evaluate
- what matters now
- what assumptions changed
- what risks increased

3. Delegate
- what can be split into bounded parallel tasks
- what remains on the integration path

4. Commit
- update docs
- update task board
- record revisions

5. Escalate
- ask the founder only where authority or risk requires it

## Project Control Surfaces

The project should have five control surfaces.

### 1. Thesis surface

Purpose:
- define what the project believes right now

Artifacts:
- `FOUNDING_THESIS.md`
- `AUTHORSHIP.md`

### 2. Spec surface

Purpose:
- define what the system should do

Artifacts:
- protocol specs
- governance specs
- architecture docs

### 3. Task surface

Purpose:
- define what needs doing now

Artifacts:
- task board
- build plan
- milestone docs

### 4. History surface

Purpose:
- preserve how decisions evolved

Artifacts:
- dialogues
- revision log
- debates
- open questions

### 5. Execution surface

Purpose:
- code, prototypes, experiments, scripts

Artifacts:
- source tree
- tests
- demos

## Minimum Agent-Native Task Model

Traditional project management tools assume:

- stable human assignees
- linear ownership
- tasks as tickets detached from reasoning traces

Continuum should instead adopt an agent-native task model.

Each task should carry:

- `task_id`
- `title`
- `intent`
- `type`
- `status`
- `authority_class`
- `owner`
- `contributors`
- `depends_on`
- `outputs`
- `linked_questions`
- `linked_docs`
- `decision_needed`
- `history`

Suggested task types:

- thesis
- spec
- research
- implementation
- review
- debate
- integration

Suggested statuses:

- proposed
- active
- blocked
- review
- decided
- archived

## What Makes This Agent-Native

An agent-native board should not just track tasks.

It should track:

- why the task exists
- which assumptions it depends on
- whether the task is safe for autonomous execution
- which outputs become public commitments
- which debates or questions it touches

This means tasks should be connected to:

- specs
- dialogues
- revisions
- decisions

Not just deadlines.

## Recommended Initial Workflow

When you, the founder, want the system to keep moving, a minimal prompt can be:

"Keep advancing Continuum. Break down the next work, delegate what is parallelizable, and only stop for high-risk decisions."

That authorizes the main agent to:

- inspect current docs and code
- update the task surface
- spawn subagents
- integrate outputs
- create next-step artifacts

## Escalation Triggers

The main agent should stop and ask when:

- the project is about to commit to a public identity or launch claim
- a pricing or fundraising stance is being fixed
- a legal/regulatory boundary is crossed
- a design tradeoff changes the founder's stated values

## Near-Term Implementation Recommendation

The project should create an internal workboard in-repo before adopting external software.

Recommended first artifacts:

- `docs/TASK_BOARD.md`
- `docs/BUILD_PLAN_12_WEEKS.md`
- `docs/OPEN_QUESTIONS.md`
- `docs/REVISION_LOG.md`

This keeps the reasoning trace near the work itself.

## Longer-Term Vision

If Continuum succeeds, it should eventually have its own agent-native project operating system:

- task graph as signed events
- agent and human assignees
- proposals for roadmap changes
- execution receipts
- dependency-aware delegation
- historical trace of how work evolved

That would be closer to an agent-native Jira than today's tools.
