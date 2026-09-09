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
