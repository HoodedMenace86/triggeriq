# LazyBotz Master System — public architecture guide

**Status: research and development.** This is a **sanitized orientation**, not a code release of the private Master System, a certification, or proof that every component is integrated. TriggerIQ is one public, scoped implementation.

## The engineering problem

AI and automation can produce plausible answers or actions before their evidence, permissions, timing, and persistence requirements have been checked. The LazyBotz architecture explores deterministic control boundaries around otherwise fallible or probabilistic components: keep observations distinct from decisions; decisions distinct from effects; and effects distinct from committed evidence.

The design priorities are **freedom over control**, **human–machine integration**, **privacy**, and **resource allocation**.

## Responsibility map

| Layer / research lane | Role | Boundary |
| --- | --- | --- |
| **TriggerIQ** | Observe, check provenance, score a defined GitHub security posture sample, and produce evidence-backed triggers | Unknown stays unknown; an observation is not permission |
| **MELLA** | Governed decision and routing contracts | Private implementation; public TriggerIQ integration currently **HOLD** |
| **Control Spine** | Orchestrate governed work, executor effects, custody and replay | Active private validation; **not** a completed, production-integrated runtime |
| **Tallyman / receipts** | Intended committed-result custody and traceability | Do not treat uncommitted proposals or missing receipts as results |
| **Ten Realms temporal architecture / Haru** | Explore independently operating logical clocks and guarded cross-domain handoffs | Time does not authorize; Haru handoffs are not governance decisions |
| **Verification, containment, integrity workers** | Check boundaries, surface anomalies, quarantine untrusted evidence and track integrity | Worker findings do not confer authority |
| **Aether Grade** | Govern how media is visually presented using **content-affect** observations | Media content, not the viewer; end-to-end safety gates still matter |
| **BetShield and sports analytics** | Evaluate probability, calibration and context-aware sports metrics | No profit guarantee, autonomous wagering authority or universal predictive edge |
| **Ten Realms game** | Independent interactive world using clocks, routing rules and original game mechanics | Game/lore is distinct from production authorization |

Some names refer to subcomponents of the **same** control architecture, not separate products or public GitHub repositories.

## What can actually be inspected today?

The public [TriggerIQ codebase](../) provides a dependency-light scorer, deterministic scoring rules, test fixtures, a source-visible observation-review path, and explicit limitations. See [the main README](../README.md), [MELLA contract](MELLA_KERNEL_INTEGRATION_v0.1.md), and [control boundary](CONTROL_BOUNDARY.md).

That scoped code is **not** evidence that the entire Master System is publicly released, operationally integrated, or production-certified. Other work is private or in review-only candidate stages. Potential reviewers can request a controlled technical walkthrough, documentation, reproducible sanitized fixtures or access to a specifically approved private artifact.

## How claims are evaluated

1. **Implemented**: locate source code and exact revision.
2. **Tested**: identify test inputs, executed suite, environment and outcomes.
3. **Reproduced**: establish whether an independent environment and exact artifacts agree.
4. **Integrated**: verify upstream/downstream contracts, custody, authorization and failure modes.
5. **Deployed**: independently confirm the real operational environment.

A claim at one level does **not** automatically establish the next. **PASS on an isolated test does not mean system-ready.**

## Public disclosure rules

Never publish raw private kernels, parameterization, secrets, security inventories, protected proof corpora, private receipts or third-party data merely to improve a portfolio. Public demonstrations should be synthetic or explicitly cleared for release. Work-in-progress experiments should retain their `HOLD`, `DRAFT` or `UNVERIFIED` labels until the applicable gate is demonstrably closed.

For questions about the public TriggerIQ scorer, see the repository's issue and test surfaces. For the broader architecture, request a controlled technical review rather than inferring private implementation details from this guide.
