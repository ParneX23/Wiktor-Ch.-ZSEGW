import customtkinter as ctk
import json
import os

USTAWIENIA = "settings.json"

def load_settings():
    if os.path.exists(USTAWIENIA):
        with open(USTAWIENIA, "r") as f:
            return json.load(f)
    return {"tryb": "Light"}

def save_settings(mode):
    with open(USTAWIENIA, "w") as f:
        json.dump({"tryb": mode}, f)

def change_theme(new_mode):
    ctk.set_appearance_mode(new_mode)
    save_settings(new_mode)

settings = load_settings()

ctk.set_appearance_mode(settings["tryb"])
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Professional Settings Manager")
app.geometry("700x400")

sidebar = ctk.CTkFrame(app, width=150)
sidebar.pack(side="left", fill="y")

title_label = ctk.CTkLabel(sidebar, text="Settings", font=("Arial", 18))
title_label.pack(pady=20)

theme_label = ctk.CTkLabel(sidebar, text="Tryb")
theme_label.pack(pady=5)

theme_menu = ctk.CTkOptionMenu(
    sidebar,
    values=["Light", "Dark"],
    command=change_theme
)
theme_menu.set(settings["tryb"])
theme_menu.pack(pady=10)

main_frame = ctk.CTkFrame(app)
main_frame.pack(fill="both", expand=True, padx=20, pady=20)

entry = ctk.CTkEntry(main_frame, placeholder_text="Text")
entry.pack(pady=10)

checkbox = ctk.CTkCheckBox(main_frame, text="Opcja")
checkbox.pack(pady=10)

def add_text():
    text = entry.get()
    if text:
        textbox.insert("end", text + "\n")
        entry.delete(0, "end")

button = ctk.CTkButton(main_frame, text="Dodaj", command=add_text)
button.pack(pady=10)

textbox = ctk.CTkTextbox(main_frame, width=400, height=200)
textbox.pack(pady=10)

app.mainloop()