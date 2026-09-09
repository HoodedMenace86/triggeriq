# MELLA Public Release Boundary v0.1

## Purpose

This document defines the public-facing surface of MELLA that may be published for technical evaluation without publishing the complete production kernel or proprietary proof corpus.

## Publicly disclose

The public surface may describe and demonstrate:

- MELLA as a governance/control kernel rather than an application feature.
- The authority boundary between observation, evidence normalization, governance, and downstream routing.
- The seven governance dispositions and their precedence:

  `BLOCK > CONTAIN > ABSTAIN > REVIEW > DEFER > LIMIT > RELEASE`

- The principle that unknown or unavailable evidence is not converted into a passing condition.
- Deterministic integer-domain requirements for core governance/state-transition logic.
- Canonical serialization as a prerequisite for deterministic hashing and replay.
- Public schemas, interface contracts, sanitized examples, and non-sensitive test vectors.
- The existence of adversarial testing, replay requirements, and explicit open findings when those findings are already part of the released contract surface.
- High-level evidence-vector and derived-metric concepts, where publication does not disclose protected derivations or production heuristics.

## Keep private by default

Do not publish without an explicit release decision:

- Complete production kernel implementation.
- Proprietary derivations of the governance mathematics.
- Complete weighting/threshold methodology when it exposes protected design choices.
- Private proof packages, internal adversarial corpora, or unpublished golden vectors.
- Internal rule corpora, customer-specific policies, or deployment heuristics.
- Secrets, credentials, keys, private inventories, or infrastructure configuration.
- Any unpublished mechanism whose disclosure would materially reduce the difficulty of cloning the production system.

## Public claims discipline

A public repository may establish that an interface, rule, test, or document exists. It must not imply that private implementation, unavailable account state, or unreleased proof artifacts have been inspected or independently verified merely because they are referenced.

Use precise labels such as:

- `PUBLIC SPECIFICATION`
- `PUBLIC CONTRACT`
- `REFERENCE IMPLEMENTATION`
- `PRIVATE IMPLEMENTATION`
- `OPEN FINDING`
- `NOT VERIFIED HERE`

## Release rule

The public surface should be sufficient for an outside engineer to understand the architecture, reproduce released reference behavior, identify the control boundary, and challenge the design.

It should not be sufficient to reconstruct the complete production kernel from the repository alone.

## Relationship to TriggerIQ

TriggerIQ is an upstream observation/evidence producer. It may emit structured observations and remediation triggers. MELLA remains the governance authority for the governed disposition.

The public TriggerIQ repository therefore exposes compatibility contracts, not the complete private MELLA implementation.
