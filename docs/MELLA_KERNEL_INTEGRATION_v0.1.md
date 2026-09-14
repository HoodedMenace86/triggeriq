# TriggerIQ and MELLA compatibility contract

This existing document path is retained for links. The machine-readable
contract is now **schema 0.2**; it supersedes the unverified baseline claims
in the original v0.1 document. Consumers must explicitly review the schema
change. Automated routing remains **HOLD**.

## Authority and identity

TriggerIQ observes checks and preserves their provenance. MELLA owns metric
computation, candidate eligibility, routing, serialization, and replay.
No kernel implementation, reconstructed model, private case library, or
candidate fix belongs in this public repository.

The recovered reference identifies itself as v0.3.4 and is pinned by
SHA-256 in [the adapter contract](../mella/mella_adapter_contract.json).
No v0.3.5 source/addendum artifact or kernel source commit was located.
Later draft doctrine is supporting context, not a substitute release.

## Observations and evidence

Observation statuses remain `pass`, `fail`, `unknown`, `not_applicable`.
Required observation fields remain `observation_id`, `source`, `check_id`,
`status`, `severity`, and `provenance`. This describes an upstream envelope;
it is not yet a runtime-validated schema or an executable vector mapping.

The reference requires the ordered 19-field input vector:

`H, A, R, D, E, P, V, U, K, KC, AG, RC, EQ, DR, RE, RP, TS, CP, FI`

Every field, including FI, is required. Missing/invalid values are malformed.
TriggerIQ must retain missing evidence and must never insert zero, a score,
or an invented value to complete a vector. The kernel's conservative shadow
evaluation is its own malformed-input behavior; substituted values are not
observations and must not be described as verified evidence.

`FI` is an input passed through to the response, not a derived metric.
Derived response metrics are `C_linear, C, Q, M, RF, PI, AR`.

## Numeric requirement versus observed implementation

The literal v0.3.4 reference accepts numeric int/float inputs in [0,1], rejects
booleans and malformed values, and computes using Python floats. It routes
on unrounded metrics and rounds response metrics to four decimal places.

The old `integer_core_required` rule is retained as an **unmet integration
requirement**, not a description of v0.3.4. No authoritative integer mapping
was recovered. Do not implement a conversion or a second arithmetic model
inside TriggerIQ to conceal this mismatch.

## Route semantics

Precedence among eligible candidates is:

`BLOCK > CONTAIN > ABSTAIN > REVIEW > DEFER > LIMIT > RELEASE`

Candidate eligibility is determined first. The reference evaluates RELEASE
before LIMIT; LIMIT is eligible only when RELEASE is not. The precedence
list alone is therefore insufficient to reproduce routing. An empty
candidate set falls back to REVIEW. Malformed inputs exclude LIMIT and RELEASE;
zero parseable fields produce ABSTAIN. Only the kernel evaluates these rules.

The kernel always reports `release_allowed: false`. A route labeled RELEASE
is not production authorization. Preserve the kernel's denied claims.

## Serialization and replay

Ownership remains with MELLA, but no canonical serializer contract was
found in the v0.3.4 package. Its harness uses `json.dumps(indent=2)` and
platform-default text writing; receipt generation inserts wall-clock time.
Same-runtime result determinism was reproduced. Archived Windows byte
identity and deterministic receipt bytes were not.

Do not replace this with a TriggerIQ serializer or label normalized JSON
as original byte replay. A versioned canonical format, encoding/newline
policy, timestamp scope, and authoritative implementation must be bound
before claiming canonical cross-runtime replay.

## Findings and gate

FINDING_001 remains present: crossing a fallback boundary can violate signed
monotonicity. Both the M >= 0.35 transition and a readiness RF >= 0.40
transition reproduce. Passing malformed-input corruption tests does not
establish signed monotonicity over well-formed inputs.

FINDING_002's RELEASE/LIMIT mechanism is verified; its governance intent is
unresolved. No candidate fix or governance decision is adopted here.

Before automated routing, resolve the explicit blockers in `integration_gate`
and bind the approved version/hash, mapping, numeric contract, canonical
serializer, and replay evidence. Public compatibility checks cannot clear
this gate or grant authority. See [the reconciliation](MELLA_COMPATIBILITY_RECONCILIATION.md).
