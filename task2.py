import tkinter as tk
from tkinter import messagebox
import random
import string

def generate_password():
    length = int(length_entry.get())
    use_letters = letters_var.get()
    use_numbers = numbers_var.get()
    use_symbols = symbols_var.get()
    exclude_chars = exclude_entry.get()

    characters = ""
    if use_letters:
        characters += string.ascii_letters
    if use_numbers:
        characters += string.digits
    if use_symbols:
        characters += string.punctuation

    characters = ''.join(c for c in characters if c not in exclude_chars)

    if not characters:
        messagebox.showerror("Error", "No valid characters selected!")
        return

    password = ''.join(random.choice(characters) for _ in range(length))
    password_entry.delete(0, tk.END)
    password_entry.insert(0, password)

def copy_to_clipboard():
    root.clipboard_clear()
    root.clipboard_append(password_entry.get())
    messagebox.showinfo("Copied", "Password copied to clipboard!")

# GUI Setup
root = tk.Tk()
root.title("Password Generator")

tk.Label(root, text="Length:").grid(row=0, column=0)
length_entry = tk.Entry(root)
length_entry.grid(row=0, column=1)

letters_var = tk.BooleanVar(value=True)
numbers_var = tk.BooleanVar(value=True)
symbols_var = tk.BooleanVar(value=True)

tk.Checkbutton(root, text="Letters", variable=letters_var).grid(row=1, column=0)
tk.Checkbutton(root, text="Numbers", variable=numbers_var).grid(row=1, column=1)
tk.Checkbutton(root, text="Symbols", variable=symbols_var).grid(row=1, column=2)

tk.Label(root, text="Exclude Characters:").grid(row=2, column=0)
exclude_entry = tk.Entry(root)
exclude_entry.grid(row=2, column=1, columnspan=2)

tk.Button(root, text="Generate Password", command=generate_password).grid(row=3, column=0, columnspan=3)
password_entry = tk.Entry(root, width=40)
password_entry.grid(row=4, column=0, columnspan=3)
tk.Button(root, text="Copy to Clipboard", command=copy_to_clipboard).grid(row=5, column=0, columnspan=3)

root.mainloop()
