import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
import sqlite3
import matplotlib.pyplot as plt
import csv

# ------------------ Database Setup ------------------
conn = sqlite3.connect("bmi_data.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS bmi_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    weight REAL NOT NULL,
    height REAL NOT NULL,
    bmi REAL NOT NULL,
    category TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")
conn.commit()

# ------------------ BMI Calculation ------------------
def calculate_bmi():
    username = entry_user.get().strip()
    if not username:
        messagebox.showerror("Error", "Please enter a username.")
        return

    try:
        weight = float(entry_weight.get())
        height = float(entry_height.get())

        if weight <= 0 or height <= 0:
            messagebox.showerror("Error", "Weight and height must be positive numbers.")
            return

        bmi = weight / (height ** 2)

        # Categorization
        if bmi < 18.5:
            category = "Underweight"
        elif 18.5 <= bmi < 24.9:
            category = "Normal weight"
        elif 25 <= bmi < 29.9:
            category = "Overweight"
        else:
            category = "Obese"

        # Display result
        result_label.config(text=f"BMI: {bmi:.2f} ({category})")

        # Store in database
        cursor.execute(
            "INSERT INTO bmi_records (username, weight, height, bmi, category) VALUES (?, ?, ?, ?, ?)",
            (username, weight, height, bmi, category)
        )
        conn.commit()

    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers.")

# ------------------ Show History ------------------
def show_history():
    username = simpledialog.askstring("Input", "Enter username to view history:")
    if not username:
        return

    cursor.execute("SELECT bmi, category, timestamp FROM bmi_records WHERE username=? ORDER BY timestamp", (username,))
    records = cursor.fetchall()

    if not records:
        messagebox.showinfo("History", "No records found for this user.")
        return

    # Show in graph
    bmi_values = [r[0] for r in records]
    timestamps = [r[2] for r in records]

    plt.figure(figsize=(8,5))
    plt.plot(timestamps, bmi_values, marker='o', linestyle='-', color='blue')
    plt.title(f"{username}'s BMI Trend Over Time")
    plt.xlabel("Timestamp")
    plt.ylabel("BMI")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# ------------------ Export to CSV ------------------
def export_to_csv():
    username = simpledialog.askstring("Input", "Enter username to export history:")
    if not username:
        return

    cursor.execute("SELECT weight, height, bmi, category, timestamp FROM bmi_records WHERE username=? ORDER BY timestamp", (username,))
    records = cursor.fetchall()

    if not records:
        messagebox.showinfo("Export", "No records found to export.")
        return

    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files","*.csv")])
    if not file_path:
        return

    with open(file_path, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Weight", "Height", "BMI", "Category", "Timestamp"])
        writer.writerows(records)

    messagebox.showinfo("Export", f"History exported successfully to {file_path}")

# ------------------ Feedback ------------------
def feedback():
    user_feedback = simpledialog.askstring("Feedback", "Please enter your feedback:")
    if not user_feedback:
        return
    # For simplicity, save feedback in a text file
    with open("feedback.txt", "a") as f:
        f.write(user_feedback + "\n")
    messagebox.showinfo("Feedback", "Thank you for your feedback!")

# ------------------ GUI Setup ------------------
root = tk.Tk()
root.title("Advanced BMI Calculator with Export & Feedback")

# User Entry
tk.Label(root, text="Username:").grid(row=0, column=0, padx=10, pady=5)
entry_user = tk.Entry(root)
entry_user.grid(row=0, column=1, padx=10, pady=5)

# Weight Entry
tk.Label(root, text="Weight (kg):").grid(row=1, column=0, padx=10, pady=5)
entry_weight = tk.Entry(root)
entry_weight.grid(row=1, column=1, padx=10, pady=5)

# Height Entry
tk.Label(root, text="Height (m):").grid(row=2, column=0, padx=10, pady=5)
entry_height = tk.Entry(root)
entry_height.grid(row=2, column=1, padx=10, pady=5)

# Buttons
tk.Button(root, text="Calculate BMI", command=calculate_bmi).grid(row=3, column=0, columnspan=2, pady=10)
tk.Button(root, text="Show History", command=show_history).grid(row=4, column=0, columnspan=2, pady=5)
tk.Button(root, text="Export to CSV", command=export_to_csv).grid(row=5, column=0, columnspan=2, pady=5)
tk.Button(root, text="Feedback", command=feedback).grid(row=6, column=0, columnspan=2, pady=5)

# Result Label
result_label = tk.Label(root, text="BMI: --")
result_label.grid(row=7, column=0, columnspan=2, pady=5)

root.mainloop()

# Close database connection
conn.close()
