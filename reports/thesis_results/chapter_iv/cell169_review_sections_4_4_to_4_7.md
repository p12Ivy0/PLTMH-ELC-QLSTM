# Cell 169 — Review Bab IV Subbab 4.4–4.7

## Status

**PASS**

## Catatan audit

Cell 169 pertama berhenti pada pemeriksaan frasa karena audit menggunakan
substring dengan spasi literal, sedangkan Markdown memecah beberapa frasa
antarlines. Cell 169-FIX menormalisasi whitespace untuk audit tersebut.

Tidak ada perubahan substansi ilmiah akibat perbaikan audit ini.

## Ruang lingkup

Review dilakukan hanya pada:

- 4.4 Respons Closed-Loop pada CL01 (D40_L-20)
- 4.5 Respons Closed-Loop pada CL02 (D20_L+10)
- 4.6 Pengaruh Penjadwalan Gain terhadap Respons Dinamik
- 4.7 Beban Komputasi

Subbab 4.1–4.3 dan 4.8–4.10 tidak diubah.

## Perbaikan utama

1. Persentase improvement negatif dinyatakan sebagai kenaikan RMSE agar arah
   perubahan kinerja tidak ambigu.
2. Simpangan puncak primer dinyatakan terjadi pada t = 2,60 s, yaitu tidak
   lebih lambat daripada pembaruan gain adaptif pertama.
3. RoCoF maksimum tetap terjadi pada t = 2,50 s sebelum pembaruan adaptif.
4. Aktivitas clipping, gain, dan duty variation diperlakukan sebagai bukti
   deskriptif dan tidak sebagai hubungan sebab-akibat tunggal.
5. Beban komputasi dibatasi sebagai overhead implementasi CPU/PennyLane,
   bukan isolated quantum inference latency atau quantum speedup.
6. Nomor Gambar 4.2–4.8 disusun menurut urutan pertama kemunculannya.
7. Tidak ada klaim signifikansi statistik, quantum advantage, generalisasi G3
   independen, maupun keunggulan QLSTM.

## Integrity

- Frozen primary results valid: True
- Frozen timing contract valid: True
- Control-effort contract valid: True
- Computational contract valid: True
- Scientific freeze valid: True
- Causal restraint audit valid: True
- Sections 4.1–4.3 unchanged: True
- Sections 4.8–4.10 unchanged: True
- Figure numbering sequential: True
- Unsupported claims: []

## SHA256

- Draft before: `edd37a5221893a126ba71b313d1bf0c483897ba242f5d4c14278ee7bb2dadc3b`
- Draft after: `b128d6c170a6f4c538e6d691b73c7a79fff18d4116b2fc0512e3363e26bffa76`
- Sections 4.4–4.7 before: `dc4f5a787dd4f0d4c961f718b715c6861a6c061106b27403fc4c7256df0c82a0`
- Sections 4.4–4.7 after: `f095ed510ffaf5a6e351882c39e7e3f3732b9c648a990ea587854b642185de0f`

## Scientific policy

The negative QLSTM result remains unchanged.

No simulation, training, model inference, scheduler retuning, scenario change,
simulator modification, or post-result tuning was performed.
