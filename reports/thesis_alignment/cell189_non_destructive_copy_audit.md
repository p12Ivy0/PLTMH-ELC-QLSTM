# Cell 189-FIX — Word-Numbered DOCX Baseline

## Status

**PASS — SOURCE STRUCTURE VERIFIED AND WORKING COPY CREATED**

## Detection correction

The source DOCX uses Word automatic multilevel numbering.

Chapter paragraph text contains only:

- PENDAHULUAN
- TINJAUAN PUSTAKA
- METODOLOGI PENELITIAN

Word supplies `BAB I`, `BAB II`, and `BAB III` through:

- `numFmt = upperRoman`
- `lvlText = BAB %1`

Section numbers are supplied through two-level numbering `%1.%2`.

The diagnostic paragraph 168 was excluded because `PENDAHULUAN`
appeared only as part of the phrase `uji pendahuluan`.

## Source

`/content/Proposal Tesis_03092026_konsep_baru.docx`

SHA256:

`3ffe05720df5aa18f33600a4308ce91e43083d1ca0d3fb290eb7eac7b40f2305`

## Working copy

`reports/thesis_integration/cell189_working_copy/Proposal_Tesis_03092026_konsep_baru_WORKING_COPY.docx`

SHA256:

`3ffe05720df5aa18f33600a4308ce91e43083d1ca0d3fb290eb7eac7b40f2305`

Byte-identical to source:

**True**

## Verified structure

- Bab I–III: True
- Sections 1.1–1.6: True
- Sections 2.1–2.11: True
- Sections 3.1–3.12: True
- Eq. (2.17) marker: True
- Eq. (2.18) marker: True
- Tables in 2.10: 1
- `Penelitian ini (2026)` rows: 1
- 2.11 = Hipotesis Penelitian: True

## Safety

- Original source DOCX modified: False
- Scientific text integrated: False
- Frozen Bab I–V modified: False
- Simulation/training/inference: False
- Post-result tuning: False
