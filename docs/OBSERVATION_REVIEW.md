# What TriggerIQ solves and how to use observation review

TriggerIQ addresses a practical evidence gap: a GitHub integration may see
repositories while being unable to verify account controls such as MFA,
recovery settings, or application access. A clean visible inventory does
not establish that the hidden controls are secure.

TriggerIQ records what was observed, what remains unknown, and what someone
needs to verify or remediate. Its public MELLA compatibility checks also
make the exact reference version and remaining integration gaps explicit,
so an old claim or a high posture score cannot stand in for routing approval.

## Example

| Available information | Observation | Next step |
| --- | --- | --- |
| A referenced public-repository inventory was reviewed | Reported pass, with evidence reference | Review that reference; its presence alone is not proof |
| Connector cannot establish MFA status | Unknown, with visibility explanation | Manual account-security verification |
| Assessment contains no applicable checks | No score; not assessed | Collect applicable evidence |
| MELLA reference checks pass but integration dependencies remain | HOLD | Resolve the named authoritative dependencies |

The checked-in example is synthetic and describes no real account.

```bash
python mella/review_observations.py examples/sample_observations.json
```

An input packet contains an `observations` list. Each record supplies the
six required fields in `mella/mella_adapter_contract.json`. Contract schema
0.3 adds explicit provenance requirements:

- `method`: manual, API, or connector.
- `scope` and `source_version`: nonempty strings.
- `evidence_ref`: required for pass, fail, and not_applicable claims.
- `visibility_limit`: required for unknown observations.

Observation IDs must be unique, nonempty, and unpadded. Status and severity
values must be explicit. Empty packets, malformed provenance, missing
references, and duplicate observation IDs are invalid. The CLI also rejects
duplicate JSON keys and non-finite JSON numbers, preventing ambiguous input.
No missing field is converted to zero or a pass.

The review produces a diagnostic report with per-observation next actions,
input issues, and integration blockers read from the contract. Input fields
claiming a perfect score, RELEASE, or approval cannot change its HOLD result.
No kernel is loaded or evaluated by this command.

Exit code 0 means structurally valid input; exit code 2 means invalid input
or an unreadable packet. Neither exit code is routing approval. Output JSON
is a diagnostic format, not MELLA canonical serialization or a receipt.

## Scorer correction and migration

Previously, an empty assessment or one containing only not_applicable
checks returned 100. That could make absence of assessment look like a
perfect result. Scorer output schema 0.2 returns `score: null`,
`assessment_status: not_assessed`, and `applicable_checks: 0` in these cases.
Consumers must support nullable scores.

Valid applicable checks retain the existing weight formula. All-unknown
checks still receive 50, with `verification_required`; failed checks produce
`action_required`. All supplied applicable checks passing produces
`observed_checks_pass`, which makes no account-wide coverage claim.

Malformed check records, duplicate check IDs, and missing severity are now
rejected rather than silently accepted or defaulted. IDs must be nonempty
unpadded strings. This prevents repeated copies of one check from diluting
its failed result in the denominator.

## Limits

This is a usable local evidence-structure review and posture-reporting tool.
It does not query GitHub automatically, verify referenced evidence, establish
complete checklist coverage, or prove that an account is secure. An evidence
reference can be false or stale and must be checked by the responsible reviewer.
It also does not define the observation-to-MELLA-vector mapping.

The v0.3.5, numeric, serialization/replay, mapping, and governance dependencies
remain unresolved. No kernel fix, candidate model, private source, or proof
corpus is added by this continuation.

## Validation

56 public tests passed with the pinned external v0.3.4 reference supplied.
Without that private reference, 55 passed and one reference test was explicitly
skipped. Coverage includes empty assessments, malformed and duplicate checks,
unknown preservation, required provenance, ambiguous JSON, and rejection of
caller-supplied release claims. The kernel implementation is unchanged.
