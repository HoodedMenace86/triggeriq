# TriggerIQ GitHub Scope Map

The integration's visibility is not equivalent to the account's security posture.

| Trigger | Initial method | Automation requirement | Fallback |
|---|---|---|---|
| GH-AUTH-001 | Manual | Account security/2FA scope | Manual |
| GH-AUTH-002 | Manual | Authentication-method inventory | Manual |
| GH-REC-001 | Manual | Recovery/security scope | Manual |
| GH-TOK-001 | Manual | Token metadata scope, if exposed | Manual |
| GH-SSH-001 | Manual | SSH-key inventory scope | Manual |
| GH-PUB-001 | API | Public repository listing | Automate |
| GH-PUB-002 | API | Public profile/repository data | Automate |
| GH-REPO-001 | API | Repository admin/ruleset scope | Elevated automation or manual |
| GH-REPO-002 | API | Collaborator/team permissions | Elevated automation or manual |
| GH-SEC-001 | API | Security-alert scope/features | Automate where authorized |
| GH-APP-001 | Manual | Authorized-app/account scope | Manual |
| GH-ORG-001 | API | Organization membership/role scope | Automate where authorized |
| GH-ACT-001 | Manual | Complete security/activity history | Manual |

## Visibility states

- **API** — GitHub API can supply sufficient evidence with intended authorization.
- **Connector** — connected integration can supply evidence under its granted scopes.
- **Manual** — human inspection is required.
- **Unknown** — evidence is unavailable; it is not converted to Pass.

## Scope expansion gate

A check moves from manual to automated only when:

1. Required permission is documented.
2. Returned data is sufficient.
3. Evidence provenance is retained.
4. Deterministic tests exist.
5. Authorization is not silently broadened.

TriggerIQ must never bypass GitHub permissions to make a check appear automated.

Correct output when visibility is insufficient:

`UNKNOWN / MANUAL VERIFICATION REQUIRED`
