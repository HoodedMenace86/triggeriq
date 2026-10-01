# Sports Analytics — NFL Corpus Plan

## Goal

Move from hand-picked game examples to a population-scale NFL test of the existing state-transition metric spine.

Primary corpus target:

- full 2025 NFL play-by-play
- 2026 NFL play-by-play through the current available date
- postseason included where present in the source season file

Do not hard-code a remembered game count. Count distinct `game_id` values from the ingested source and record the actual corpus size in the run receipt.

## Source

Planned bulk source: nflverse season-level play-by-play releases.

Verified release metadata observed on 2026-09-30:

- `play_by_play_2025.csv`
  - size: 97,951,481 bytes
  - upstream SHA-256: `8ce0001826f0f7b895b7a1068e4db7f43696c699db7064ccb1201855768fd06c`

- `play_by_play_2026.csv`
  - size: 16,681,238 bytes
  - upstream SHA-256: `0b085c0a3a2dc7e5e595a4d5234e16096362b82c87f6bdb01a11d8264fe00e37`

The 2026 release asset was updated on 2026-09-30, so ingestion receipts must record source timestamp/hash to make later reruns comparable.

## Core metric spine

Do not replace the seven core metrics during football adaptation:

- DQ — Decision Quality
- ΔC — Control Change
- PC — Pressure Conversion
- SPR — State Preservation Rate
- FP — Failure Propagation
- RV — Recovery Velocity
- RT — Recovery Time

## NFL variants to test

### DQ

- DQ-Macro: fourth-down, punt, field-goal, two-point, timeout, spike/kneel decisions
- DQ-State: decision outcome conditioned on score, field position, down, distance, clock, timeouts, and pre-play EP/WP where available

### ΔC

Treat control as a vector before considering scalar compression:

```text
ΔC = [ΔEP, ΔWP, ΔField, ΔSeries]
```

Candidate variants:

- ΔC-Field
- ΔC-Transfer
- ΔC-Series

### PC

- PC-4D
- PC-RZ
- PC-2M
- PC-TO

### SPR

- SPR-Lead
- SPR-Drive
- SPR-Series

### FP

Base concept:

```text
P(failure at t+k | failure at t) - baseline failure rate
```

Shock-conditioned variants:

- turnover
- sack
- penalty
- failed fourth down
- explosive play allowed
- missed kick

### RV

- RV-Play
- RV-Drive

### RT

- RT-Play
- RT-Possession

Unrecovered cases must remain right-censored rather than assigned an artificial recovery time.

## Required derived state

At minimum, preserve:

- game_id
- play_id
- possession_team
- defensive_team
- quarter
- game_seconds_remaining
- down
- yards_to_go
- yardline / field position
- score differential
- timeouts
- drive / series identity where recoverable
- EPA
- WP / WPA where available
- turnover markers
- sack markers
- penalty markers
- fourth-down decisions
- scoring state
- red-zone state
- two-minute state

## Ingestion checks

A corpus run should fail closed if any of these are unresolved:

- duplicate play identity
- non-monotonic play ordering within game
- impossible down/distance values after normalization
- missing game identity
- team identity corruption
- duplicated games across season sources
- source hash mismatch
- silent row drops
- silent null coercion in required state fields

## Required run receipt

Each corpus execution should emit:

- source filenames
- source SHA-256 values
- ingestion timestamp
- distinct game count
- row count
- rows accepted
- rows quarantined
- rows rejected
- null-rate report for required fields
- metric version
- variant version
- code commit
- output hash

## Validation sequence

1. Ingest full 2025.
2. Reproduce raw game counts and play counts.
3. Run base seven metrics.
4. Add NFL variants without altering base definitions.
5. Compare team-season distributions.
6. Run sensitivity tests against alternative shock/recovery thresholds.
7. Add 2026-to-date as out-of-sample continuation.
8. Only then test whether any metric adds predictive or explanatory value beyond standard EPA/WP/drive statistics.

## BetShield relationship

BetShield should remain a helper/decision-support layer, not a gambling engine.

If these metrics later feed BetShield, the first use should be:

- uncertainty-aware context;
- matchup/state characterization;
- model calibration checks;
- identifying where conventional aggregate statistics hide state-transition behavior.

Do not convert exploratory metric effects into betting claims without proper out-of-sample validation and calibration.
