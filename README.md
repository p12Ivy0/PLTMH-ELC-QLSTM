# PLTMH-ELC-QLSTM
Penelitian Peningkatan Kinerja Electronic Load Controller (ELC) Pembangkit Listrik Tenaga Mikro Hidro (PLTMH) Berbasis Quantum Long Short Term Memory (QLSTM)
Struktur project sebagai berikut
PLTMH-ELC-QLSTM/
│
├── README.md
├── requirements.txt
├── .gitignore
│
├── config/
│   ├── plant.yaml
│   ├── controller.yaml
│   ├── qlstm.yaml
│   └── experiment.yaml
│
├── src/
│   ├── plant/
│   │   ├── turbine.py
│   │   ├── synchronous_generator.py
│   │   ├── consumer_load.py
│   │   ├── elc.py
│   │   └── dump_load.py
│   │
│   ├── control/
│   │   ├── pi_controller.py
│   │   ├── pwm.py
│   │   ├── limiter.py
│   │   └── gain_scheduler.py
│   │
│   ├── simulation/
│   │   ├── solver.py
│   │   ├── scenario.py
│   │   ├── simulator.py
│   │   └── state_manager.py
│   │
│   ├── data/
│   │   ├── preprocessing.py
│   │   ├── normalization.py
│   │   ├── windowing.py
│   │   └── logger.py
│   │
│   ├── models/
│   │   ├── lstm.py
│   │   ├── qlstm.py
│   │   └── vqc.py
│   │
│   └── evaluation/
│       ├── metrics.py
│       ├── statistics.py
│       └── plots.py
│
├── notebooks/
│   ├── 00_setup.ipynb
│   ├── 01_validate_turbine.ipynb
│   ├── 02_validate_generator.ipynb
│   ├── 03_validate_elc.ipynb
│   ├── 04_validate_pi.ipynb
│   ├── 05_generate_dataset.ipynb
│   ├── 06_preprocessing.ipynb
│   ├── 07_train_lstm.ipynb
│   ├── 08_train_qlstm.ipynb
│   ├── 09_closed_loop.ipynb
│   └── 10_final_analysis.ipynb
│
├── tests/
│   ├── test_turbine.py
│   ├── test_generator.py
│   ├── test_elc.py
│   └── test_pi.py
│
└── docs/
    ├── equations.md
    └── methodology.md
