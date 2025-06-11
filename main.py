#Budujemy na tym pliku, tu działa autozapis do .txt

import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog, Toplevel
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
        self.listbox.bind('<Double-1>', lambda event: self.wyswielt_i_edytuj_liste(event))

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

        self.listy[tytul] = []
        self.odswiez_liste()
        self.wyswielt_i_edytuj_liste(None, tytul)

    def usun_liste(self):
        wybor = self.listbox.curselection()
        if not wybor:
            return
        indeks = wybor[0]
        tytul = self.listbox.get(indeks)
        del self.listy[tytul]
        self.odswiez_liste()

        if self.listbox.size() > 0:
            nastepny_wybor = min(indeks, self.listbox.size() - 1)
            self.listbox.select_set(nastepny_wybor)
            self.listbox.activate(nastepny_wybor)

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

    def wyswielt_i_edytuj_liste(self, event=None, tytul=None):
        if event:
            wybor = self.listbox.curselection()
            if not wybor:
                return
            tytul = self.listbox.get(wybor)
        if tytul is None:
            return

        okno = Toplevel(self.root)
        okno.title(f"Edytuj: {tytul}")
        okno.resizable(False, False)

        lista = tk.Listbox(okno, selectmode=tk.MULTIPLE, width=50)
        lista.pack(padx=10, pady=10)

        for pozycja in self.listy[tytul]:
            lista.insert(tk.END, pozycja)

        def zapisz():
            nowe = lista.get(0, tk.END)
            self.listy[tytul] = [p.strip() for p in nowe if p.strip()]
            self.odswiez_liste()
            okno.destroy()

        def dodaj():
            nowa = simpledialog.askstring("Dodaj pozycję", "Wpisz nową pozycję:", parent=okno)
            if nowa:
                lista.insert(tk.END, nowa.strip())

        def usun():
            zaznaczone = list(lista.curselection())
            if not zaznaczone:
                return
            for i in reversed(zaznaczone):
                lista.delete(i)
            if lista.size() > 0:
                nastepny_wybor = min(zaznaczone[0], lista.size() - 1)
                lista.select_set(nastepny_wybor)
                lista.activate(nastepny_wybor)

        przyciski = tk.Frame(okno)
        przyciski.pack(pady=5)

        tk.Button(przyciski, text="Dodaj", command=dodaj).pack(side=tk.LEFT, padx=5)
        tk.Button(przyciski, text="Usuń zaznaczone", command=usun).pack(side=tk.LEFT, padx=5)
        tk.Button(przyciski, text="Zapisz i zamknij", command=zapisz).pack(side=tk.LEFT, padx=5)


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
