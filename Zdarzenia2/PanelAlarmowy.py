import tkinter as tk

class PanelAlarmowy():
    status_panel = None
    def __init__(self):
        root = tk.Tk()
        root.title("Formularz Rejestracyjny")
        root.geometry("300x100")

        self.status_panel = tk.Label(
            root,
            text="SYSTEM ROZBROJONY",
            bg="green",
            fg="black",
            font=('Arial', 16, 'bold'),
            width=25,
            height=3
        )
        self.status_panel.pack(padx=20, pady=20)

        self.status_panel.bind('<Enter>', self.na_najechaniu)
        self.status_panel.bind('<Button-1>', self.na_kliknieciu)
        self.status_panel.bind('<Leave>', self.na_opuszczeniu)

        root.mainloop()

    def na_najechaniu(self, event):
        self.status_panel.config(text = "UZBROJENIE MOŻLIWE", bg = "yellow", fg = "black")

    def na_kliknieciu(self, event):
        self.status_panel.config(text = "SYSTEM UZBROJONY", bg = "red")

    def na_opuszczeniu(self, event):
        self.status_panel.config(text = "SYSTEM ROZBROJONY", bg = "green")

panelalarmowy = PanelAlarmowy()