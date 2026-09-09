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
