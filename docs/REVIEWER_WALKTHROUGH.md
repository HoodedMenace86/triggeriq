# Reviewer walkthrough — TriggerIQ public evidence workflow

**Audience:** engineers, hiring reviewers, security researchers, and potential collaborators.  
**Time:** approximately one short technical walkthrough.  
**Revision boundary:** all commands apply to the checked-out public repository revision; do not generalize to private MELLA/Control Spine candidates.

## Goal

Reproduce a deterministic posture-scoring **heuristic** and an upstream observation-structure review, then demonstrate why a high score or an apparently valid observation cannot authorize a governed action.

### 1. Set up the public source

```bash
git clone https://github.com/HoodedMenace86/triggeriq.git
cd triggeriq
python -m pip install -r requirements-dev.txt
python -m pytest -q -ra
```

Read the test report. `tests/test_mella_compatibility.py::test_pinned_external_reference` **skips** when `MELLA_KERNEL_PATH` is not supplied. Do not count the private reference as reproduced by this command. The checked-in [public CI workflow](CI_SCOPE.md) preserves the same boundary. [This verified run](https://github.com/HoodedMenace86/triggeriq/actions/runs/38633058923) passed on Python 3.11, 3.12 and 3.13 with the expected skip in each job.

### 2. Run the deterministic scorer

```bash
python score_posture.py examples/sample_assessment.json
```

The checked-in fixture explicitly marks authentication, recovery and several other checks **unknown** because their actual account state is not established. Review the JSON output:

- `score` — a weighted heuristic **only over supplied applicable checks**; not an account-security certificate.
- `assessment_status` — distinguishes `verification_required`, `action_required`, `observed_checks_pass` or `not_assessed`.
- `manual_verification` — preserves unknown controls, ordered by severity.
- `open_triggers` — remediation candidates for explicitly failed checks.

The weighting is source-visible in [`score_posture.py`](../score_posture.py). An `unknown` control receives half of its severity penalty; it is **not** treated as `pass`. A set of zero applicable checks returns `score: null`, not 100.

### 3. Review evidence provenance structure

```bash
python mella/review_observations.py examples/sample_observations.json
```

The fixture is **synthetic**. The validation checks that required provenance fields and either an evidence reference or a visibility explanation are present. It does **not** check whether a referenced fact is true.

Inspect these output fields:

```json
{
  "observation_validation": "VALID",
  "evidence_truth_verified": false,
  "integration_status": "HOLD",
  "automated_routing_allowed": false,
  "kernel_evaluated": false
}
```

These are independent claims: `VALID` means the observation packet structure passed, **not** that its evidence is true or that MELLA authorized a release.

### 4. Evaluate the failure boundary

Review the existing tests in `tests/test_scorer_boundaries.py` and `tests/test_observation_review.py`. They include duplicate check identifiers, malformed provenance, unknown-state preservation and attempts to smuggle claimed approvals/100 scores into an observation packet.

**Question for the reviewer:** If a connector cannot observe MFA, is the account secure?  
**Expected answer:** It is `UNKNOWN` under that connector's scope; a manual or differently authorized check is needed. No unobserved fact can be promoted to a pass.

### 5. Identify what remains unverified

Read [`mella/STATUS.md`](../mella/STATUS.md) and [the public control boundary](CONTROL_BOUNDARY.md). The recovered MELLA v0.3.4 artifact is not the current public application. The reported reconciliation identified an unmet integer contract, unbound observation-to-vector mapping, unresolved candidate governance, and noncanonical cross-runtime receipt replay. Public tests do not close these dependencies.

## Optional interview demonstration narrative

> “This example shows how I separate observations from authority. The scorer performs deterministic checks over a declared input scope; the evidence reviewer validates shape and provenance-reference presence. Neither can authorize an operational action. The integration remains on HOLD until the governing contract, canonical evidence, and approval gates can be independently verified.”

## Evidence request format for deeper review

For any stronger claim, request the **exact Git commit / package SHA-256**, runtime and dependency versions, fixture source, expected and observed outputs, full test transcript, failure cases, and any custody receipt. A private walkthrough must be specifically approved; do not request credentials, recovery factors or private kernel bytes in public issues.
