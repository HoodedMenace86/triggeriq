# Public Control Boundary

This repository is intentionally the public/Grok-facing surface for TriggerIQ.

## What belongs here
- Sanitized TriggerIQ source
- Security trigger definitions
- Deterministic scoring logic
- Public integration contracts
- Test fixtures that contain no secrets
- Documentation needed to reproduce behavior

## What does not belong here
- GitHub tokens or credentials
- Recovery codes
- Private keys
- Private account/security inventories
- Raw security evidence containing secrets
- Proprietary/private MELLA implementation unless deliberately released
- Claims of verification that have not been reproduced from authoritative artifacts

## Evidence rule

A connector limitation is an observation about visibility, not proof that a control is absent or present.

Use:

`PASS` = evidence establishes the control.

`FAIL` = evidence establishes the control is not satisfied.

`UNKNOWN` = available evidence is insufficient.

Never convert `UNKNOWN` to `PASS` for convenience.

Compatibility hashes and aggregate verification counts may be published.
Private reference paths, raw receipts, exact private evidence vectors,
candidate models, and proof corpora must stay outside this repository.
Keep any reference checkout in a separate directory. The optional verifier
accepts an external path; it must not download or vendor the kernel.

A reference-check PASS is not integration approval. The current contract records
unmet numeric, version, mapping, serialization, and governance dependencies;
neither a high posture score nor a RELEASE route can clear that HOLD.

## Grok-facing rule

An external model may inspect this repository as an implementation/documentation surface. It should not infer that private repositories, hidden account settings, or unavailable security controls have been inspected merely because this public repository describes them.
