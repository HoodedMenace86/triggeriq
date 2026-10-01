# GitHub Lineage Audit — 2026-09-30

## Purpose

This document records the visible GitHub state before any modernization work. It is an inventory, not a claim that GitHub contains the full current system.

## Repositories visible to the connected GitHub account

1. `HoodedMenace86/trigger-iq-demo` — private
2. `HoodedMenace86/trigger-iq-smarter-retail-ops` — private
3. `HoodedMenace86/Core-Engine-.3` — private
4. `HoodedMenace86/triggeriq` — public

## Current public `triggeriq` scope

The current README describes TriggerIQ as a GitHub security-posture trigger/scoring project with a MELLA compatibility boundary. The repository presently includes:

- deterministic posture scoring
- observation review
- public/private control-boundary documentation
- a MELLA adapter contract
- MELLA compatibility verification utilities
- regression tests

The README also records a historical integration HOLD tied to a 2026-09-14 reconciliation state. That statement is part of the repository's evidence lineage and should not be silently rewritten to imply later external work is already present here.

## Material project areas not presently represented in the visible repositories

Code search and root inspection did not find current implementations for:

- BetShield
- Ten Realms
- Tartarus
- Aether Grade
- Jimmy Layer
- current Pulse defense/runtime work
- System Raptors / Vaelthor runtime integration
- current cross-sport state-transition analytics

Absence from these repositories does not mean those projects do not exist elsewhere. It means they are not presently represented in the GitHub surface available to this audit.

## Migration rule

Do not turn an older narrow repository into a false representation of the current architecture.

Preferred handling:

- preserve old repositories as historical/product-specific lineages;
- migrate only verified artifacts;
- keep source provenance and test receipts with migrated code;
- distinguish implemented runtime from design/canon/specification;
- do not upgrade claims merely because documentation has advanced;
- never overwrite historical compatibility findings without an explicit superseding record.

## Immediate conclusion

`triggeriq` is a useful lineage anchor and staging surface, but it should not become the master repository for every current project by accumulation. A new root repository is justified if the goal is to represent the current multi-domain architecture coherently.
