import customtkinter as ctk

# ustawienie początkowego trybu
ctk.set_appearance_mode("Light")

app = ctk.CTk()
app.title("Zmiana motywu")
app.geometry("300x200")


# funkcja zmieniająca tryb
def zmien_tryb(new_mode):
    ctk.set_appearance_mode(new_mode)


# lista motywów
motywy = ["Light", "Dark"]

# OptionMenu
option_menu = ctk.CTkOptionMenu(
    app,
    values=motywy,
    command=zmien_tryb
)

option_menu.pack(pady=40)

app.mainloop()