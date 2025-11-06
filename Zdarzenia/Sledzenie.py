import tkinter as tk

class Sledzenie():
    def __init__(self):
        root = tk.Tk()
        root.title("Formularz Rejestracyjny")
        root.geometry("600x600")

        self.coords_label = tk.Label(root, text="Pozycja: (X: ?, Y: ?)", font=('Arial', 14))
        self.coords_label.pack(pady=50)

        root.bind('<Motion>', self.aktualizuj_wspolrzedne)

        root.mainloop()

    def aktualizuj_wspolrzedne(self, event):
        self.coords_label.config(text="Koordynaty : X:"+str(event.x)+", Y:"+str(event.y))

sledzenie = Sledzenie()