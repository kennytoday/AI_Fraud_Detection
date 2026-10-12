# Fraud Detection System

A desktop application for analyzing individual transactions for fraud risk, built with Python and Tkinter for the interface and a scikit-learn model for prediction.

## Overview

The app takes in details about a single transaction, runs them through a trained classifier, and shows:
- A fraud / legitimate verdict
- A confidence score (how likely the transaction is fraudulent)
- A risk level (Low / Medium / High / Critical)
- The specific factors that drove the result
- A running history of predictions made during the session, exportable to CSV

## Files

| File | Purpose |
|---|---|
| `app.py` | Tkinter UI — collects transaction details, displays results, manages history and CSV export |
| `model.py` | `FraudDetector` class — trains (or loads) a `RandomForestClassifier` and exposes `predict`, `risk_level`, and `risk_factors` |
| `fraud_model.pkl` | Auto-generated on first run — the cached trained model, so training only happens once |

## Requirements

```
pip install scikit-learn numpy joblib
```

Tkinter ships with most standard Python installs; if it's missing on Linux, install it via your package manager (e.g. `sudo apt install python3-tk`).

## Running it

```
python3 app.py
```

On first launch, `model.py` trains a new model on synthetic transaction data and saves it as `fraud_model.pkl` in the same folder. Subsequent launches load that file directly, so startup is fast after the first run.

## Using the app

1. Enter the transaction **Amount**, **Hour (0–23)**, and number of **Previous Transactions** for the account.
2. Select **Yes/No** for whether the transaction is **International**, from a **New Device**, or from a **High Risk Country**.
3. Click **Predict** to see the verdict, confidence, and risk factors.
4. Click **Clear** to reset the form.
5. Click **Export History** to save every prediction made this session to a CSV file.

## About the model

`FraudDetector` is currently trained on **synthetically generated data**, not real transactions. The synthetic data is built so that fraud likelihood rises with:
- Higher transaction amounts
- Late-night / early-morning hours (0–5)
- Thin transaction history (few previous transactions)
- International transactions
- New devices
- High-risk countries

This makes the model behave sensibly for testing and demoing the UI, but it should **not** be treated as production-accurate. To use it on real data, replace `_generate_dataset()` in `model.py` with a loader for your actual labeled transaction dataset, then delete `fraud_model.pkl` so it retrains.

## Known limitations

- No persistence of prediction history between sessions (it's in-memory only, cleared on close — use Export History to keep a record)
- Single-transaction predictions only; no batch/CSV upload for scoring multiple transactions at once
- Model is a demo baseline, not tuned or validated against real fraud data
