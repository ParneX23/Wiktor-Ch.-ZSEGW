import tkinter as tk
from tkinter import ttk

def zapisz():
    pbar.start()
    root.after(3000, pbar.stop)

root = tk.Tk()
root.title("Ustawienia Systemu")
root.geometry("350x350")

notebook = ttk.Notebook(root)
notebook.pack(pady=10, padx=10, expand=True, fill="both")

strona1 = ttk.Frame(notebook, padding="10")
strona2 = ttk.Frame(notebook, padding="10")

notebook.add(strona1, text="Wygląd")
notebook.add(strona2, text="Prywatność")

# pierwsza strona

ttk.Label(strona1, text="Motyw:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
motywy = ["Jasny", "Ciemny", "Systemowy"]

motyw = ttk.Combobox(strona1, values=motywy, state="readonly")
motyw.current(0)
motyw.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

kontr_var = tk.BooleanVar()
kontr = ttk.Checkbutton(strona1, text="Włącz wysoki kontrast", variable=kontr_var)
kontr.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

# druga strona

udost_label = ttk.Label(strona2, text="Poziom Udostępniania danych")
udost_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

udost_var = tk.StringVar();

radio1 = ttk.Radiobutton(strona2, text="Wszystkie", value="Wszystkie", variable=udost_var)
radio1.grid(row=1, column=0, padx=5, pady=5, sticky="w")

radio2 = ttk.Radiobutton(strona2, text="Anonimowe", value="Anonimowe", variable=udost_var)
radio2.grid(row=2, column=0, padx=5, pady=5, sticky="w")

radio3 = ttk.Radiobutton(strona2, text="Żadne", value="Żadne", variable=udost_var)
radio3.grid(row=3, column=0, padx=5, pady=5, sticky="w")

pbar = ttk.Progressbar(root, orient="horizontal", length=300, mode="indeterminate")
pbar.pack(pady=10)

ttk.Button(root, text="Zapisz ustawienia", command=zapisz).pack(side="top", padx=5, pady=5)

root.mainloop()