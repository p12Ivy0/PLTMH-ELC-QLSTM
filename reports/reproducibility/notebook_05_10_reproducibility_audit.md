# Notebook 05–10 Final Reproducibility Audit

## Status

**PASS**

Audit checkpoint basis:

`5ea9c093748656baedfa00b036e5532c7f66b0b6`

## Notebook suite

The following research notebooks are populated, structurally valid, syntax-valid,
and frozen to their expected SHA256 values:

1. `05_generate_dataset.ipynb`
2. `06_preprocessing.ipynb`
3. `07_train_lstm.ipynb`
4. `08_train_qlstm.ipynb`
5. `09_closed_loop.ipynb`
6. `10_final_analysis.ipynb`

No notebook was executed by Cell 168.

## Frozen scientific handoff

- Final supervised windows: **17,600**
- Train/validation/test: **11,200 / 3,200 / 3,200**
- LSTM trainable parameters: **5,426**
- QLSTM trainable parameters: **5,422**
- Quantum parameters: **48**
- Closed-loop deterministic runs: **12**
- Independent primary families: **2**
- Fixed PI primary mean RMSE: **0.012478396116524 Hz**
- LSTM–PI primary mean RMSE: **0.013809947252480 Hz**
- QLSTM–PI primary mean RMSE: **0.016150128696581 Hz**

## Scientific claim freeze

- QLSTM superiority supported: **False**
- Statistical significance claimed: **False**
- Independent G3 generalization claimed: **False**
- Quantum advantage claimed: **False**
- Post-result retuning allowed: **False**
- Negative QLSTM result retained: **True**

## Historical provenance

The exact original Cell 1–138 execution history was not available during
migration. Those cell numbers were **not reconstructed by guesswork**.

The 05→06 boundary was reconstructed from frozen scientific artifact semantics.

Exact runtime source was preserved for:

- Cell 146–150/150-FIX;
- Cell 151–155;
- Cell 156–159-FIX.

Cell 159 is provenance only. Cell 159-FIX is authoritative.

## Reproducibility scope

The migrated notebook suite supports repository-based reproduction from frozen
artifacts and explicit reproduction switches. Expensive simulation/training is
disabled by default.

Cell 168 did not execute simulation, model training, model inference, PennyLane,
or thesis-result regeneration.
