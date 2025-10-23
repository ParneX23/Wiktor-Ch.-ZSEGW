import tkinter as tk

root = tk.Tk()
root.title("Wybory Demo")

txt = tk.Text(root, height=30, width=200)
txt.pack(anchor='w', padx=10, pady=5)
txt.insert(tk.END, "Tutaj wpisz text")

# Możliwośc pisania
disable_var = tk.IntVar(value=1)

def text_change() :
    if disable_var.get() == 0:
        txt.config(state="disabled")
    else :
        txt.config(state="normal")


disableFrame = tk.Frame(root)
disableFrame.pack(anchor="w", padx=10)
tk.Label(disableFrame, text="Włącz pisanie :").pack(side="left", padx=10, pady=5)
tk.Radiobutton(disableFrame, text="Tak", variable=disable_var, value=1).pack(side="left", padx=0, pady=0)
tk.Radiobutton(disableFrame, text="Nie", variable=disable_var, value=0).pack(side="left", padx=0, pady=0)
tk.Button(disableFrame, text="Zastosuj", command=text_change).pack(side="left")

# Buforowanie

bufor_var = tk.IntVar(value=0)
bufor_notatki = ""

def bufforing():
    global bufor_notatki
    if disable_var.get() == 0 :
        txt.config(state="normal")
    if bufor_var.get() == 1:
        bufor_notatki = txt.get("1.0", tk.END)
        txt.delete("1.0", tk.END)
        txt.insert(tk.END, "Notatki przeniesione do buforu")
    else :
        txt.delete("1.0", tk.END)
        txt.insert(tk.END, bufor_notatki)
        bufor_notatki = ""
    if disable_var.get() == 0 :
        txt.config(state="disabled")

tk.Checkbutton(root, text="Przenieś do bufora", variable=bufor_var, onvalue=1, offvalue=0, command=bufforing).pack(anchor="w", padx=20)


root.mainloop()