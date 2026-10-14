# TriggerIQ
> **Larger system context:** TriggerIQ is a scoped public implementation, not the entire LazyBotz Master System. See the [public architecture guide](docs/LAZYBOTZ_PUBLIC_ARCHITECTURE.md) for component responsibilities, review boundaries and why private MELLA/Control Spine work must not be mistaken for a production-integrated release.


Detect and score weak GitHub account security posture—especially on new or low-activity accounts—and emit concrete remediation triggers.

TriggerIQ turns security observations into deterministic, evidence-backed triggers while explicitly separating API-visible, connector-visible, and human-manual checks.

## Start here — reviewers and collaborators

[![Public TriggerIQ regression](https://github.com/HoodedMenace86/triggeriq/actions/workflows/public-regression.yml/badge.svg)](https://github.com/HoodedMenace86/triggeriq/actions/workflows/public-regression.yml)

| Goal | Inspect |
| --- | --- |
| Run the public implementation | [Scorer](score_posture.py) and [sample assessment](examples/sample_assessment.json) |
| Reproduce tests | [Public Python CI](.github/workflows/public-regression.yml) and [CI claim boundaries](docs/CI_SCOPE.md) |
| Follow a short technical walkthrough | [Reviewer walkthrough](docs/REVIEWER_WALKTHROUGH.md) |
| Understand the wider architecture | [LazyBotz public guide](docs/LAZYBOTZ_PUBLIC_ARCHITECTURE.md) |
| Check integration blockers | [MELLA public status](mella/STATUS.md) |
| Propose a code/documentation improvement | [Contribution rules](CONTRIBUTING.md) and [security guidance](SECURITY.md) |

**Executed GitHub evidence:** [October 14, 2026, PR run #38633058923](https://github.com/HoodedMenace86/triggeriq/actions/runs/38633058923) — Ubuntu Python 3.11, 3.12 and 3.13 each reported **55 passed / 1 skipped**; one private MELLA reference test was deliberately not executed. This validates the *public implementation only*. A passing workflow cannot approve MELLA routing or certify an account.

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

## Next engineering gates

The public regression workflow and existing scorer fixtures now exist; they do not establish end-to-end readiness.

1. Keep the trigger catalog and scorer fixture tests synchronized whenever behavior changes.
2. Close or explicitly retain the **MELLA integration HOLD** on exact reference, numeric contract, serialization, mapping and governance findings before any automated routing.
3. Add GitHub API adapters only when the permission scope, evidence provenance and false-positive behavior are documented and approved.
4. Validate issue-creation and external-effect workflows separately before enabling actions that change user or repository state.
5. Preserve the distinction between public demonstrations, private experimental PRs and independently reproduced integration evidence.

Contributions and vulnerability reports must follow [CONTRIBUTING.md](CONTRIBUTING.md) and [SECURITY.md](SECURITY.md); do not expose credentials or private kernel material.
