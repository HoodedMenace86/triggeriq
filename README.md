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
- `docs/CONTROL_BOUNDARY.md` — public/private and evidence-boundary rules
- `mella/mella_adapter_contract.json` — machine-readable adapter contract

## Core rule

**Unknown is not Pass.**

If the available connector/API cannot observe a control, TriggerIQ records `unknown` and preserves the manual verification requirement.

## MELLA relationship

TriggerIQ is an observation-and-trigger layer. It does **not** replace the MELLA kernel. The public integration contract treats MELLA as the governance decision point and TriggerIQ as an evidence-producing upstream component.

See `docs/MELLA_KERNEL_INTEGRATION_v0.1.md` for the compatibility boundary.

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
