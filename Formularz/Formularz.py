import tkinter as tk
from tkinter import messagebox

class Formularz:
    def __init__(self):
        root = tk.Tk()
        root.title("Formularz Rejestracyjny")
        root.geometry("600x600")

        form = tk.Frame(root)
        form.pack(side="top")

        tk.Label(form,text="Imię").grid(row=0, column=0)
        self.imie = tk.Entry(form)
        self.imie.grid(row=0, column=1)

        tk.Label(form, text="Email").grid(row=1, column=0)
        self.email = tk.Entry(form)
        self.email.grid(row=1, column=1)

        tk.Label(form, text="Wiek").grid(row=2, column=0)

        wiek = tk.Frame(form)
        wiek.grid(row=2, column=1)

        self.wiekvalue = tk.StringVar()
        self.wiekvalue.set("no age wiekvalue")
        self.wiek1 = tk.Radiobutton(wiek, text='18-30', value='18-30', variable=self.wiekvalue)
        self.wiek1.pack(side="left")
        self.wiek2 = tk.Radiobutton(wiek, text='31-50', value='31-50', variable=self.wiekvalue)
        self.wiek2.pack(side="left")
        self.wiek3 = tk.Radiobutton(wiek, text='50+', value='50+', variable=self.wiekvalue)
        self.wiek3.pack(side="left")

        tk.Label(form, text="Zainteresowania").grid(row=3, column=0)

        zainteresowania = tk.Frame(form)
        zainteresowania.grid(row=3, column=1)

        self.boksvalue = tk.BooleanVar()
        self.szachyvalue = tk.BooleanVar()

        self.boks = tk.Checkbutton(zainteresowania, text='Boks',variable=self.boksvalue)
        self.boks.pack(side="left")
        self.szachy = tk.Checkbutton(zainteresowania, text='Szachy',variable=self.szachyvalue)
        self.szachy.pack(side="left")

        tk.Label(form, text="Uwagi").grid(row=4, column=0)

        self.uwagi = tk.Text(form)
        self.uwagi.grid(row=4, column=1)

        self.submit = tk.Button(form, text="Zarejestruj", command=self.submit_form)
        self.submit.grid(row=5, column=0)

        root.mainloop()
    def submit_form(self):
        print("Wysłano!")
        if(self.boksvalue.get()):
            if(self.szachyvalue.get()):
                messagebox.showinfo(title="Wysłany formularz", message=
                                    "Wysłano formularz! \n"
                                    "Imie : "+self.imie.get()+"\n"+
                                    "Email : "+self.email.get()+"\n"+
                                    "Wiek : "+self.wiekvalue.get()+"\n"+
                                    "Zainteresowania : Boks i Szachy \n"+
                                    "Uwagi : "+self.uwagi.get("1.0", "end")
                                    )
            else :
                messagebox.showinfo(
                    title="Wysłany formularz", message=
                    "Wysłano formularz! \n"
                    "Imie : " + self.imie.get() + "\n" +
                    "Email : " + self.email.get() + "\n" +
                    "Wiek : " + self.wiekvalue.get() + "\n" +
                    "Zainteresowania : Boks \n" +
                    "Uwagi : " + self.uwagi.get("1.0", "end")
                                    )
        else :
            if(self.szachyvalue.get()):
                messagebox.showinfo(
                    title="Wysłany formularz", message=
                    "Wysłano formularz! \n"
                    "Imie : " + self.imie.get() + "\n" +
                    "Email : " + self.email.get() + "\n" +
                    "Wiek : " + self.wiekvalue.get() + "\n" +
                    "Zainteresowania : Szachy \n" +
                    "Uwagi : " + self.uwagi.get("1.0", "end")
                )
            else :
                messagebox.showinfo(
                title="Wysłany formularz", message=
                "Wysłano formularz! \n"
                "Imie : " + self.imie.get() + "\n" +
                "Email : " + self.email.get() + "\n" +
                "Wiek : " + self.wiekvalue.get() + "\n" +
                "Zainteresowania : Brak \n" +
                "Uwagi : " + self.uwagi.get("1.0", "end")
            )
formularz = Formularz()