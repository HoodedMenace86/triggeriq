# MELLA Public Integration Status

## Current baseline

- Kernel baseline: `MELLA_UNIFIED_CONSEQUENCE_READINESS_ROUTE_KERNEL v0.3.4` (frozen baseline from the established work).
- v0.3.5 work: evidence-vector/addendum layer.
- TriggerIQ role: upstream observation/evidence producer.
- MELLA role: governance and route authority.

## Preserved invariants

1. Unknown evidence remains unknown.
2. Core decisions use deterministic integer arithmetic.
3. Canonical serialization and receipt/replay semantics remain kernel-owned.
4. TriggerIQ cannot override MELLA route precedence.
5. Public documentation must not imply that private kernel artifacts are present here.

## Route precedence

`BLOCK > CONTAIN > ABSTAIN > REVIEW > DEFER > LIMIT > RELEASE`

## Known open dependency

`PACKET_2_FINDING_001`: monotonicity discontinuity at the `M >= 0.35` boundary.

This is recorded as an explicit dependency. It is not silently repaired in TriggerIQ. Resolution belongs in the authoritative MELLA specification, vectors, and adversarial test suite.

## Required next kernel work

- Reconcile the v0.3.5 evidence-vector/addendum with the authoritative frozen kernel implementation.
- Re-run the kernel and adapter behavioral vectors after any boundary change.
- Preserve deterministic serialization and replay byte identity.
- Keep TriggerIQ adapter tests separate from kernel tests so a connector failure cannot masquerade as a kernel failure.
