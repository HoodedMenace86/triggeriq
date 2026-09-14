# MELLA public integration status

**HOLD — reference audited; runtime integration remains unbound.**

The 2026-09-14 reconciliation directly tested the recovered v0.3.4 kernel
with SHA-256 `cb20f2bb433723f153b84cb87c040bdc83824360112fb7c86a7f8616dec1b494`.
The archive receipt agrees with this hash. A kernel source commit and an
authoritative v0.3.5 artifact were not located in the searched sources.
Hash agreement establishes artifact identity, not release approval.

Verified: all 19 inputs (including FI) are required; malformed evidence is
not a pass; route precedence is unchanged; RELEASE excludes LIMIT during
candidate formation. The literal reference uses Python floats, so the
previous claim that this baseline implements an integer core was incorrect.
The original integer integration requirement remains unmet.

42 kernel tests passed. The 8 application and 14 adversarial results replay
semantically. Fresh result files repeat byte-for-byte on the tested runtime,
but differ from archived bytes because of Windows line endings. Receipts
also contain the current time. Canonical cross-runtime receipt/replay is
unverified.

`PACKET_2_FINDING_001` is reproduced and unpatched. The sampled signed sweep
finds two violations (E and KC), at the M/DEFER and readiness/fallback
boundaries. Historical A1/A2 candidate results reproduce, but no candidate
is adopted here. Later draft prose saying “closed” does not establish an
applied fix or governance acceptance. `PACKET_2_FINDING_002` remains an
intent question despite the RELEASE/LIMIT mechanism being verified.

Automated integration also requires an authoritative observation-to-vector
mapping and canonical serialization/replay binding. Unknown observations
must remain unknown; adapters cannot fill missing fields or patch routing.

See [the reconciliation](../docs/MELLA_COMPATIBILITY_RECONCILIATION.md),
[the current contract](mella_adapter_contract.json), and
[the sanitized verification record](compatibility_verification.json).
