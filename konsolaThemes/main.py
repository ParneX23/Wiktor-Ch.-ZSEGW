import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Lista motywów ttk")

style = ttk.Style()

# pobranie listy motywów
themes = style.theme_names()

print("Dostępne motywy ttk:")

for theme in themes:
    print(theme)

root.mainloop()