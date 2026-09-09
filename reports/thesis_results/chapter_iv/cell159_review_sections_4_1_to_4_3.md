# Cell 159 — Review Bab IV Subbab 4.1–4.3

## Status

PASS

## Perbaikan yang diterapkan

1. Memperjelas posisi CL01 dan CL02 sebagai dua keluarga uji independen utama.
2. Menegaskan bahwa agregasi dua keluarga bersifat deskriptif, bukan inferensial.
3. Menjelaskan bahwa MSE model merupakan MSE target Kp dan Ki terstandardisasi.
4. Menghindari implikasi kausal bahwa komponen kuantum menyebabkan penurunan kinerja.
5. Membatasi kesimpulan QLSTM pada arsitektur dan konfigurasi yang diuji.
6. Menambahkan Tabel 4.1 untuk kinerja estimasi gain.
7. Menambahkan Tabel 4.2 untuk RMSE closed-loop primer.
8. Mempertahankan negative result QLSTM tanpa penalaan ulang.
9. Tidak mengubah Subbab 4.4–4.10.

## Bukti numerik beku

LSTM standardized test MSE:
0.868628680000

QLSTM standardized test MSE:
2.963549411758

Fixed PI mean primary RMSE:
0.012478396117 Hz

LSTM-PI mean primary RMSE:
0.013809947252 Hz

QLSTM-PI mean primary RMSE:
0.016150128697 Hz

## Scientific constraints

- no statistical-significance claim
- no independent G3 generalization claim
- no post-result model/scheduler tuning
- no quantum-advantage claim
- negative QLSTM result retained
