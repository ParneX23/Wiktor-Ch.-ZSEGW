import tkinter as tk

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Prosta apka")
        self.geometry("300x150")
        self.entry = tk.Entry(self)
        self.entry.pack()
        self.label = tk.Label(self, text="Czekam...")
        self.label.pack()
        self.btn1 = tk.Button(self, text="Powitaj", command=self.say_hello)
        self.btn1.pack()
        self.btn2 = tk.Button(self, text="Wyczyść", command=self.clear)
        self.btn2.pack()

    def say_hello(self):
        name = self.entry.get()
        self.label.config(text=f"Witaj, {name}!")

    def clear(self):
        self.entry.delete(0, tk.END)
        self.label.config(text="Czekam...")

import unittest


class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = App()
        self.app.withdraw()  # Ukrywamy okno podczas testów

    def tearDown(self):
        self.app.destroy()

    def test_greeting(self):
        # 1. Symulacja wpisania tekstu
        self.app.entry.insert(0, "Jan")

        # 2. Symulacja kliknięcia (wywołanie komendy przycisku)
        self.app.btn1.invoke()

        # 3. Sprawdzenie wyniku
        result = self.app.label.cget("text")
        self.assertEqual(result, "Witaj, Jan!")

    def test_clear(self):
        self.app.entry.insert(0, "Jan")

        self.app.btn2.invoke()

        result1 = self.app.label.cget("text")
        result2 = self.app.entry.get()

        self.assertEqual(result1, "Czekam...")
        self.assertEqual(result2, "")

    def test_button_visibility(self):
        self.app.update()

        result = self.app.btn1.winfo_ismapped()

        self.assertTrue(result)

if __name__ == "__main__":
    unittest.main()