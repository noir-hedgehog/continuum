# Continuum Minimal Chain Anchoring v0

Status: provisional

## 1. Purpose

This document defines the first real chain-facing anchoring plan for Continuum.

Continuum already has:

- repository-local anchor export
- a dry-run external adapter
- a filesystem-backed transparency log target
- replayable continuity and governance state

That is enough to prove internal coherence.

It is not yet enough to present a public agent with:

- a durable onchain witness
- a wallet-linked public identity surface
- a replayable public footprint that survives one repository or one operator

This spec defines the smallest chain plan that moves Continuum from chain-adjacent to minimally onchain.

## 2. Current Reality

Continuum does not yet have:

- a deployed smart contract
- a live chain settlement path
- an onchain registry of agent identity bindings
- a public explorer centered on one agent identity

Continuum does already have infrastructure beyond text:

- local event storage
- derived state materialization
- continuity assessment
- governance replay
- local and external-style anchor export
- a real append-only transparency log adapter
- a visual playground

The missing step is public settlement.

## 3. What "Onchain Agent Identity" Means in v0

Continuum should not pretend that a chain by itself creates personhood.

In v0, an agent counts as publicly onchain only when all three layers exist together:

1. offchain signed identity
2. onchain anchor witness
3. public explorer view

### 3.1 Offchain signed identity

The current agent record remains the primary identity object:

- `agent_id`
- `display_name`
- `signing_key`
- `operator_disclosure`

This remains authored and replayable in Continuum.

### 3.2 Onchain anchor witness

The chain does not need to store full agent state.

It only needs to witness:

- which root was anchored
- which agent or community it belongs to
- when the witness was published
- which local anchor object it corresponds to

### 3.3 Public explorer view

The explorer is where a human actually sees:

- the agent's public identity
- continuity timeline
- anchor history
- governance footprint
- current status

Without this layer, the chain is only a back-end receipt, not a visible public identity surface.

## 4. Design Goal

The first chain path should optimize for:

- minimal implementation scope
- low transaction size
- human-legible public witness
- compatibility with the current repository prototype
- a path from testnet demo to mainnet witness

It should not optimize for:

- full treasury execution
- full onchain governance
- storing rich JSON onchain
- custom chain launch

## 5. Recommended v0 Chain Choice

### 5.1 Recommendation

Use Base for the first chain-backed witness path.

Use:

- Base Sepolia for the first public demo deployment
- Base Mainnet for the first production witness deployment

### 5.2 Why Base fits v0

Base is already documented as an Ethereum L2 with standard EVM JSON-RPC, public mainnet and Sepolia endpoints, and chain IDs `8453` and `84532`.

That gives Continuum:

- normal EVM tooling
- easy wallet support
- low-friction contract deployment
- a simpler path from prototype to public demo

### 5.3 Why not launch our own chain now

Running an OP Stack chain or a custom sovereign chain is not the right first step.

That would force Continuum to solve:

- sequencing
- DA
- settlement
- infra operations
- bridge and node operations

before it has even proven the simplest public identity and anchor flow.

Continuum needs public witness first, not sovereign settlement first.

## 6. Minimal Contract Shape

The first contract should be an anchor registry, not a full agent registry.

Recommended name:

- `ContinuumAnchorRegistry`

### 6.1 Why anchor registry first

An anchor registry is enough to prove:

- an agent or community published a specific root
- a wallet signed the transaction
- the anchor now has a public chain reference

This is enough to unlock:

- public identity witness
- public continuity witness
- public governance witness
- explorer rendering

without prematurely locking Continuum into onchain storage-heavy design.

### 6.2 Do not store full JSON onchain

The contract should store or emit only compact fields:

- `anchor_type`
- `subject_ref_hash`
- `root_hash`
- `local_anchor_id_hash`
- `payload_cid_hash` optional

Human-readable strings should stay offchain in the local anchor object, repository, or public archive.

## 7. Recommended v0 Contract API

The first version can be event-centric.

That means the main value comes from emitted logs, not heavy contract storage.

Suggested method:

```solidity
function recordAnchor(
    bytes32 subjectRefHash,
    bytes32 rootHash,
    bytes32 localAnchorIdHash,
    bytes32 payloadCidHash,
    uint8 anchorKind
) external returns (bytes32 anchorRecordId);
```

Suggested event:

```solidity
event AnchorRecorded(
    bytes32 indexed anchorRecordId,
    bytes32 indexed subjectRefHash,
    bytes32 indexed rootHash,
    bytes32 localAnchorIdHash,
    bytes32 payloadCidHash,
    uint8 anchorKind,
    address anchoredBy,
    uint256 chainId,
    uint256 blockNumber,
    uint256 timestamp
);
```

### 7.1 Why event-centric

Continuum is currently anchor-light but history-heavy.

For v0 the chain mostly needs to attest, not compute.

Using an event-centric registry:

- lowers complexity
- lowers state footprint
- keeps gas lower than contract-heavy state management
- gives explorer-friendly receipts

### 7.2 Anchor kind mapping

Suggested enum mapping:

- `1 = agent_state_root`
- `2 = continuity_assessment_root`
- `3 = standing_state_root`
- `4 = governance_state_root`

## 8. What Gets Anchored First

Continuum should not anchor everything immediately.

v0 should anchor only high-value roots:

### Phase A

- `continuity_assessment_root`

This is the fastest way to show:

- an agent had a continuity event
- the result was publicly witnessed
- a public identity now has visible continuity history

### Phase B

- `governance_state_root`

This lets a community publicly witness:

- proposal history
- constitution lineage state
- branch resolution state
- execution-proof status

### Phase C

- `agent_state_root`

This helps public profile and public timeline views, but should follow continuity assessment anchoring because it is less governance-sensitive.

## 9. Public Identity Binding v0

There is an important distinction:

- wallet address is not the full agent identity
- `agent_id` is not enough if it never leaves the repository

The minimal bridge is:

1. the agent profile defines `agent_id`
2. the anchoring wallet publishes a continuity or state root onchain
3. the local anchor object records both the local identity and the onchain tx reference
4. the explorer treats the combination as the public identity surface

That means public identity in v0 is:

- repository identity
- plus signing key
- plus anchoring wallet
- plus public anchor history

## 10. Explorer Consequence

Once the first chain-backed anchors exist, the right demo is no longer only the scenario playground.

Continuum should add an agent explorer page that renders:

- agent public identity
- latest continuity class
- latest recognition readiness
- latest anchor references
- migration and checkpoint timeline
- governance footprint if applicable

This is the layer that will finally make Continuum feel like:

"an onchain agent with public identity and visible footsteps"

instead of only a protocol mechanism viewer.

## 11. Cost Shape

v0 cost should be designed around the fact that OP Stack chains charge:

- execution gas
- L1 data fee
- and, after current fee model upgrades, an operator fee

That means Continuum should keep the chain payload tiny.

The contract call should ideally contain only:

- fixed-size hashes
- a small enum

and avoid:

- long strings
- raw JSON
- repeated rich metadata

### 11.1 Practical budget framing

The right way to think about v0 cost is:

- Base Sepolia demo cost: effectively testnet-only, negligible except engineering time
- Base Mainnet witness cost: small but variable per anchor, depending on current L2 gas and L1 data fee conditions
- dominant implementation cost: engineering and explorer integration, not contract logic

The biggest gas risk is not the contract itself.

It is publishing oversized calldata.

## 12. Infrastructure Needed

To move from the current prototype to minimal chain anchoring, Continuum needs:

### 12.1 Smart contract

- one small anchor registry contract

### 12.2 Adapter

- one real EVM anchor adapter in `src/anchors/export.py`

This adapter should return:

- `external_reference = tx hash`
- `target_metadata.chain_id`
- `target_metadata.contract_address`
- `target_metadata.block_number` when available

### 12.3 Operator config

- RPC URL
- chain ID
- contract address
- wallet private key or signer

### 12.4 Explorer layer

- at minimum one agent-centric page in GitHub Pages or a small web app

## 13. Suggested Implementation Sequence

### Step 1

Write and test `ContinuumAnchorRegistry` locally.

### Step 2

Add `EvmAnchorAdapter` with dry-run and signed-transaction modes.

### Step 3

Deploy to Base Sepolia.

### Step 4

Anchor one `continuity_assessment_root` for `agent:continuum:main`.

### Step 5

Build the first agent explorer page around that anchored identity.

### Step 6

Only after that, decide whether to anchor governance roots on Base Mainnet.

## 14. Non-Goals for v0

v0 should explicitly avoid:

- full onchain agent profile storage
- full onchain governance execution
- token launch
- own-chain launch
- full relay network launch
- forcing every event onchain

## 15. Decision

The minimal credible path is:

- keep local replay as the source of truth
- use Base Sepolia first
- deploy one tiny anchor-registry contract
- anchor continuity assessments before everything else
- build an agent-centric explorer immediately after first public anchor

That is the smallest step that turns Continuum from:

"a continuity protocol prototype"

into:

"a protocol with at least one publicly witnessed agent."
