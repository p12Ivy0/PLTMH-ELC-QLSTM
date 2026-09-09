# AUTHORITATIVE BAB I–V REVISION PACKAGE

## Status

This package contains the frozen authoritative scientific text and exact
Bab-II compositional integration instructions approved before DOCX integration.

**The proposal DOCX has not been modified by Cell188-FIX2.**

---

# BAB I — AUTHORITATIVE FULL TEXT

Source:

`reports/thesis_alignment/cell176_bab_i_full_revised_candidate.md`

SHA256:

`f3177316be40a527466f1270d7f0f3acfd2694f14d39d30b1fa824abf0faff98`

# BAB I
# PENDAHULUAN

## 1.1 Latar Belakang

Pembangkit Listrik Tenaga Mikrohidro (PLTMH) berperan dalam penyediaan
listrik berbasis sumber daya lokal, terutama pada sistem terisolasi yang tidak
memperoleh dukungan jaringan interkoneksi. Khosravi et al. (2025)
menempatkan stabilitas frekuensi sebagai salah satu tantangan utama mikrogrid
terisolasi berbasis energi terbarukan. Pada konfigurasi tersebut, perubahan
daya beban harus segera diimbangi oleh pembangkitan atau perangkat pengatur
beban. Milano et al. (2018) menjelaskan bahwa rendahnya inersia sistem
mempercepat perubahan frekuensi setelah terjadi gangguan, sedangkan Fang
et al. (2019) menunjukkan bahwa ketidakseimbangan daya aktif menyebabkan
frekuensi menyimpang dari nilai nominal. Karakteristik tersebut menempatkan
stabilitas frekuensi sebagai salah satu aspek utama keandalan operasi PLTMH
terisolasi.

Pada PLTMH dengan daya mekanik turbin yang dipertahankan mendekati konstan,
*Electronic Load Controller* (ELC) menjaga keseimbangan daya dengan
mengalihkan selisih antara daya pembangkitan dan daya beban konsumen menuju
beban buangan (*dump load*). Kalla et al. (2016) menjelaskan bahwa ELC
meningkatkan penyerapan daya oleh beban buangan ketika beban konsumen
menurun. Singh et al. (2018) menunjukkan bahwa ketika beban konsumen
meningkat, daya yang dialirkan menuju beban buangan dikurangi agar total daya
listrik yang diserap tetap sesuai dengan daya yang tersedia dari generator.
Mekanisme tersebut membentuk interaksi antara turbin, generator sinkron,
beban konsumen, dan ELC dalam sistem kendali frekuensi.

Pengendali *proportional–integral* (PI) banyak digunakan pada ELC karena
strukturnya sederhana dan mampu menghilangkan galat keadaan tunak. Singh
et al. (2018) menunjukkan bahwa aksi PI pada ELC menentukan perintah
pengaturan perangkat daya berdasarkan galat frekuensi. Kinerja pengendali
ditentukan oleh gain proporsional \(K_p\) dan gain integral \(K_i\).
Salhi et al. (2014) memperlihatkan bahwa satu pasangan gain tetap belum tentu
mempertahankan kualitas respons yang sama ketika PLTMH menghadapi rentang
perubahan beban yang luas. Ndukwe et al. (2024) juga menunjukkan bahwa
pembaruan gain PI berdasarkan kondisi operasi dapat memperbaiki respons
dinamis pengendali beban. Temuan tersebut mengarahkan persoalan dari
pencarian satu pasangan gain menuju penentuan gain yang sesuai dengan kondisi
operasi sistem.

Águila-León et al. (2020) menunjukkan penggunaan GWO, PSO, dan GA untuk
mencari parameter pengendali yang meminimalkan galat pada konverter daya,
sedangkan Hosseini et al. (2024) mengidentifikasi penggunaan metaheuristik
yang luas pada aplikasi energi. Pendekatan tersebut relevan sebagai bagian
perkembangan metode penalaan parameter, tetapi tidak digunakan sebagai
mekanisme penentu gain adaptif dalam penelitian ini. Target gain penelitian
dibentuk secara luring melalui pencarian grid bertahap pada model simulasi,
sedangkan penentuan gain ketika pengendali beroperasi dilakukan oleh model
pembelajaran temporal.

Hochreiter dan Schmidhuber (1997) mengembangkan *Long Short-Term Memory*
(LSTM) untuk mempelajari dependensi pada data sekuensial melalui keadaan sel
dan mekanisme gerbang. Chen et al. (2022) kemudian memperkenalkan
*Quantum Long Short-Term Memory* (QLSTM) dengan mengintegrasikan
*variational quantum circuit* (VQC) ke dalam transformasi gerbang LSTM.
Khan et al. (2024) memperlihatkan bahwa perbandingan QLSTM dan LSTM perlu
dilakukan secara empiris pada domain dan dataset yang sebanding. Landasan
tersebut mendukung penggunaan LSTM sebagai pembanding klasik terhadap QLSTM
tanpa mengasumsikan terlebih dahulu bahwa QLSTM akan menghasilkan kinerja
yang lebih baik.

Dalam penelitian ini, QLSTM tidak diposisikan sebagai algoritma optimasi dan
tidak menggantikan pengendali PI. QLSTM berfungsi sebagai model pembelajaran
temporal yang mengestimasi \(K_p\) dan \(K_i\) dari jendela kondisi operasi.
Pengendali PI tetap membentuk sinyal kendali ELC, sedangkan QLSTM bertindak
sebagai penjadwal gain pada tingkat supervisori. Dengan struktur tersebut,
QLSTM menjadi komponen pembelajaran yang menentukan pasangan gain adaptif,
sementara struktur kendali utama ELC tetap berbasis PI.

Pembelajaran terawasi memerlukan target \(K_p^*\) dan \(K_i^*\). Target
tersebut dibentuk melalui simulasi kandidat gain dengan pencarian grid
bertahap (*coarse-to-fine grid search*) menggunakan fungsi objektif yang telah
ditetapkan. Proses pencarian hanya digunakan pada tahap pembentukan label
dataset dan tidak dijalankan di dalam *closed-loop* ketika LSTM–PI maupun
QLSTM–PI dievaluasi. Struktur ini memisahkan dengan jelas proses pembentukan
target dari proses estimasi gain adaptif.

Jendela temporal model akhir menggunakan empat fitur, yaitu deviasi frekuensi,
daya mekanik, daya elektrik, dan daya beban buangan. Pemisahan dataset
dilakukan pada tingkat keluarga dinamik, bukan melalui pengacakan baris atau
titik waktu. Pendekatan tersebut menjaga keluarga pelatihan, validasi, dan
pengujian tetap terpisah sehingga ketergantungan temporal dari keluarga yang
sama tidak tersebar ke beberapa subset data. Prinsip tersebut sejalan dengan
perhatian Bergmeir et al. (2018) terhadap risiko bias evaluasi ketika
ketergantungan temporal tidak dipertimbangkan.

Gain yang dihasilkan model tidak langsung diterapkan tanpa pembatasan.
Prediksi dikembalikan ke skala fisik, diperiksa keterhinggaannya, dibatasi
pada *envelope* gain yang telah ditetapkan, kemudian dikenai pembatasan laju
perubahan gain sebelum diaplikasikan pada PI. Mekanisme tersebut digunakan
secara identik pada LSTM–PI dan QLSTM–PI sehingga perbandingan kedua model
tidak dipengaruhi oleh perbedaan aturan penerapan gain.

Berdasarkan uraian tersebut, penelitian diarahkan pada pengembangan dan
evaluasi penjadwalan gain PI adaptif berbasis QLSTM untuk ELC PLTMH
terisolasi. Kontribusi metodologis penelitian terletak pada rantai yang dapat
ditelusuri mulai dari pembentukan target gain, pembentukan dataset temporal,
pembelajaran LSTM dan QLSTM, penerapan gain melalui mekanisme supervisori,
hingga evaluasi *closed-loop*. Perbandingan dengan PI gain tetap dan LSTM–PI
digunakan untuk menilai kinerja QLSTM–PI secara empiris tanpa menjadikan
superioritas QLSTM sebagai asumsi penelitian.


## 1.2 Perumusan Masalah

ELC dengan gain PI tetap dapat menghasilkan kualitas respons yang berbeda
ketika sistem menghadapi perubahan kondisi operasi. Penggunaan model temporal
untuk menentukan gain adaptif memerlukan sumber target gain yang dapat
ditelusuri, pemisahan data yang mencegah kebocoran, mekanisme penerapan gain
yang konsisten, serta evaluasi *closed-loop* yang memperlakukan LSTM dan QLSTM
secara sebanding. Berdasarkan permasalahan tersebut, penelitian dirumuskan
melalui pertanyaan berikut.

1. Bagaimana membangun model dinamis PLTMH terisolasi yang merepresentasikan
   interaksi turbin, generator sinkron, beban konsumen, dan ELC terhadap
   perubahan frekuensi?

2. Bagaimana membentuk target \(K_p^*\) dan \(K_i^*\) melalui pencarian grid
   bertahap berbasis simulasi untuk menyediakan label pembelajaran LSTM dan
   QLSTM tanpa menggunakan algoritma metaheuristik sebagai penentu gain
   adaptif?

3. Bagaimana mengembangkan QLSTM sebagai model pembelajaran temporal yang
   menentukan \(K_p\) dan \(K_i\) secara adaptif serta mengintegrasikan
   keluarannya ke pengendali PI melalui pembatasan gain dan pembatasan laju
   perubahan gain?

4. Bagaimana kinerja ELC dengan penjadwalan gain PI berbasis QLSTM
   dibandingkan dengan PI gain tetap dan LSTM–PI pada keluarga dinamik
   pengujian yang telah dipisahkan dari data pelatihan?


## 1.3 Tujuan Penelitian

Penelitian ini bertujuan mengembangkan dan mengevaluasi penjadwalan gain PI
adaptif berbasis QLSTM pada ELC PLTMH terisolasi serta membandingkan
kinerjanya dengan PI gain tetap dan LSTM–PI pada kondisi evaluasi yang telah
ditetapkan.

Tujuan khusus penelitian meliputi:

1. membangun dan memvalidasi model dinamis PLTMH–ELC yang
   merepresentasikan respons frekuensi akibat perubahan beban;

2. membentuk dataset temporal beserta target \(K_p^*\) dan \(K_i^*\) melalui
   pencarian grid bertahap berbasis simulasi menggunakan fungsi objektif yang
   telah ditetapkan;

3. mengembangkan LSTM dan QLSTM untuk memetakan jendela kondisi operasi
   menjadi estimasi gain PI yang diterapkan melalui mekanisme penjadwalan
   gain supervisori yang sama; dan

4. membandingkan secara deskriptif kinerja PI gain tetap, LSTM–PI, dan
   QLSTM–PI dengan RMSE deviasi frekuensi sebagai metrik primer pada
   keluarga dinamik uji independen, disertai indikator respons dinamik dan
   beban komputasi sebagai bukti pendukung.


## 1.4 Manfaat Penelitian

Penelitian ini memberikan manfaat pada aspek konseptual, metodologis, dan
praktis dalam pengembangan pengendalian frekuensi PLTMH terisolasi. Pada aspek
konseptual, penelitian memperjelas kedudukan QLSTM sebagai model pembelajaran
temporal pada tingkat supervisori yang mengestimasi gain \(K_p\) dan \(K_i\),
sedangkan pengendali PI tetap menjadi pengendali utama ELC. Struktur tersebut
memberikan kerangka yang jelas untuk membedakan fungsi model pembelajaran dari
fungsi pengendali *closed-loop*.

Pada aspek metodologis, penelitian menghasilkan alur yang dapat ditelusuri
mulai dari pembentukan target gain melalui pencarian grid bertahap, pembentukan
jendela temporal, pelatihan LSTM dan QLSTM dengan target yang sama, hingga
evaluasi ketiga konfigurasi pengendali. Pemisahan data dilakukan berdasarkan
keluarga dinamik sehingga keluarga pelatihan, validasi, dan pengujian tetap
terpisah serta tidak terjadi *family leakage* maupun *scenario leakage*.
Pendekatan tersebut memperkuat keterlacakan evaluasi kemampuan model pada
kondisi dinamik yang tidak digunakan sebagai keluarga pelatihan.

Manfaat metodologis lain terletak pada mekanisme penerapan gain yang sama bagi
LSTM–PI dan QLSTM–PI. Prediksi gain dikembalikan ke skala fisik, diperiksa
keterhinggaannya, dibatasi pada *envelope* gain *admissible*, kemudian dikenai
pembatasan laju perubahan sebelum diterapkan pada PI. Mekanisme tersebut
memisahkan pengaruh keluaran model dari aturan keselamatan dan transisi gain
yang diterapkan pada sistem *closed-loop*.

Pada aspek praktis, penelitian menyediakan bukti simulasi mengenai kinerja,
aktivitas kendali, dan beban komputasi penjadwalan gain adaptif pada ELC PLTMH.
Hasil tersebut dapat digunakan sebagai dasar untuk menilai kelayakan
pengembangan lebih lanjut menuju model plant yang lebih lengkap, pengujian
ketidakpastian stokastik, *hardware-in-the-loop*, maupun implementasi waktu
nyata. Manfaat ini tidak didasarkan pada asumsi bahwa QLSTM harus lebih unggul,
melainkan pada evaluasi empiris terhadap kemampuan dan keterbatasannya pada
konfigurasi yang diuji.


## 1.5 Ruang Lingkup Penelitian

Penelitian dibatasi pada ketentuan berikut.

1. Objek penelitian adalah PLTMH terisolasi berkapasitas nominal 100 kW
   dengan generator sinkron, beban konsumen, ELC, dan beban buangan
   resistif.

2. Model *closed-loop* menggunakan representasi ELC *averaged* dengan daya
   mekanik pada simulasi utama dipertahankan konstan. Dinamika governor,
   *waterway*, CFD turbin, dan transien switching IGBT secara rinci tidak
   menjadi bagian dari model evaluasi akhir.

3. Pengendali utama ELC adalah PI. LSTM dan QLSTM hanya berfungsi sebagai
   penjadwal gain supervisori yang menghasilkan estimasi \(K_p\) dan \(K_i\);
   keduanya bukan pengendali langsung.

4. Target gain dibentuk melalui pencarian grid bertahap berbasis simulasi.
   Penelitian tidak menggunakan GA, PSO, GWO, SOS, maupun algoritma
   metaheuristik lain sebagai mekanisme penentu gain adaptif.

5. *Envelope* gain yang digunakan adalah
   \(K_p \in [2{,}16,\ 3{,}36]\) dan
   \(K_i \in [3{,}0368,\ 14{,}144]\).
   Rentang tersebut diperlakukan sebagai rentang gain *admissible* yang
   dibekukan dari label pembelajaran final, bukan sebagai jaminan kestabilan
   fisik universal.

6. Jendela input model menggunakan empat fitur, yaitu deviasi frekuensi,
   daya mekanik, daya elektrik, dan daya beban buangan. Dataset akhir terdiri
   atas 17.600 *window* dengan 11 titik observasi per *window* pada frekuensi
   observasi 20 Hz.

7. Pemisahan dataset dilakukan berdasarkan keluarga dinamik untuk mencegah
   kebocoran informasi. Tujuh keluarga digunakan untuk pelatihan, dua untuk
   validasi, dan dua untuk pengujian, dengan jumlah
   11.200/3.200/3.200 *window*. Tidak digunakan pemisahan acak pada tingkat
   baris.

8. Regime gain G3 tidak memiliki keluarga uji independen pada pembagian data
   akhir. Pengujian primer independen berlaku pada keluarga G1 dan G2,
   sedangkan evaluasi G3 hanya digunakan sebagai diagnostik dalam distribusi
   dan tidak menjadi dasar klaim generalisasi independen.

9. Evaluasi *closed-loop* akhir menggunakan empat skenario deterministik
   yang ditetapkan sebelum hasil diketahui. Masing-masing skenario
   dijalankan dengan PI gain tetap, LSTM–PI, dan QLSTM–PI sehingga diperoleh
   12 *run*. CL01 dan CL02 digunakan sebagai dua keluarga dinamik primer,
   CL03 sebagai *boundary stress*, dan CL04 sebagai diagnostik G3 dalam
   distribusi.

10. Metrik primer evaluasi *closed-loop* adalah RMSE deviasi frekuensi.
    Simpangan frekuensi maksimum, RoCoF, waktu tunak, aktivitas beban
    buangan, perilaku gain, dan beban komputasi digunakan sebagai indikator
    pendukung. Karena hanya tersedia dua keluarga dinamik primer independen,
    penelitian tidak melakukan uji signifikansi statistik pada tingkat
    keluarga.

11. Simulasi Monte Carlo 50 *run* tidak menjadi bagian dari evaluasi primer.
    Model dan skenario evaluasi akhir bersifat deterministik dan penelitian
    tidak menetapkan distribusi probabilistik ketidakpastian plant maupun
    gangguan. Analisis Monte Carlo ditempatkan sebagai ruang pengembangan
    penelitian selanjutnya.

12. Implementasi QLSTM menggunakan simulasi kuantum dalam kerangka
    *hybrid quantum–classical* pada lingkungan CPU/PennyLane, bukan perangkat
    keras kuantum. Penelitian merupakan *proof of concept* berbasis simulasi
    dan tidak mengklaim validasi *hardware-in-the-loop* atau implementasi
    waktu nyata pada plant fisik.



## 1.6 Orisinalitas Penelitian

Orisinalitas penelitian ditempatkan pada integrasi metodologis QLSTM sebagai
penjadwal gain PI adaptif untuk ELC PLTMH terisolasi, bukan pada klaim bahwa
QLSTM merupakan pengendali langsung atau algoritma optimasi gain. QLSTM
menerima jendela kondisi operasi dan menghasilkan estimasi \(K_p\) dan \(K_i\),
sedangkan aksi kendali terhadap ELC tetap dibentuk oleh pengendali PI.

Aspek orisinalitas pertama terletak pada pemisahan yang tegas antara proses
pembentukan target dan proses penjadwalan gain. Target \(K_p^*\) dan \(K_i^*\)
dibentuk secara luring melalui pencarian grid bertahap pada model simulasi.
LSTM dan QLSTM kemudian dilatih menggunakan target pembelajaran yang sama,
sehingga perbandingan kedua model tidak bergantung pada perbedaan sumber
label.

Aspek kedua adalah penggunaan data temporal dengan pemisahan berdasarkan
keluarga dinamik. Keluarga pelatihan, validasi, dan pengujian dipisahkan untuk
mencegah kebocoran informasi antar keluarga maupun antar skenario. Evaluasi
primer independen dilakukan pada keluarga dinamik pengujian dari regime G1 dan
G2. Regime G3 tidak mempunyai keluarga pengujian independen pada pembagian data
akhir sehingga evaluasinya hanya ditempatkan sebagai diagnostik dalam
distribusi dan tidak digunakan untuk mengklaim generalisasi G3 independen.

Aspek ketiga terletak pada penerapan keluaran LSTM dan QLSTM melalui kebijakan
scheduler yang identik. Setelah prediksi dikembalikan ke skala fisik,
nilai gain diperiksa keterhinggaannya, dibatasi pada *envelope* gain
*admissible*, kemudian dikenai pembatasan laju perubahan gain sebelum
diterapkan pada PI. Observasi temporal dilakukan pada 20 Hz dan pembaruan gain
dilakukan pada 10 Hz. Struktur yang sama digunakan untuk kedua model agar
perbedaan respons *closed-loop* tidak berasal dari aturan penerapan gain yang
berbeda.

Aspek keempat adalah evaluasi yang menghubungkan kinerja tingkat model dengan
kinerja tingkat *closed-loop*. PI gain tetap, LSTM–PI, dan QLSTM–PI diuji pada
skenario deterministik yang telah ditetapkan sebelum hasil diketahui. Evaluasi
tidak hanya mempertimbangkan RMSE deviasi frekuensi, tetapi juga indikator
dinamik, perilaku scheduler, aktivitas beban buangan, serta beban komputasi.
Pendekatan ini memungkinkan kemampuan dan keterbatasan QLSTM dinilai secara
empiris tanpa menjadikan superioritas QLSTM, signifikansi statistik, maupun
*quantum advantage* sebagai asumsi penelitian.

---

# BAB II — AUTHORITATIVE COMPOSITION

Bab II is intentionally represented as a compositional revision package rather
than a fabricated standalone merged text because Sections 2.1–2.6 and retained
parts of Sections 2.7 and 2.10 remain authoritative in the source DOCX.

## Bab-II integration operations

| Section | Operation | Authoritative source | Detail |
|---|---|---|---|
| 2.1 | RETAIN_SOURCE | Proposal Tesis_03092026_konsep_baru.docx | Retain reviewed source section 2.1. Preserve final audited scope. |
| 2.2 | RETAIN_SOURCE | Proposal Tesis_03092026_konsep_baru.docx | Retain source section 2.2 unchanged. |
| 2.3 | RETAIN_SOURCE | Proposal Tesis_03092026_konsep_baru.docx | Retain source section 2.3 unchanged. |
| 2.4 | RETAIN_SOURCE | Proposal Tesis_03092026_konsep_baru.docx | Retain reviewed source section 2.4. Do not introduce unexecuted grid-sensitivity claims. |
| 2.5 | RETAIN_SOURCE | Proposal Tesis_03092026_konsep_baru.docx | Retain source section 2.5 unchanged. |
| 2.6 | RETAIN_SOURCE | Proposal Tesis_03092026_konsep_baru.docx | Retain source section 2.6 unchanged. |
| 2.7 | PARTIAL_REPLACE | source proposal + cell180_bab_ii_section_2_7_and_table_revision.md | Retain source literature discussion and Eq. (2.17)–(2.18). Integrate corrected Cell180 implementation text through Eq. (2.21) and scheduler handoff. |
| 2.8 | FULL_REPLACE | cell178_bab_ii_targeted_revisions.md | Replace complete Section 2.8 with frozen Cell178 text, including Eq. (2.22)–(2.23), clipping, rate limiting, 20-Hz observation, 10-Hz update and zero-order hold. |
| 2.9 | FULL_REPLACE | cell178_bab_ii_targeted_revisions.md | Replace complete Section 2.9 with frozen Cell178 text, including Eq. (2.24)–(2.27), primary RMSE and descriptive family-level evaluation. |
| 2.10 | COMPOSITE_REPLACE | source proposal + Cell180 research row + Cell178 research-position tail | Retain source literature synthesis and literature-table rows except 'Penelitian ini (2026)'. Replace that row with Cell180 and replace only the final research-position paragraphs with Cell178. |
| 2.11 | FULL_REPLACE_AND_RETITLE | cell178_bab_ii_targeted_revisions.md | Replace former 'Hipotesis Penelitian' completely with 'Kerangka Evaluasi Penelitian'. Remove obsolete Eq. (2.28) and Eq. (2.29). |

## Cell180 authoritative revision text

Source:

`reports/thesis_alignment/cell180_bab_ii_section_2_7_and_table_revision.md`

SHA256:

`5c9474252d802711ebe12b53b64012838f7cdd86768b34e7b9a5754cbcb31296`

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

## Cell178 authoritative revision text

Source:

`reports/thesis_alignment/cell178_bab_ii_targeted_revisions.md`

SHA256:

`fa8a8bea9fc612f7ccdc99a466acfbda0d9764b3b0c9313e26f9b65c45c44f06`

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

---

# BAB III — AUTHORITATIVE FULL TEXT

Source:

`reports/thesis_alignment/cell185_bab_iii_full_revised_candidate.md`

SHA256:

`d8e70a621f5b0e1aa047a65945ae035345be49d002082f861f8083dfa3fbe373`

# BAB III METODE PENELITIAN

## 3.1 Desain Penelitian

Penelitian ini menggunakan pendekatan eksperimen komputasional berbasis
simulasi untuk mengevaluasi penjadwalan gain PI pada ELC PLTMH terisolasi.
Tahapan penelitian mencakup validasi model PLTMH–ELC, penetapan PI gain tetap,
pembentukan target gain secara luring, pembentukan dataset temporal, pelatihan
LSTM dan QLSTM, integrasi kedua model sebagai scheduler gain, serta evaluasi
closed-loop menggunakan protokol yang dibekukan sebelum hasil akhir diketahui.

Variabel perlakuan pada tahap closed-loop adalah konfigurasi pengendali:
PI gain tetap, LSTM–PI, dan QLSTM–PI. Unit independen utama untuk evaluasi
generalization adalah keluarga dinamik, bukan titik waktu integrasi numerik
maupun satu baris dataset. Dua keluarga dinamik uji independen digunakan
sebagai bukti primer, sedangkan skenario boundary stress dan diagnostik G3
dilaporkan secara terpisah sesuai fungsi masing-masing.

Metrik primer penelitian adalah RMSE deviasi frekuensi pada periode
pascagangguan. Simpangan puncak, RoCoF, waktu tunak, galat frekuensi akhir,
aktivitas beban buangan, lintasan gain, variasi duty, saturasi atau fallback,
dan beban komputasi digunakan sebagai indikator pendukung. Analisis bersifat
deskriptif karena jumlah keluarga uji independen tidak memadai untuk klaim
signifikansi statistik.

Rentang keluaran gain yang digunakan selama evaluasi merupakan envelope gain
admissible yang dibekukan dari ruang label supervised. Rentang tersebut tidak
ditafsirkan sebagai jaminan kestabilan fisik universal PLTMH. Penelitian juga
tidak menetapkan keberhasilan berdasarkan keharusan QLSTM mengungguli LSTM
atau PI gain tetap; hasil setara maupun lebih rendah tetap dipertahankan sebagai
hasil empiris yang sah.

## 3.2 Tempat, Perangkat, dan Waktu Penelitian

Penelitian dilaksanakan secara komputasional menggunakan alur kerja berbasis
Python yang terdokumentasi dalam notebook proyek dan repositori GitHub.
Pemodelan, pembentukan dataset, pelatihan model, simulasi closed-loop, serta
analisis hasil dilakukan dalam lingkungan komputasi yang dapat direproduksi
dari artefak proyek yang dibekukan.

LSTM direalisasikan menggunakan PyTorch. QLSTM dikembangkan sebagai model
hybrid quantum–classical menggunakan PyTorch dan PennyLane, dengan eksekusi
akhir pada CPU. Implementasi final tidak menggunakan perangkat keras kuantum.
MATLAB/Simulink dan Qiskit tidak digunakan sebagai lingkungan utama untuk
menghasilkan hasil eksperimen final yang dilaporkan.

Tahapan komputasi direpresentasikan oleh notebook pembentukan dataset,
prapengolahan, pelatihan LSTM, pelatihan QLSTM, pengujian closed-loop, dan
analisis akhir. Tahap analisis akhir difokuskan pada perbandingan deskriptif
ketiga konfigurasi pengendali dan beban komputasinya, bukan pada pengujian
signifikansi inferensial.

## 3.3 Pemodelan Sistem PLTMH–ELC

Model penelitian merepresentasikan PLTMH terisolasi berkapasitas nominal
100 kW yang terhubung dengan generator sinkron, beban konsumen, pengendali PI,
dan Electronic Load Controller (ELC). Keseimbangan daya dijaga dengan
mengalihkan selisih daya ke beban buangan resistif sehingga perubahan daya
beban konsumen dapat dikompensasi oleh ELC.

Dinamika frekuensi mengikuti hubungan keseimbangan antara daya mekanik dan
daya elektrik sebagaimana dirumuskan pada Bab II. Pada model primer yang
digunakan untuk memperoleh hasil akhir, daya mekanik diperlakukan konstan
selama satu simulasi closed-loop. Oleh karena itu, dinamika governor, bukaan
katup atau gate, waterway, dan model hidraulik rinci tidak dimasukkan ke dalam
scope hasil utama.

ELC dimodelkan menggunakan representasi averaged sehingga aksi pengalihan daya
beban buangan direpresentasikan pada tingkat daya rata-rata. Model ini tidak
mensimulasikan detail switching individual IGBT/PWM pada skala waktu
elektronika daya. Pendekatan averaged dipilih agar evaluasi difokuskan pada
dinamika frekuensi dan pengaruh perubahan gain PI pada tingkat supervisori.

Scope tersebut digunakan secara konsisten pada pembentukan bukti closed-loop.
Dengan demikian, kesimpulan penelitian dibatasi pada model ELC averaged,
daya mekanik konstan, simulasi deterministik, serta kebijakan observasi dan
pembaruan gain yang telah dibekukan.

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

## 3.6 Pembentukan Target Gain

Target supervised \(K_p^*\) dan \(K_i^*\) dibentuk secara luring menggunakan
simulator PLTMH–ELC dan pencarian grid bertahap. Untuk setiap kondisi operasi
yang digunakan dalam pembentukan label, pasangan gain kandidat dievaluasi
dengan fungsi objektif yang telah ditetapkan pada tahap pembentukan dataset.
Pasangan dengan nilai objektif terbaik digunakan sebagai target gain untuk
data temporal yang berasal dari kondisi tersebut.

Pencarian dilakukan secara deterministik dengan skema coarse-to-fine sehingga
eksplorasi awal dilakukan pada grid yang lebih kasar dan dilanjutkan pada
daerah kandidat yang lebih relevan. Prosedur ini digunakan untuk menghasilkan
target pembelajaran dan tidak berperan sebagai mekanisme adaptasi gain saat
simulasi closed-loop.

Hanya prosedur pencarian grid yang benar-benar dieksekusi dan artefaknya
tersimpan yang digunakan sebagai dasar metodologi. Penelitian tidak mengklaim
adanya aturan tie-break tambahan berbasis variasi gain tetangga atau margin
stabilitas apabila aturan tersebut tidak termasuk dalam prosedur final yang
dibekukan. Penelitian juga tidak menyatakan telah melakukan analisis
sensitivitas ukuran grid apabila analisis tersebut tidak menjadi bagian dari
eksperimen final.

Envelope gain admissible yang kemudian digunakan oleh scheduler berasal dari
ruang label final. Envelope tersebut berfungsi sebagai pembatas operasional
eksperimen, bukan sebagai bukti jaminan kestabilan universal.

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

## 3.8 Pengembangan Model LSTM dan QLSTM

LSTM dan QLSTM dikembangkan menggunakan masukan temporal, target gain, split
keluarga dinamik, serta prosedur standardisasi yang sama agar perbandingan
kedua model tidak dipengaruhi oleh perbedaan informasi masukan. Setiap jendela
berisi 11 titik observasi dari empat fitur, yaitu deviasi frekuensi, daya
mekanik, daya elektrik, dan daya beban buangan. Target model adalah \(K_p\)
dan \(K_i\) yang telah dibentuk melalui pencarian grid luring.

Standardisasi fitur dan target dihitung hanya dari data latih. Kedua model
mempelajari target pada ruang yang telah distandardisasi dan menghasilkan dua
keluaran regresi. Keluaran model tidak langsung dianggap sebagai gain aman.
Setelah inverse target scaling, kebijakan scheduler melakukan pemeriksaan nilai
berhingga, clipping pada envelope gain admissible, dan pembatasan laju
perubahan sebelum gain diterapkan pada PI.

LSTM diimplementasikan menggunakan PyTorch. QLSTM direalisasikan sebagai model
hybrid quantum–classical berbasis PennyLane dengan empat qubit, kedalaman VQC
satu lapisan, keadaan tersembunyi berdimensi empat, dan kepala regresi akhir
berstruktur \(4\rightarrow64\rightarrow60\rightarrow16\rightarrow2\).
Implementasi QLSTM akhir dijalankan pada CPU dan tidak menggunakan perangkat
keras kuantum.

Protokol final LSTM dan QLSTM masing-masing menggunakan seed tetap 20260909.
Pelatihan multi-seed tidak digunakan sebagai dasar estimasi ketidakpastian
hasil akhir. Setelah model final dibekukan, tidak dilakukan pelatihan ulang
berdasarkan hasil closed-loop dan tidak dilakukan pemilihan ulang konfigurasi
untuk memperbaiki hasil pengujian.

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

## 3.11 Kriteria Keberhasilan Penelitian

Keberhasilan penelitian ditentukan oleh keterlaksanaan metodologi secara
konsisten dan dapat ditelusuri, bukan oleh kewajiban QLSTM menghasilkan
kinerja yang lebih baik daripada seluruh pembanding. Kriteria metodologis
meliputi terbentuknya model PLTMH–ELC yang tervalidasi untuk scope penelitian,
tersedianya target gain dan dataset temporal tanpa leakage antar keluarga,
berhasilnya pelatihan LSTM dan QLSTM dengan kontrak data yang sama, serta
terintegrasinya kedua model sebagai scheduler gain pada simulasi closed-loop.

Tahap evaluasi dianggap berhasil apabila PI gain tetap, LSTM–PI, dan QLSTM–PI
dapat dibandingkan menggunakan protokol yang sama dan metrik yang telah
dibekukan. RMSE deviasi frekuensi digunakan sebagai metrik primer, sedangkan
indikator dinamik dan beban komputasi digunakan untuk memperkaya interpretasi.

Penelitian tidak mensyaratkan superioritas QLSTM sebagai kriteria keberhasilan.
Apabila QLSTM menunjukkan hasil setara atau lebih rendah dibandingkan LSTM
maupun PI gain tetap, hasil tersebut tetap merupakan temuan empiris yang sah
dan harus dilaporkan. Karena hanya terdapat dua keluarga dinamik uji primer
independen, tidak digunakan signifikansi statistik untuk menetapkan
keberhasilan atau superioritas salah satu pengendali.

Kesimpulan akhir juga harus mempertahankan batas generalisasi. Regime G3 tidak
memiliki keluarga uji independen sehingga hasil pada CL04 hanya diperlakukan
sebagai diagnostik dalam distribusi dan bukan bukti generalisasi independen
terhadap G3.

## 3.12 Alur Penelitian

Alur penelitian dimulai dengan penetapan spesifikasi dan validasi model
PLTMH–ELC sesuai scope simulasi akhir. PI gain tetap kemudian ditetapkan
sebagai baseline dan fallback, sedangkan ruang label digunakan untuk membentuk
envelope gain admissible yang akan diterapkan secara konsisten selama
evaluasi.

Tahap berikutnya membentuk target \(K_p^*\) dan \(K_i^*\) melalui pencarian
grid bertahap secara luring. Hasil simulasi kemudian diubah menjadi dataset
temporal empat fitur menggunakan jendela 11 observasi pada 20 Hz. Dataset
dipisahkan pada tingkat keluarga dinamik dengan komposisi tujuh keluarga untuk
pelatihan, dua untuk validasi, dan dua untuk pengujian. Standardisasi fitur dan
target dihitung hanya dari data latih untuk mencegah leakage.

LSTM dan QLSTM dilatih menggunakan input, target, dan split yang sama. Setelah
model akhir dibekukan, keduanya diintegrasikan sebagai scheduler gain PI.
Keluaran model menjalani inverse target scaling, pemeriksaan nilai berhingga,
clipping pada envelope gain admissible, serta pembatasan laju perubahan gain.
Gain kemudian diterapkan pada PI dengan pembaruan scheduler 10 Hz, sedangkan
observasi sistem dilakukan pada 20 Hz.

Evaluasi closed-loop akhir membandingkan PI gain tetap, LSTM–PI, dan QLSTM–PI
pada empat skenario deterministik. CL01 dan CL02 mewakili dua keluarga dinamik
uji independen dan menjadi bukti primer. CL03 digunakan sebagai boundary
stress. CL04 digunakan sebagai diagnostik G3 dalam distribusi dan tidak
digunakan untuk membuat klaim generalisasi independen terhadap G3.

Analisis akhir menggunakan RMSE deviasi frekuensi sebagai metrik primer dan
indikator dinamik serta beban komputasi sebagai bukti pendukung. Interpretasi
dilakukan secara deskriptif tanpa klaim signifikansi statistik. Simulasi Monte
Carlo tidak menjadi bagian dari tahap evaluasi primer dan ditempatkan sebagai
ruang pengembangan penelitian selanjutnya. Setelah hasil pengujian diperoleh,
tidak dilakukan pelatihan ulang model, pemilihan ulang skenario, maupun
perubahan kebijakan scheduler.

---

# BAB IV — REVIEWED AUTHORITATIVE RESULT TEXT

Source:

`reports/thesis_results/chapter_iv/Bab_IV_Hasil_dan_Pembahasan_draft.md`

SHA256:

`366c9f0ee5ec73e290876beef6e9dc6f5fd47bb4341f29902123c5efe63238e1`

# BAB IV
# HASIL DAN PEMBAHASAN

## 4.1 Kerangka Evaluasi Hasil

Evaluasi hasil dilakukan setelah model PLTMH–ELC, dataset, pembagian keluarga
dinamik, model pembelajaran, serta kebijakan penjadwalan gain ditetapkan.
Tahap *closed-loop* membandingkan tiga konfigurasi pengendali, yaitu PI dengan
gain tetap, LSTM–PI, dan QLSTM–PI. Ketiga konfigurasi menggunakan model plant,
solver, kondisi operasi, batas gain, periode observasi, periode pembaruan gain,
dan mekanisme pembatasan laju perubahan gain yang sama. Dengan rancangan
tersebut, perbedaan respons yang diperoleh tidak berasal dari perubahan
konfigurasi simulasi setelah hasil pengujian diketahui.

Evaluasi primer menggunakan dua keluarga dinamik uji independen, yaitu CL01
(D40_L-20) dan CL02 (D20_L+10). Kedua keluarga tersebut tidak digunakan sebagai
keluarga pelatihan. CL03 (D20_L+20) ditempatkan sebagai skenario
*boundary stress* tanpa target gain supervisi yang keras, sedangkan CL04
(D30_L+20) digunakan sebagai diagnostik G3 dalam distribusi pelatihan.
Oleh karena itu, hasil CL03 dan CL04 dibahas secara terpisah dan tidak
digunakan untuk memperluas klaim generalisasi pada evaluasi primer.

Simulasi menggunakan RK4 langkah tetap dengan interval 0,0025 s. Gangguan
diterapkan pada t = 2,50 s dan respons dievaluasi selama 7,50 s setelah
gangguan. Data masukan model adaptif diamati pada 20 Hz, sedangkan gain PI
diperbarui pada 10 Hz dengan mekanisme *zero-order hold* di antara dua
pembaruan. Pembaruan gain adaptif pertama diizinkan pada t = 2,60 s.
Pengaturan tersebut telah ditetapkan sebelum simulasi komparatif dan tidak
diubah berdasarkan hasil yang diperoleh.

## 4.2 Kinerja Model dalam Mengestimasi Gain PI

Sebelum integrasi ke sistem *closed-loop*, model LSTM dan QLSTM dievaluasi
terhadap target gain PI pada data uji yang telah dibekukan. MSE yang digunakan
pada tahap ini dihitung terhadap target Kp dan Ki yang telah distandardisasi,
sehingga nilainya merupakan ukuran galat regresi pada ruang target
terstandardisasi dan bukan galat frekuensi dalam satuan hertz.

**Tabel 4.1. Kinerja estimasi gain PI pada data uji**

| Model | MSE target terstandardisasi | RMSE Kp | RMSE Ki |
|---|---:|---:|---:|
| LSTM | 0,868629 | 0,289101 | 4,157301 |
| QLSTM | 2,963549 | 0,515339 | 7,789278 |

Tabel 4.1 menunjukkan bahwa LSTM menghasilkan MSE terstandardisasi
0,868629, sedangkan QLSTM menghasilkan
2,963549. Pada model beku yang dievaluasi, MSE QLSTM
sekitar 241,18% lebih tinggi daripada LSTM.
RMSE Kp dan Ki QLSTM juga lebih tinggi daripada LSTM pada data uji yang sama.

Hasil tersebut menunjukkan bahwa **arsitektur QLSTM yang digunakan dalam
konfigurasi penelitian ini belum menghasilkan akurasi estimasi gain yang lebih
baik daripada LSTM**. Temuan ini tidak ditafsirkan sebagai bukti bahwa komponen
kuantum secara umum menurunkan kinerja. QLSTM yang diuji merupakan arsitektur
*hybrid quantum–classical* dengan 5.422 parameter, yang terdiri atas 48
parameter kuantum dan komponen klasik yang membentuk sebagian besar parameter
model. Kesimpulan karena itu dibatasi pada arsitektur, dataset, proses
pelatihan, dan pembagian data yang digunakan dalam penelitian ini.

Galat estimasi gain juga tidak dapat digunakan secara langsung sebagai ukuran
akhir kinerja pengendalian. Pengaruh suatu pasangan Kp dan Ki terhadap respons
frekuensi ditentukan oleh dinamika plant, kondisi operasi, pembatasan gain,
dan sensitivitas sistem *closed-loop*. Evaluasi berikutnya karena itu
memeriksa secara langsung respons frekuensi setelah LSTM dan QLSTM
diintegrasikan sebagai penjadwal gain PI.

## 4.3 Hasil Utama Closed-Loop pada Keluarga Uji Independen

Evaluasi primer *closed-loop* menggunakan CL01 dan CL02 sebagai dua keluarga
dinamik uji independen. Metrik utama yang telah ditetapkan adalah RMSE deviasi
frekuensi selama horizon 7,50 s setelah gangguan. Hasil setiap keluarga
disajikan pada Tabel 4.2.

**Tabel 4.2. RMSE deviasi frekuensi pada keluarga uji independen**

| Skenario | Keluarga | PI gain tetap (Hz) | LSTM–PI (Hz) | QLSTM–PI (Hz) | RMSE terendah |
|---|---|---:|---:|---:|---|
| CL01 | D40_L-20 | 0,016638 | 0,020160 | 0,023913 | PI gain tetap |
| CL02 | D20_L+10 | 0,008319 | 0,007460 | 0,008388 | LSTM–PI |
| **Rerata tidak tertimbang** | **2 keluarga** | **0,012478** | **0,013810** | **0,016150** | **PI gain tetap** |

Rerata tidak tertimbang dari kedua keluarga uji menghasilkan RMSE
0,012478 Hz untuk PI gain tetap,
0,013810 Hz untuk LSTM–PI, dan
0,016150 Hz untuk QLSTM–PI. Dibandingkan PI gain tetap,
rerata RMSE LSTM–PI lebih tinggi 10,67%,
sedangkan QLSTM–PI lebih tinggi 29,42%.
Rerata RMSE QLSTM–PI juga lebih tinggi
16,95% dibandingkan LSTM–PI.

Rerata tersebut bersifat **deskriptif**, karena evaluasi primer hanya terdiri
atas dua keluarga dinamik independen. Ribuan titik waktu hasil RK4 maupun
*window* temporal dari masing-masing keluarga tidak diperlakukan sebagai
observasi independen. Oleh karena itu, hasil pada bagian ini tidak digunakan
untuk membuat klaim signifikansi statistik.

**[Masukkan Gambar 4.1 — fig157_primary_rmse_comparison.png]**

**Gambar 4.1.** Perbandingan RMSE deviasi frekuensi PI gain tetap, LSTM–PI,
dan QLSTM–PI pada dua keluarga dinamik uji independen.

Tabel 4.2 dan Gambar 4.1 memperlihatkan perbedaan kinerja yang bergantung pada
kondisi operasi. PI gain tetap menghasilkan RMSE terendah pada CL01, sedangkan
LSTM–PI menghasilkan RMSE terendah pada CL02. Dengan demikian, LSTM–PI belum
menunjukkan peningkatan yang konsisten terhadap PI gain tetap pada kedua
keluarga uji. QLSTM–PI tidak menghasilkan RMSE terendah pada salah satu dari
dua keluarga uji independen.

Bukti primer tersebut **tidak mendukung klaim bahwa QLSTM–PI meningkatkan
kinerja pengendalian frekuensi dibandingkan PI gain tetap maupun LSTM–PI**
pada dua keluarga uji independen yang tersedia. Hasil ini dipertahankan
sebagaimana diperoleh dari protokol yang telah dibekukan dan tidak digunakan
untuk melakukan pelatihan ulang model, perubahan skenario, maupun penalaan
ulang pengendali.

## 4.4 Respons Closed-Loop pada CL01 (D40_L-20)

CL01 merepresentasikan kondisi daya mekanik 90 kW, daya *dump* awal 40 kW,
dan penurunan beban konsumen sebesar 20 kW. Sebelum gangguan, beban konsumen
sebesar 50 kW dan *dump load* sebesar 40 kW. Setelah beban konsumen turun
menjadi 30 kW, titik keseimbangan daya yang baru memerlukan peningkatan daya
*dump* menuju sekitar 60 kW.

Pada skenario ini, PI gain tetap menghasilkan RMSE deviasi frekuensi sebesar
0,016638 Hz. LSTM–PI menghasilkan RMSE 0,020160 Hz, sedangkan QLSTM–PI
menghasilkan 0,023913 Hz. Dibandingkan PI gain tetap, RMSE LSTM–PI meningkat
21,17% dan RMSE QLSTM–PI meningkat 43,72%. Penyajian dalam bentuk kenaikan RMSE
digunakan agar arah perubahan kinerja tidak bergantung pada tanda negatif dari
definisi persentase *improvement* pada artefak evaluasi.

**[Masukkan Gambar 4.2 — fig157_cl01_frequency_response.png]**

**Gambar 4.2.** Respons deviasi frekuensi pada CL01 (D40_L-20). Garis
putus-putus menunjukkan waktu pembaruan gain adaptif pertama pada t = 2,60 s.

Hasil tersebut menunjukkan bahwa penjadwalan gain adaptif pada CL01 belum
memperbaiki RMSE dibandingkan PI gain tetap. Diagnostik scheduler memperlihatkan
bahwa LSTM–PI memiliki *clip fraction* 1,00 pada skenario ini, dengan rerata Ki
yang diaplikasikan sekitar 3,10, yaitu dekat batas bawah Ki sebesar 3,0368.
QLSTM–PI memiliki rerata Ki yang diaplikasikan sekitar 4,82 dan *rate-limit
fraction* yang lebih tinggi daripada LSTM–PI pada CL01. Informasi tersebut
menunjukkan bahwa mekanisme pembatas gain aktif selama operasi, tetapi tidak
digunakan untuk menyimpulkan hubungan sebab-akibat tunggal antara nilai gain
tertentu dan peningkatan RMSE.

**[Masukkan Gambar 4.3 — fig157_cl01_applied_gain_trajectories.png]**

**Gambar 4.3.** Trajektori Kp dan Ki yang diaplikasikan pada CL01 setelah
melalui batas gain dan pembatasan laju perubahan yang sama.

**[Masukkan Gambar 4.4 — fig157_cl01_dump_duty_response.png]**

**Gambar 4.4.** Respons *duty* *dump load* pada CL01 untuk ketiga konfigurasi
pengendali.

Respons CL01 karena itu memperlihatkan bahwa fleksibilitas penjadwalan gain
tidak dengan sendirinya menghasilkan respons frekuensi yang lebih baik. Pada
kondisi D40_L-20 yang diuji, PI gain tetap tetap menghasilkan RMSE terendah
meskipun LSTM–PI dan QLSTM–PI dapat mengubah gain selama fase pemulihan.


## 4.5 Respons Closed-Loop pada CL02 (D20_L+10)

CL02 merepresentasikan kondisi daya mekanik 90 kW, daya *dump* awal 20 kW,
dan kenaikan beban konsumen sebesar 10 kW. Beban konsumen meningkat dari
70 kW menjadi 80 kW sehingga daya *dump* yang diperlukan pada keseimbangan
baru berkurang dari 20 kW menuju sekitar 10 kW.

PI gain tetap menghasilkan RMSE deviasi frekuensi sebesar 0,008319 Hz.
LSTM–PI menghasilkan 0,007460 Hz sehingga RMSE menurun 10,33% dibandingkan
PI gain tetap. QLSTM–PI menghasilkan RMSE 0,008388 Hz atau sekitar 0,83% lebih
tinggi daripada PI gain tetap. Dengan demikian, hanya LSTM–PI yang menghasilkan
RMSE lebih rendah daripada PI gain tetap pada CL02.

**[Masukkan Gambar 4.5 — fig157_cl02_frequency_response.png]**

**Gambar 4.5.** Respons deviasi frekuensi pada CL02 (D20_L+10). LSTM–PI
menghasilkan RMSE terendah pada skenario ini.

Hasil CL02 menunjukkan bahwa penjadwalan gain dapat memberikan manfaat pada
kondisi operasi tertentu, tetapi temuan tersebut tidak dapat diperluas sebagai
keunggulan LSTM–PI yang konsisten karena hasil CL01 menunjukkan arah yang
berbeda. Dengan kata lain, manfaat LSTM–PI pada evaluasi primer bersifat
bergantung pada keluarga dinamik yang diuji.

Pada CL02, rerata gain QLSTM–PI yang diaplikasikan adalah sekitar Kp = 3,26 dan
Ki = 13,21. Nilai tersebut berada dekat sisi atas rentang gain yang dibekukan,
yaitu Kp maksimum 3,36 dan Ki maksimum 14,144. *Clip fraction* QLSTM–PI pada
CL02 sebesar sekitar 0,689, sedangkan LSTM–PI tidak mengalami clipping pada
skenario yang sama. Kondisi ini menunjukkan bahwa gain guard bekerja secara
material pada keluaran QLSTM. Hubungan antara kondisi tersebut dan respons
*closed-loop* diperlakukan sebagai bukti deskriptif, bukan sebagai hubungan
kausal yang berdiri sendiri.

**[Masukkan Gambar 4.6 — fig157_cl02_applied_gain_trajectories.png]**

**Gambar 4.6.** Trajektori Kp dan Ki yang diaplikasikan pada CL02 setelah
melalui kebijakan pembatasan gain yang sama.

**[Masukkan Gambar 4.7 — fig157_cl02_dump_duty_response.png]**

**Gambar 4.7.** Respons *duty* *dump load* pada CL02 untuk ketiga konfigurasi
pengendali.

Perbedaan hasil CL01 dan CL02 menegaskan bahwa evaluasi model penjadwal gain
tidak cukup dilakukan dari satu kondisi operasi. Namun, karena evaluasi primer
penelitian ini hanya terdiri atas dua keluarga dinamik independen, perbedaan
tersebut tetap diperlakukan sebagai hasil deskriptif dan tidak digunakan untuk
membuat klaim generalisasi yang lebih luas.


## 4.6 Pengaruh Penjadwalan Gain terhadap Respons Dinamik

Seluruh dua belas simulasi mempertahankan frekuensi dalam rentang diagnostik
45–55 Hz. Kondisi tersebut menunjukkan bahwa ketiga konfigurasi dapat
menyelesaikan skenario yang diuji tanpa keluar dari domain kestabilan
diagnostik yang telah ditetapkan. Akan tetapi, pemenuhan kriteria tersebut
tidak identik dengan peningkatan kualitas respons dinamik.

Pada kedua skenario primer, simpangan frekuensi absolut maksimum terjadi pada
t = 2,60 s, sedangkan RoCoF absolut maksimum terjadi pada t = 2,50 s.
Pembaruan gain adaptif pertama juga dijadwalkan pada t = 2,60 s. Oleh karena
itu, simpangan puncak terjadi **tidak lebih lambat daripada** pembaruan adaptif
pertama, sedangkan RoCoF maksimum terbentuk sebelum pembaruan tersebut.
Pernyataan ini lebih tepat daripada menganggap seluruh simpangan puncak terjadi
sebelum pengendali adaptif mulai bekerja.

Pada masing-masing skenario primer, nilai simpangan puncak dan RoCoF maksimum
identik untuk PI gain tetap, LSTM–PI, dan QLSTM–PI. Dengan cadence observasi
20 Hz dan pembaruan gain 10 Hz yang dibekukan, bukti tersebut menunjukkan
bahwa perbedaan antarpengendali terutama muncul pada fase respons setelah
ekstrem awal, yang kemudian tercermin pada RMSE selama horizon evaluasi.
Temuan ini tidak digunakan untuk menyimpulkan bahwa penjadwalan gain secara
umum tidak dapat memengaruhi puncak transien pada konfigurasi waktu pembaruan
yang berbeda.

Perbedaan antarpengendali juga terlihat pada aktivitas *dump load*. Pada dua
keluarga uji primer, rerata *total variation duty* QLSTM–PI sekitar 6,40 kali
PI gain tetap dan 5,57 kali LSTM–PI. Gain guard tercatat aktif secara material
dan tidak terjadi *fallback* model. Aktivitas kendali QLSTM–PI yang lebih besar
tersebut tidak disertai RMSE yang lebih rendah pada kedua keluarga uji primer.
Hubungan ini diperlakukan sebagai karakteristik implementasi yang diamati,
bukan sebagai bukti bahwa variasi *duty* yang tinggi secara tunggal menyebabkan
penurunan kinerja frekuensi.


## 4.7 Beban Komputasi

Beban komputasi dievaluasi dari waktu eksekusi simulasi *closed-loop* 10 s
pada implementasi CPU yang digunakan. Rerata waktu satu simulasi adalah
0,675 s untuk PI gain tetap, 0,897 s untuk LSTM–PI, dan 32,570 s untuk
QLSTM–PI. Dengan konfigurasi perangkat lunak dan perangkat keras yang sama pada
pengujian ini, rerata waktu simulasi QLSTM–PI sekitar 36,33 kali waktu simulasi
LSTM–PI.

**[Masukkan Gambar 4.8 — fig157_computational_runtime_comparison.png]**

**Gambar 4.8.** Perbandingan rerata waktu komputasi simulasi *closed-loop*
pada implementasi CPU yang digunakan.

Estimasi *paired overhead* terhadap PI gain tetap adalah sekitar 0,0030 s per
pembaruan gain untuk LSTM–PI dan 0,4310 s per pembaruan untuk QLSTM–PI.
Periode pembaruan gain yang dibekukan adalah 0,10 s. Berdasarkan pengukuran
implementasi tersebut, overhead LSTM–PI masih berada di bawah anggaran waktu
nominal pembaruan 10 Hz, sedangkan implementasi QLSTM–PI yang digunakan belum
menunjukkan kemampuan memenuhi anggaran yang sama.

Nilai *paired overhead* tersebut **bukan pengukuran latensi inferensi model
secara terisolasi**. Pengukuran mencakup overhead implementasi yang muncul
selama simulasi *closed-loop*, termasuk komponen simulasi PennyLane pada CPU.
Oleh karena itu, rasio waktu komputasi yang diperoleh tidak digunakan untuk
menyatakan latensi intrinsik komputasi kuantum, keunggulan atau kelemahan
perangkat keras kuantum, maupun *quantum speedup*. Hasil ini hanya menunjukkan
beban komputasi dari implementasi *hybrid quantum–classical* yang digunakan
dalam lingkungan simulasi penelitian ini.

Dari sudut pandang implementasi pengendali, hasil tersebut tetap relevan karena
scheduler harus menghasilkan gain dalam periode pembaruan yang tersedia.
Dengan demikian, selain kualitas pengendalian frekuensi, kebutuhan komputasi
menjadi salah satu keterbatasan praktis QLSTM–PI pada konfigurasi simulasi yang
diuji.

## 4.8 Sintesis Hasil dan Posisi QLSTM

Hasil penelitian menunjukkan bahwa kinerja model dalam mengestimasi gain dan
kinerja sistem setelah gain tersebut diterapkan pada *closed-loop* perlu
dibedakan secara eksplisit. Pada data uji model, MSE target terstandardisasi
QLSTM sebesar 2,963549 atau sekitar 241,18% lebih tinggi daripada LSTM yang
menghasilkan MSE 0,868629. Pada evaluasi *closed-loop* primer, rerata RMSE
QLSTM–PI sebesar 0,016150 Hz atau 16,95% lebih tinggi daripada LSTM–PI yang
menghasilkan 0,013810 Hz. Perbedaan besarnya kedua persentase tersebut
menunjukkan bahwa galat estimasi gain dan perubahan kinerja pengendalian
frekuensi tidak membentuk hubungan proporsional langsung.

Hubungan antara keluaran model dan respons pengendalian dipengaruhi oleh
penerapan *inverse scaling*, pembatasan gain, pembatasan laju perubahan gain,
dinamika plant, kondisi operasi, serta sensitivitas sistem terhadap pasangan Kp
dan Ki yang diaplikasikan. Oleh karena itu, peningkatan galat regresi gain tidak
ditafsirkan sebagai peningkatan galat frekuensi dengan faktor yang sama.
Sebaliknya, kualitas model juga tidak dinilai hanya dari MSE regresi tanpa
memeriksa konsekuensinya setelah diintegrasikan ke sistem *closed-loop*.

Pada empat skenario deterministik yang telah ditetapkan sebelum eksperimen,
LSTM–PI menghasilkan RMSE lebih rendah daripada QLSTM–PI pada empat dari empat
skenario. Temuan tersebut tetap memerlukan pembatasan ruang lingkup karena
hanya CL01 dan CL02 yang merupakan keluarga dinamik uji independen untuk klaim
primer. CL03 merupakan *boundary stress*, sedangkan CL04 merupakan diagnostik
G3 dalam distribusi pelatihan. Dengan demikian, hasil empat skenario tidak
diperlakukan sebagai empat replikasi independen untuk inferensi statistik.

Pada CL03, RMSE PI gain tetap, LSTM–PI, dan QLSTM–PI masing-masing sebesar
0,059777 Hz, 0,059768 Hz, dan 0,060131 Hz. Perbedaan tersebut sangat kecil dan
hanya digunakan untuk menggambarkan perilaku pengendali pada kondisi
*boundary stress*. Hasil CL03 tidak digunakan untuk memperluas klaim kinerja
primer.

Pada CL04, PI gain tetap menghasilkan RMSE 0,016638 Hz, LSTM–PI
0,015532 Hz, dan QLSTM–PI 0,015833 Hz. Dibandingkan PI gain tetap, RMSE
LSTM–PI menurun sekitar 6,65% dan RMSE QLSTM–PI menurun sekitar 4,84%.
Walaupun kedua penjadwal adaptif memberikan RMSE yang lebih rendah pada kasus
tersebut, CL04 berasal dari keluarga G3 yang berada dalam distribusi pelatihan.
Hasil tersebut karena itu hanya berfungsi sebagai diagnostik dan **tidak
menjadi bukti generalisasi independen terhadap G3**.

Posisi QLSTM dalam penelitian ini dengan demikian bukan sebagai metode yang
terbukti lebih unggul daripada LSTM atau PI gain tetap. QLSTM menunjukkan bahwa
arsitektur *hybrid quantum–classical* dapat diintegrasikan sebagai penjadwal
gain PI, menghasilkan gain yang tetap berada dalam kebijakan keselamatan yang
dibekukan, dan menyelesaikan seluruh skenario deterministik dalam rentang
kestabilan diagnostik 45–55 Hz. Namun, pada konfigurasi yang diuji, QLSTM belum
menghasilkan akurasi estimasi gain maupun RMSE *closed-loop* primer yang lebih
baik daripada LSTM. QLSTM juga disertai aktivitas *dump-duty* dan beban
komputasi yang lebih besar pada implementasi simulasi yang digunakan.

Hasil negatif tersebut dipertahankan sebagai bagian dari temuan penelitian.
Evaluasi ini menunjukkan kondisi dan batas implementasi QLSTM sebagai penjadwal
gain PI pada ELC PLTMH tanpa mengubah model, skenario, scheduler, ataupun
simulator setelah hasil pengujian diketahui.


## 4.9 Keterbatasan Hasil

Interpretasi hasil dibatasi oleh rancangan penelitian dan ruang model yang
digunakan. Keterbatasan pertama berkaitan dengan jumlah unit evaluasi
independen. Evaluasi primer hanya memiliki dua keluarga dinamik uji independen,
yaitu D40_L-20 dan D20_L+10. Jumlah tersebut belum memadai untuk mendukung uji
signifikansi statistik pada tingkat keluarga. Oleh sebab itu, perbandingan
rerata RMSE pada penelitian ini diperlakukan sebagai hasil deskriptif.

Keterbatasan kedua berkaitan dengan struktur data temporal. Ribuan titik waktu
RK4 maupun *window* temporal dari satu keluarga dinamik berasal dari realisasi
sistem yang sama dan tidak diperlakukan sebagai observasi independen.
Konsekuensinya, jumlah titik waktu tersebut tidak digunakan untuk memperbesar
ukuran sampel statistik, menghitung nilai p, atau membuat klaim signifikansi
yang tidak didukung oleh jumlah keluarga independen.

Keterbatasan ketiga berasal dari ruang model plant. Simulasi menggunakan ELC
*averaged*, daya mekanik konstan, serta model generator sinkron yang telah
ditetapkan, tanpa mengaktifkan dinamika governor dan *waterway*. Dengan
demikian, hasil penelitian berlaku pada konfigurasi model tersebut dan belum
secara langsung menunjukkan kinerja pada plant fisik dengan seluruh dinamika
hidraulik, aktuator, pengukuran, dan ketidakpastian lapangan.

Keterbatasan keempat berkaitan dengan kebijakan temporal pengendali. Observasi
model dilakukan pada 20 Hz dan pembaruan gain pada 10 Hz, dengan pembaruan
adaptif pertama pada t = 2,60 s setelah gangguan diterapkan pada t = 2,50 s.
RoCoF maksimum pada dua skenario primer terjadi pada t = 2,50 s, sedangkan
simpangan frekuensi absolut maksimum terjadi pada t = 2,60 s. Karena simpangan
puncak terjadi tidak lebih lambat daripada pembaruan adaptif pertama dan
nilainya identik untuk ketiga konfigurasi, eksperimen ini tidak menunjukkan
adanya pengurangan ekstrem awal oleh penjadwal adaptif pada kebijakan waktu
yang dibekukan. Temuan tersebut tidak digunakan untuk menyimpulkan perilaku
pada cadence observasi atau pembaruan gain yang berbeda.

Keterbatasan kelima berkaitan dengan cakupan regime target. Regime G3 tidak
tersedia sebagai keluarga uji independen pada pembagian data akhir. CL04 yang
menggunakan G3 berasal dari keluarga pelatihan dan hanya digunakan sebagai
diagnostik dalam distribusi. Oleh karena itu, penelitian ini tidak membuat
klaim generalisasi independen terhadap G3.

Keterbatasan keenam berkaitan dengan beban komputasi. Pengukuran pada
implementasi CPU/PennyLane menunjukkan bahwa QLSTM–PI belum memenuhi anggaran
waktu nominal pembaruan gain 10 Hz pada konfigurasi perangkat lunak yang diuji.
Pengukuran tersebut mencakup overhead simulasi dan bukan latensi inferensi
perangkat keras kuantum secara terisolasi. Karena itu, hasil ini tidak dapat
digunakan sebagai dasar untuk menyatakan *quantum speedup* ataupun
membandingkan efisiensi intrinsik perangkat keras klasik dan kuantum.

Keterbatasan-keterbatasan tersebut menentukan ruang berlakunya kesimpulan.
Perluasan hasil di luar ruang tersebut memerlukan evaluasi tambahan yang
dirancang terlebih dahulu, bukan perubahan *post hoc* terhadap model atau
protokol yang telah menghasilkan hasil primer penelitian ini.


## 4.10 Ringkasan Bab

Bab ini mengevaluasi LSTM–PI dan QLSTM–PI sebagai penjadwal gain pada ELC PLTMH
dengan PI gain tetap sebagai pembanding. Pada tahap estimasi gain, LSTM
menghasilkan galat lebih rendah daripada QLSTM pada data uji yang dibekukan.
Setelah diintegrasikan ke *closed-loop*, seluruh dua belas run deterministik
tetap berada dalam rentang kestabilan diagnostik 45–55 Hz, tetapi peningkatan
kinerja akibat penjadwalan gain tidak konsisten antar-kondisi operasi.

Pada dua keluarga dinamik uji independen, PI gain tetap menghasilkan rerata
RMSE terendah sebesar 0,012478 Hz. LSTM–PI menghasilkan 0,013810 Hz dan
QLSTM–PI 0,016150 Hz. LSTM–PI menghasilkan RMSE lebih rendah daripada PI gain
tetap pada CL02 tetapi lebih tinggi pada CL01, sedangkan QLSTM–PI tidak
menghasilkan RMSE terendah pada salah satu dari kedua skenario primer.
Perbandingan tersebut bersifat deskriptif karena unit evaluasi independen
primer hanya terdiri atas dua keluarga dinamik.

Hasil model dan hasil *closed-loop* juga menunjukkan bahwa galat estimasi gain
tidak mempunyai hubungan proporsional langsung dengan degradasi respons
frekuensi. Selain itu, implementasi QLSTM–PI menghasilkan variasi *dump-duty*
yang lebih besar dan membutuhkan waktu komputasi yang jauh lebih tinggi
daripada LSTM–PI pada lingkungan simulasi CPU/PennyLane yang digunakan. Hasil
beban komputasi tersebut merupakan karakteristik implementasi penelitian dan
bukan bukti mengenai keunggulan atau kelemahan intrinsik perangkat keras
kuantum.

Bukti primer penelitian ini tidak mendukung superioritas QLSTM–PI terhadap PI
gain tetap maupun LSTM–PI. Hasil CL03 tetap diposisikan sebagai
*boundary stress*, sedangkan hasil CL04 hanya merupakan diagnostik G3 dalam
distribusi pelatihan dan tidak digunakan sebagai bukti generalisasi G3
independen. Tidak ada klaim signifikansi statistik maupun *quantum advantage*
yang dibuat dari hasil tersebut.

Dengan demikian, kontribusi hasil penelitian terletak pada evaluasi terkontrol
terhadap penggunaan QLSTM sebagai penjadwal gain PI pada ELC PLTMH, termasuk
identifikasi keterbatasan akurasi, kinerja *closed-loop*, aktivitas kendali,
dan beban komputasi pada konfigurasi yang diuji. Hasil negatif QLSTM
dipertahankan sebagai temuan ilmiah dan menjadi dasar yang objektif untuk
perumusan kesimpulan serta rekomendasi penelitian selanjutnya pada Bab V.

---

# BAB V — AUTHORITATIVE FULL TEXT

Source:

`reports/thesis_results/chapter_v/Bab_V_Kesimpulan_dan_Saran_draft.md`

SHA256:

`f7751c5e8ab4367daa16021df611a4ba62d88c70286679535d8259de85b40929`

# BAB V
# KESIMPULAN DAN SARAN

## 5.1 Kesimpulan

Berdasarkan tahapan pemodelan, pembentukan dataset, pelatihan model, dan
evaluasi *closed-loop* yang telah dilakukan, penelitian menghasilkan empat
kesimpulan utama yang mengikuti tujuan penelitian.

1. Model PLTMH–ELC terisolasi telah digunakan untuk mengevaluasi respons
   frekuensi pada lingkup model akhir berupa ELC *averaged* dengan daya
   mekanik konstan. Model primer tidak memasukkan dinamika governor,
   *waterway*, CFD turbin, maupun transien *switching* IGBT secara rinci.
   Dengan lingkup tersebut, seluruh 12 simulasi deterministik dapat
   diselesaikan dalam rentang diagnostik frekuensi 45–55 Hz. Kesimpulan
   penelitian karena itu dibatasi pada representasi plant dan kondisi
   simulasi tersebut.

2. Target gain PI dibentuk secara luring melalui pencarian grid bertahap
   berbasis simulasi dan selanjutnya digunakan untuk membentuk dataset
   temporal. Dataset akhir terdiri atas 17.600 *window* dengan 11 titik
   observasi per *window* pada 20 Hz dan menggunakan empat fitur, yaitu
   deviasi frekuensi, daya mekanik, daya elektrik, dan daya beban buangan.
   Pemisahan data dilakukan pada tingkat keluarga dinamik dengan komposisi
   7 keluarga untuk pelatihan, 2 untuk validasi, dan 2 untuk pengujian,
   setara dengan 11.200/3.200/3.200 *window*. Pemisahan tersebut tidak
   menggunakan pengacakan baris dan tidak menghasilkan *family leakage*
   maupun *scenario leakage*.

3. LSTM dan QLSTM berhasil dikembangkan sebagai model estimasi gain
   \(K_p\) dan \(K_i\) serta diintegrasikan sebagai scheduler supervisori
   dengan aturan penerapan gain yang sama. Keluaran model dikembalikan ke
   skala fisik, diperiksa keterhinggaannya, dibatasi pada *envelope* gain
   *admissible*, dan dikenai pembatasan laju perubahan sebelum diterapkan
   pada PI. Pada data uji, MSE target terstandardisasi LSTM sebesar
   0,868629, sedangkan QLSTM sebesar
   2,963549. MSE QLSTM dengan demikian sekitar
   241,18% lebih tinggi daripada LSTM
   pada konfigurasi model yang diuji. Hasil tersebut menunjukkan bahwa
   arsitektur QLSTM yang digunakan belum menghasilkan estimasi gain yang
   lebih akurat daripada LSTM, tanpa menjadikannya sebagai kesimpulan umum
   mengenai seluruh arsitektur QLSTM atau komputasi kuantum.

4. Evaluasi primer pada dua keluarga dinamik uji independen menunjukkan
   rerata RMSE deviasi frekuensi sebesar 0,012478 Hz
   untuk PI gain tetap, 0,013810 Hz untuk LSTM–PI, dan
   0,016150 Hz untuk QLSTM–PI. Dibandingkan PI gain
   tetap, rerata RMSE LSTM–PI lebih tinggi 10,67%,
   sedangkan QLSTM–PI lebih tinggi 29,42%.
   Rerata RMSE QLSTM–PI juga lebih tinggi 16,95%
   dibandingkan LSTM–PI. PI gain tetap menghasilkan RMSE terendah pada
   CL01, sedangkan LSTM–PI menghasilkan RMSE terendah pada CL02; QLSTM–PI
   tidak menghasilkan RMSE terendah pada kedua keluarga uji primer.
   Dengan demikian, bukti primer penelitian ini tidak mendukung
   superioritas QLSTM–PI terhadap PI gain tetap maupun LSTM–PI.
   Perbandingan tersebut bersifat deskriptif karena hanya tersedia dua
   keluarga uji independen dan tidak digunakan untuk membuat klaim
   signifikansi statistik.

Dari sisi implementasi komputasional, waktu rata-rata satu *run* adalah
0,896540 s untuk LSTM–PI dan
32,570478 s untuk QLSTM–PI pada lingkungan CPU yang
digunakan. Rasio waktu komputasi QLSTM terhadap LSTM sekitar
36,33 kali. Estimasi *overhead* per pembaruan adalah
sekitar 0,002998 s pada LSTM dan
0,431024 s pada QLSTM, sedangkan anggaran pembaruan
10 Hz adalah 0,100000 s. Pada implementasi ini LSTM
memenuhi anggaran nominal 10 Hz, sedangkan QLSTM belum menunjukkannya.
Pengukuran tersebut mencakup *implementation-level simulation overhead* dan
tidak diperlakukan sebagai waktu inferensi model murni.

Kesimpulan keseluruhan menunjukkan bahwa penjadwalan gain adaptif tidak secara
otomatis menghasilkan respons frekuensi yang lebih baik daripada PI gain tetap.
LSTM–PI memberikan manfaat pada kondisi CL02 tetapi tidak pada CL01, sedangkan
QLSTM–PI belum menunjukkan keunggulan pada dua keluarga uji primer. Hasil
negatif tersebut dipertahankan sebagai bagian dari bukti ilmiah penelitian dan
tidak digunakan untuk melakukan pelatihan ulang model, pemilihan ulang
skenario, atau penalaan ulang scheduler setelah hasil diketahui.

## 5.2 Saran

Pengembangan penelitian selanjutnya diarahkan pada keterbatasan yang terukur
dalam eksperimen ini.

1. Evaluasi generalisasi perlu diperluas menggunakan lebih banyak keluarga
   dinamik independen. Regime G3 perlu memiliki keluarga validasi dan
   pengujian *held-out* yang benar-benar terpisah dari pelatihan sehingga
   kemampuan generalisasi terhadap regime tersebut dapat dinilai secara
   independen, bukan hanya melalui diagnostik dalam distribusi seperti CL04.

2. Analisis ketidakpastian stokastik dapat dikembangkan melalui simulasi
   Monte Carlo setelah distribusi probabilistik untuk variasi plant,
   gangguan, beban, dan/atau pengukuran ditetapkan sebelum eksperimen.
   Pengujian tersebut sebaiknya dipra-spesifikasikan agar tidak berubah
   berdasarkan hasil deterministik penelitian ini.

3. Model plant dapat diperluas dengan dinamika governor, *waterway*,
   karakteristik turbin yang lebih rinci, gangguan pengukuran, serta
   representasi elektronika daya yang lebih detail. Pengembangan ini
   diperlukan untuk menguji apakah pola kinerja yang ditemukan pada model
   ELC *averaged* dengan daya mekanik konstan tetap bertahan ketika tingkat
   fidelitas plant ditingkatkan.

4. Kelayakan implementasi waktu nyata QLSTM perlu difokuskan pada pengurangan
   beban komputasi dan latensi. Arsitektur, backend simulasi kuantum, strategi
   eksekusi, dan perangkat komputasi dapat dibandingkan menggunakan protokol
   yang ditetapkan sebelum pengujian. Evaluasi tersebut tidak boleh
   mengasumsikan adanya *quantum advantage* dan perlu melaporkan secara
   terpisah waktu inferensi model murni dari *overhead* simulasi sistem.

5. Robustness pelatihan LSTM dan QLSTM dapat diperluas menggunakan beberapa
   *seed* yang ditentukan sebelum eksperimen, disertai evaluasi variasi
   kinerja pada keluarga dinamik independen yang lebih banyak. Pendekatan
   tersebut dapat memberikan gambaran yang lebih kuat mengenai sensitivitas
   hasil terhadap inisialisasi model tanpa menggantikan hasil dengan
   konfigurasi yang dipilih secara *post hoc*.

6. Pengujian *hardware-in-the-loop* dan implementasi waktu nyata dapat
   dilakukan setelah model, scheduler, batas gain, mekanisme fallback, dan
   anggaran komputasi memenuhi persyaratan yang telah ditetapkan. Tahap ini
   penting untuk mengevaluasi pengaruh keterlambatan komputasi, periode
   sampling fisik, noise sensor, serta keterbatasan perangkat kendali yang
   belum direpresentasikan dalam simulasi deterministik saat ini.

---

# PACKAGE SCIENTIFIC FREEZE

- Bab I final aligned: True
- Bab II final aligned: True
- Bab III final aligned: True
- Bab IV result text frozen by SHA: True
- Bab V final aligned: True
- Bab I–V cross-chapter scientific alignment: True
- QLSTM superiority claim: False
- Statistical significance claim: False
- Independent G3 generalization claim: False
- Quantum advantage claim: False
- Monte Carlo performed: False
- Post-result tuning: False
- Proposal DOCX modified by this package stage: False
