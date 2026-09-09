# Cell 170 — Review Bab IV Subbab 4.8–4.10

## Status

**PASS**

## Ruang lingkup

Review dilakukan hanya pada:

- 4.8 Sintesis Hasil dan Posisi QLSTM
- 4.9 Keterbatasan Hasil
- 4.10 Ringkasan Bab

Subbab 4.1–4.7 tidak diubah.

## Perbaikan utama

1. Kinerja tingkat-model dan tingkat-closed-loop dipisahkan secara eksplisit.
2. Kenaikan MSE gain QLSTM sebesar 241,18% terhadap LSTM tidak ditafsirkan
   sebagai degradasi closed-loop yang proporsional.
3. Fakta bahwa LSTM–PI memiliki RMSE lebih rendah daripada QLSTM–PI pada
   empat dari empat skenario dipertahankan dengan pembatasan bahwa hanya
   CL01 dan CL02 merupakan keluarga uji independen primer.
4. CL03 tetap ditempatkan sebagai boundary stress.
5. CL04 tetap ditempatkan sebagai diagnostik G3 dalam distribusi pelatihan
   dan tidak menjadi bukti generalisasi G3 independen.
6. Keterbatasan statistik mempertahankan dua keluarga independen sebagai
   unit primer dan tidak memperlakukan titik RK4/window sebagai replikasi.
7. Keterbatasan plant tetap mencakup averaged ELC, daya mekanik konstan,
   serta tidak diaktifkannya governor dan waterway.
8. Wording timing diperbaiki: RoCoF maksimum terjadi pada 2,50 s, sedangkan
   simpangan puncak primer terjadi pada 2,60 s, yaitu tidak lebih lambat
   daripada pembaruan adaptif pertama.
9. Beban komputasi QLSTM dibatasi pada implementasi CPU/PennyLane dan tidak
   digunakan sebagai klaim quantum speedup.
10. Hasil negatif QLSTM dipertahankan tanpa post-result tuning.

## Frozen model/control evidence

- LSTM gain-test MSE: 0.868628680000
- QLSTM gain-test MSE: 2.963549411758
- QLSTM gain-MSE increase vs LSTM: 241.175634651891%
- QLSTM primary closed-loop RMSE increase vs LSTM:
  16.945621886292%

## Secondary scenarios

### CL03 — boundary stress

- Fixed PI RMSE: 0.059776619767454 Hz
- LSTM–PI RMSE: 0.059768281505451 Hz
- QLSTM–PI RMSE: 0.060130993264313 Hz
- Primary claim: False

### CL04 — G3 in-distribution diagnostic

- Fixed PI RMSE: 0.016637861488701 Hz
- LSTM–PI RMSE: 0.015532183044927 Hz
- QLSTM–PI RMSE: 0.015832587706501 Hz
- LSTM improvement vs Fixed: 6.645556248469%
- QLSTM improvement vs Fixed: 4.840007730243%
- Independent G3 generalization: False

## Integrity

- Sections 4.1–4.7 unchanged: True
- Scientific claim freeze valid: True
- Model/control contract valid: True
- Secondary-scenario contract valid: True
- LSTM lower than QLSTM in 4/4 predefined scenarios:
  True
- Timing scope valid: True
- Computational scope valid: True
- Unsupported claims: []

## SHA256

- Draft before: `b128d6c170a6f4c538e6d691b73c7a79fff18d4116b2fc0512e3363e26bffa76`
- Draft after: `366c9f0ee5ec73e290876beef6e9dc6f5fd47bb4341f29902123c5efe63238e1`
- Sections 4.8–4.10 before: `58faf97aaf11c224eb5ded8b3505296f5e216991317dc1e84d665631bbc4cf90`
- Sections 4.8–4.10 after: `f057e61995def080b5b4e4c4dfe00d0e8ae2c937ab24321aa67c5e673971b649`

## Scientific policy

No simulation, training, model inference, scheduler retuning, scenario change,
simulator modification, significance testing, or post-result tuning was
performed.

The negative QLSTM result remains authoritative.
