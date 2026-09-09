# CELL 178 — TARGETED BAB-II REVISION PACKAGE

## 2.8 Penerapan Gain dalam Loop Kendali

Penjadwalan gain memerlukan pemisahan antara laju observasi kondisi sistem dan
laju pembaruan parameter pengendali. Dalam implementasi penelitian ini,
jendela kondisi operasi diperbarui dari observasi 20 Hz, sedangkan pasangan
gain baru diterapkan pada interval supervisori 10 Hz. Di antara dua pembaruan,
gain yang sedang berlaku dipertahankan dengan mekanisme *zero-order hold*.

Keluaran model tidak langsung diterapkan pada pengendali PI. Setelah prediksi
dikembalikan dari skala target ke satuan fisik dan lolos pemeriksaan
keterhinggaan, pasangan gain dibatasi pada *envelope* admissible. Dengan
\(\boldsymbol{\theta}_k=[K_{p,k},K_{i,k}]^\mathsf{T}\), hasil pembatasan
dinyatakan sebagai

\[
\boldsymbol{\theta}^{\mathrm{clip}}_k
=
\min\left(
\boldsymbol{\theta}^{\max},
\max\left(
\boldsymbol{\theta}^{\min},
\hat{\boldsymbol{\theta}}_k
\right)
\right),
\tag{2.22}
\]

dengan
\(\boldsymbol{\theta}^{\min}=[2{,}16,\ 3{,}0368]^\mathsf{T}\) dan
\(\boldsymbol{\theta}^{\max}=[3{,}36,\ 14{,}144]^\mathsf{T}\).
Rentang tersebut merupakan *envelope* gain admissible yang diturunkan dari
label pembelajaran final dan tidak ditafsirkan sebagai jaminan kestabilan
global untuk seluruh kondisi fisik PLTMH.

Perubahan gain selanjutnya dibatasi terhadap nilai yang sedang diterapkan.
Untuk interval pembaruan \(\Delta t_u=0{,}1\) s dan vektor batas laju
\(\mathbf{r}=[1{,}2,\ 11{,}1072]^\mathsf{T}\) per detik, gain terapan
dirumuskan sebagai

\[
\boldsymbol{\theta}_k
=
\boldsymbol{\theta}_{k-1}
+
\operatorname{clip}\left(
\boldsymbol{\theta}^{\mathrm{clip}}_k
-
\boldsymbol{\theta}_{k-1},
-\mathbf{r}\Delta t_u,
\mathbf{r}\Delta t_u
\right).
\tag{2.23}
\]

Persamaan (2.22) dan Persamaan (2.23) merepresentasikan dua perlindungan yang
berbeda. *Clipping* membatasi besar gain pada *envelope* admissible, sedangkan
*pembatasan laju* membatasi besar perubahan antarpembaruan. Penelitian ini
tidak menggunakan *exponential smoothing* sebagai tahap tambahan.

Rugh dan Shamma (2000) menekankan bahwa *gain scheduling* tidak hanya
memerlukan kualitas pengendali pada titik operasi tertentu, tetapi juga perlu
memperhatikan perpindahan antarparameter. Atas dasar tersebut, LSTM–PI dan
QLSTM–PI menggunakan aturan penerapan gain yang identik agar perbedaan respons
*closed-loop* merefleksikan perbedaan keluaran model, bukan perbedaan mekanisme
transisi gain. Jika keluaran model tidak berhingga atau tidak tersedia,
scheduler menggunakan pasangan fallback PI tetap yang telah dibekukan.


## 2.9 Indikator Kinerja dan Pengujian

Evaluasi penelitian dibedakan menjadi kinerja estimasi gain pada tingkat model
dan kinerja respons pada tingkat *closed-loop*. Pemisahan tersebut diperlukan
karena galat estimasi gain yang rendah tidak secara otomatis menghasilkan
respons frekuensi yang lebih baik setelah gain diterapkan pada pengendali PI.

Deviasi frekuensi terhadap nilai referensi dinyatakan sebagai

\[
\Delta f(t)=f(t)-f_{\mathrm{ref}}.
\tag{2.24}
\]

Metrik primer untuk perbandingan *closed-loop* adalah *root mean square error*
(RMSE) deviasi frekuensi pada interval pascagangguan,

\[
\mathrm{RMSE}_{\Delta f}
=
\sqrt{
\frac{1}{N}
\sum_{n=1}^{N}
\left(\Delta f_n\right)^2
}.
\tag{2.25}
\]

Simpangan maksimum digunakan sebagai indikator pendukung dan dinyatakan
sebagai

\[
\Delta f_{\max}
=
\max_n
\left|\Delta f_n\right|.
\tag{2.26}
\]

Perubahan relatif suatu metrik terhadap baseline dapat dituliskan sebagai

\[
\Delta M_{\%}
=
100\%
\frac{
M_{\mathrm{metode}}-M_{\mathrm{baseline}}
}{
M_{\mathrm{baseline}}
}.
\tag{2.27}
\]

Untuk metrik yang semakin baik ketika nilainya mengecil, nilai
\(\Delta M_{\%}<0\) menunjukkan penurunan terhadap baseline, sedangkan
\(\Delta M_{\%}>0\) menunjukkan peningkatan nilai metrik dan tidak boleh
secara otomatis disebut sebagai perbaikan kinerja.

Selain RMSE, interpretasi respons menggunakan simpangan maksimum, RoCoF,
waktu tunak, aktivitas beban buangan, lintasan gain, dan beban komputasi
sebagai bukti pendukung. Pada tingkat model, kualitas estimasi dianalisis
menggunakan kesalahan pada data uji, termasuk MSE terstandarisasi serta RMSE
\(K_p\) dan \(K_i\). Kinerja tingkat model dan tingkat kendali dilaporkan
secara terpisah.

Evaluasi primer *closed-loop* menggunakan dua keluarga dinamik uji independen.
Karena jumlah unit evaluasi primer independen hanya dua keluarga, hasil tidak
digunakan untuk melakukan *paired t-test*, Wilcoxon *signed-rank test*, atau
klaim signifikansi statistik. Perbandingan utama bersifat deskriptif pada
tingkat keluarga dinamik, sedangkan skenario tambahan hanya digunakan sesuai
peran diagnostiknya. Dengan demikian, banyaknya titik waktu hasil integrasi
numerik tidak diperlakukan sebagai replikasi statistik independen.


### Pengganti paragraf penutup Subbab 2.10

Kajian LSTM dan QLSTM menunjukkan bahwa kedua arsitektur dapat digunakan untuk
pemodelan data sekuensial, tetapi literatur tersebut tidak dengan sendirinya
membuktikan bahwa penambahan komponen kuantum akan menghasilkan kinerja yang
lebih baik pada penjadwalan gain ELC PLTMH. Karena itu, LSTM ditempatkan
sebagai pembanding klasik dengan target, data, dan mekanisme penerapan gain
yang sebanding.

Posisi penelitian ini terletak pada integrasi jendela temporal kondisi operasi,
pembentukan target gain berbasis simulasi, serta penggunaan QLSTM sebagai
penjadwal gain PI pada tingkat supervisori. Target \(K_p^*\) dan \(K_i^*\)
dibentuk secara luring melalui pencarian grid bertahap, sedangkan pada tahap
*closed-loop* keluaran model dikembalikan ke skala fisik, diperiksa
keterhinggaannya, dibatasi pada *envelope* gain admissible, dan dikenai
pembatasan laju perubahan sebelum diterapkan pada PI. Mekanisme tersebut
digunakan secara identik pada LSTM–PI dan QLSTM–PI.

Evaluasi kemampuan generalisasi primer dibatasi pada dua keluarga dinamik uji
independen dari regime G1 dan G2. Regime G3 tidak mempunyai keluarga uji
independen pada pembagian data akhir; karena itu, evaluasi G3 hanya diposisikan
sebagai diagnostik dalam distribusi dan bukan sebagai bukti generalisasi G3.
Posisi penelitian juga dibatasi pada simulasi numerik berbasis CPU dan
simulator kuantum PennyLane. Hasil tersebut tidak ditafsirkan sebagai bukti
*quantum speedup*, *quantum advantage*, atau implementasi perangkat keras
kuantum.


## 2.11 Kerangka Evaluasi Penelitian

Penelitian ini tidak menetapkan hipotesis inferensial yang mengharuskan
QLSTM–PI lebih unggul daripada PI gain tetap atau LSTM–PI. QLSTM diperlakukan
sebagai metode yang diuji secara empiris sehingga hasil yang setara maupun
lebih rendah daripada pembanding tetap merupakan hasil penelitian yang sah.

Evaluasi dilakukan pada dua tingkat. Tingkat pertama menilai kemampuan model
dalam mengestimasi pasangan gain \(K_p\) dan \(K_i\) pada data pengujian.
LSTM dan QLSTM dibandingkan menggunakan ukuran galat estimasi serta baseline
model yang telah ditetapkan. Hasil pada tingkat ini digunakan untuk memahami
kemampuan model mempelajari pemetaan kondisi temporal menuju target gain,
tetapi tidak digunakan sebagai satu-satunya dasar untuk menyimpulkan kinerja
pengendalian.

Tingkat kedua menilai respons *closed-loop* PI gain tetap, LSTM–PI, dan
QLSTM–PI. Klaim primer dibatasi pada dua keluarga dinamik uji independen,
sedangkan skenario *boundary stress* dan diagnostik G3 digunakan sebagai bukti
sekunder sesuai ruang lingkupnya. RMSE deviasi frekuensi menjadi metrik primer,
dengan respons dinamik, aktivitas kendali, lintasan gain, dan beban komputasi
sebagai indikator pendukung.

Karena hanya tersedia dua keluarga primer independen, penelitian tidak
melakukan pengujian signifikansi statistik antar-konfigurasi pengendali.
Kesimpulan ditarik secara deskriptif berdasarkan arah dan besar perbedaan
kinerja pada unit evaluasi yang benar-benar independen. Pendekatan ini juga
mencegah ribuan titik waktu hasil integrasi numerik diperlakukan secara keliru
sebagai replikasi eksperimen independen.

Kerangka evaluasi tersebut mempertahankan prinsip falsifiabilitas penelitian.
Apabila QLSTM–PI tidak lebih baik daripada LSTM–PI atau PI gain tetap pada
konfigurasi yang diuji, hasil tersebut dipertahankan tanpa penalaan ulang
pascahasil, pergantian skenario primer, atau perubahan aturan scheduler.
