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
