#Budujemy na tym pliku, tu działa autozapis do .txt

import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
import os

# Plik do automatycznego zapisu
PLIK = "listy_zakupow.txt"

class AplikacjaListaZakupow:
    def __init__(self, root):
        self.root = root
        self.root.title("Lista Zakupów")
        self.root.geometry("400x500")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f0f0")

        self.listy = {}  # Słownik przechowujący listy zakupów

        # Nagłówek
        self.label = tk.Label(root, text="Twoje Listy Zakupów", font=("Arial", 16, "bold"), bg="#f0f0f0")
        self.label.pack(pady=10)

        # Interfejs użytkownika
        self.przyciski_frame = tk.Frame(root, bg="#f0f0f0")
        self.przyciski_frame.pack(pady=5)

        self.add_list_button = tk.Button(self.przyciski_frame, text="Dodaj listę", width=15, command=self.dodaj_liste)
        self.add_list_button.grid(row=0, column=0, padx=5, pady=5)

        self.delete_list_button = tk.Button(self.przyciski_frame, text="Usuń listę", width=15, command=self.usun_liste)
        self.delete_list_button.grid(row=0, column=1, padx=5, pady=5)

        self.search_button = tk.Button(self.przyciski_frame, text="Szukaj listy", width=15, command=self.szukaj_listy)
        self.search_button.grid(row=1, column=0, padx=5, pady=5)

        self.save_button = tk.Button(self.przyciski_frame, text="Zapisz do pliku", width=15, command=self.zapisz_do_pliku)
        self.save_button.grid(row=1, column=1, padx=5, pady=5)

        self.listbox = tk.Listbox(root, font=("Arial", 12), height=15, bg="white", selectbackground="#c0d6e4")
        self.listbox.pack(pady=10, fill=tk.BOTH, expand=True, padx=10)
        self.listbox.bind('<Double-1>', self.wyswielt_i_edytuj_liste)

        self.wczytaj_liste()
        self.odswiez_liste()

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # Funkcjonalności

    def dodaj_liste(self):
        self.root.resizable(False, False)
        tytul = simpledialog.askstring("Nowa lista", "Podaj nazwę listy:")
        if tytul is None:
            return
        while not tytul:
            messagebox.showwarning("Błąd", "Podaj tytuł listy")
            tytul = simpledialog.askstring("Nowa lista", "Podaj nazwę listy:")
            if tytul is None:
                return

        if tytul in self.listy:
            messagebox.showwarning("Błąd", "Lista o tym tytule już istnieje")
            tytul = simpledialog.askstring("Nowa lista", "Podaj nazwę listy:")
            if tytul is None:
                return

        pozycje = simpledialog.askstring("Pozycje", "Wprowadź pozycje oddzielone przecinkami")
        if pozycje:
            self.listy[tytul] = [p.strip() for p in pozycje.split(',')]
            self.odswiez_liste()

    def usun_liste(self):
        wybor = self.listbox.curselection()
        if not wybor:
            messagebox.showwarning("Błąd", "Nie wybrano listy")
            return
        tytul = self.listbox.get(wybor)
        del self.listy[tytul]
        self.odswiez_liste()

    def szukaj_listy(self):         #to możemy poprawić żeby actually szukało
        nazwa = simpledialog.askstring("Szukaj", "Podaj nazwę listy")
        if nazwa is None:
            return
        if nazwa in self.listy:
            pozycje = self.listy[nazwa]
            messagebox.showinfo(f"Lista: {nazwa}", "\n".join(pozycje))
        else:
            messagebox.showwarning("Nie znaleziono", "Brak listy o podanej nazwie")

    def zapisz_do_pliku(self):
        sciezka = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Pliki tekstowe", "*.txt")])
        if sciezka:
            with open(sciezka, 'w', encoding='utf-8') as f:
                for tytul, pozycje in self.listy.items():
                    f.write(f"{tytul}:{','.join(pozycje)}\n")
            messagebox.showinfo("Zapisano", f"Zapisano do {sciezka}")

    def wyswielt_i_edytuj_liste(self, event):
        wybor = self.listbox.curselection()
        if not wybor:
            return
        tytul = self.listbox.get(wybor)

        nowe_pozycje = simpledialog.askstring(tytul, "Pozycje", 
            initialvalue=", ".join(self.listy[tytul]))
        if nowe_pozycje:
            self.listy[tytul] = [p.strip() for p in nowe_pozycje.split(',')]

        self.odswiez_liste()

    def odswiez_liste(self):
        self.listbox.delete(0, tk.END)
        for tytul in self.listy:
            self.listbox.insert(tk.END, tytul)

    def zapisz_liste(self):
        with open(PLIK, 'w', encoding='utf-8') as f:
            for tytul, pozycje in self.listy.items():
                f.write(f"{tytul}:{','.join(pozycje)}\n")

    def wczytaj_liste(self):
        if os.path.exists(PLIK):
            with open(PLIK, 'r', encoding='utf-8') as f:
                for linia in f:
                    if ':' in linia:
                        tytul, pozycje = linia.strip().split(':', 1)
                        self.listy[tytul] = [p.strip() for p in pozycje.split(',') if p.strip()]

    def on_close(self):
        self.zapisz_liste()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    AplikacjaListaZakupow(root)
    root.mainloop()
