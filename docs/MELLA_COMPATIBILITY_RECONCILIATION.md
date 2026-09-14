# MELLA compatibility reconciliation — 2026-09-14

Historical reconciliation at commit `f68d2d78b1f85ea4d1924c50e94dde856f48dbfc`.
For subsequent upstream checks and scorer changes, see [observation review](OBSERVATION_REVIEW.md).

**Result: v0.3.4 reference identity and selected behavior verified; automated
integration HOLD. v0.3.5 remains unverified.**

Public starting commit: `f0b90b14e99367f4684ee07cb0b22556631bfe93`.
This report publishes compatibility facts and aggregate checks only.
Private source, proof material, exact private vectors, and location details
are excluded.

## Reference provenance

| Artifact | SHA-256 |
| --- | --- |
| Recovered v0.3.4 archive | `540540449ff4214039b4ab809c58ab958899b01ae0b2eb962fa959f59ecee804` |
| Literal kernel | `cb20f2bb433723f153b84cb87c040bdc83824360112fb7c86a7f8616dec1b494` |
| Archived applied-route receipt | `1ec31d92b513f59b89ea1a5aff996bfd41a36e1ccb17187ec06aae8aad4fc641` |

All six file hashes listed by the archived receipt and its own sidecar
match. All 15 entries in the recovered governance-analysis manifest also
match. Hashes bind recovered bytes; they do not establish signed approval.
The runtime reports v0.3.4 despite an older directory name/class-docstring
heading. No kernel commit SHA is available for the recovered source.

Discovery covered the three relevant accessible private repositories'
listed branch trees (9, 8, and 1 branches), their releases, Drive searches
for MELLA/kernel/0.3.5, local workspace filenames, and 58 local download
archives, with a bounded nested search of the recovered-candidates bundle.
GitHub code search returned no MELLA matches; branch-tree inspection was
used as additional evidence. The private hardening contract explicitly
labels itself a non-canonical derivation. It is not this v0.3.4 kernel.
No standalone v0.3.5 artifact was found. These are bounded search results,
not a claim that such an artifact does not exist elsewhere.

## Reconciled claims

| Previous public claim | Direct evidence / correction |
| --- | --- |
| Integer core is the v0.3.4 baseline | Contradicted: reference converts values to Python floats. Integer integration requirement remains unmet. |
| 19-field vector | Confirmed; FI is required, even though stored separately from the other 18 in the input list. |
| FI is derived | Corrected: FI passes through; C_linear is also a derived response metric. |
| Route order is sufficient | Order confirmed, plus RELEASE/LIMIT candidate coupling and empty REVIEW fallback are required context. |
| Canonical deterministic serialization | Not established by this package; platform defaults affect bytes. |
| Byte-identical receipt/replay | Result semantics and same-runtime result bytes repeat; archived bytes and timestamped receipts do not. |
| v0.3.5 evidence/addendum baseline | Artifact missing; no compatibility claim is made. |
| FINDING_001 concerns M >= 0.35 | Reproduced; sampled KC violation also occurs at readiness/fallback boundary. No fix applied. |

## Executed checks

Environment: Python 3.12.14, pytest 9.1.1, Windows 10.

- Public suite: 14/14 passed with the pinned external reference supplied;
  13 passed and 1 explicitly skipped without it. The optional verifier checks
  127 nonempty route-candidate subsets in both orders, 19 missing fields,
  7 malformed values, candidate coupling, fallback, and the open defects.
- 42/42 original kernel tests passed, including 1,064 single-field corruption
  evaluations. The package's historical claim of 43 additional domain-adapter
  tests is not part of this kernel suite or evidence for this GitHub adapter.
- 8 application and 14 adversarial cases reproduced archived result semantics;
  all supplied expectations matched.
- Two result runs on this runtime produced identical bytes. Archived LF bytes
  and new Windows CRLF bytes differ; diagnostic newline normalization matches.
  This is not canonical byte replay. Original result SHA-256:
  `d6b953ec865cb0d98a7d0f11d48c86fec6f083e11e704da63e94c6ab3350d01a`;
  new Windows result SHA-256:
  `7f2d645d947692d7efc637e0875a36ff89bced82d437208c2a6d3682a0bc2033`.
- Two receipt generations differed; their wall-clock timestamps are dynamic.
- The original candidate harness reproduced historical results semantically
  after excluding its generation timestamp.
- 100,000 well-formed random vectors (seed 20260806): literal kernel and
  historical proxy agree on final routes and candidate sets in every case.
  They are not byte-identical models: response shapes differ and the proxy
  rounds metrics to six places while the kernel uses four; all 100,000 cases
  differed on at least one compared rounded metric.
- Direct kernel signed monotonicity sweep: 19 fields × 30 base vectors ×
  25 steps (seed 13), 14,250 evaluations, 2 violations (E and KC).
- Candidate sweep against literal baseline: A1 changes 508/100,000 routes
  (0.508%); A2 changes 3,539/100,000 (3.539%). Both have zero violations in
  the historical sampled signed sweep. No universal proof or adoption follows.
- Literal route/C/Q/M repeat stability: 25 vectors × 100 repeats passed.

The E violation goes from REVIEW to DEFER as M crosses 0.35. The KC violation
goes from DEFER to REVIEW as readiness improves past its DEFER condition.
The latter does not cross M=0.35. Both implicate the REVIEW fallback.

Later draft notes disagree about FINDING_001 closure and literal/proxy
provenance. Executed bytes take precedence for compatibility: the pinned
kernel remains unchanged and the violation remains reproducible. There is
no verified governance acceptance or approved replacement here. FINDING_002
remains an owner-intent question; source behavior alone cannot settle it.

## Public changes and validation boundary

Schema 0.2 separates observed facts from unmet requirements, pins identity,
corrects FI and numeric claims, describes candidate eligibility, and records
explicit HOLD blockers. The status and integration documents now match it.
`compatibility_verification.json` contains aggregate evidence, not private
receipts or case libraries. The reference verifier hashes external source
before execution and calls that exact source; it contains no routing formula,
replacement serializer, or candidate fix. Its fixtures are newly constructed
synthetic compatibility probes, not copied from the private proof corpus.

Public tests verify contract coherence, rejection before execution of a
wrong-hash reference, and fail-closed observation behavior in the existing
scorer. Optional reference tests require an explicitly supplied private path;
skipped reference tests provide no kernel verification. Running the verifier
successfully reports reference checks PASS while integration remains HOLD.

## Unresolved integration dependencies

1. Locate and authenticate the exact v0.3.5 source/addendum and reconcile its
   release status; do not infer a kernel version from later doctrine numbering.
2. Resolve the original integer-core requirement against the floating reference.
3. Bind authoritative canonical serialization, timestamp scope, and replay.
4. Supply an approved observation-to-vector mapping with evidence provenance.
5. Resolve or explicitly accept FINDING_001 in the authoritative kernel process.
6. Establish FINDING_002's intended RELEASE/LIMIT behavior.

No private repository was changed, no kernel/proof corpus was published,
and no second kernel implementation was created.
