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
