import tkinter as tk

class Konwerter:
    def __init__(self):
        root = tk.Tk()
        root.title("Konwerter")
        root.geometry("600x600")

        tk.Label(root,text="Wprowadź wartość (metry)").pack(side="top",padx=10, pady=10)
        self.wejscie = tk.Entry(root,textvariable=tk.StringVar())
        self.wejscie.pack(side="top",padx=10, pady=10)
        btn = tk.Button(root,text="Konwertuj na stopy", command=self.przelicz)
        btn.pack(side="top",padx=10, pady=10)
        self.wyjscie = tk.Label(root,text="Wynik 0.0 stóp")
        self.wyjscie.pack(side="top",padx=10, pady=10)

        root.mainloop()

    def przelicz(self):
        wynik = round(float(self.wejscie.get())*3.280839895, 2)
        self.wyjscie.config(text="Wynik " + str(wynik) + " stóp")

konwerter = Konwerter()