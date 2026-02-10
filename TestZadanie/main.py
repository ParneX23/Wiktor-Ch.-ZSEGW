import tkinter as tk

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Kalkulator Sumy z Walidacją")
        self.geometry("300x150")
        self.number1 = tk.Entry(self)
        self.number1.pack()
        self.number2 = tk.Entry(self)
        self.number2.pack()
        self.label = tk.Label(self, text="[Wynik]")
        self.label.pack()
        self.btn = tk.Button(self, text="Oblicz", command=self.count)
        self.btn.pack()

    def is_number(self, x):
        try:
            float(x)
            return True
        except ValueError:
            return False

    def count(self):
        n1 = self.number1.get()
        n2 = self.number2.get()

        if(n1!= "" and n2!= "" and self.is_number(n1) and self.is_number(n2)):
            wynik = float(n1)+float(n2)
            self.label["text"] = str(wynik)
        else :
            self.label["text"] = "Błąd danych"

import unittest


class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = App()
        self.app.withdraw()

    def tearDown(self):
        self.app.destroy()

    def test1(self):
        self.app.number1.insert(0, "5")
        self.app.number2.insert(0, "10")

        self.app.btn.invoke()

        result = self.app.label.cget("text")
        self.assertEqual(result, "15.0")

    def test2(self):
        self.app.number1.insert(0, "abc")
        self.app.number2.insert(0, "5")

        self.app.btn.invoke()

        result = self.app.label.cget("text")
        self.assertEqual(result, "Błąd danych")

    def test3(self):
        self.app.btn.invoke()

        result = self.app.label.cget("text")
        self.assertEqual(result, "Błąd danych")

if __name__ == "__main__":
    unittest.main()