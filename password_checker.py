import tkinter as tk
import re
import random
import string

# Optional: NLTK dictionary detection
try:
    import nltk
    from nltk.corpus import words
    nltk.download('words')
    word_list = set(words.words())
except:
    word_list = set()

def check_password_strength(password):
    result = ""
    suggestions = []

    if len(password) < 8:
        result = "Weak"
        suggestions.append("Use at least 8 characters.")
    else:
        has_upper = re.search(r"[A-Z]", password)
        has_lower = re.search(r"[a-z]", password)
        has_digit = re.search(r"[0-9]", password)
        has_special = re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)

        if all([has_upper, has_lower, has_digit, has_special]):
            result = "Strong"
        else:
            result = "Moderate"
            if not has_upper:
                suggestions.append("Add an uppercase letter.")
            if not has_lower:
                suggestions.append("Add a lowercase letter.")
            if not has_digit:
                suggestions.append("Add a number.")
            if not has_special:
                suggestions.append("Add a special character.")

    if word_list and password.lower() in word_list:
        result = "Weak"
        suggestions.append("Avoid dictionary words.")

    return result, suggestions

def analyze_password():
    password = entry.get()
    strength, suggestions = check_password_strength(password)
    color = {"Weak": "red", "Moderate": "orange", "Strong": "green"}.get(strength, "black")

    result_label.config(text=f"Strength: {strength}", fg=color)

    if suggestions:
        suggestion_label.config(text="Suggestions:\n- " + "\n- ".join(suggestions))
    else:
        suggestion_label.config(text="Great password!")

def generate_custom_password():
    length = length_var.get()
    try:
        length = int(length)
        if length < 4:
            raise ValueError
    except ValueError:
        result_label.config(text="Please enter valid length (>=4)", fg="red")
        return

    chars = ""
    if var_upper.get():
        chars += string.ascii_uppercase
    if var_lower.get():
        chars += string.ascii_lowercase
    if var_digits.get():
        chars += string.digits
    if var_special.get():
        chars += "!@#$%^&*()_+-=[]{}|;:,.<>?/"

    if not chars:
        result_label.config(text="Select at least one character type.", fg="red")
        return

    # Ensure at least one character from each selected set is included
    password = []
    if var_upper.get(): password.append(random.choice(string.ascii_uppercase))
    if var_lower.get(): password.append(random.choice(string.ascii_lowercase))
    if var_digits.get(): password.append(random.choice(string.digits))
    if var_special.get(): password.append(random.choice("!@#$%^&*()_+-=[]{}|;:,.<>?/"))

    while len(password) < length:
        password.append(random.choice(chars))

    random.shuffle(password)
    final_password = ''.join(password)

    entry.delete(0, tk.END)
    entry.insert(0, final_password)
    analyze_password()

def show_password():
    if show_var.get():
        entry.config(show="")
    else:
        entry.config(show="*")

def copy_to_clipboard():
    password = entry.get()
    if password:
        app.clipboard_clear()
        app.clipboard_append(password)
        result_label.config(text="Password copied!", fg="blue")
    else:
        result_label.config(text="No password to copy!", fg="red")

# ---------------- GUI ----------------

app = tk.Tk()
app.title("Password Strength Checker")
app.geometry("520x540")
app.configure(bg="#e6f2ff")

# Title
tk.Label(app, text="Password Strength Checker", font=("Segoe UI", 16, "bold"), bg="#e6f2ff", fg="#003366").pack(pady=15)

# Entry Box
tk.Label(app, text="Enter your password:", font=("Segoe UI", 12), bg="#e6f2ff").pack(pady=(5, 2))
entry = tk.Entry(app, show="*", width=30, font=("Segoe UI", 12), relief="solid", bd=2)
entry.pack(pady=5)

# Show/Hide Password checkbox
show_var = tk.BooleanVar(value=False)
tk.Checkbutton(app, text="Show Password", variable=show_var, command=show_password, bg="#e6f2ff", font=("Segoe UI", 10)).pack(pady=2)

# --- Custom Generation Settings ---
tk.Label(app, text="Custom Password Generator", font=("Segoe UI", 12, "bold"), bg="#e6f2ff", fg="#003366").pack(pady=10)

settings_frame = tk.Frame(app, bg="#e6f2ff")
settings_frame.pack(pady=5)

tk.Label(settings_frame, text="Length:", font=("Segoe UI", 11), bg="#e6f2ff").grid(row=0, column=0, padx=5, sticky="w")
length_var = tk.StringVar(value="12")
tk.Entry(settings_frame, textvariable=length_var, width=5, font=("Segoe UI", 11)).grid(row=0, column=1, padx=5)

var_upper = tk.BooleanVar(value=True)
var_lower = tk.BooleanVar(value=True)
var_digits = tk.BooleanVar(value=True)
var_special = tk.BooleanVar(value=True)

tk.Checkbutton(settings_frame, text="Uppercase", variable=var_upper, bg="#e6f2ff", font=("Segoe UI", 10)).grid(row=1, column=0, sticky="w")
tk.Checkbutton(settings_frame, text="Lowercase", variable=var_lower, bg="#e6f2ff", font=("Segoe UI", 10)).grid(row=1, column=1, sticky="w")
tk.Checkbutton(settings_frame, text="Numbers", variable=var_digits, bg="#e6f2ff", font=("Segoe UI", 10)).grid(row=2, column=0, sticky="w")
tk.Checkbutton(settings_frame, text="Special", variable=var_special, bg="#e6f2ff", font=("Segoe UI", 10)).grid(row=2, column=1, sticky="w")

# --- Buttons ---
btn_frame = tk.Frame(app, bg="#e6f2ff")
btn_frame.pack(pady=15)

tk.Button(btn_frame, text="Check Strength", font=("Segoe UI", 11, "bold"), bg="#0066cc", fg="white", padx=10, pady=5, command=analyze_password).grid(row=0, column=0, padx=10)
tk.Button(btn_frame, text="Generate Custom Password", font=("Segoe UI", 11), bg="#00b300", fg="white", padx=10, pady=5, command=generate_custom_password).grid(row=0, column=1, padx=10)

tk.Button(btn_frame, text="Copy to Clipboard", font=("Segoe UI", 11), bg="#ffaa00", fg="black", padx=10, pady=5, command=copy_to_clipboard).grid(row=1, column=0, columnspan=2, pady=10)

# --- Results ---
result_label = tk.Label(app, text="", font=("Segoe UI", 13, "bold"), bg="#e6f2ff")
result_label.pack(pady=5)

suggestion_label = tk.Label(app, text="", font=("Segoe UI", 10), wraplength=450, justify="left", fg="#333333", bg="#e6f2ff")
suggestion_label.pack(pady=10)

app.mainloop()