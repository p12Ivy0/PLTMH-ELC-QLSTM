# CELL 184 — REMAINING BAB-III REVISION PACKAGE

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
