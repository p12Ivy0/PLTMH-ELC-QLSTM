# PLTMH–ELC–QLSTM

## Pengendalian Frekuensi PLTMH–ELC dengan Penjadwalan Gain PI Berbasis LSTM dan QLSTM

Repository ini merupakan lingkungan komputasi penelitian pengendalian frekuensi **Pembangkit Listrik Tenaga Mikro Hidro (PLTMH) terisolasi** menggunakan **Electronic Load Controller (ELC)** dan pengendali PI.

Penelitian dikembangkan berbasis Python mulai dari pemodelan turbin, generator sinkron, beban, ELC, dump load, PI, pembentukan dataset, preprocessing, pelatihan LSTM dan QLSTM, simulasi *closed-loop*, hingga analisis hasil akhir.

Tiga konfigurasi pengendalian dibandingkan:

1. **PI gain tetap** sebagai baseline.
2. **LSTM–PI** dengan LSTM sebagai penjadwal gain adaptif.
3. **QLSTM–PI** dengan QLSTM sebagai penjadwal gain adaptif.

---

## Tujuan Penelitian

Penelitian bertujuan mengevaluasi kemampuan LSTM dan QLSTM sebagai penjadwal gain PI untuk pengendalian frekuensi PLTMH terisolasi.

Tujuan teknis penelitian meliputi:

- membangun model dinamik PLTMH–ELC berbasis Python;
- memvalidasi turbin, generator sinkron, ELC, dan PI;
- menetapkan PI gain tetap sebagai baseline;
- membentuk dataset temporal dari variasi operasi dan gangguan beban;
- melakukan normalisasi, splitting, dan windowing;
- melatih LSTM dan QLSTM untuk mengestimasi Kp dan Ki;
- mengintegrasikan model sebagai *gain scheduler*;
- membandingkan PI, LSTM–PI, dan QLSTM–PI pada skenario uji independen;
- mengevaluasi kinerja dinamik dan kebutuhan komputasi.

Hasil positif maupun negatif dipertahankan berdasarkan eksperimen yang telah dibekukan sebelum interpretasi akhir.

---

## Arsitektur Sistem

PLTMH dimodelkan sebagai sistem terisolasi yang terdiri atas turbin air, generator sinkron, beban konsumen, ELC, PWM, dan dump load resistif.

```text
Turbin → Generator Sinkron → Bus PLTMH → Beban Konsumen
                              │
                              └→ ELC/PWM → Dump Load
                                   ▲
                                   │ u(t)
                              PI Controller
                                   ▲
                                   │ Kp(t), Ki(t)
                         ┌─────────┴─────────┐
                         │                   │
                       LSTM                QLSTM
                         ▲                   ▲
                         └──── X(t-L+1:t) ───┘
```

Vektor observasi:

$$
\mathbf{x}(t)=[f(t),\Delta f(t),P_m(t),P_e(t),P_{dump}(t)]
$$

Masukan temporal:

$$
\mathbf{X}_t=[\mathbf{x}(t-L+1),\ldots,\mathbf{x}(t)]
$$

Estimasi gain:

$$
[\hat K_p(t),\hat K_i(t)]=\mathcal{M}(\mathbf{X}_t)
$$

---

## Model Matematis

### Dinamika frekuensi

$$
\frac{d\Delta f}{dt}=\frac{1}{2H}(P_m-P_e)
$$

$$
f(t)=f_{ref}+\Delta f(t), \qquad f_{ref}=50\ \text{Hz}
$$

### Keseimbangan daya ELC

$$
P_{gen}=P_{load}+P_{dump}
$$

### Pengendali PI

$$
e(t)=f_{ref}-f(t)
$$

$$
u(t)=K_p(t)e(t)+K_i(t)\int_0^t e(\tau)d\tau
$$

Pada PI tetap, Kp dan Ki konstan. Pada LSTM–PI dan QLSTM–PI, gain diperbarui berdasarkan estimasi model.

---

## Struktur Repositori

Struktur berikut dibuat menyerupai tampilan folder tree pada File Explorer.

```text
📁 PLTMH-ELC-QLSTM
│
├── 📄 README.md
├── 📄 requirements.txt
├── 📄 pytest.ini
├── 📄 .gitignore
│
├── 📁 config
│   ├── 📄 plant.yaml
│   ├── 📄 controller.yaml
│   ├── 📄 qlstm.yaml
│   └── 📄 experiment.yaml
│
├── 📁 data
│   ├── 📁 audits
│   ├── 📁 closed_loop
│   ├── 📁 enrichment
│   ├── 📁 final
│   ├── 📁 recovery
│   └── 📁 splits
│
├── 📁 docs
│   ├── 📄 equations.md
│   └── 📄 methodology.md
│
├── 📁 models
│   ├── 📁 endpoint_mlp_baseline
│   ├── 📁 lstm_baseline
│   └── 📁 qlstm
│
├── 📁 notebooks
│   ├── 📓 00_setup.ipynb
│   ├── 📓 01_validate_turbine.ipynb
│   ├── 📓 02_validate_generator.ipynb
│   ├── 📓 03_validate_elc.ipynb
│   ├── 📓 04_validate_pi.ipynb
│   ├── 📓 05_generate_dataset.ipynb
│   ├── 📓 06_preprocessing.ipynb
│   ├── 📓 07_train_lstm.ipynb
│   ├── 📓 08_train_qlstm.ipynb
│   ├── 📓 09_closed_loop.ipynb
│   └── 📓 10_final_analysis.ipynb
│
├── 📁 reports
│   ├── 📁 reproducibility
│   ├── 📁 thesis_alignment
│   ├── 📁 thesis_integration
│   └── 📁 thesis_results
│       ├── 📄 cell157_thesis_results_summary.md
│       ├── 📄 cell157_thesis_evidence_manifest.json
│       ├── 📄 cell157_figure_captions.csv
│       ├── 📁 chapter_iv
│       ├── 📁 chapter_v
│       ├── 📁 figures
│       └── 📁 tables
│
├── 📁 src
│   ├── 📄 __init__.py
│   ├── 📁 plant
│   ├── 📁 control
│   ├── 📁 simulation
│   ├── 📁 data
│   ├── 📁 models
│   └── 📁 evaluation
│
└── 📁 tests
    ├── 🧪 test_plant_model.py
    ├── 🧪 test_turbine.py
    ├── 🧪 test_generator.py
    ├── 🧪 test_elc.py
    └── 🧪 test_pi.py
```

Pemisahan tersebut membantu menjaga keterlacakan source code, dataset, model, eksperimen, dan artefak hasil penelitian.

---

## Instalasi

Clone repository:

```bash
git clone https://github.com/p12Ivy0/PLTMH-ELC-QLSTM.git
cd PLTMH-ELC-QLSTM
```

Instal dependency:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Dependency utama: NumPy, SciPy, Pandas, Matplotlib, Scikit-learn, PyTorch, PennyLane, Statsmodels, PyYAML, Joblib, dan Pytest.

Pengujian:

```bash
pytest
```

---

## Google Colab

Repository dapat dijalankan pada Google Colab:

```python
!git clone https://github.com/p12Ivy0/PLTMH-ELC-QLSTM.git
%cd PLTMH-ELC-QLSTM
!pip install -r requirements.txt
```

Urutan notebook:

```text
00_setup.ipynb
      ↓
01_validate_turbine.ipynb
      ↓
02_validate_generator.ipynb
      ↓
03_validate_elc.ipynb
      ↓
04_validate_pi.ipynb
      ↓
05_generate_dataset.ipynb
      ↓
06_preprocessing.ipynb
      ↓
07_train_lstm.ipynb
      ↓
08_train_qlstm.ipynb
      ↓
09_closed_loop.ipynb
      ↓
10_final_analysis.ipynb
```

---

## Eksperimen

| Tahap | Notebook | Fungsi utama |
|---|---|---|
| 1 | `00_setup.ipynb` | Persiapan environment |
| 2 | `01_validate_turbine.ipynb` | Validasi turbin |
| 3 | `02_validate_generator.ipynb` | Validasi generator |
| 4 | `03_validate_elc.ipynb` | Validasi ELC |
| 5 | `04_validate_pi.ipynb` | Validasi PI baseline |
| 6 | `05_generate_dataset.ipynb` | Pembentukan dataset |
| 7 | `06_preprocessing.ipynb` | Preprocessing |
| 8 | `07_train_lstm.ipynb` | Pelatihan LSTM |
| 9 | `08_train_qlstm.ipynb` | Pelatihan QLSTM |
| 10 | `09_closed_loop.ipynb` | Evaluasi closed-loop |
| 11 | `10_final_analysis.ipynb` | Analisis akhir |

Metrik utama meliputi RMSE deviasi frekuensi, simpangan puncak, RoCoF, settling time, aktivitas dump load, perubahan gain, kestabilan, dan waktu komputasi.

---

## Reprodusibilitas

Reproduksi eksperimen dilakukan dengan:

1. menggunakan commit source code yang sama;
2. menggunakan dependency pada `requirements.txt`;
3. menjalankan notebook sesuai urutan workflow;
4. mempertahankan pemisahan train, validation, dan test;
5. menggunakan model yang dibekukan sebelum evaluasi test;
6. tidak melakukan tuning ulang berdasarkan hasil test;
7. mempertahankan konfigurasi skenario;
8. menyimpan artefak audit, model, data, tabel, dan gambar.

---

## Hasil

### Perbandingan kinerja closed-loop

Evaluasi utama menggunakan keluarga uji independen **D40_L-20** dan **D20_L+10**.

| Pengendali | RMSE deviasi frekuensi | Dibanding PI tetap |
|---|---:|---:|
| **PI gain tetap** | **0,012478 Hz** | Baseline |
| **LSTM–PI** | 0,013810 Hz | 10,67% lebih tinggi |
| **QLSTM–PI** | 0,016150 Hz | 29,42% lebih tinggi |

PI gain tetap menghasilkan RMSE rata-rata terendah.

Pada **D20_L+10**, LSTM–PI menurunkan RMSE sebesar **10,33%**. Pada **D40_L-20**, RMSE LSTM–PI meningkat sebesar **21,17%**.

QLSTM–PI tidak menghasilkan RMSE terendah pada kedua keluarga uji.

### Simpangan puncak dan RoCoF

Gangguan diberikan pada 2,50 s, sedangkan pembaruan gain adaptif pertama dilakukan pada 2,60 s. Karena itu, gain adaptif belum memengaruhi ekstrem awal RoCoF dan simpangan frekuensi.

### Kestabilan

Seluruh **12 simulasi closed-loop** tetap berada dalam rentang diagnostik **45–55 Hz**.

### Aktivitas pengendalian

Total variasi duty dump load QLSTM–PI sekitar **6,40 kali** PI gain tetap dan **5,57 kali** LSTM–PI.

### Beban komputasi

Waktu simulasi QLSTM–PI sekitar **36,33 kali** LSTM–PI. Overhead QLSTM sekitar **0,431 s/update**, sedangkan periode pembaruan gain adalah 0,10 s.

Implementasi CPU/PennyLane saat ini belum memenuhi eksekusi real-time pada pembaruan **10 Hz**. Laju observasi adalah **20 Hz**.

### Interpretasi hasil

Eksperimen yang telah dibekukan tidak memberikan bukti bahwa QLSTM–PI meningkatkan kinerja dibandingkan PI gain tetap maupun LSTM–PI pada dua keluarga uji independen.

Temuan negatif dipertahankan tanpa pelatihan ulang, perubahan arsitektur, perubahan skenario uji, atau penalaan ulang berdasarkan hasil test.
