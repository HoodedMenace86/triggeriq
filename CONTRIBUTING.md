# Contributing to public TriggerIQ

This repository exposes a **scoped security posture scoring and observation-review implementation**. It is not the complete LazyBotz Master System or a public copy of private MELLA/Control Spine implementations.

## Safe contributions

Bug reports, deterministic regression tests, documentation, synthetic examples and approved adapter proposals are welcome in principle. Proposals should first describe the observed defect, affected source revision, reproduction command and expected versus actual behavior.

Do not submit real account access tokens, private security inventories, login or recovery factors, sensitive user data, customer leads, private kernels, protected fixtures, nonpublic dependency archives or unreleased parameterization.

## Validation

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q -ra
python score_posture.py examples/sample_assessment.json
python mella/review_observations.py examples/sample_observations.json
```

A test run without the privately held `MELLA_KERNEL_PATH` **must** show an expected skip. Do not simulate the private reference, replace its hash, or claim integration approval to make CI look green.

## Pull request expectations

- Restrict changes to one objective and document any new permission, dependency, external endpoint, or data-handling path.
- Preserve `unknown` when a control is not observable; do not auto-fill missing facts.
- Include a failing test first when reporting a regression; prefer synthetic fixtures.
- Separate evidence validation from authorization, and authorization from effects and receipts.
- State measured behavior at the exact revision. Do not present local PASS as external reproduction or production readiness.
- Do not add workflow write permissions or external effects without a distinct explicit review.

## Disclosure and licensing boundaries

Review [SECURITY.md](SECURITY.md) before reporting sensitive findings and [docs/CONTROL_BOUNDARY.md](docs/CONTROL_BOUNDARY.md) before publishing any integration material.

No license is declared by this file. Do **not** infer that source publication alone grants a license to redistribute or reuse proprietary portions. Licensing decisions are reserved to the repository owner.
