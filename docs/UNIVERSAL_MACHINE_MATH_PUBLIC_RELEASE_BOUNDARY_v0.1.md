# Universal Machine Math — Public Release Boundary v0.1

## Purpose

This document defines a safe public-facing description of Universal Machine Math without publishing the complete proprietary mathematics, derivations, parameterization, or production decision machinery.

## Public surface

The public release may establish the following architectural ideas:

- A mathematical substrate intended to make system behavior explicit, measurable, testable, and reproducible.
- Separation between raw observations, derived quantities, governance decisions, and downstream product behavior.
- Deterministic state-transition requirements where mathematical results participate in routing, receipts, replay, or integrity checks.
- Integer-domain computation as the preferred core representation for governance-critical operations.
- Explicit interfaces between the mathematical substrate and MELLA governance rather than allowing application code to silently redefine governance semantics.
- Sanitized equations or illustrative examples whose disclosure does not reveal the protected production derivation.
- Public reference vectors and challenge cases when intentionally released.

## Protected surface

The following remain private by default:

- Complete proprietary derivations and proofs that constitute the protected mathematical core.
- Production weights, parameter sets, threshold construction, calibration methods, and tuning methodology when those details expose protected competitive design.
- Internal variable semantics that are not required to understand the public interface.
- Complete model-selection, optimization, or heuristic procedures used in production.
- Unreleased golden vectors, private fixtures, internal notebooks, and research notes.
- Customer-specific or deployment-specific parameterization.

## Safe publication pattern

A public mathematical release should publish the **interface and falsifiability surface** before publishing the full implementation:

`definitions → domains → invariants → reference examples → public vectors → tests`

The public artifact should let an outside reviewer challenge whether the stated mathematics is coherent and reproducible without giving them the complete production recipe.

## Relationship to MELLA

Universal Machine Math is treated as a mathematical substrate. MELLA is the governance/control authority that applies its own versioned rules to evidence and state.

A public UMM artifact therefore must not imply that every internal UMM equation, variable, parameter, or derivation is present in the public repository.

## Claims discipline

Do not label an unpublished result as proven merely because it is mathematically plausible. Use explicit status labels such as:

- `PUBLIC DEFINITION`
- `PUBLIC EXAMPLE`
- `REFERENCE VECTOR`
- `PRIVATE DERIVATION`
- `RESEARCH / UNVERIFIED`
- `OPEN QUESTION`

## Release objective

The goal is to expose enough structure for serious technical examination while preserving the unpublished machinery that differentiates the production system.
