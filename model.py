"""
model.py
---------

Loads the trained fraud detection model and performs predictions.

Author: ChatGPT
"""

import os
import joblib
import numpy as np


class FraudDetector:

    def __init__(self, model_path="fraud_model.pkl"):

        self.model = None

        if os.path.exists(model_path):
            self.model = joblib.load(model_path)

    ############################################################

    def is_model_loaded(self):

        return self.model is not None

    ############################################################

    def predict(self, values):

        """
        values =
        [
            Amount,
            Hour,
            PreviousTransactions,
            International,
            NewDevice,
            HighRiskCountry
        ]
        """

        if self.model is None:
            raise Exception(
                "Model not found.\n\nRun train_model.py first."
            )

        X = np.array(values).reshape(1, -1)

        prediction = int(self.model.predict(X)[0])

        probability = self.model.predict_proba(X)[0]

        confidence = float(max(probability))

        return prediction, confidence

    ############################################################

    def risk_factors(self, values):

        """
        Returns simple explanations
        regardless of ML algorithm.
        """

        amount = values[0]
        hour = values[1]
        previous = values[2]
        international = values[3]
        new_device = values[4]
        high_risk_country = values[5]

        reasons = []

        if amount > 5000:
            reasons.append("Large transaction amount")

        if hour <= 5:
            reasons.append("Transaction occurred late at night")

        if previous == 0:
            reasons.append("No previous transaction history")

        if international:
            reasons.append("International transaction")

        if new_device:
            reasons.append("New device used")

        if high_risk_country:
            reasons.append("High-risk country")

        if len(reasons) == 0:
            reasons.append("No obvious risk factors")

        return reasons

    ############################################################

    def risk_level(self, confidence):

        """
        Converts confidence into
        Low / Medium / High.
        """

        percent = confidence * 100

        if percent < 50:
            return "LOW"

        elif percent < 80:
            return "MEDIUM"

        return "HIGH"