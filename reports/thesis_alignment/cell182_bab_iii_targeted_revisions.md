# CELL 182 — TARGETED BAB-III REVISION PACKAGE

## 3.4 Perancangan PI Baseline dan Rentang Gain

Konfigurasi PI gain tetap digunakan sebagai pembanding utama sekaligus nilai
fallback bagi kedua scheduler adaptif. Pasangan yang dibekukan pada tahap
akhir penelitian adalah \(K_p=2{,}16\) dan \(K_i=5{,}72\). Pasangan tersebut
digunakan secara identik ketika model adaptif belum diaktifkan atau ketika
inferensi menghasilkan keluaran yang tidak dapat diterapkan.

Rentang gain untuk keluaran scheduler mengikuti *envelope* gain
*admissible* final,

\[
2{,}16 \leq K_p \leq 3{,}36,
\qquad
3{,}0368 \leq K_i \leq 14{,}144.
\]

Rentang tersebut diturunkan dari *envelope* label supervised yang telah
difinalkan sebelum pengujian *closed-loop*. Oleh karena itu, istilah
*admissible* digunakan untuk menunjukkan batas operasional yang diterapkan
dalam eksperimen, bukan sebagai jaminan kestabilan fisik universal untuk
seluruh kemungkinan kondisi PLTMH.

Kebijakan batas gain yang sama digunakan pada LSTM–PI dan QLSTM–PI.
Pemilihan batas, pasangan fallback, serta pembatas laju perubahan gain tidak
diubah setelah hasil pengujian *closed-loop* diketahui.


## 3.5 Penyusunan Skenario Operasi

Evaluasi *closed-loop* akhir menggunakan empat skenario deterministik yang
ditetapkan sebelum hasil pengujian diketahui. Setiap skenario dijalankan
menggunakan tiga konfigurasi pengendali, yaitu PI gain tetap, LSTM–PI, dan
QLSTM–PI, sehingga keseluruhan tahap evaluasi menghasilkan 12 *run*
deterministik.

CL01 dan CL02 merupakan skenario primer pada dua keluarga dinamik uji
independen, yaitu D40_L-20 dan D20_L+10. Kedua keluarga tersebut digunakan
sebagai unit utama untuk membandingkan ketiga konfigurasi pengendali. CL03
diposisikan sebagai *boundary stress* dan dilaporkan terpisah dari klaim
primer. CL04 digunakan sebagai diagnostik dalam distribusi untuk regime G3.
Karena G3 tidak mempunyai keluarga uji independen pada pembagian data final,
CL04 tidak digunakan sebagai bukti generalisasi independen terhadap G3.

Gangguan *closed-loop* diterapkan pada \(t=2{,}5\) s. Scheduler adaptif baru
diizinkan melakukan pembaruan gain pertama pada \(t=2{,}6\) s, sedangkan
sebelum pembaruan tersebut sistem menggunakan PI gain tetap. Rancangan ini
dibekukan sebelum hasil respons ketiga pengendali diketahui.

Tahap evaluasi primer tidak menggunakan gangguan *multi-step*, variasi acak,
atau pengulangan stokastik sebagai sumber bukti utama. Simulasi Monte Carlo
juga tidak menjadi bagian dari tahap evaluasi primer karena simulator akhir
bersifat deterministik dan penelitian tidak menetapkan distribusi
probabilistik ketidakpastian plant maupun gangguan. Pengujian Monte Carlo
ditempatkan sebagai kemungkinan pengembangan penelitian selanjutnya dengan
distribusi ketidakpastian yang harus ditetapkan sebelum eksperimen.


## 3.7 Variabel dan Pembentukan Dataset

Masukan temporal LSTM dan QLSTM menggunakan empat fitur yang sama, yaitu
deviasi frekuensi, daya mekanik, daya elektrik, dan daya beban buangan.
Representasi fitur pada satu titik observasi dapat dituliskan sebagai

\[
\mathbf{x}_t =
\begin{bmatrix}
\Delta f(t) &
P_m(t) &
P_e(t) &
P_{\mathrm{dump}}(t)
\end{bmatrix}^{\mathsf T}.
\]

Setiap sampel pembelajaran berbentuk jendela dengan 11 titik observasi.
Frekuensi observasi adalah 20 Hz atau \(\Delta t_{\mathrm{obs}}=0{,}05\) s,
sehingga satu jendela mencakup rentang 0,5 s. Dataset final berisi 17.600
jendela supervised dengan target \(K_p\) dan \(K_i\).

Pemisahan data dilakukan pada tingkat keluarga dinamik, bukan melalui
pengacakan baris maupun rasio jumlah skenario. Tujuh keluarga dinamik
digunakan untuk pelatihan, dua untuk validasi, dan dua untuk pengujian.
Pembagian tersebut menghasilkan masing-masing 11.200, 3.200, dan 3.200
jendela. Tidak terdapat *family leakage* maupun *scenario leakage* antar
kelompok data.

Standardisasi fitur dan target dihitung hanya menggunakan data latih.
Parameter standardisasi yang telah dibekukan kemudian diterapkan pada data
validasi dan data uji. Dengan prosedur tersebut, informasi dari keluarga uji
tidak digunakan untuk menentukan parameter prapengolahan atau pemilihan model.

Regime gain G1, G2, dan G3 terdapat pada data pelatihan, sedangkan keluarga
validasi dan pengujian independen hanya mencakup G1 dan G2. Oleh karena itu,
klaim generalisasi *held-out* dibatasi pada keluarga G1/G2. Regime G3 tidak
mempunyai keluarga uji independen dan hanya dianalisis melalui diagnostik
dalam distribusi. Skenario *boundary stress* tidak dimasukkan ke tensor
supervised final.


## 3.9 Integrasi Gain Adaptif dalam Simulasi Closed-Loop

LSTM dan QLSTM diintegrasikan sebagai penjadwal gain pada tingkat supervisori,
sedangkan pengendali PI tetap menghasilkan sinyal kendali ELC. Kedua model
menerima jendela observasi dengan struktur, scaler, batas gain, fallback,
pembatas laju, dan frekuensi pembaruan yang sama.

Observasi kondisi sistem dilakukan pada 20 Hz. Satu pembaruan gain dilakukan
setelah dua observasi sehingga frekuensi pembaruan scheduler adalah 10 Hz atau
\(\Delta t_u=0{,}1\) s. Di antara dua pembaruan, gain terakhir dipertahankan
dengan *zero-order hold*.

Urutan pemrosesan scheduler dibekukan sebagai berikut:

1. membentuk jendela observasi mentah;
2. melakukan standardisasi fitur menggunakan scaler data latih;
3. menjalankan inferensi model beku;
4. mengembalikan keluaran dari skala target ke satuan fisik;
5. memeriksa keterhinggaan keluaran;
6. melakukan *clipping* pada *envelope* gain *admissible*;
7. membatasi laju perubahan gain; dan
8. menerapkan gain ke pengendali PI.

Laju perubahan maksimum \(K_p\) adalah 1,2 per detik atau 0,12 per pembaruan,
sedangkan laju perubahan maksimum \(K_i\) adalah 11,1072 per detik atau
1,11072 per pembaruan. Jika inferensi gagal atau menghasilkan nilai tidak
berhingga, scheduler menggunakan pasangan fallback
\(K_p=2{,}16\) dan \(K_i=5{,}72\) melalui pembatas laju yang sama.

Tidak digunakan *exponential smoothing* pada keluaran LSTM maupun QLSTM.
Seluruh aturan scheduler tersebut ditetapkan sebelum hasil *closed-loop*
diperoleh dan tidak diubah berdasarkan kinerja pengujian.


## 3.10 Metode Analisis Data

Analisis dilakukan pada tingkat model dan tingkat sistem kendali. Pada tingkat
model, galat estimasi gain pada data uji digunakan untuk mendeskripsikan
kemampuan LSTM dan QLSTM mempelajari pemetaan jendela temporal menuju target
\(K_p\) dan \(K_i\). Hasil tingkat model dilaporkan terpisah dari kinerja
*closed-loop* karena galat estimasi gain tidak diasumsikan mempunyai hubungan
proporsional langsung dengan kualitas respons frekuensi.

Pada tingkat *closed-loop*, metrik primer adalah RMSE deviasi frekuensi pada
interval pascagangguan. Analisis primer menggunakan keluarga dinamik sebagai
unit agregasi. Hasil dilaporkan untuk setiap keluarga secara individual dan
dapat diringkas menggunakan rerata keluarga tidak berbobot.

Simpangan frekuensi maksimum, RoCoF maksimum, waktu tunak, galat frekuensi
akhir, aktivitas beban buangan, variasi total duty, lintasan gain, kejadian
saturasi atau fallback, serta beban komputasi digunakan sebagai indikator
pendukung. Indikator tersebut membantu menjelaskan mekanisme respons tetapi
tidak menggantikan RMSE deviasi frekuensi sebagai metrik primer.

Jumlah keluarga dinamik uji primer independen hanya dua. Oleh karena itu,
penelitian tidak melakukan *paired t-test*, Wilcoxon *signed-rank test*,
pengujian signifikansi pada tingkat keluarga, interval kepercayaan 95%,
ukuran efek inferensial, maupun koreksi perbandingan berganda untuk
menyatakan superioritas salah satu pengendali. Titik-titik waktu hasil
integrasi numerik juga tidak diperlakukan sebagai replikasi statistik
independen.

Analisis sensitivitas multi-parameter terhadap panjang jendela, interval
pembaruan, faktor smoothing, jumlah qubit, atau kedalaman VQC tidak menjadi
bagian dari evaluasi akhir yang dibekukan. Analisis tersebut ditempatkan
sebagai rekomendasi penelitian selanjutnya dan tidak digunakan untuk
memilih kembali konfigurasi setelah hasil uji diketahui.

Simulasi Monte Carlo tidak dilakukan pada tahap evaluasi primer. Evaluasi
akhir menggunakan empat skenario deterministik dan tiga konfigurasi
pengendali sehingga menghasilkan 12 *run*. Analisis ketidakpastian stokastik
melalui Monte Carlo dapat dikembangkan pada penelitian selanjutnya setelah
distribusi probabilistik ketidakpastian plant, gangguan, atau pengukuran
ditetapkan sebelum eksperimen.

Setelah hasil pengujian tersedia, tidak dilakukan pelatihan ulang model,
pemilihan ulang skenario primer, maupun perubahan aturan scheduler.
Kesimpulan ditarik secara deskriptif berdasarkan bukti yang dihasilkan oleh
protokol yang telah dibekukan.
