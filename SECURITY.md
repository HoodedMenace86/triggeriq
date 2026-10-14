# Security policy — public TriggerIQ repository

## Scope

TriggerIQ is a scoped **public demonstration and research codebase** for GitHub security posture observations and scoring. It does not access hidden account factors, replace GitHub security controls, make a definitive security certification or authorize MELLA/Control Spine actions.

No production service or vulnerability-response SLA is claimed here.

## Reporting problems safely

**Do not post secrets or exploitable private account details in public issues or pull requests.** This includes passwords, tokens, MFA recovery codes, private keys, evidence corpora, customer data, confidential CI logs and private MELLA/Control Spine package bytes.

For a finding that can be reproduced entirely with public synthetic data and does not disclose a real vulnerability, a scoped public GitHub issue is appropriate. Include the exact commit, expected versus observed behavior and safe reproduction steps.

For a genuine vulnerability or private-data exposure, use GitHub's **private vulnerability reporting feature if it is enabled** for this repository, or contact the repository maintainer through an already established private channel. If no private channel is available, **do not** reveal the sensitive details in a public issue merely to initiate contact. This policy does not assert that a specific private reporting channel is enabled.

## Public-data and dependency rules

- Use synthetic account and evidence fixtures unless there is explicit authorization to process other data.
- Account-level settings invisible to the permitted API or connector must remain `UNKNOWN`.
- Never insert credentials into PR comments, issues, commit history, GitHub Actions configuration or logged commands.
- Run the public test suite without `MELLA_KERNEL_PATH`; a private-reference skip is expected.
- Keep GitHub Actions at minimum permissions and review any proposed external network or write-effect change.

## Integration and assurance boundary

A vulnerability fix or green GitHub Action for this repository does **not** authorize automated routing, effect execution, MELLA release, or Tallyman custody. Such claims require separate exact-artifact verification and accepted governance gates.

See [public control boundary](docs/CONTROL_BOUNDARY.md) and [CI scope](docs/CI_SCOPE.md).
