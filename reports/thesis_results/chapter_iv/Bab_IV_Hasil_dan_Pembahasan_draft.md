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

CL01 merepresentasikan kondisi daya mekanik 90 kW, daya dump awal 40 kW,
dan penurunan beban konsumen sebesar 20 kW. Pada kondisi awal, beban
konsumen sebesar 50 kW dan dump load sebesar 40 kW. Setelah gangguan, beban
konsumen turun menjadi 30 kW sehingga titik keseimbangan baru membutuhkan
daya dump sekitar 60 kW.

RMSE PI gain tetap pada CL01 adalah 0.016638 Hz. LSTM–PI
menghasilkan 0.020160 Hz, sedangkan QLSTM–PI menghasilkan
0.023913 Hz. Dibandingkan PI gain tetap, perubahan RMSE
LSTM–PI adalah -21.17% dan perubahan QLSTM–PI adalah
-43.72%. Nilai negatif menunjukkan bahwa RMSE meningkat.

**[Masukkan Gambar 4.2 — fig157_cl01_frequency_response.png]**

**Gambar 4.2.** Respons deviasi frekuensi pada CL01 (D40_L-20).

Pada skenario ini, pengaturan gain adaptif tidak memperbaiki RMSE terhadap
gain tetap. Salah satu karakteristik LSTM–PI pada CL01 adalah keluaran Ki
yang sering mencapai batas bawah rentang gain, sedangkan QLSTM–PI menghasilkan
variasi gain yang lebih besar. Kebijakan pembatas gain mencegah keluaran
model diterapkan di luar rentang yang telah ditetapkan.

**[Masukkan Gambar 4.4 — fig157_cl01_applied_gain_trajectories.png]**

**Gambar 4.4.** Trajektori Kp dan Ki yang diaplikasikan pada CL01.

**[Masukkan Gambar 4.6 — fig157_cl01_dump_duty_response.png]**

**Gambar 4.6.** Respons duty dump load pada CL01.

## 4.5 Respons Closed-Loop pada CL02 (D20_L+10)

CL02 merepresentasikan kondisi daya mekanik 90 kW, daya dump awal 20 kW,
dan kenaikan beban konsumen sebesar 10 kW. Beban konsumen berubah dari
70 kW menjadi 80 kW sehingga daya dump yang diperlukan pada keseimbangan
baru turun dari 20 kW menjadi sekitar 10 kW.

Pada CL02, RMSE PI gain tetap sebesar 0.008319 Hz. LSTM–PI
menghasilkan 0.007460 Hz dan QLSTM–PI menghasilkan
0.008388 Hz. LSTM–PI memperbaiki RMSE sebesar
10.33% dibandingkan PI gain tetap. Sebaliknya,
perubahan QLSTM–PI terhadap PI gain tetap sebesar
-0.83%.

**[Masukkan Gambar 4.3 — fig157_cl02_frequency_response.png]**

**Gambar 4.3.** Respons deviasi frekuensi pada CL02 (D20_L+10).

Hasil CL02 menunjukkan bahwa gain adaptif dapat memberikan manfaat pada
kondisi operasi tertentu. Meskipun demikian, manfaat tersebut pada eksperimen
primer hanya muncul pada LSTM–PI dan tidak konsisten dengan hasil CL01.
Temuan ini memperlihatkan bahwa hubungan antara kondisi operasi dan gain PI
optimal bersifat spesifik terhadap dinamika gangguan.

Pada QLSTM–PI, nilai Ki yang diaplikasikan pada CL02 cenderung jauh lebih
tinggi dan pada sebagian interval mendekati batas atas yang telah dibekukan.
Kondisi ini berhubungan dengan aktivitas pembatas gain yang lebih tinggi serta
variasi duty ELC yang lebih besar.

**[Masukkan Gambar 4.5 — fig157_cl02_applied_gain_trajectories.png]**

**Gambar 4.5.** Trajektori Kp dan Ki yang diaplikasikan pada CL02.

**[Masukkan Gambar 4.7 — fig157_cl02_dump_duty_response.png]**

**Gambar 4.7.** Respons duty dump load pada CL02.

## 4.6 Pengaruh Penjadwalan Gain terhadap Respons Dinamik

Seluruh konfigurasi mempertahankan frekuensi dalam rentang diagnostik
45–55 Hz pada dua belas simulasi yang dilakukan. Namun, kemampuan menjaga
kestabilan tidak secara otomatis menunjukkan peningkatan kualitas respons.

Simpangan frekuensi puncak pada kedua skenario primer terjadi pada sekitar
t = 2,60 s, sedangkan RoCoF maksimum terjadi pada t = 2,50 s. Pembaruan gain
adaptif pertama baru diterapkan pada t = 2,60 s. Dengan demikian, respons
awal yang membentuk simpangan puncak dan RoCoF maksimum pada kedua skenario
primer pada dasarnya terbentuk sebelum pengendali adaptif memiliki kesempatan
untuk mengubah dinamika plant.

Konsekuensi ini menjelaskan mengapa ketiga konfigurasi mempunyai simpangan
puncak dan RoCoF maksimum yang sama pada masing-masing skenario primer,
meskipun RMSE dan respons setelah puncak berbeda. Manfaat atau kerugian
penjadwalan gain pada konfigurasi penelitian ini terutama tercermin pada
pemulihan setelah transien awal, bukan pada ekstrem awal gangguan.

Pada dua keluarga uji primer, total variation duty QLSTM–PI sekitar
6.40 kali PI gain tetap dan
5.57 kali LSTM–PI. Besarnya variasi tersebut menunjukkan
bahwa perubahan gain yang dihasilkan QLSTM menyebabkan aktivitas pengendalian
dump load yang lebih tinggi, tanpa diikuti penurunan RMSE pada dua skenario
uji independen.

## 4.7 Beban Komputasi

Perbedaan lain yang terlihat jelas terdapat pada kebutuhan komputasi.
Rerata waktu simulasi 10 s untuk PI gain tetap adalah
0.675 s. LSTM–PI membutuhkan
0.897 s, sedangkan QLSTM–PI membutuhkan
32.570 s.

Dengan konfigurasi CPU dan PennyLane yang digunakan, waktu simulasi QLSTM–PI
sekitar 36.33 kali waktu simulasi LSTM–PI.

**[Masukkan Gambar 4.8 — fig157_computational_runtime_comparison.png]**

**Gambar 4.8.** Perbandingan rerata waktu komputasi simulasi *closed-loop*.

Estimasi overhead implementasi LSTM adalah sekitar
0.0030 s per pembaruan gain, sedangkan QLSTM sekitar
0.4310 s. Periode pembaruan gain yang dibekukan
adalah 0,10 s. Implementasi LSTM pada CPU masih berada di bawah anggaran
tersebut, sedangkan implementasi QLSTM belum menunjukkan kemampuan memenuhi
pembaruan 10 Hz.

Nilai tersebut tidak boleh ditafsirkan sebagai latensi intrinsik komputasi
kuantum karena pengukuran mencakup overhead implementasi PennyLane dan proses
simulasi pada CPU. Namun, hasil tersebut tetap relevan sebagai indikator
beban komputasi implementasi yang digunakan dalam penelitian ini.

## 4.8 Sintesis Hasil dan Posisi QLSTM

Hasil penelitian memperlihatkan perbedaan antara kemampuan model dalam
mengestimasi gain dan dampaknya terhadap respons *closed-loop*. Pada pengujian
model, MSE terstandar QLSTM sekitar 241.18% lebih
tinggi daripada LSTM. Pada evaluasi *closed-loop*, rerata RMSE QLSTM hanya
16.95% lebih tinggi daripada LSTM. Perbedaan tersebut
menunjukkan bahwa galat estimasi gain dan degradasi pengendalian frekuensi
bukan besaran yang mempunyai hubungan proporsional langsung.

Secara keseluruhan, hasil primer tidak mendukung hipotesis bahwa QLSTM–PI
memberikan peningkatan kinerja ELC dibandingkan PI gain tetap atau LSTM–PI
pada dua keluarga dinamik uji independen yang tersedia. PI gain tetap
menghasilkan rerata RMSE terendah, sedangkan LSTM–PI memberikan manfaat
hanya pada salah satu dari dua kondisi uji utama.

Meskipun demikian, hasil ini tetap memberikan informasi penting mengenai
kelayakan penggunaan QLSTM sebagai penjadwal gain. Sistem QLSTM dapat
diintegrasikan ke *closed-loop*, menghasilkan gain yang terbatas dalam
rentang aman penelitian, dan mempertahankan kestabilan simulasi. Hambatan
utama pada konfigurasi saat ini adalah kemampuan generalisasi gain, aktivitas
pengendalian yang lebih besar, serta kebutuhan komputasi yang jauh lebih tinggi.

Hasil CL04 menunjukkan bahwa LSTM–PI dan QLSTM–PI dapat memperbaiki RMSE pada
kasus G3 dalam distribusi pelatihan. Akan tetapi, CL04 berasal dari keluarga
pelatihan sehingga hasil tersebut hanya bersifat diagnostik. Hasil ini tidak
dapat digunakan sebagai bukti generalisasi independen terhadap regime G3.

## 4.9 Keterbatasan Hasil

Interpretasi hasil dibatasi oleh beberapa karakteristik rancangan penelitian.
Pertama, evaluasi primer hanya memiliki dua keluarga dinamik uji independen.
Jumlah tersebut tidak memadai untuk mendukung uji signifikansi statistik pada
tingkat keluarga.

Kedua, ribuan titik RK4 maupun *window* temporal yang berasal dari satu
keluarga dinamik tidak diperlakukan sebagai observasi independen. Oleh karena
itu, penelitian ini tidak menggunakan jumlah titik waktu untuk menghasilkan
nilai p atau klaim signifikansi statistik.

Ketiga, model plant menggunakan ELC *averaged*, daya mekanik konstan,
generator sinkron dengan model dinamik yang telah ditetapkan, dan tidak
mengaktifkan dinamika governor maupun waterway. Kesimpulan penelitian
berlaku pada ruang model tersebut.

Keempat, periode pengamatan 20 Hz dan pembaruan gain 10 Hz merupakan bagian
dari rancangan eksperimen yang telah dibekukan. Pembaruan pertama setelah
gangguan menyebabkan penjadwal adaptif tidak dapat memengaruhi RoCoF maksimum
dan puncak awal pada skenario primer.

Kelima, regime G3 hanya tersedia sebagai keluarga pelatihan pada evaluasi
akhir. Karena itu, penelitian ini tidak membuat klaim generalisasi independen
untuk G3.

## 4.10 Ringkasan Bab

Hasil utama menunjukkan bahwa seluruh konfigurasi mampu mempertahankan
kestabilan frekuensi pada skenario yang diuji, tetapi peningkatan kinerja
akibat penjadwalan gain tidak konsisten. PI gain tetap menghasilkan rerata
RMSE terendah pada dua keluarga uji independen. LSTM–PI memperbaiki kinerja
pada D20_L+10 tetapi menurunkannya pada D40_L-20. QLSTM–PI tidak menghasilkan
RMSE terendah pada kedua skenario primer serta membutuhkan variasi duty dan
beban komputasi yang lebih besar.

Dengan demikian, kontribusi hasil penelitian bukan berupa pembuktian
superioritas QLSTM, melainkan evaluasi terkontrol mengenai penggunaan QLSTM
sebagai penjadwal gain PI pada ELC PLTMH dan identifikasi kondisi ketika
pendekatan tersebut belum memberikan keuntungan dibandingkan pengendali yang
lebih sederhana.
