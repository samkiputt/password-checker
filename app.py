import customtkinter as ctk
from tkinter import messagebox
import re
import hashlib
import random
import string
import math  


ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Password Checker")
app.geometry("500x450")


COMMON_PASSWORDS = {
    "password", "password1", "password123", "123456", "12345678",
    "123456789", "1234567890", "12345", "qwerty", "qwerty123",
    "abc123", "admin", "admin123", "letmein", "welcome", "monkey",
    "dragon", "master", "login", "princess", "football", "iloveyou",
    "sunshine", "shadow", "superman", "michael", "654321", "111111",
    "000000", "123123", "666666", "121212", "987654321", "whatever",
    "trustno1", "passw0rd", "zaq12wsx", "P@ssw0rd", "password1!",
    "changeme", "test", "test123", "guest", "hello", "hello123",
    "batman", "starwars", "soccer", "baseball", "hockey", "jordan"
}

SEQUENCES = "abcdefghijklmnopqrstuvwxyz0123456789"
KEYBOARD_ROWS = ["qwertyuiop", "asdfghjkl", "zxcvbnm", "1234567890"]
SYMBOLS = r'[!@#$%^&*(),.?":{}|<>]'


def contains_sequence(password):
    
    pwd = password.lower()
    for i in range(len(pwd) - 2):
        chunk = pwd[i:i + 3]
        if chunk in SEQUENCES or chunk[::-1] in SEQUENCES:
            return True
    return False


def contains_keyboard_pattern(password):
    
    pwd = password.lower()
    for i in range(len(pwd) - 2):
        chunk = pwd[i:i + 3]
        for row in KEYBOARD_ROWS:
            if chunk in row or chunk[::-1] in row:
                return True
    return False


def has_repeated_chars(password):
    """Deteksi pengulangan karakter (aaa, 1111)."""
    return re.search(r'(.)\1{2,}', password) is not None


def has_leet_substitution(password):
    
    leet = password.lower()
    leet = leet.replace("4", "a").replace("1", "l").replace("3", "e")
    leet = leet.replace("0", "o").replace("5", "s").replace("7", "t")
    leet = leet.replace("$", "s").replace("@", "a").replace("!", "i")
    return leet in COMMON_PASSWORDS or any(
        w in leet for w in ("password", "admin", "qwerty", "letmein",
                            "welcome", "iloveyou", "monkey", "dragon")
    )


def estimate_entropy(password):
    
    pool = 0
    if re.search(r'[a-z]', password):
        pool += 26
    if re.search(r'[A-Z]', password):
        pool += 26
    if re.search(r'[0-9]', password):
        pool += 10
    if re.search(SYMBOLS, password):
        pool += 33
    if pool == 0:
        return 0
    return len(password) * math.log2(pool)


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def suggest_password(password):
    
    if password.lower() in COMMON_PASSWORDS or len(password) < 8:
        length = max(12, len(password))
        chars = string.ascii_letters + string.digits + "!@#$%^&*()"
        return ''.join(random.choice(chars) for _ in range(length))

    suggestions = []
    if not re.search(r'[A-Z]', password):
        suggestions.append(random.choice(string.ascii_uppercase))

    if not re.search(r'[a-z]', password):
        suggestions.append(random.choice(string.ascii_lowercase))

    if not re.search(r'[0-9]', password):
        suggestions.append(random.choice(string.digits))

    if not re.search(SYMBOLS, password):
        suggestions.append(random.choice(string.punctuation))

    while len(suggestions) + len(password) < 12:
        suggestions.append(random.choice(string.ascii_letters + string.digits + "!@#$%^&*()"))

    return password + ''.join(suggestions)

def check_password():
    password = password_entry.get()

    
    if not password:
        result_label.configure(text="Enter a password to analyze", text_color=TEXT)
        suggestion_label.configure(text="")
        progress_bar.set(0)
        return

    strength = 0  

    
    length = len(password)
    if length >= 20:
        strength += 25
    elif length >= 16:
        strength += 20
    elif length >= 12:
        strength += 15
    elif length >= 10:
        strength += 10
    elif length >= 8:
        strength += 5

    
    if re.search(r'[A-Z]', password):
        strength += 5
    if re.search(r'[a-z]', password):
        strength += 5
    if re.search(r'[0-9]', password):
        strength += 5
    if re.search(SYMBOLS, password):
        strength += 5

    
    entropy = estimate_entropy(password)
    if entropy >= 80:
        strength += 20
    elif entropy >= 60:
        strength += 15
    elif entropy >= 40:
        strength += 10
    elif entropy >= 25:
        strength += 5

        deductions = 0
    if password.lower() in COMMON_PASSWORDS:
        deductions += 60   
    if has_leet_substitution(password):
        deductions += 15
    if contains_sequence(password):
        deductions += 15
    if contains_keyboard_pattern(password):
        deductions += 15
    if has_repeated_chars(password):
        deductions += 15
    if re.search(r'(19|20)\d{2}', password):  
        deductions += 10
    if length <= 6:
        deductions += 20
    if len(set(password)) == 1:  
        deductions += 30

    strength = max(0, strength - deductions)

    
    if (re.search(r'[A-Z]', password) and re.search(r'[a-z]', password)
            and re.search(r'[0-9]', password) and re.search(SYMBOLS, password)
            and length >= 12 and deductions == 0):
        strength = min(100, strength + 10)

    # ---- Tampilkan hasil ----
    progress_bar.set(strength / 100)

    if strength < 40:
        result_label.configure(text="Weak Password", text_color="red")
        suggestion = suggest_password(password)
        suggestion_label.configure(text=f"Suggest: {suggestion}")
    elif strength < 65:
        result_label.configure(text="Moderate Password", text_color="orange")
        suggestion_label.configure(text="try adding more characters, numbers, or symbols.")
    elif strength < 85:
        result_label.configure(text="Strong Password", text_color="green")
        suggestion_label.configure(text="")
    else:
        result_label.configure(text="Excellent Password", text_color="blue")
        suggestion_label.configure(text="")

    if save_var.get():
        hashed = hash_password(password)
        with open("password.txt", "a") as file:
            file.write(hashed + "\n")
        messagebox.showinfo("Saved", "Password has been hashed and saved to password.txt")

def toogle_password():
    if password_entry.cget("show") == "*":
        password_entry.configure(show="")
        toggle_button.configure(text="Hide password")
    else:
        password_entry.configure(show="*")
        toggle_button.configure(text="Show password")

        
#UI elements
ctk.set_appearance_mode("dark")

app = ctk.CTk()
app.title("Password Checker")
app.geometry("560x600")
app.resizable(False, False)

BG = "#080808"
CARD = "#111111"
INPUT = "#181818"
WHITE = "#FFFFFF"
TEXT = "#E8E8E8"
MUTED = "#777777"
BORDER = "#2A2A2A"
HOVER = "#242424"

app.configure(fg_color=BG)

header = ctk.CTkFrame(
    app,
    fg_color="transparent"
)
header.pack(
    fill="x",
    padx=35,
    pady=(28, 12)
)

title_label = ctk.CTkLabel(
    header,
    text="PASSWORD CHECKER",
    font=("Arial", 24, "bold"),
    text_color=WHITE
)
title_label.pack(anchor="w")

subtitle_label = ctk.CTkLabel(
    header,
    text="Analyze password strength and security",
    font=("Arial", 12),
    text_color=MUTED
)
subtitle_label.pack(
    anchor="w",
    pady=(4, 0)
)

main_card = ctk.CTkFrame(
    app,
    fg_color=CARD,
    corner_radius=18,
    border_width=1,
    border_color=BORDER
)

main_card.pack(
    fill="both",
    expand=True,
    padx=30,
    pady=(5, 25)
)

password_title = ctk.CTkLabel(
    main_card,
    text="PASSWORD",
    font=("Arial", 10, "bold"),
    text_color=MUTED
)

password_title.pack(
    anchor="w",
    padx=30,
    pady=(25, 8)
)


password_entry = ctk.CTkEntry(
    main_card,
    placeholder_text="Enter your password",
    placeholder_text_color="#555555",
    show="*",
    height=48,
    corner_radius=10,
    fg_color=INPUT,
    border_color=BORDER,
    border_width=1,
    text_color=WHITE,
    font=("Arial", 14)
)

password_entry.pack(
    fill="x",
    padx=30
)

toggle_button = ctk.CTkButton(
    main_card,
    text="Show password",
    width=125,
    height=30,
    corner_radius=8,
    fg_color="transparent",
    hover_color=HOVER,
    border_width=1,
    border_color=BORDER,
    text_color=TEXT,
    font=("Arial", 11),
    command=toogle_password
)

toggle_button.pack(
    anchor="e",
    padx=30,
    pady=(8, 15)
)

check_button = ctk.CTkButton(
    main_card,
    text="CHECK PASSWORD",
    height=45,
    corner_radius=10,
    fg_color=WHITE,
    hover_color="#D5D5D5",
    text_color="#000000",
    font=("Arial", 12, "bold"),
    command=check_password
)
check_button.pack(
    fill="x",
    padx=30
)



strength_title = ctk.CTkLabel(
    main_card,
    text="PASSWORD STRENGTH",
    font=("Arial", 10, "bold"),
    text_color=MUTED
)
strength_title.pack(
    anchor="w",
    padx=30,
    pady=(24, 8)
)

progress_bar = ctk.CTkProgressBar(
    main_card,
    height=8,
    corner_radius=4,
    fg_color="#252525",
    progress_color=WHITE
)
progress_bar.pack(
    fill="x",
    padx=30
)
progress_bar.set(0)


result_label = ctk.CTkLabel(
    main_card,
    text="Enter a password to analyze",
    font=("Arial", 17, "bold"),
    text_color=TEXT
)
result_label.pack(
    pady=(14, 4)
)


suggestion_label = ctk.CTkLabel(
    main_card,
    text="",
    font=("Arial", 11),
    text_color=MUTED,
    wraplength=440
)
suggestion_label.pack(
    padx=30,
    pady=(0, 15)
)



save_var = ctk.BooleanVar(value=False)

save_checkbox = ctk.CTkCheckBox(
    main_card,
    text="Save password hash",
    variable=save_var,
    text_color=MUTED,
    fg_color=WHITE,
    hover_color="#D5D5D5",
    border_color="#555555",
    checkmark_color="#000000",
    font=("Arial", 11)
)
save_checkbox.pack(
    anchor="w",
    padx=30,
    pady=(5, 20)
)


footer = ctk.CTkLabel(
    app,
    text="PASSWORD SECURITY TOOL  •  LOCAL ANALYSIS",
    font=("Arial", 9),
    text_color="#444444"
)
footer.pack(
    pady=(0, 10)
)


app.mainloop()
