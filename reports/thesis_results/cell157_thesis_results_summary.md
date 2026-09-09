# Ringkasan Hasil Utama Closed-Loop

## Perbandingan pada keluarga uji independen

Evaluasi utama dilakukan pada dua keluarga dinamik yang telah ditetapkan sebelum
simulasi komparatif, yaitu D40_L-20 dan D20_L+10. Berdasarkan rerata tidak
tertimbang kedua keluarga tersebut, PI gain tetap menghasilkan RMSE deviasi
frekuensi terendah sebesar 0.012478 Hz. LSTM–PI menghasilkan
RMSE 0.013810 Hz atau 10.67% lebih
tinggi dibandingkan PI gain tetap, sedangkan QLSTM–PI menghasilkan RMSE
0.016150 Hz atau 29.42% lebih tinggi
dibandingkan PI gain tetap.

Performa LSTM–PI bergantung pada kondisi operasi. Pada D20_L+10, LSTM–PI
menurunkan RMSE sebesar 10,33% dibandingkan PI gain tetap. Sebaliknya, pada
D40_L-20, RMSE LSTM–PI meningkat sebesar 21,17%. QLSTM–PI tidak menghasilkan
RMSE terendah pada kedua keluarga uji independen tersebut.

## Peak deviation dan RoCoF

Nilai simpangan frekuensi puncak dan RoCoF maksimum pada dua skenario utama
identik untuk ketiga pengendali. Kondisi ini berkaitan dengan kebijakan
pembaruan gain adaptif pertama pada 2,60 s, sedangkan RoCoF maksimum terjadi
pada saat gangguan 2,50 s dan simpangan frekuensi puncak telah terbentuk pada
2,60 s. Dengan demikian, gain adaptif belum memengaruhi state plant yang
membentuk kedua ekstrem awal tersebut.

## Aktivitas pengendalian

Semua dua belas simulasi tetap berada dalam rentang diagnostik kestabilan
45–55 Hz. Namun, QLSTM–PI menghasilkan variasi total duty dump load sekitar
6.40 kali PI gain tetap dan
5.57 kali LSTM–PI pada dua keluarga uji utama.
Kebijakan pembatas gain juga aktif pada beberapa keluaran LSTM dan QLSTM,
sehingga gain yang diaplikasikan merupakan keluaran model yang telah melalui
pembatasan rentang dan laju perubahan.

## Beban komputasi

Pada implementasi CPU/PennyLane yang digunakan dalam penelitian ini, waktu
simulasi QLSTM–PI sekitar 36.33 kali waktu simulasi
LSTM–PI. Audit Cell 156 memperkirakan overhead QLSTM sekitar 0,431 s per
pembaruan gain, sedangkan periode pembaruan yang ditetapkan adalah 0,10 s.
Oleh karena itu, implementasi QLSTM saat ini belum menunjukkan kemampuan
eksekusi 10 Hz secara waktu nyata. Hasil ini merupakan karakteristik
implementasi simulator yang digunakan dan bukan pengukuran latensi perangkat
keras kuantum khusus.

## Interpretasi

Berdasarkan eksperimen primer yang telah dibekukan, bukti yang diperoleh tidak
mendukung klaim bahwa QLSTM–PI meningkatkan kinerja pengendalian frekuensi ELC
dibandingkan PI gain tetap atau LSTM–PI pada dua keluarga uji independen.
Temuan negatif tersebut dipertahankan tanpa pelatihan ulang, perubahan
arsitektur, perubahan skenario, atau penalaan ulang berdasarkan hasil uji.

Kesimpulan ini dibatasi pada model ELC averaged, daya mekanik konstan, dua
keluarga uji independen, simulasi deterministik, pengamatan 20 Hz, dan
pembaruan gain 10 Hz. Tidak dilakukan klaim signifikansi statistik dan tidak
dilakukan klaim generalisasi independen terhadap regime G3.
