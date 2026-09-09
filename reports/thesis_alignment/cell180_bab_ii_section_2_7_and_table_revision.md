# CELL 180 — BAB-II REMAINING REVISION PACKAGE

## 2.7 Arsitektur QLSTM untuk Estimasi Gain — Revisi Final

Paragraf kajian literatur dan Persamaan (2.17)–(2.18) pada naskah sumber
dipertahankan. Persamaan tersebut tetap digunakan untuk menjelaskan penggantian
transformasi affine klasik pada gerbang LSTM dengan transformasi berbasis VQC.

Pada implementasi final, QLSTM menerima urutan temporal dengan empat fitur pada
setiap titik observasi,

\[
\mathbf{x}_t =
\begin{bmatrix}
\Delta f(t) &
P_m(t) &
P_e(t) &
P_{\mathrm{dump}}(t)
\end{bmatrix}^{\mathsf T}.
\]

Urutan terdiri atas 11 titik observasi dengan frekuensi observasi 20 Hz sehingga
mencakup rentang waktu 0,5 s. Empat fitur tersebut adalah deviasi frekuensi,
daya mekanik, daya elektrik, dan daya beban buangan. Vektor masukan yang sama
digunakan pada LSTM dan QLSTM agar perbandingan kedua model tidak dipengaruhi
oleh perbedaan informasi masukan.

Arsitektur QLSTM final menggunakan empat *qubit*, kedalaman VQC satu lapisan,
dan keadaan tersembunyi berdimensi empat. Keadaan tersembunyi terakhir
diteruskan ke kepala regresi klasik dengan struktur
\(4\rightarrow64\rightarrow60\rightarrow16\rightarrow2\).
Kepala regresi menghasilkan dua keluaran pada ruang target yang telah
distandardisasi. Dengan \(\mathbf{h}_T\) sebagai keadaan tersembunyi terakhir,
keluaran regresi dinyatakan sebagai

\[
\hat{\mathbf z}
=
g_{\boldsymbol{\phi}}(\mathbf h_T)
=
\begin{bmatrix}
\hat z_{K_p}\\
\hat z_{K_i}
\end{bmatrix},
\tag{2.19}
\]

dengan \(g_{\boldsymbol{\phi}}(\cdot)\) merupakan kepala regresi klasik.
Tidak digunakan fungsi sigmoid pada kepala keluaran untuk membatasi
\(K_p\) dan \(K_i\).

Target \(K_p\) dan \(K_i\) distandardisasi menggunakan statistik data latih.
Keluaran pada Persamaan (2.19) dikembalikan ke skala fisik melalui transformasi
balik

\[
\hat{\boldsymbol{\theta}}
=
\boldsymbol{\mu}_{y}
+
\boldsymbol{\sigma}_{y}
\odot
\hat{\mathbf z}
=
\begin{bmatrix}
\hat K_p\\
\hat K_i
\end{bmatrix},
\tag{2.20}
\]

dengan \(\boldsymbol{\mu}_{y}\) dan \(\boldsymbol{\sigma}_{y}\) masing-masing
merupakan vektor rerata dan simpangan baku target yang dihitung hanya dari data
latih, sedangkan \(\odot\) menyatakan perkalian elemen per elemen. Persamaan
(2.20) menghasilkan estimasi gain dalam satuan fisik, tetapi belum merupakan
gain yang langsung diterapkan pada pengendali.

Fungsi rugi pelatihan menggunakan *mean squared error* (MSE) pada dua target
yang telah distandardisasi,

\[
\mathcal{L}_{\mathrm{MSE}}
=
\frac{1}{N d_y}
\sum_{j=1}^{N}
\left\|
\mathbf z_j
-
\hat{\mathbf z}_j
\right\|_2^2,
\qquad d_y=2,
\tag{2.21}
\]

dengan \(N\) sebagai jumlah sampel pelatihan dan \(d_y=2\) sebagai jumlah komponen target. Faktor \(1/(N d_y)\) membuat Persamaan (2.21) identik dengan *mean squared error* yang dirata-ratakan terhadap seluruh elemen target, sesuai implementasi `nn.MSELoss(reduction="mean")`. Tidak digunakan pembobot
\(w_p\) atau \(w_i\) pada fungsi rugi final karena standardisasi target telah
menempatkan kedua komponen gain pada skala pembelajaran yang sebanding.
Parameter klasik dan parameter rangkaian kuantum QLSTM dilatih bersama melalui
optimisasi gradien. Istilah optimisasi pada konteks ini merujuk pada pelatihan
parameter model dan bukan pada penggunaan QLSTM sebagai algoritma optimasi
gain.

Estimasi gain pada Persamaan (2.20) tidak secara otomatis dianggap aman untuk
diterapkan. Pada tahap *closed-loop*, keluaran tersebut diproses menggunakan
rantai scheduler yang sama bagi LSTM–PI dan QLSTM–PI: transformasi balik target,
pemeriksaan keterhinggaan, *clipping* pada *envelope* gain *admissible*,
pembatasan laju perubahan gain, dan penerapan gain. Mekanisme tersebut
dijelaskan pada Subbab 2.8 melalui Persamaan (2.22) dan Persamaan (2.23).

Dengan struktur tersebut, QLSTM berfungsi sebagai model pembelajaran temporal
untuk mengestimasi gain PI dan bukan sebagai pengendali ELC secara langsung.
Pengendali PI tetap membentuk aksi kendali terhadap ELC. Gambar 2.3 tetap
digunakan sebagai ilustrasi konseptual aliran informasi, dengan interpretasi
bahwa keluaran model harus melewati tahap inverse scaling dan kebijakan
scheduler sebelum diterapkan sebagai gain PI.


## Tabel II.1 — Baris Pengganti `Penelitian ini (2026)`

| Peneliti dan Tahun | Metode/Pendekatan | Objek Studi | Kontribusi dan Keterbatasan | Posisi terhadap Penelitian Ini |
|---|---|---|---|---|
| Penelitian ini (2026) | QLSTM sebagai penjadwal gain PI adaptif pada tingkat supervisori | ELC PLTMH 100 kW pada sistem terisolasi | QLSTM mempelajari pemetaan jendela temporal empat fitur terhadap target \(K_p\) dan \(K_i\) yang dibentuk melalui pencarian grid bertahap secara luring pada model simulasi. Keluaran model dikembalikan ke skala fisik, diperiksa keterhinggaannya, dibatasi pada *envelope* gain *admissible*, kemudian dikenai pembatasan laju perubahan sebelum diterapkan pada PI pada interval pembaruan 10 Hz. Evaluasi primer dibatasi pada dua keluarga dinamik uji independen; G3 hanya digunakan sebagai diagnostik dalam distribusi. | Mengintegrasikan pemodelan PLTMH–ELC, pembentukan target gain, pembelajaran temporal LSTM/QLSTM, dan evaluasi *closed-loop* PI gain tetap, LSTM–PI, serta QLSTM–PI dalam satu kerangka yang dapat ditelusuri. QLSTM dievaluasi secara empiris tanpa asumsi superioritas, tanpa klaim generalisasi G3 independen, dan tanpa klaim *quantum advantage*. |
