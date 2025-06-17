import tkinter as tk

class Kalkulator:
    def __init__(self):
        self.liczba_1 = "0"
        self.liczba_2 = ""
        self.operacja = ""

        root = tk.Tk()
        root.title("Kalkulator")
        root.geometry("300x300")

        self.pole = tk.Entry(root, state='readonly', width=25, font=("Consolas", 15))
        self.pole.pack(anchor=tk.CENTER)
        self.napisz("0")

        #
        # Ustawianie kontenera
        #

        klawiatura = tk.Frame(root)
        klawiatura.pack(pady=10)
        klawiatura.rowconfigure(0, weight=1)
        klawiatura.rowconfigure(1, weight=1)
        klawiatura.rowconfigure(2, weight=1)
        klawiatura.rowconfigure(3, weight=1)
        klawiatura.columnconfigure(0, weight=1)
        klawiatura.columnconfigure(1, weight=1)
        klawiatura.columnconfigure(2, weight=1)
        klawiatura.columnconfigure(3, weight=1)
        klawiatura.columnconfigure(4, weight=1)

        #
        # Tworzenie klawiatury
        #

        btn0 = tk.Button(klawiatura, text="0",width=5,height=2,font=("Consolas", 15), bg="#f7cae9", command=self.add0)
        btn0.grid(column=0, row=3)
        btn1 = tk.Button(klawiatura, text="1",width=5,height=2,font=("Consolas", 15), bg="#f7cae9", command=self.add1)
        btn1.grid(column=0, row=0)
        btn2 = tk.Button(klawiatura, text="2",width=5,height=2,font=("Consolas", 15), bg="#f7cae9", command=self.add2)
        btn2.grid(column=1, row=0)
        btn3 = tk.Button(klawiatura, text="3",width=5,height=2,font=("Consolas", 15), bg="#f7cae9", command=self.add3)
        btn3.grid(column=2, row=0)
        btn4 = tk.Button(klawiatura, text="4",width=5,height=2,font=("Consolas", 15), bg="#f7cae9", command=self.add4)
        btn4.grid(column=0, row=1)
        btn5 = tk.Button(klawiatura, text="5",width=5,height=2,font=("Consolas", 15), bg="#f7cae9", command=self.add5)
        btn5.grid(column=1, row=1)
        btn6 = tk.Button(klawiatura, text="6",width=5,height=2,font=("Consolas", 15), bg="#f7cae9", command=self.add6)
        btn6.grid(column=2, row=1)
        btn7 = tk.Button(klawiatura, text="7",width=5,height=2,font=("Consolas", 15), bg="#f7cae9", command=self.add7)
        btn7.grid(column=0, row=2)
        btn8 = tk.Button(klawiatura, text="8",width=5,height=2,font=("Consolas", 15), bg="#f7cae9", command=self.add8)
        btn8.grid(column=1, row=2)
        btn9 = tk.Button(klawiatura, text="9",width=5,height=2,font=("Consolas", 15), bg="#f7cae9", command=self.add9)
        btn9.grid(column=2, row=2)

        #
        # Tworzenie pozostałych przycisków
        #

        plus = tk.Button(klawiatura, text="+",width=5,height=2,font=("Consolas", 15), command=self.dodaj)
        plus.grid(column=3, row=0)
        minus = tk.Button(klawiatura, text="-",width=5,height=2,font=("Consolas", 15), command=self.odejmij)
        minus.grid(column=4, row=0)
        razy = tk.Button(klawiatura, text="x",width=5,height=2,font=("Consolas", 15), command=self.pomnoz)
        razy.grid(column=3, row=1)
        podziel = tk.Button(klawiatura, text="/",width=5,height=2,font=("Consolas", 15), command=self.podziel)
        podziel.grid(column=4, row=1)
        kropka = tk.Button(klawiatura, text=".", width=5, height=2, font=("Consolas", 15), bg="#f7cae9", command=self.kropka)
        kropka.grid(column=1, row=3)
        rowna = tk.Button(klawiatura, text="=",width=5,height=2,font=("Consolas", 15), bg="#f243bd", fg="white", command=self.rownaSie)
        rowna.grid(column=2, row=3)
        clear = tk.Button(klawiatura, text="C",width=5,height=2,font=("Consolas", 15), command=self.clear)
        clear.grid(column=3, row=2, columnspan=2, rowspan=2, sticky="nsew")

        #
        # Wyświetlanie okna
        #

        root.mainloop()

    #
    # Inne funkcje
    #

    def debug(self):
        print("### DEBUG ###")
        print("Liczba_1 : "+self.liczba_1)
        print("Liczba_2 : "+self.liczba_2)
        print("Operacja : "+self.operacja)
    def is_number(self, abc):
        try:
            float(abc)
            return True
        except ValueError:
            return False
    def napisz(self, text):
        self.wyczyscEkran()
        self.pole.config(state="normal")
        if self.is_number(text):
            if float(text).is_integer():
                self.pole.insert(0, str(int(float(text))))
            else:
                self.pole.insert(0,str(round(float(text),5)))
        else:
            self.pole.insert(0, text)
        self.pole.config(state="readonly")

    def wyczyscEkran(self):
        self.pole.config(state="normal")
        self.pole.delete(0, tk.END)
        self.pole.config(state="readonly")

    def funkcja(self):
        print("funkcja")
        self.liczba_2 = self.liczba_1
        self.napisz("0")
        self.liczba_1 = ""

    #
    # Operatory arytmetyczne
    #

    def dodaj(self):
        print("dodaj")
        if(self.liczba_2==""):
            self.funkcja()
            self.operacja="+"
        elif(self.liczba_1!="" and self.liczba_2!=""):
            self.operacja = "+"
            self.rownaSie()
        else:
            self.operacja="+"
        self.debug()

    def odejmij(self):
        print("odejmij")
        if (self.liczba_2 == ""):
            self.funkcja()
            self.operacja = "-"
        elif (self.liczba_1 != "" and self.liczba_2 != ""):
            self.operacja = "-"
            self.rownaSie()
        else:
            self.operacja = "-"
        self.debug()

    def pomnoz(self):
        print("pomnóż")
        if (self.liczba_2 == ""):
            self.funkcja()
            self.operacja = "x"
        elif (self.liczba_1 != "" and self.liczba_2 != ""):
            self.operacja = "x"
            self.rownaSie()
        else:
            self.operacja = "x"
        self.debug()

    def podziel(self):
        print("podziel")
        if (self.liczba_2 == ""):
            self.funkcja()
            self.operacja = "/"
        elif (self.liczba_1 != "" and self.liczba_2 != ""):
            self.operacja = "/"
            self.rownaSie()
        else:
            self.operacja = "/"
        self.debug()

    #
    # Pozostałe operatory
    #

    def kropka(self):
        if (self.liczba_1 != ""):
            self.liczba_1 += "."
            self.napisz(self.liczba_1)
        else:
            self.liczba_1 += "0."
            self.napisz(self.liczba_1)

    def rownaSie(self):
        print("Równa Się")
        if self.liczba_1 != "" and self.liczba_2 != "" :
            match self.operacja:
                case '+':
                    self.liczba_2 = str(float(self.liczba_2) + float(self.liczba_1))
                    self.liczba_1 = ""
                    self.napisz(self.liczba_2)
                case '-':
                    self.liczba_2 = str(float(self.liczba_2) - float(self.liczba_1))
                    self.liczba_1 = ""
                    self.napisz(self.liczba_2)
                case 'x':
                    self.liczba_2 = str(float(self.liczba_2) * float(self.liczba_1))
                    self.liczba_1 = ""
                    self.napisz(self.liczba_2)
                case '/':
                    try:
                        self.liczba_2 = str(float(self.liczba_2) / float(self.liczba_1))
                        self.liczba_1 = ""
                        self.napisz(self.liczba_2)
                    except ZeroDivisionError:
                        self.clear()
                        self.napisz("DZIELENIE PRZEZ ZERO")
                case _:
                    print("Nie podano operacji")


    def clear(self):
        self.wyczyscEkran()
        self.liczba_1 = ""
        self.liczba_2 = ""
        self.operacja = ""
        self.napisz("0")

    #
    # Klawiatura cyfr
    #

    def add0(self):
        if(self.liczba_1 != "0"):
            self.liczba_1 += "0"
            self.napisz(self.liczba_1)
    def add1(self):
        if(self.liczba_1=="0"):
            self.liczba_1 = "1"
            self.napisz(self.liczba_1)
        else:
            self.liczba_1 += "1"
            self.napisz(self.liczba_1)
    def add2(self):
        if (self.liczba_1 == "0"):
            self.liczba_1 = "2"
            self.napisz(self.liczba_1)
        else:
            self.liczba_1 += "2"
            self.napisz(self.liczba_1)
    def add3(self):
        if (self.liczba_1 == "0"):
            self.liczba_1 = "3"
            self.napisz(self.liczba_1)
        else:
            self.liczba_1 += "3"
            self.napisz(self.liczba_1)
    def add4(self):
        if (self.liczba_1 == "0"):
            self.liczba_1 = "4"
            self.napisz(self.liczba_1)
        else:
            self.liczba_1 += "4"
            self.napisz(self.liczba_1)
    def add5(self):
        if (self.liczba_1 == "0"):
            self.liczba_1 = "5"
            self.napisz(self.liczba_1)
        else:
            self.liczba_1 += "5"
            self.napisz(self.liczba_1)
    def add6(self):
        if (self.liczba_1 == "0"):
            self.liczba_1 = "6"
            self.napisz(self.liczba_1)
        else:
            self.liczba_1 += "6"
            self.napisz(self.liczba_1)
    def add7(self):
        if (self.liczba_1 == "0"):
            self.liczba_1 = "7"
            self.napisz(self.liczba_1)
        else:
            self.liczba_1 += "7"
            self.napisz(self.liczba_1)
    def add8(self):
        if (self.liczba_1 == "0"):
            self.liczba_1 = "8"
            self.napisz(self.liczba_1)
        else:
            self.liczba_1 += "8"
            self.napisz(self.liczba_1)
    def add9(self):
        if (self.liczba_1 == "0"):
            self.liczba_1 = "9"
            self.napisz(self.liczba_1)
        else:
            self.liczba_1 += "9"
            self.napisz(self.liczba_1)

kalkulator = Kalkulator()