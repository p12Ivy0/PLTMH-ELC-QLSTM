# Cell 172 — Bab I–IV Thesis Alignment Audit

## Status

**AUDIT PASS — BAB I–III REVISION REQUIRED**

This status means the alignment audit executed successfully. It does **not**
mean that the current proposal text is already aligned with the completed
research.

## Proposal source reviewed

`Proposal Tesis_03092026_konsep_baru.docx`

Because the proposal DOCX is not stored in this Git repository, Cell 172
preserves a semantic snapshot of the proposal statements used by this audit.

## Final frozen implementation

- Input features: `['frequency_deviation_hz', 'mechanical_power_kw', 'electrical_power_kw', 'dump_power_kw']`
- Sequence length: 11 observations
- Observation rate: 20.0 Hz
- Split: `LEAKAGE_FREE_DYNAMIC_FAMILY_GROUP_SPLIT`
- Train/validation/test families:
  7/
  2/
  2
- Closed-loop deterministic runs:
  12
- Independent primary families:
  2
- Primary metric:
  `frequency_deviation_rmse_hz`
- Family-level significance test: False
- QLSTM superiority supported: False
- Independent G3 generalization supported: False

## Alignment result

- Total audited items: 20
- Aligned: 7
- Retain with scope: 1
- Revision required: 12

## Principal revisions required before Bab V

1. Neutralize research-question wording that presupposes QLSTM improvement.
2. Remove paired significance testing from the realized research objective.
3. Replace the old model-input feature list with the final four features.
4. Replace 70:15:15 scenario wording with the actual dynamic-family split.
5. Replace exponential smoothing with the actual clipping + rate-limit policy.
6. Restrict final closed-loop scope to the predefined deterministic scenarios
   actually evaluated.
7. Align the analysis metrics with frequency-deviation RMSE as the primary
   metric and the frozen secondary diagnostics.
8. Remove or explicitly mark the planned paired t-test/Wilcoxon procedure as
   not performed because only two independent primary families are available.
9. Move the unrealized sensitivity sweep to future work.
10. Replace universal 'safe/stable gain range' wording with the frozen
    admissible gain-envelope interpretation.
11. Convert prospective Abstract wording into actual-result wording.
12. Add the G3 generalization limitation explicitly.

## Bab IV status

Bab IV remains fully reviewed and unchanged.

SHA256:

`366c9f0ee5ec73e290876beef6e9dc6f5fd47bb4341f29902123c5efe63238e1`

## Bab V gate

**Bab V drafting remains blocked until Bab I–III alignment revisions are
prepared and reviewed.**

No simulation, training, inference, scheduler tuning, or scientific result
modification was performed by Cell 172.
