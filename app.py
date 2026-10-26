"""
Fraud Detection System
----------------------
Part 1 - User Interface (with Risk Analysis widget)

Author: Kehinde_Oni

This app lets a user enter transaction details,
then uses a trained machine learning model to
predict if the transaction is FRAUD or LEGITIMATE.

A rookie can follow the comments below.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
from datetime import datetime

# Import our own FraudDetector class from model.py
from model import FraudDetector


class FraudDetectionApp:

    def __init__(self):
        # Create the detector (it loads fraud_model.pkl if it exists)
        self.detector = FraudDetector()

        # Create the main window
        self.root = tk.Tk()
        self.root.title("Fraud Detection System")
        self.root.geometry("1000x820")          # a bit taller for the new widget
        self.root.minsize(950, 740)
        self.root.configure(bg="#ECEFF4")

        # List that stores every prediction we make (for export)
        self.history = []

        # Build the visual style and all the widgets
        self.create_style()
        self.create_widgets()

    # ------------------------------------------------------------------
    # STYLE
    # ------------------------------------------------------------------
    def create_style(self):
        """Set colors and fonts so the app looks clean."""
        self.style = ttk.Style()
        self.style.theme_use("clam")

        self.style.configure(
            "Title.TLabel",
            font=("Segoe UI", 24, "bold"),
            background="#1976D2",
            foreground="white"
        )
        self.style.configure(
            "Subtitle.TLabel",
            font=("Segoe UI", 11),
            background="#1976D2",
            foreground="white"
        )
        self.style.configure("Card.TFrame", background="white")
        self.style.configure("TLabel", font=("Segoe UI", 10))
        self.style.configure(
            "Header.TLabel",
            font=("Segoe UI", 13, "bold"),
            background="white"
        )
        self.style.configure(
            "Predict.TButton",
            font=("Segoe UI", 11, "bold")
        )

    # ------------------------------------------------------------------
    # WIDGETS
    # ------------------------------------------------------------------
    def create_widgets(self):
        """Create every button, label, entry box, etc."""

        # ==================== HEADER ====================
        header = tk.Frame(self.root, bg="#1976D2", height=90)
        header.pack(fill="x")

        ttk.Label(
            header,
            text="Fraud Detection System",
            style="Title.TLabel"
        ).pack(pady=(12, 0))

        ttk.Label(
            header,
            text="Machine Learning Based Transaction Analysis",
            style="Subtitle.TLabel"
        ).pack()

        # ==================== MAIN AREA ====================
        main = tk.Frame(self.root, bg="#ECEFF4")
        main.pack(fill="both", expand=True, padx=20, pady=20)

        # ---------- LEFT PANEL (input form) ----------
        left = ttk.Frame(main, style="Card.TFrame", padding=20)
        left.pack(side="left", fill="y")

        ttk.Label(
            left,
            text="Transaction Details",
            style="Header.TLabel"
        ).grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Amount
        ttk.Label(left, text="Amount").grid(row=1, column=0, sticky="w", pady=8)
        self.amount = ttk.Entry(left, width=25)
        self.amount.grid(row=1, column=1)

        # Hour (0-23)
        ttk.Label(left, text="Hour (0-23)").grid(row=2, column=0, sticky="w", pady=8)
        self.hour = ttk.Entry(left, width=25)
        self.hour.grid(row=2, column=1)

        # Previous Transactions
        ttk.Label(left, text="Previous Transactions").grid(row=3, column=0, sticky="w", pady=8)
        self.previous = ttk.Entry(left, width=25)
        self.previous.grid(row=3, column=1)

        # International (Yes/No radio buttons)
        ttk.Label(left, text="International").grid(row=4, column=0, sticky="w", pady=8)
        self.international = tk.IntVar(value=0)
        ttk.Radiobutton(left, text="No",  variable=self.international, value=0).grid(row=4, column=1, sticky="w")
        ttk.Radiobutton(left, text="Yes", variable=self.international, value=1).grid(row=4, column=1, sticky="e")

        # New Device
        ttk.Label(left, text="New Device").grid(row=5, column=0, sticky="w", pady=8)
        self.device = tk.IntVar(value=0)
        ttk.Radiobutton(left, text="No",  variable=self.device, value=0).grid(row=5, column=1, sticky="w")
        ttk.Radiobutton(left, text="Yes", variable=self.device, value=1).grid(row=5, column=1, sticky="e")

        # High Risk Country
        ttk.Label(left, text="High Risk Country").grid(row=6, column=0, sticky="w", pady=8)
        self.country = tk.IntVar(value=0)
        ttk.Radiobutton(left, text="No",  variable=self.country, value=0).grid(row=6, column=1, sticky="w")
        ttk.Radiobutton(left, text="Yes", variable=self.country, value=1).grid(row=6, column=1, sticky="e")

        # Buttons
        ttk.Button(
            left,
            text="Predict",
            style="Predict.TButton",
            command=self.predict
        ).grid(row=7, column=0, columnspan=2, pady=(30, 10), sticky="ew")

        ttk.Button(
            left,
            text="Clear",
            command=self.clear
        ).grid(row=8, column=0, columnspan=2, sticky="ew")

        ttk.Button(
            left,
            text="Export History",
            command=self.export_history
        ).grid(row=9, column=0, columnspan=2, pady=10, sticky="ew")

        # ---------- RIGHT PANEL (results) ----------
        right = ttk.Frame(main, style="Card.TFrame", padding=20)
        right.pack(side="left", fill="both", expand=True, padx=(20, 0))

        # Prediction status
        ttk.Label(right, text="Prediction", style="Header.TLabel").pack(anchor="w")

        self.status = tk.Label(
            right,
            text="Waiting...",
            font=("Segoe UI", 18, "bold"),
            fg="blue",
            bg="white"
        )
        self.status.pack(pady=20)

        # Confidence
        ttk.Label(right, text="Confidence").pack(anchor="w")
        self.confidence = tk.Label(
            right,
            text="0%",
            font=("Segoe UI", 16),
            bg="white"
        )
        self.confidence.pack(anchor="w")

        # Progress bar (visual risk score)
        ttk.Label(right, text="Risk Score").pack(anchor="w", pady=(20, 5))
        self.progress = ttk.Progressbar(
            right,
            orient="horizontal",
            mode="determinate",
            length=400
        )
        self.progress.pack(fill="x")

        # ========== NEW WIDGET: RISK ANALYSIS ==========
        # This is the small but noticeable addition.
        # It shows the risk level (LOW/MEDIUM/HIGH) and the reasons.
        ttk.Label(
            right,
            text="Risk Analysis",
            style="Header.TLabel"
        ).pack(anchor="w", pady=(20, 5))

        # Colored label that shows LOW / MEDIUM / HIGH
        self.risk_level = tk.Label(
            right,
            text="—",
            font=("Segoe UI", 14, "bold"),
            bg="white",
            fg="#555555"
        )
        self.risk_level.pack(anchor="w")

        # Listbox that will hold the risk-factor sentences
        self.risk_factors = tk.Listbox(
            right,
            height=4,
            font=("Segoe UI", 9),
            activestyle="none",
            bg="#F7F9FC",
            relief="flat",
            highlightthickness=1,
            highlightbackground="#E0E0E0"
        )
        self.risk_factors.pack(fill="x", pady=(4, 10))
        # ===============================================

        # History table
        ttk.Label(
            right,
            text="Prediction History",
            style="Header.TLabel"
        ).pack(anchor="w", pady=(15, 10))

        columns = ("Time", "Amount", "Result", "Confidence")
        self.table = ttk.Treeview(
            right,
            columns=columns,
            show="headings",
            height=8
        )
        for col in columns:
            self.table.heading(col, text=col)
            self.table.column(col, anchor="center", width=120)
        self.table.pack(fill="both", expand=True)

    # ------------------------------------------------------------------
    # HELPER METHODS
    # ------------------------------------------------------------------
    def get_input_values(self):
        """
        Read the form, check that the numbers are valid,
        and return them as a list.
        Returns None if something is wrong.
        """
        try:
            amount   = float(self.amount.get())
            hour     = int(self.hour.get())
            previous = int(self.previous.get())

            if amount < 0:
                raise ValueError("Amount cannot be negative")

            if hour < 0 or hour > 23:
                messagebox.showerror("Invalid Hour", "Hour must be between 0 and 23.")
                return None

            if previous < 0:
                raise ValueError("Previous transactions cannot be negative")

            # The six features the model expects
            values = [
                amount,
                hour,
                previous,
                self.international.get(),   # 0 or 1
                self.device.get(),          # 0 or 1
                self.country.get()          # 0 or 1
            ]
            return values

        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                "Please enter valid numeric values."
            )
            return None

    def predict(self):
        """
        Called when the user clicks the Predict button.
        1. Get the input values
        2. Ask the model for a prediction
        3. Show the result, confidence, risk level and reasons
        4. Add the row to the history table
        """
        values = self.get_input_values()
        if values is None:
            return   # stop if the input was bad

        try:
            # Ask the model
            prediction, confidence = self.detector.predict(values)
            risk    = self.detector.risk_level(confidence)
            reasons = self.detector.risk_factors(values)
        except Exception as e:
            messagebox.showerror("Prediction Error", str(e))
            return

        # Turn confidence into a percentage (0-100)
        confidence_percent = confidence * 100
        self.progress["value"] = confidence_percent

        # Update the big status label
        if prediction == 1:
            self.status.config(text="⚠ FRAUD DETECTED", fg="red")
        else:
            self.status.config(text="✓ LEGITIMATE", fg="green")

        # Update confidence text
        self.confidence.config(text=f"{confidence_percent:.2f}%")

        # ---------- Update the new Risk Analysis widget ----------
        risk_colors = {
            "LOW":    "#2E7D32",   # green
            "MEDIUM": "#EF6C00",   # orange
            "HIGH":   "#C62828"    # red
        }
        self.risk_level.config(
            text=risk,
            fg=risk_colors.get(risk, "#555555")
        )

        # Clear old reasons and insert the new ones
        self.risk_factors.delete(0, tk.END)
        for reason in reasons:
            self.risk_factors.insert(tk.END, f"• {reason}")
        # ---------------------------------------------------------

        # Add to the history table
        now = datetime.now().strftime("%H:%M:%S")
        self.table.insert(
            "",
            tk.END,
            values=(
                now,
                f"{values[0]:,.2f}",
                "Fraud" if prediction else "Legitimate",
                f"{confidence_percent:.2f}%"
            )
        )

        # Keep a copy for CSV export
        self.history.append([
            now,
            values[0],
            prediction,
            confidence_percent
        ])

    def clear(self):
        """Reset the form and all result displays."""
        self.amount.delete(0, tk.END)
        self.hour.delete(0, tk.END)
        self.previous.delete(0, tk.END)
        self.international.set(0)
        self.device.set(0)
        self.country.set(0)

        self.status.config(text="Waiting...", fg="blue")
        self.confidence.config(text="0%")
        self.progress["value"] = 0

        # Reset the Risk Analysis widget too
        self.risk_level.config(text="—", fg="#555555")
        self.risk_factors.delete(0, tk.END)

    def export_history(self):
        """Save the prediction history to a CSV file."""
        if len(self.history) == 0:
            messagebox.showinfo("History", "Nothing to export.")
            return

        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV File", "*.csv")]
        )
        if filename == "":
            return   # user cancelled

        with open(filename, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Time", "Amount", "Prediction", "Confidence"])
            for row in self.history:
                writer.writerow(row)

        messagebox.showinfo(
            "Export Complete",
            "Prediction history exported successfully."
        )


# ----------------------------------------------------------------------
# START THE APP
# ----------------------------------------------------------------------
if __name__ == "__main__":
    app = FraudDetectionApp()
    app.root.mainloop()
