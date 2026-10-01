# Next Repository Blueprint

## Objective

Define a clean repository shape for the current architecture without collapsing distinct products, evidence classes, or runtime responsibilities into one undifferentiated codebase.

This is a migration blueprint. It does not declare that all listed components are already implemented in GitHub.

## Recommended top-level model

A new root repository should act as a control-and-integration spine, not as a dumping ground for every artifact.

Suggested shape:

```text
/
  README.md
  GOVERNANCE.md
  ARCHITECTURE.md
  pyproject.toml

  core/
    governance/
    receipts/
    routing/
    time/
    provenance/

  processes/
    vaelthor/
    raptors/
    swarm/
    slowbot/
    jimmy/

  products/
    triggeriq/
    betshield/
    aether_grade/

  realms/
    ten_realms/
    tartarus/

  analytics/
    state_transition/
    nfl/
    baseball/

  adapters/
    github/
    sports_data/
    game_runtime/

  tests/
    unit/
    adversarial/
    integration/
    reproduction/

  evidence/
    manifests/
    receipts/
    external_reproduction/

  docs/
    doctrine/
    contracts/
    architecture/
    migration/
```

## Boundary rules

### 1. Governance is not product logic

MELLA-style governance, transition gates, receipts, certification state, provenance, and routing belong in `core/`.

Products consume those capabilities. They do not redefine them.

### 2. Named system processes need executable standing

A named process should have:

- a documented purpose;
- explicit inputs and outputs;
- authority boundary;
- failure behavior;
- tests;
- observability;
- a clear distinction between lore/display identity and actual runtime behavior.

A process that exists only in prose must be labeled specification/canon, not runtime.

### 3. Sports analytics should be domain-independent at the mathematical core

The reusable state-transition layer belongs in `analytics/state_transition/`.

Sport adapters belong under their own domains.

Core metric spine currently under evaluation:

- DQ — Decision Quality
- ΔC — Control Change
- PC — Pressure Conversion
- SPR — State Preservation Rate
- FP — Failure Propagation
- RV — Recovery Velocity
- RT — Recovery Time

Football-specific and baseball-specific variants should extend those metrics rather than silently changing the core definitions.

### 4. Historical evidence stays historical

Older repositories should be imported by verified artifact, not copied by filename alone.

Every migrated artifact should record:

- source repository or source package;
- original path;
- source commit or source hash when available;
- destination path;
- migration date;
- semantic changes, if any.

### 5. No false completion

Documentation may describe planned placement before implementation exists, but status must remain explicit:

- PRESENT
- MIGRATED
- VERIFIED
- SPEC_ONLY
- MISSING
- BLOCKED

## Repository naming

The root repo should be named for the architecture rather than one narrow product. Avoid using `triggeriq` as the umbrella name because TriggerIQ now represents only one product/domain lineage.

## Migration order

1. Freeze the repository inventory.
2. Recover authoritative artifacts by hash/provenance.
3. Establish the core governance/receipt/time contracts.
4. Bind executable system processes one at a time.
5. Import product lanes.
6. Import Ten Realms/Tartarus runtime work.
7. Import cross-sport analytics.
8. Add integration tests only after each lane has independent tests.
9. Publish a system-wide status manifest showing implemented versus specified components.

## Non-claim

A new repository structure does not itself create a new operating system, autonomous agent framework, certified governance product, or validated predictive sports engine. Those claims require implementation and evidence.
