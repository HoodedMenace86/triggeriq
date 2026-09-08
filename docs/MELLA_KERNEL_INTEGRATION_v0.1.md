# TriggerIQ ↔ MELLA Kernel Integration Contract v0.1

## Purpose

Define the public interface between TriggerIQ observations and the MELLA governance kernel without claiming that TriggerIQ is the kernel itself.

## Authority boundary

TriggerIQ is upstream of governance:

`OBSERVE → NORMALIZE → EVIDENCE → MELLA GOVERNANCE → ROUTE`

TriggerIQ may detect conditions and emit structured evidence. MELLA decides the governed disposition.

TriggerIQ must not silently override, reinterpret, or replace MELLA route precedence.

## Known MELLA compatibility constraints

The integration is designed around the current frozen MELLA kernel contract carried forward from the established v0.3.x work:

- Deterministic integer arithmetic in the core.
- No floating-point dependency in core state transitions or governance decisions.
- Canonical deterministic serialization for hashed artifacts.
- Unknown evidence remains unknown; missing evidence is not a pass.
- Receipt/replay semantics are outside TriggerIQ's authority.
- Governance outcomes are inputs to downstream monitoring rather than mutable ledger state.

## Evidence vector boundary

The current MELLA evidence model uses a 19-field evidence vector concept:

`(H, A, R, D, E, P, V, U, K, KC, AG, RC, EQ, DR, RE, RP, TS, CP, FI)`

Derived governance metrics include:

`C, Q, M, RF, PI, AR, FI`

TriggerIQ should supply only the evidence fields it can establish. It must not fabricate missing values to complete the vector.

Where a TriggerIQ check is unavailable because GitHub/API/connector permissions do not expose the necessary control, the adapter should emit `unknown` and preserve provenance.

## Route boundary

The established MELLA route precedence is:

`BLOCK > CONTAIN > ABSTAIN > REVIEW > DEFER > LIMIT > RELEASE`

TriggerIQ can recommend remediation severity, but MELLA remains authoritative for governed routing.

## Kernel versioning

The known frozen kernel baseline is **MELLA_UNIFIED_CONSEQUENCE_READINESS_ROUTE_KERNEL v0.3.4**.

The v0.3.5 work adds an evidence-vector/addendum layer. This public TriggerIQ repository does not claim to contain the complete private kernel implementation or its complete proof/test corpus.

That distinction is intentional.

## Adapter contract

A TriggerIQ-to-MELLA adapter should normalize an observation to a structure equivalent to:

```json
{
  "observation_id": "uuid-or-deterministic-id",
  "source": "github",
  "check_id": "GH-AUTH-001",
  "status": "unknown",
  "severity": "critical",
  "observed_at": "deterministic timestamp supplied by the execution layer",
  "evidence": {},
  "provenance": {
    "method": "manual",
    "scope": "account-security-unavailable",
    "source_version": "triggeriq-0.1"
  }
}
```

The actual MELLA receipt schema, canonical serializer, hashing rules, and replay logic remain kernel-owned artifacts and must be imported from their authoritative implementation rather than duplicated here.

## Known open kernel finding

The v0.3.x behavioral validation work identified a monotonicity discontinuity at the `M >= 0.35` boundary. This repository records that fact as an integration dependency; it does **not** silently patch or redefine the kernel threshold.

Any change to that boundary belongs in the kernel's own versioned specification, vectors, and adversarial test suite.

## Integration gate

Before TriggerIQ observations are allowed to drive automated MELLA routing:

1. Observation schema is frozen.
2. Evidence provenance is present.
3. Unknown/manual states survive normalization.
4. Integer-domain conversion is deterministic.
5. Canonical serialization is delegated to the authoritative kernel implementation.
6. Replay produces byte-identical normalized observations.
7. Route precedence is tested against boundary/collision cases.
8. Adapter tests pass independently of the GitHub connector.

## What this file does not claim

This is a compatibility contract, not a copy of the MELLA kernel. A public TriggerIQ consumer must not infer that the complete private kernel, receipts, proofs, or test corpus are present in this repository.
