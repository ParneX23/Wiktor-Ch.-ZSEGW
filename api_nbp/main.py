import customtkinter as ctk
import requests as rq
import threading
import json

class NBP:
    waluty = []

    def __init__(self):
        print(self.kody())
        print(self.waluty)
        app = ctk.CTk()
        app.geometry("300x300")
        app.title("Apka NBP")

        self.label1 = ctk.CTkLabel(app, text="Ostatnia aktualizacja : ")
        self.label1.pack(pady=10)

        self.label2 = ctk.CTkLabel(app, text="Wpisz kwotę w PLN")
        self.label2.pack(pady=10)

        self.entry_kwota = ctk.CTkEntry(app, placeholder_text="np. 100")
        self.entry_kwota.pack(pady=5)

        self.optionmenu = ctk.CTkOptionMenu(app, values=self.waluty)
        self.optionmenu.pack(pady=10)

        self.wynik_label = ctk.CTkLabel(app, text="Wynik pojawi się tutaj")
        self.wynik_label.pack(pady=10)

        self.button = ctk.CTkButton(app, text="Przelicz", command=self.watek)
        self.button.pack(pady=10)
        app.mainloop()

    def watek(self):
        t = threading.Thread(target=self.przelicz())
        t.start()

    def przelicz(self):
        try:
            dane = json.loads(rq.get("https://api.nbp.pl/api/exchangerates/rates/A/" + self.optionmenu.get() + "/?format=json").content)
            kurs = float(dane["rates"][0]["mid"])
            kwota = float(self.entry_kwota.get())
            wynik = round(kurs * kwota, 2)
            self.label1.configure(text="Ostatnia aktualizacja : " + dane["rates"][0]["effectiveDate"])
            self.wynik_label.configure(text=str(wynik))
            self.entry_kwota.delete(0, "end")
            print("dokonano przeliczenia")
        except:
            self.wynik_label.configure(text="An error has occured!")

    def kody(self):
        dane = json.loads(rq.get("http://api.nbp.pl/api/exchangerates/tables/A/?format=json").content)
        for kod in dane[0]["rates"]:
            self.waluty.append(kod["code"])
        return dane

nbp = NBP()