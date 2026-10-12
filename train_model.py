"""
train_model.py
------------------------------
Creates a synthetic fraud dataset,
trains a Random Forest model,
evaluates it,
and saves the trained model.

Author: ChatGPT
"""

import random
import joblib
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

# ============================================================
# CONFIGURATION
# ============================================================

DATASET_SIZE = 10000

MODEL_FILE = "fraud_model.pkl"

CSV_FILE = "transactions.csv"

# ============================================================
# GENERATE DATASET
# ============================================================

transactions = []

for _ in range(DATASET_SIZE):

    amount = round(random.uniform(10, 15000), 2)

    hour = random.randint(0, 23)

    previous = random.randint(0, 40)

    international = random.randint(0, 1)

    new_device = random.randint(0, 1)

    high_risk_country = random.randint(0, 1)

    fraud_score = 0

    # ---------- Rules ----------

    if amount > 8000:
        fraud_score += 2

    elif amount > 5000:
        fraud_score += 1

    if hour <= 4:
        fraud_score += 1

    if previous == 0:
        fraud_score += 1

    if international:
        fraud_score += 2

    if new_device:
        fraud_score += 2

    if high_risk_country:
        fraud_score += 3

    # Random behaviour
    fraud_score += random.choice([0, 0, 0, 1])

    fraud = 1 if fraud_score >= 5 else 0

    transactions.append([

        amount,

        hour,

        previous,

        international,

        new_device,

        high_risk_country,

        fraud

    ])

# ============================================================
# SAVE DATASET
# ============================================================

columns = [

    "Amount",

    "Hour",

    "PreviousTransactions",

    "International",

    "NewDevice",

    "HighRiskCountry",

    "Fraud"

]

df = pd.DataFrame(transactions, columns=columns)

df.to_csv(CSV_FILE, index=False)

print("Dataset saved:", CSV_FILE)

# ============================================================
# SPLIT
# ============================================================

X = df.drop("Fraud", axis=1)

y = df["Fraud"]

X_train, X_test, y_train, y_test = train_test_split(

    X,

    y,

    test_size=0.20,

    random_state=42

)

# ============================================================
# TRAIN MODEL
# ============================================================

model = RandomForestClassifier(

    n_estimators=300,

    random_state=42

)

model.fit(X_train, y_train)

# ============================================================
# TEST
# ============================================================

predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

print("\nAccuracy")

print(f"{accuracy*100:.2f}%")

print("\nConfusion Matrix")

print(confusion_matrix(y_test, predictions))

print("\nClassification Report")

print(classification_report(y_test, predictions))

# ============================================================
# SAVE MODEL
# ============================================================

joblib.dump(model, MODEL_FILE)

print("\nModel saved as")

print(MODEL_FILE)