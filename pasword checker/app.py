import customtkinter as ctk
from tkinter import messagebox
import re
import hashlib
import random
import string


ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Password Checker")
app.geometry("500x450")

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def suggest_password(password):
    suggestions = []
    if not re.search(r'[A-Z]', password):
        suggestions.append(random.choice(string.ascii_uppercase))

    if not re.search(r'[a-z]', password):
        suggestions.append(random.choice(string.ascii_lowercase))
    
    if not re.search(r'[0-9]', password):
        suggestions.append(random.choice(string.digits))

    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        suggestions.append(random.choice(string.punctuation))
        
    while len(suggestions) + len(password) < 12:
        suggestions.append(random.choice(string.ascii_letters + string.digits + "1@#$%^&*()"))

    return password + ''.join(suggestions)

def check_password():
    password = password_entry.get()
    strength = 0 

    if len(password) >= 12:
        strength += 2
    elif len(password) >= 8:
        strength += 1

    if re.search(r'[A-Z]', password):
        strength += 1

    if re.search(r'[a-z]', password):
        strength += 1

    if re.search(r'[0-9]', password):
        strength += 1
    
    if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        strength += 1


    progress_bar.set(strength / 6)

    if strength < 4:
        result_label.configure(text="Weak Password", text_color="red")
        suggestion = suggest_password(password)
        suggestion_label.configure(text=f"Suggest: {suggestion}")
    elif strength <= 4:
        result_label.configure(text="Moderate Password", text_color="orange")
        suggestion_label.configure(text="try adding more characters, numbers, or symbols.")
    elif strength <= 5:
        result_label.configure(text="Strong Password", text_color="green")
        suggestion_label.configure(text="")
    else:
        result_label.configure(text="Excellent Password", text_color="blue")
        suggestion_label.configure(text="")

    if save_var.get():
        hashed = hash_password(password)
        with open("password.txt", "a") as file:
            file.write(hashed + "\n")
        messagebox.showinfo("Saved","Password has been hashed and saved to password.txt")

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


# =========================
# FOOTER
# =========================

footer = ctk.CTkLabel(
    app,
    text="PASSWORD SECURITY TOOL  •  LOCAL ANALYSIS",
    font=("Arial", 9),
    text_color="#444444"
)
footer.pack(
    pady=(0, 10)
)


# =========================
# START APPLICATION
# =========================

app.mainloop()