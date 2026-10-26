"""
train_model.py
------------------------------
Creates a synthetic fraud dataset,
trains a Random Forest model,
evaluates it,
and saves the trained model.

Author: Kehinde_Oni

A rookie can follow the comments below step by step.
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

# How many fake transactions we will create
DATASET_SIZE = 10000

# Where to save the trained model
MODEL_FILE = "fraud_model.pkl"

# Where to save the generated dataset (so you can look at it)
CSV_FILE = "transactions.csv"

# ============================================================
# 1. GENERATE SYNTHETIC DATASET
# ============================================================
# We create fake data because we don't have real bank data.
# The rules below try to make the data look a bit realistic.

print("Generating synthetic transactions...")

transactions = []

for _ in range(DATASET_SIZE):

    # Random values for the features
    amount           = round(random.uniform(10, 15000), 2)
    hour             = random.randint(0, 23)
    previous         = random.randint(0, 40)
    international    = random.randint(0, 1)   # 0 or 1
    new_device       = random.randint(0, 1)   # 0 or 1
    high_risk_country = random.randint(0, 1)  # 0 or 1

    # Simple scoring system to decide if this transaction is fraud
    fraud_score = 0

    if amount > 8000:
        fraud_score += 2
    elif amount > 5000:
        fraud_score += 1

    if hour <= 4:                    # very late night
        fraud_score += 1

    if previous == 0:                # first-time customer
        fraud_score += 1

    if international:
        fraud_score += 2

    if new_device:
        fraud_score += 2

    if high_risk_country:
        fraud_score += 3

    # Add a little randomness so the data is not 100% rule-based
    fraud_score += random.choice([0, 0, 0, 1])

    # If the score is high enough, call it fraud
    fraud = 1 if fraud_score >= 5 else 0

    # Store the row
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
# 2. SAVE THE DATASET TO CSV
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
print(f"Dataset saved: {CSV_FILE}")

# ============================================================
# 3. SPLIT INTO TRAINING AND TEST SETS
# ============================================================
# X = the features the model will learn from
# y = the answer we want the model to predict (Fraud or not)

X = df.drop("Fraud", axis=1)
y = df["Fraud"]

# 80% for training, 20% for testing
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42   # so we get the same split every time
)

# ============================================================
# 4. TRAIN THE MODEL
# ============================================================
print("\nTraining Random Forest model...")

model = RandomForestClassifier(
    n_estimators=300,   # number of trees in the forest
    random_state=42
)

model.fit(X_train, y_train)

# ============================================================
# 5. EVALUATE THE MODEL
# ============================================================
print("\nEvaluating model...")

predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)
print(f"\nAccuracy: {accuracy*100:.2f}%")

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, predictions))

print("\nClassification Report:")
print(classification_report(y_test, predictions))

# ============================================================
# 6. SAVE THE TRAINED MODEL
# ============================================================
joblib.dump(model, MODEL_FILE)
print(f"\nModel saved as: {MODEL_FILE}")
print("You can now run app.py")
