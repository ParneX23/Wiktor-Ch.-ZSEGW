import tkinter as tk
from tkinter import filedialog, messagebox
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from datetime import datetime

pdfmetrics.registerFont(TTFont("DejaVuSans", "DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DejaVuSans-Bold", "DejaVuSans-Bold.ttf"))

def is_float(x):
    try:
        float(x)
        return True
    except ValueError:
        return False

def generuj_pdf():
    if not entry_netto.get() and not entry_netto.get() and not entry_vat.get():
        messagebox.showwarning("Błąd", "Wpisz wszystkie dane!")
        return

    produkt = entry_prod.get()
    if not is_float(entry_netto.get()):
        messagebox.showwarning("Błąd", "Wartość netto musi być liczbą!")
        return
    netto = float(entry_netto.get())
    if not is_float(entry_vat.get()):
        messagebox.showwarning("Błąd", "Wartość netto musi być liczbą!")
        return
    vat = float(entry_vat.get())
    if vat < 0 or vat > 100:
        messagebox.showwarning("Błąd", "Podaj stawkę VAT w procentach!")
        return
    # 2. Wybór lokalizacji zapisu
    sciezka = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("Pliki PDF", "*.pdf")],
        title="Zapisz raport jako..."
    )

    if sciezka:
        try:
            # 3. Tworzenie dokumentu PDF
            c = canvas.Canvas(sciezka, pagesize=A4)
            szerokosc, wysokosc = A4

            # Nagłówek
            c.setFont("DejaVuSans-Bold", 16)
            c.drawString(100, wysokosc - 50, "UPROSZCZONA FAKTURA")

            # Linia oddzielająca
            c.line(100, wysokosc - 60, 500, wysokosc - 60)

            # Treść

            data = [
                ["Pole", "Wartość"],
                ["Produkt", produkt],
                ["Wartość Netto", netto],
                ["Stawka VAT", f"{vat}%"],
                ["Wartość Brutto", ((netto * vat) / 100) + netto]
            ]

            # tworzenie tabeli
            table = Table(data, colWidths=[200, 200])

            table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),

                ("GRID", (0, 0), (-1, -1), 1, colors.black),

                ("FONTNAME", (0, 0), (-1, 0), "DejaVuSans-Bold"),
                ("FONTNAME", (0, 1), (-1, -1), "DejaVuSans"),

                ("ALIGN", (1, 1), (-1, -1), "LEFT")
            ]))

            # pozycja tabeli w PDF
            table.wrapOn(c, szerokosc, wysokosc)
            table.drawOn(c, 100, wysokosc - 180)

            c.setFont("DejaVuSans", 10)

            data = datetime.now().strftime("%d-%m-%Y")
            c.drawString(100, wysokosc - 200, f"Data: {data}")

            # Zapisanie pliku
            c.save()
            messagebox.showinfo("Sukces", "Plik PDF został utworzony pomyślnie!")
        except Exception as e:
            messagebox.showerror("Błąd", f"Wystąpił błąd: {e}")


# --- Konfiguracja Okna Tkinter ---
root = tk.Tk()
root.title("Generator PDF")
root.geometry("400x400")

tk.Label(root, text="Nazwa Produktu:", font=("Arial", 10, "bold")).pack(pady=5)
entry_prod = tk.Entry(root, width=40)
entry_prod.pack(pady=5)

tk.Label(root, text="Cena Netto:", font=("Arial", 10, "bold")).pack(pady=5)
entry_netto = tk.Entry(root, width=40)
entry_netto.pack(pady=5)

tk.Label(root, text="Stawka VAT:", font=("Arial", 10, "bold")).pack(pady=5)
entry_vat = tk.Entry(root, width=40)
entry_vat.pack(pady=5)

btn_export = tk.Button(root, text="Eksportuj do PDF", command=generuj_pdf, bg="#27ae60", fg="white", padx=20)
btn_export.pack(pady=20)

root.mainloop()