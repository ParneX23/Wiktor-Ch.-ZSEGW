import tkinter as tk
from tkinter import ttk, messagebox, IntVar
from xml.etree.ElementTree import tostring

import mysql.connector

def dbcon():
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="pycrud"
        )
        return mydb
    except mysql.connector.Error as err:
        messagebox.showerror("Błąd Połączenia", f"Nie można połączyć się z bazą danych: {err}")
        return None

def dodaj_film(tytul, rezyser, rok, ocena):
    conn = dbcon()
    if conn is None: return

    cursor = conn.cursor()
    sql = "INSERT INTO filmy (tytul, rezyser, rok, ocena) VALUES (%s, %s, %s, %s)"
    val = (tytul, rezyser, rok, ocena)
    try:
        cursor.execute(sql, val)
        conn.commit()
        messagebox.showinfo("Udało się!", "Dodano film do biblioteki!")
    except mysql.connector.Error as err:
        messagebox.showerror("Błąd", f"Wystąpił błąd podczas dodawania: {err}")
    finally:
        cursor.close()
        conn.close()

def pobierz_biblioteke():
    conn = dbcon()
    if conn is None: return []

    cursor = conn.cursor()
    sql = "SELECT id, tytul, rezyser, rok, ocena FROM filmy"
    try:
        cursor.execute(sql)
        wyniki = cursor.fetchall()
        return wyniki
    except mysql.connector.Error as err:
        messagebox.showerror("Błąd", f"Wystąpił błąd podczas pobierania biblioteki filmów: {err}")
        return []
    finally:
        cursor.close()
        conn.close()

def aktualizuj(id, tytul, rezyser, rok, ocena):
    conn = dbcon()
    if conn is None: return

    cursor = conn.cursor()
    sql = "UPDATE filmy SET tytul='"+tytul+"', rezyser='"+rezyser+"', rok='"+str(rok)+"', ocena='"+str(ocena)+"' WHERE id="+str(id)
    print("UPDATE filmy SET tytul='"+tytul+"', rezyser='"+rezyser+"', rok='"+str(rok)+"', ocena='"+str(ocena)+"' WHERE id="+str(id))

    try:
        cursor.execute(sql)
        conn.commit()
        messagebox.showinfo("Sukces", "Film zaktualizowany pomyślnie.")
    except mysql.connector.Error as err:
        messagebox.showerror("Błąd", f"Wystąpił błąd podczas aktualizacji filmu: {err}")
    finally:
        cursor.close()
        conn.close()
        odswiez_treeview(tree)

#
# --- FUNKCJE GUI ---
#
def obsluga_aktualizacji(event):
    selected = tree.focus()
    if not selected:
        return

    values = tree.item(selected, "values")
    id, tytul, rezyser, rok, ocena = values

    id_var = tk.IntVar()
    id_var.set(id)

    new_tytul_var = tk.StringVar()
    new_tytul_var.set(tytul)

    new_rezyser_var = tk.StringVar()
    new_rezyser_var.set(rezyser)

    new_rok_var = tk.IntVar()
    new_rok_var.set(rok)

    new_ocena_var = tk.IntVar()
    new_ocena_var.set(ocena)

    win = tk.Toplevel(root)
    win.title("Edytuj film")

    tk.Label(win, text="Id :").grid(row=0, column=0)
    tk.Label(win, text=id).grid(row=0, column=1)

    tk.Label(win, text="Tytul :").grid(row=1, column=0)
    tk.Entry(win, textvariable=new_tytul_var, width=30).grid(row=1, column=1)

    tk.Label(win, text="Ocena :").grid(row=2, column=0)
    tk.Entry(win, textvariable=new_rezyser_var, width=30).grid(row=2, column=1)

    tk.Label(win, text="Rok :").grid(row=3, column=0)
    tk.Entry(win, textvariable=new_rok_var, width=30).grid(row=3, column=1)

    tk.Label(win, text="Ocena :").grid(row=4, column=0)
    tk.Entry(win, textvariable=new_ocena_var, width=30).grid(row=4, column=1)

    def zmien():
        if new_tytul_var.get() and new_rezyser_var.get() and new_rok_var.get() and (new_ocena_var.get() >= 1 and new_ocena_var.get() <= 10):
            new_tytul = new_tytul_var.get()
            new_rezyser = new_rezyser_var.get()
            try:
                new_rok = int(new_rok_var.get())

            except ValueError:
                messagebox.showerror("Błąd", "Rok musi być liczbą.")
                return

            try:
                new_ocena = float(new_ocena_var.get())

            except ValueError:
                messagebox.showerror("Błąd", "Ocena musi być od od 1 do 10.")
                return
            aktualizuj(id, new_tytul, new_rezyser, new_rok, new_ocena)

            win.destroy()
            messagebox.showinfo("Sukces", "Zaktualizowano rekord!")
        else:
            messagebox.showwarning("Uwaga", "Wypełnij poprawnie wszystkie pola.")

    ttk.Button(win, text="Zapisz", command=zmien).grid(row=5, column=0, columnspan=2, pady=10)
    odswiez_treeview(tree)

def odswiez_treeview(tree):
    for item in tree.get_children():
        tree.delete(item)
    dane = pobierz_biblioteke()
    for wiersz in dane:
        tree.insert('', tk.END, values=wiersz)

def obsluga_dodawania(tytul_var, rezyser_var, rok_var, ocena_var, tree):
    tytul = tytul_var.get()
    rezyser = rezyser_var.get()

    try:
        rok = int(rok_var.get())

    except ValueError:
        messagebox.showerror("Błąd", "Ilość musi być liczbą od 1 do 10.")
        return

    try:
        ocena = float(ocena_var.get())

    except ValueError:
        messagebox.showerror("Błąd", "Ilość musi być liczbą od 1 do 10.")
        return

    if tytul and rezyser and rok and (ocena >= 1 and ocena <= 10):
        dodaj_film(tytul, rezyser, rok, ocena)
        odswiez_treeview(tree)
        tytul_var.set("")
        rezyser_var.set("")
        rok_var.set("")
        ocena_var.set("")
    else:
        messagebox.showwarning("Uwaga", "Wypełnij poprawnie wszystkie pola.")

def obsluga_aktualizacji_old(id_var, tytul_var, rezyser_var, rok_var, ocena_var, tree):
    id = int(id_var.get())
    tytul = tytul_var.get()
    rezyser = rezyser_var.get()

    try:
        rok = int(rok_var.get())

    except ValueError:
        messagebox.showerror("Błąd", "Ilość musi być liczbą od 1 do 10.")
        return

    try:
        ocena = float(ocena_var.get())

    except ValueError:
        messagebox.showerror("Błąd", "Ilość musi być liczbą od 1 do 10.")
        return

    if tytul and rezyser and rok and (ocena >= 1 and ocena <= 10):
        aktualizuj(id,tytul, rezyser, rok, ocena)
        odswiez_treeview(tree)
        tytul_var.set("")
        rezyser_var.set("")
        rok_var.set("")
        ocena_var.set("")

    else:
        messagebox.showwarning("Uwaga", "Wypełnij poprawnie wszystkie pola.")

def obsluga_usuwania():
    selected = tree.focus()
    if not selected:
        return

    values = tree.item(selected, "values")
    del_id = values[0]

    conn = dbcon()
    if conn is None: return

    cursor = conn.cursor()
    sql = "DELETE FROM filmy WHERE id="+str(del_id)

    try:
        cursor.execute(sql)
        conn.commit()
        messagebox.showinfo("Sukces", "Usunięto film.")
    except mysql.connector.Error as err:
        messagebox.showerror("Błąd", f"Wystąpił błąd podczas usuwania filmu: {err}")
    finally:
        cursor.close()
        conn.close()
        odswiez_treeview(tree)

def obsluga_wyszukiwania(search_var):
    selected = tree.focus()
    if not selected:
        return

# --- KONFIGURACJA GŁÓWNEGO OKNA ---

root = tk.Tk()
root.title("System Zarządzania Magazynem")

# Zmienne kontrolne dla pól wejściowych
id_var = tk.IntVar()
tytul_var = tk.StringVar()
rezyser_var = tk.StringVar()
rok_var = tk.IntVar()
ocena_var = tk.IntVar()
search_var = tk.StringVar()

# --- Sekcja formularza (INPUT) ---
form_frame = ttk.Frame(root, padding="10")
form_frame.pack(padx=10, pady=10, fill='x')

ttk.Label(form_frame, text="Tytuł :").grid(row=0, column=0, padx=5, pady=5, sticky='w')
ttk.Entry(form_frame, textvariable=tytul_var, width=30).grid(row=0, column=1, padx=5, pady=5)

ttk.Label(form_frame, text="Rezyser :").grid(row=1, column=0, padx=5, pady=5, sticky='w')
ttk.Entry(form_frame, textvariable=rezyser_var, width=30).grid(row=1, column=1, padx=5, pady=5)

ttk.Label(form_frame, text="Rok :").grid(row=2, column=0, padx=5, pady=5, sticky='w')
ttk.Entry(form_frame, textvariable=rok_var, width=10).grid(row=2, column=1, padx=5, pady=5, sticky='w')

ttk.Label(form_frame, text="Ocena :").grid(row=3, column=0, padx=5, pady=5, sticky='w')
ttk.Entry(form_frame, textvariable=ocena_var, width=10).grid(row=3, column=1, padx=5, pady=5, sticky='w')

dodaj_btn = ttk.Button(form_frame, text="Dodaj film",
    command=lambda: obsluga_dodawania(tytul_var, rezyser_var, rok_var, ocena_var, tree))
dodaj_btn.grid(row=4, column=0, pady=10)

usun_btn = ttk.Button(form_frame, text="Usuń Film",
    command=lambda: obsluga_usuwania())
usun_btn.grid(row=4, column=1, pady=10)

ttk.Label(form_frame, text="Szukaj po tytule :").grid(row=4, column=2, padx=5, pady=5, sticky='w')
ttk.Entry(form_frame, textvariable=search_var, width=20).grid(row=4, column=3, padx=5, pady=5, sticky='w')
usun_btn = ttk.Button(form_frame, text="🔎",
    command=lambda: obsluga_wyszukiwania(search_var))
usun_btn.grid(row=4, column=4)


# --- Sekcja wyświetlania danych (Treeview) ---

columns = ('id', 'tytul', 'rezyser', 'rok', 'ocena')
tree = ttk.Treeview(root, columns=columns, show='headings')

tree.heading('id', text='ID')
tree.column('id', width=50, anchor='center')
tree.heading('tytul', text='Tytul filmu')
tree.column('tytul', width=250)
tree.heading('rezyser', text='Rezyser')
tree.column('rezyser', width=80, anchor='center')
tree.heading('rok', text='Rok')
tree.column('rok', width=80, anchor='center')
tree.heading('ocena', text='Ocena')
tree.column('ocena', width=80, anchor='center')

tree.pack(pady=10, padx=10, fill='both', expand=True)

tree.bind('<Double-1>', obsluga_aktualizacji)

# Początkowe załadowanie danych
odswiez_treeview(tree)

root.mainloop()