# Public TriggerIQ CI: exact scope and claim boundary

**Status:** Public GitHub Actions workflow exists. Its [October 14, 2026 PR run #38633058923](https://github.com/HoodedMenace86/triggeriq/actions/runs/38633058923) completed successfully on historical head `6a4b572e417f449fd34c2a653303893df9fe142d`. This **does not establish CI status for later commits**, including the October 29 input-hardening candidate.

## Workflow

[Public TriggerIQ regression](../.github/workflows/public-regression.yml) is limited to:

- Linux GitHub-hosted runners with CPython 3.11, 3.12, and 3.13.
- Dependencies in the repository-pinned `requirements-dev.txt`.
- The checked-in `tests/` suite via `python -m pytest -q -ra`.
- A smoke run of the documented public scoring sample.
- A smoke run of the documented observation-review example.
- `contents: read` permission only; no write-scoped token, cloud credentials or protected evidence required.

## What a green result would prove

For the **exact run commit and host environments**, the listed public tests and examples executed successfully. Review job logs for failure, skipped cases and exact commands. Compare source revision and expected output claims directly.

## Scorer input-ambiguity regression scope (2026-10-29 candidate)

The existing `score_posture.py` command-line parser now rejects **duplicate JSON object keys at any nesting level**, `NaN`/`Infinity` constants and numeric tokens whose finite float conversion overflows. This closes a concrete last-key-wins ambiguity that could overwrite a failed check with a passing status. Tests exercise rejected malformed inputs and one valid unknown-status input. This is **proposed branch code** until its exact-head checks complete; it does not inspect evidence truth, validate account controls, or authorize any downstream action.

## What green does not prove

- **MELLA private reference verification:** `MELLA_KERNEL_PATH` is intentionally blank; the optional private-source test is expected to skip. The job must not download or vendor private kernel bytes.
- **MELLA/TriggerIQ integration:** status is `HOLD`; upstream observations are not mapped into an authorized runtime vector.
- **Account security certification:** API/connector-invisible account settings are `UNKNOWN`, not secure.
- **Independent external reproduction:** running an Action on the same repository code is a separate host check, not a third-party independent implementation or complete cold reproduce of private governance artifacts.
- **Production validation:** no production traffic, privilege-bound executor, live data collection, incident response or audited deployment is exercised.
- **Platform independence:** this matrix is Linux only; Windows/macOS, alternative Python implementations and canonical cross-runtime receipt parity are not tested.
- **Coverage or exhaustive adversarial assurance:** no coverage threshold, formal proof, fuzz benchmark or performance claim follows from these tests.

## Review checklist

1. Confirm the workflow file matches the reviewed PR and is approved before merge.
2. Check that every matrix leg completed, not just a subset, and examine expected skips.
3. Verify the public baseline dependencies and exact checked-out commit.
4. Preserve the private/reference separation and HOLD statements.
5. For future CI changes, require a separate scope diff and review of permissions, new data sources, and external actions.

**No receipt = no result** applies to governed system outputs. A CI green check is *test execution evidence*, not a Tallyman governance receipt.
