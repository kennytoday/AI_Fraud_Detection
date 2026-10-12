"""
Fraud Detection System
----------------------
Part 1 - User Interface

Author: ChatGPT

"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
from datetime import datetime

# We'll create this later
from model import FraudDetector


class FraudDetectionApp:

    def __init__(self):

        self.detector = FraudDetector()

        self.root = tk.Tk()
        self.root.title("Fraud Detection System")

        self.root.geometry("1000x760")
        self.root.minsize(950,700)
        self.root.configure(bg="#ECEFF4")

        self.history = []

        self.create_style()
        self.create_widgets()



    ##########################################################

    def create_style(self):

        self.style = ttk.Style()

        self.style.theme_use("clam")

        self.style.configure(
            "Title.TLabel",
            font=("Segoe UI",24,"bold"),
            background="#1976D2",
            foreground="white"
        )

        self.style.configure(
            "Subtitle.TLabel",
            font=("Segoe UI",11),
            background="#1976D2",
            foreground="white"
        )

        self.style.configure(
            "Card.TFrame",
            background="white"
        )

        self.style.configure(
            "TLabel",
            font=("Segoe UI",10)
        )

        self.style.configure(
            "Header.TLabel",
            font=("Segoe UI",13,"bold"),
            background="white"
        )

        self.style.configure(
            "Predict.TButton",
            font=("Segoe UI",11,"bold")
        )

    ##########################################################

    def create_widgets(self):

        ###########################################
        # HEADER
        ###########################################

        header = tk.Frame(
            self.root,
            bg="#1976D2",
            height=90
        )

        header.pack(fill="x")

        ttk.Label(
            header,
            text="Fraud Detection System",
            style="Title.TLabel"
        ).pack(pady=(12,0))

        ttk.Label(
            header,
            text="Machine Learning Based Transaction Analysis",
            style="Subtitle.TLabel"
        ).pack()

        ###########################################
        # MAIN FRAME
        ###########################################

        main = tk.Frame(
            self.root,
            bg="#ECEFF4"
        )

        main.pack(fill="both",expand=True,padx=20,pady=20)

        ###########################################
        # LEFT SIDE
        ###########################################

        left = ttk.Frame(
            main,
            style="Card.TFrame",
            padding=20
        )

        left.pack(side="left",fill="y")

        ttk.Label(
            left,
            text="Transaction Details",
            style="Header.TLabel"
        ).grid(row=0,column=0,columnspan=2,pady=(0,20))

        #################################################

        ttk.Label(left,text="Amount").grid(
            row=1,
            column=0,
            sticky="w",
            pady=8
        )

        self.amount = ttk.Entry(left,width=25)

        self.amount.grid(row=1,column=1)

        #################################################

        ttk.Label(left,text="Hour (0-23)").grid(
            row=2,
            column=0,
            sticky="w",
            pady=8
        )

        self.hour = ttk.Entry(left,width=25)

        self.hour.grid(row=2,column=1)

        #################################################

        ttk.Label(left,text="Previous Transactions").grid(
            row=3,
            column=0,
            sticky="w",
            pady=8
        )

        self.previous = ttk.Entry(left,width=25)

        self.previous.grid(row=3,column=1)

        #################################################

        ttk.Label(left,text="International").grid(
            row=4,
            column=0,
            sticky="w",
            pady=8
        )

        self.international = tk.IntVar(value=0)

        ttk.Radiobutton(
            left,
            text="No",
            variable=self.international,
            value=0
        ).grid(row=4,column=1,sticky="w")

        ttk.Radiobutton(
            left,
            text="Yes",
            variable=self.international,
            value=1
        ).grid(row=4,column=1,sticky="e")

        #################################################

        ttk.Label(left,text="New Device").grid(
            row=5,
            column=0,
            sticky="w",
            pady=8
        )

        self.device = tk.IntVar(value=0)

        ttk.Radiobutton(
            left,
            text="No",
            variable=self.device,
            value=0
        ).grid(row=5,column=1,sticky="w")

        ttk.Radiobutton(
            left,
            text="Yes",
            variable=self.device,
            value=1
        ).grid(row=5,column=1,sticky="e")

        #################################################

        ttk.Label(left,text="High Risk Country").grid(
            row=6,
            column=0,
            sticky="w",
            pady=8
        )

        self.country = tk.IntVar(value=0)

        ttk.Radiobutton(
            left,
            text="No",
            variable=self.country,
            value=0
        ).grid(row=6,column=1,sticky="w")

        ttk.Radiobutton(
            left,
            text="Yes",
            variable=self.country,
            value=1
        ).grid(row=6,column=1,sticky="e")

        #################################################

        ttk.Button(
            left,
            text="Predict",
            style="Predict.TButton",
            command=self.predict
        ).grid(
            row=7,
            column=0,
            columnspan=2,
            pady=(30,10),
            sticky="ew"
        )

        ttk.Button(
            left,
            text="Clear",
            command=self.clear
        ).grid(
            row=8,
            column=0,
            columnspan=2,
            sticky="ew"
        )

        ttk.Button(
            left,
            text="Export History",
            command=self.export_history
        ).grid(
            row=9,
            column=0,
            columnspan=2,
            pady=10,
            sticky="ew"
        )

        ###########################################
        # RIGHT SIDE
        ###########################################

        right = ttk.Frame(
            main,
            style="Card.TFrame",
            padding=20
        )

        right.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(20,0)
        )

        ttk.Label(
            right,
            text="Prediction",
            style="Header.TLabel"
        ).pack(anchor="w")

        self.status = tk.Label(
            right,
            text="Waiting...",
            font=("Segoe UI",18,"bold"),
            fg="blue",
            bg="white"
        )

        self.status.pack(pady=20)

        ttk.Label(
            right,
            text="Confidence"
        ).pack(anchor="w")

        self.confidence = tk.Label(
            right,
            text="0%",
            font=("Segoe UI",16),
            bg="white"
        )

        self.confidence.pack(anchor="w")

        ttk.Label(
            right,
            text="Risk Score"
        ).pack(anchor="w",pady=(20,5))

        self.progress = ttk.Progressbar(
            right,
            orient="horizontal",
            mode="determinate",
            length=400
        )

        self.progress.pack(fill="x")

        ###########################################
        # HISTORY TABLE
        ###########################################

        ttk.Label(
            right,
            text="Prediction History",
            style="Header.TLabel"
        ).pack(anchor="w",pady=(30,10))

        columns = (
            "Time",
            "Amount",
            "Result",
            "Confidence"
        )

        self.table = ttk.Treeview(
            right,
            columns=columns,
            show="headings",
            height=12
        )

        for col in columns:

            self.table.heading(col,text=col)

            self.table.column(
                col,
                anchor="center",
                width=120
            )

        self.table.pack(fill="both",expand=True)

    ##########################################################
    # These methods will be completed in Part 2
    ##########################################################
    ##########################################################
    # Validate Input
    ##########################################################

    def get_input_values(self):

        try:

            amount = float(self.amount.get())

            hour = int(self.hour.get())

            previous = int(self.previous.get())

            if amount < 0:
                raise ValueError

            if hour < 0 or hour > 23:
                messagebox.showerror(
                    "Invalid Hour",
                    "Hour must be between 0 and 23."
                )
                return None

            if previous < 0:
                raise ValueError

            values = [

                amount,

                hour,

                previous,

                self.international.get(),

                self.device.get(),

                self.country.get()

            ]

            return values

        except ValueError:

            messagebox.showerror(

                "Invalid Input",

                "Please enter valid numeric values."

            )

            return None
    def predict(self):

        values = self.get_input_values()

        if values is None:
            return

        try:

            prediction, confidence = self.detector.predict(values)

            risk = self.detector.risk_level(confidence)

            reasons = self.detector.risk_factors(values)

        except Exception as e:

            messagebox.showerror(

                "Prediction Error",

                str(e)

            )

            return

        confidence_percent = confidence * 100

        self.progress["value"] = confidence_percent

        if prediction == 1:

            self.status.config(

                text="⚠ FRAUD DETECTED",

                fg="red"

            )

        else:

            self.status.config(

                text="✓ LEGITIMATE",

                fg="green"

            )

        self.confidence.config(

            text=f"{confidence_percent:.2f}%"

        )

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

        self.history.append([

            now,

            values[0],

            prediction,

            confidence_percent

        ])

    def clear(self):

        self.amount.delete(0, tk.END)

        self.hour.delete(0, tk.END)

        self.previous.delete(0, tk.END)

        self.international.set(0)

        self.device.set(0)

        self.country.set(0)

        self.status.config(

            text="Waiting...",

            fg="blue"

        )

        self.confidence.config(

            text="0%"

        )

        self.progress["value"] = 0

    def export_history(self):

        if len(self.history) == 0:

            messagebox.showinfo(

                "History",

                "Nothing to export."

            )

            return

        filename = filedialog.asksaveasfilename(

            defaultextension=".csv",

            filetypes=[

                ("CSV File","*.csv")

            ]

        )

        if filename == "":
            return

        with open(

            filename,

            "w",

            newline=""

        ) as file:

            writer = csv.writer(file)

            writer.writerow([

                "Time",

                "Amount",

                "Prediction",

                "Confidence"

            ])

            for row in self.history:

                writer.writerow(row)

        messagebox.showinfo(

            "Export Complete",

            "Prediction history exported successfully."

        )


# if __name__ == "__main__":
#     FraudDetectionApp()


if __name__ == "__main__":
    app = FraudDetectionApp()
    app.root.mainloop()