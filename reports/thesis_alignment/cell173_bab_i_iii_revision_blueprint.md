# Cell 173 — Exact Bab I–III Revision Blueprint

## Status

**PASS — REVISION BLUEPRINT READY**

Bab V remains blocked until the revisions below are completed.

## Revision sequence

1. **Bab I** — Research questions, objectives and scope must be neutral and consistent with the actual experiment.

2. **Bab II** — Conceptual framework and evaluation terminology must match the method actually implemented.

3. **Bab III** — Methodology must describe the realized dataset, scheduler, split, scenarios and analysis.

4. **Abstract** — Abstract must be rewritten only after Bab I–III and Bab IV are scientifically aligned.

5. **Bab I–IV cross-audit** — Verify all revised claims before unlocking Bab V.

## Exact revision items

### 1. Abstract — Abstract

**Priority:** CRITICAL

**Topic:** Prospective QLSTM added-value claim

**Current problem**

Proposal-style wording expects added value or superiority of QLSTM over classical LSTM.

**Required revision**

Convert prospective language into actual-result language. State that QLSTM was evaluated but its superiority was not supported by the frozen results.

**Replacement core**

Hasil menunjukkan bahwa QLSTM dapat diintegrasikan sebagai penjadwal gain PI, tetapi pada konfigurasi yang diuji belum menghasilkan akurasi estimasi gain maupun kinerja closed-loop primer yang lebih baik daripada LSTM.

**Evidence basis:** Cell156 + reviewed Bab IV

### 2. Bab I — 1.1 Latar Belakang

**Priority:** HIGH

**Topic:** Input features and prospective superiority

**Current problem**

Earlier conceptual text may describe a different feature vector and may imply expected QLSTM benefit.

**Required revision**

Use the final four-feature temporal input and keep motivation neutral regarding eventual superiority.

**Replacement core**

Informasi temporal yang digunakan terdiri atas deviasi frekuensi, daya mekanik, daya elektrik, dan daya dump load. QLSTM dievaluasi sebagai penjadwal gain adaptif, bukan diasumsikan sejak awal pasti lebih unggul.

**Evidence basis:** Final dataset metadata

### 3. Bab I — 1.2 Rumusan Masalah — butir 4

**Priority:** CRITICAL

**Topic:** Presupposition that QLSTM improves performance

**Current problem**

Wording 'sejauh mana meningkatkan' presupposes that improvement exists.

**Required revision**

Change to a neutral comparative research question.

**Replacement core**

Bagaimana kinerja ELC dengan penjadwalan gain PI berbasis QLSTM dibandingkan dengan PI gain tetap dan LSTM–PI pada skenario evaluasi yang telah ditetapkan?

**Evidence basis:** Cell155/156 primary results

### 4. Bab I — 1.3 Tujuan Penelitian — butir 4

**Priority:** CRITICAL

**Topic:** Paired significance testing in research objective

**Current problem**

Objective still includes paired inferential statistical testing.

**Required revision**

Replace inferential testing with descriptive family-level closed-loop comparison.

**Replacement core**

Membandingkan kinerja PI gain tetap, LSTM–PI, dan QLSTM–PI secara deskriptif berdasarkan RMSE deviasi frekuensi pada keluarga dinamik uji independen, disertai indikator dinamik dan beban komputasi.

**Evidence basis:** Cell152 preregistration

### 5. Bab I — 1.5 Batasan Penelitian

**Priority:** CRITICAL

**Topic:** Dataset split, scenario scope, gain envelope, G3

**Current problem**

Earlier scope may use scenario-ratio split, multi-step/random closed-loop claims, universal safe-gain language, and insufficient G3 caveat.

**Required revision**

State the actual family-held-out split, deterministic closed-loop scope, admissible gain envelope, and G3 generalization limitation.

**Replacement core**

Data dibagi berdasarkan keluarga dinamik untuk mencegah kebocoran antar kondisi, dengan 7 keluarga pelatihan, 2 validasi, dan 2 pengujian. Evaluasi closed-loop akhir menggunakan empat skenario deterministik yang telah ditetapkan. Rentang Kp–Ki diposisikan sebagai rentang gain admissible hasil label final, bukan jaminan stabilitas universal. Regime G3 tidak memiliki keluarga uji independen.

**Evidence basis:** Dataset metadata + Cell151/152

### 6. Bab II — 2.8 Mekanisme Penjadwalan Gain

**Priority:** CRITICAL

**Topic:** Exponential smoothing

**Current problem**

Conceptual methodology includes exponential smoothing of predicted gains.

**Required revision**

Remove exponential smoothing from the realized method. Replace it with the actual frozen processing order: inverse scaling → finite check → clipping → gain-rate limiting → applied gain.

**Replacement core**

Gain hasil estimasi dikembalikan ke skala fisik, diperiksa keterhinggaannya, dibatasi pada rentang admissible, kemudian dilewatkan melalui pembatas laju perubahan sebelum diaplikasikan ke PI.

**Evidence basis:** Cell151 frozen scheduler policy

### 7. Bab II — 2.9 Indikator Kinerja

**Priority:** HIGH

**Topic:** Final primary metric

**Current problem**

Earlier conceptual indicators may make IAE/ITAE or several metrics appear equally primary.

**Required revision**

Identify frequency-deviation RMSE as the frozen primary closed-loop metric. Peak deviation, RoCoF, settling, control effort and computational burden remain supporting diagnostics.

**Replacement core**

Metrik primer evaluasi closed-loop adalah RMSE deviasi frekuensi pada interval pascagangguan. Simpangan puncak, RoCoF, waktu tunak, aktivitas dump load, perilaku gain, dan beban komputasi digunakan sebagai indikator pendukung.

**Evidence basis:** Cell152 metric freeze

### 8. Bab II — 2.11 Hipotesis / Kerangka Pengujian

**Priority:** CRITICAL

**Topic:** Formal inferential hypotheses

**Current problem**

Formal H0/H1 may imply statistical hypothesis testing that was not performed.

**Required revision**

Reframe as evaluative propositions/research comparisons, or explicitly state that inferential hypotheses were not tested because only two independent primary families were available.

**Replacement core**

Perbandingan ketiga konfigurasi dilakukan secara deskriptif pada tingkat keluarga dinamik. Penelitian tidak menarik kesimpulan signifikansi statistik karena jumlah unit evaluasi primer independen hanya dua keluarga.

**Evidence basis:** Cell152 analysis policy

### 9. Bab II / Bab III — Generalisasi Regime G3

**Priority:** CRITICAL

**Topic:** Independent G3 generalization

**Current problem**

Wording may imply validation/test generalization for G3.

**Required revision**

State explicitly that independently held-out generalization is demonstrated only for the test families belonging to G1/G2; CL04/G3 is an in-distribution diagnostic.

**Replacement core**

Regime G3 tidak memiliki keluarga pengujian independen pada pembagian data akhir. Evaluasi CL04 hanya digunakan sebagai diagnostik dalam distribusi dan tidak menjadi bukti generalisasi G3.

**Evidence basis:** Dataset metadata + Cell156

### 10. Bab III — 3.4 Rentang Gain

**Priority:** HIGH

**Topic:** Safe/stable gain range wording

**Current problem**

The gain envelope may be described as universally safe or stable.

**Required revision**

Use the exact frozen interpretation: finalized supervised-label admissible envelope, not universal physical stability guarantee.

**Replacement core**

Rentang gain yang digunakan adalah Kp = [2,16; 3,36] dan Ki = [3,0368; 14,144]. Rentang tersebut merupakan envelope admissible yang diturunkan dari label supervised final dan tidak ditafsirkan sebagai jaminan stabilitas fisik universal.

**Evidence basis:** Cell151 admissible gain envelope

### 11. Bab III — 3.5 Skenario Evaluasi

**Priority:** CRITICAL

**Topic:** Actual closed-loop scenario design

**Current problem**

Earlier methodology may state multi-step/random closed-loop disturbances as realized evaluation.

**Required revision**

Describe the actual final stage: four predefined deterministic scenarios and three controllers.

**Replacement core**

Evaluasi closed-loop akhir terdiri atas empat skenario deterministik yang ditetapkan sebelum hasil diketahui. Masing-masing diuji menggunakan PI gain tetap, LSTM–PI, dan QLSTM–PI sehingga diperoleh 12 run.

**Evidence basis:** Cell152 preregistration

### 12. Bab III — 3.7 Pembentukan Dataset dan Split

**Priority:** CRITICAL

**Topic:** Final feature vector and leakage-free split

**Current problem**

Earlier method uses another feature list and 70:15:15 scenario-count split.

**Required revision**

Replace with final four-feature vector and exact dynamic-family group split.

**Replacement core**

Setiap window menggunakan empat fitur, yaitu deviasi frekuensi, daya mekanik, daya elektrik, dan daya dump load. Dataset akhir berisi 17.600 window dengan 11 titik per window. Split dilakukan berdasarkan keluarga dinamik: 7 keluarga train, 2 validasi, dan 2 test, menghasilkan 11.200/3.200/3.200 window tanpa family leakage dan scenario leakage.

**Evidence basis:** Final dataset metadata

### 13. Bab III — 3.9 Integrasi Scheduler ke PI

**Priority:** CRITICAL

**Topic:** Actual gain-processing chain

**Current problem**

Old method contains exponential smoothing.

**Required revision**

Replace with frozen gain guard and rate-limit chain.

**Replacement core**

Window pengamatan distandardisasi menggunakan scaler data train dan diproses oleh model beku. Prediksi Kp dan Ki kemudian diinvers-skala, diperiksa keterhinggaannya, di-clipping pada envelope admissible, dibatasi laju perubahannya, dan selanjutnya diaplikasikan ke pengendali PI. Tidak digunakan exponential smoothing.

**Evidence basis:** Cell151 scheduler contract

### 14. Bab III — 3.10 Analisis Data dan Statistik

**Priority:** CRITICAL

**Topic:** Descriptive rather than inferential primary analysis

**Current problem**

Old plan includes paired t-test/Wilcoxon, p-value, 95% CI, effect size and multiple-comparison correction.

**Required revision**

Replace with descriptive family-level comparison. State explicitly why inferential significance testing is not performed.

**Replacement core**

Analisis primer dilakukan pada tingkat keluarga dinamik independen menggunakan RMSE deviasi frekuensi. Karena hanya tersedia dua keluarga uji primer independen, penelitian tidak melakukan paired t-test, Wilcoxon, maupun klaim signifikansi statistik. Hasil dilaporkan secara deskriptif per keluarga dan melalui rerata tidak berbobot.

**Evidence basis:** Cell152/156

### 15. Bab III — 3.10 Analisis Sensitivitas

**Priority:** HIGH

**Topic:** Unrealized sensitivity sweep

**Current problem**

Planned sensitivity tests over window length, update interval, smoothing factor, qubits and VQC depth were not part of the final frozen results.

**Required revision**

Remove from realized methodology or state clearly that it was not performed and move it to future work.

**Replacement core**

Analisis sensitivitas multi-parameter tidak menjadi bagian dari evaluasi akhir penelitian ini. Pengujiannya ditempatkan sebagai rekomendasi penelitian selanjutnya.

**Evidence basis:** Final result package

### 16. Bab III / Bab V — Monte Carlo / Analisis Ketidakpastian

**Priority:** CRITICAL

**Topic:** Monte Carlo 50 run

**Current problem**

If the current Bab I–III still states Monte Carlo 50-run analysis as a realized method, that statement does not match the frozen final experiment.

**Required revision**

Do not claim Monte Carlo was performed. State that the final primary evaluation is deterministic. Move Monte Carlo uncertainty analysis to future work.

**Replacement core**

Evaluasi closed-loop akhir dilakukan secara deterministik pada empat skenario yang telah ditetapkan, masing-masing dengan tiga konfigurasi pengendali, sehingga diperoleh 12 run. Simulasi Monte Carlo tidak menjadi bagian dari tahap evaluasi primer karena model yang dibekukan bersifat deterministik dan penelitian ini tidak menetapkan distribusi probabilistik ketidakpastian plant maupun gangguan. Analisis Monte Carlo dapat dikembangkan pada penelitian selanjutnya dengan distribusi ketidakpastian yang ditetapkan sebelum eksperimen.

**Evidence basis:** Cell152: NOT_PART_OF_THIS_DETERMINISTIC_PRIMARY_STAGE

## Monte Carlo clarification

Monte Carlo 50-run simulation is not part of the frozen deterministic primary evaluation.

The final closed-loop experiment consists of four predefined deterministic scenarios evaluated using three controllers, giving 12 runs.

Monte Carlo is therefore not described as a completed Bab IV experiment. If it remains in Bab I–III as a realized method, it must be removed or moved to future work.

## Scientific freeze

- QLSTM superiority supported: **False**
- Statistical significance claim: **False**
- Independent G3 generalization: **False**
- Monte Carlo primary evaluation: **False**
- Post-result tuning: **False**
- Negative QLSTM result retained: **True**

## Bab V gate

**BAB V DRAFTING: BLOCKED**

Bab V may be drafted only after Bab I–III has been revised and the revised Bab I–IV alignment has passed.