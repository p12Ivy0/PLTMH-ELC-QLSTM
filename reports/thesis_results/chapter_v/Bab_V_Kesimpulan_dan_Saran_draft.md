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
