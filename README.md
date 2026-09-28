# TriggerIQ

Detect and score weak GitHub account security posture—especially on new or low-activity accounts—and emit concrete remediation triggers.

TriggerIQ turns security observations into deterministic, evidence-backed triggers while explicitly separating API-visible, connector-visible, and human-manual checks.

## Initial scope
- GitHub account security posture
- Public repository/profile surface
- Authentication and recovery controls where evidence is available
- Deterministic severity/posture scoring
- Explicit connector/API scope limitations
- Concrete remediation triggers

## Non-goals
Not a full SIEM/SOAR, generic AI trigger engine, social-content intelligence product, trading signal system, replacement for GitHub security controls, or authorization-bypass tool.

## Layout
- `security_triggers.yaml` — structured trigger catalog
- `scope_map.md` — automation/scope boundary
- `score_posture.py` — dependency-free deterministic scorer
- `examples/sample_assessment.json` — example input
- `tests/test_scorer.py` — regression tests
- `docs/MELLA_KERNEL_INTEGRATION_v0.1.md` — MELLA compatibility contract for governed routing
- `docs/MELLA_PUBLIC_RELEASE_BOUNDARY_v0.1.md` — public release boundary for MELLA
- `docs/UNIVERSAL_MACHINE_MATH_PUBLIC_RELEASE_BOUNDARY_v0.1.md` — public release boundary for Universal Machine Math
- `docs/CONTROL_BOUNDARY.md` — public/private and evidence-boundary rules
- `mella/mella_adapter_contract.json` — machine-readable adapter contract

## Core rule

**Unknown is not Pass.**

If the available connector/API cannot observe a control, TriggerIQ records `unknown` and preserves the manual verification requirement.

## MELLA relationship

TriggerIQ is an observation-and-trigger layer. It does **not** replace the MELLA kernel. The public integration contract treats MELLA as the governance decision point and TriggerIQ as an evidence-producing upstream component.

See `docs/MELLA_KERNEL_INTEGRATION_v0.1.md` for the compatibility boundary.

**Integration is on HOLD.** The [2026-09-14 reconciliation](docs/MELLA_COMPATIBILITY_RECONCILIATION.md)
pins and directly tests the recovered v0.3.4 reference. That implementation
uses Python floats; the original integer requirement remains unmet.
v0.3.5 and canonical receipt replay remain unverified. Route precedence and
the 19 required fields are verified, with unpatched monotonicity findings.
Passing public tests does not authorize automated routing.

The current [adapter contract](mella/mella_adapter_contract.json) is schema 0.3.
It supplies compatibility metadata and upstream observation validation rules;
an executable observation-to-vector adapter is not yet bound.

## Run

```bash
python score_posture.py examples/sample_assessment.json
```

Valid statuses: `pass`, `fail`, `unknown`, `not_applicable`.

Severity weights:
- critical = 40
- high = 25
- medium = 10

Scoring:
`score = 100 × (1 - observed_penalty / maximum_applicable_penalty)`

A failed check receives its full severity weight; an unknown check receives half weight. This is a posture heuristic, not a security guarantee.

Scorer output schema 0.2 uses `score: null` and `assessment_status: not_assessed`
when no applicable checks exist. Consumers must handle a nullable score.
Malformed checks, duplicate check IDs, and missing severities are rejected.
Scores cover only the checks supplied; even 100 is not an account-wide
security certificate or MELLA release approval.

## Review observations

```bash
python mella/review_observations.py examples/sample_observations.json
```

This synthetic example records a visible public-inventory check alongside
MFA that the connector cannot verify. The result keeps MFA `unknown` and
requests manual verification. Pass/fail/not-applicable claims require an
evidence reference; unknowns require a visibility explanation. Missing or
malformed provenance is reported as invalid.

The review validates structure and reference presence only. It does not
inspect referenced evidence, convert observations into kernel values, or
authorize routing. See [the workflow and problem it solves](docs/OBSERVATION_REVIEW.md).

## Compatibility checks

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
python mella/verify_reference.py --kernel /private/path/mella_unified_kernel.py
```

The optional verifier requires the exact pinned source, verifies its hash
before execution, and runs synthetic interface checks. It reports integration
HOLD even when reference checks pass. To include these checks in pytest,
set `MELLA_KERNEL_PATH` to that private file. Without it, the reference test
is explicitly skipped. Keep the source outside this public checkout.

## Evidence discipline

Every assessment should retain evidence provenance. Never store credentials, recovery codes, private keys, token values, or other secrets as evidence.

## Repository visibility

This repository is the intended public/Grok-facing surface. Sensitive source repositories remain private unless their contents have first been sanitized and deliberately published here.

## Next steps

1. Freeze and review the trigger catalog.
2. Validate scorer behavior against fixtures.
3. Validate the MELLA adapter contract against the frozen kernel test vectors.
4. Add GitHub API adapters only for explicitly authorized scopes.
5. Add a GitHub Action after the core behavior is stable.
6. Add issue creation only after false-positive behavior is tested.
