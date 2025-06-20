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
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f4f8")  # już jedno ustawienie wystarczy
        self.ustaw_okno(400, 500, 0, 0, self.root) # ustawia okno 

        self.listy = {}

        # Nagłówek
        self.label = tk.Label(root, text="Twoje Listy Zakupów", font=("Arial", 16, "bold"), bg="#f0f4f8")
        self.label.pack(pady=10)

        # Interfejs użytkownika (jeden frame do gridowania przycisków)
        self.przyciski_frame = tk.Frame(root, bg="#f0f4f8")
        self.przyciski_frame.pack(pady=5)

        self.add_list_button = tk.Button(
            self.przyciski_frame, text="Dodaj listę", width=15, command=self.dodaj_liste,
            bg="#4CAF50", fg="white", activebackground="#45A049", relief=tk.FLAT
        )
        self.add_list_button.grid(row=0, column=0, padx=5, pady=5)

        self.delete_list_button = tk.Button(
            self.przyciski_frame, text="Usuń listę", width=15, command=self.usun_liste,
            bg="#f44336", fg="white", activebackground="#da190b", relief=tk.FLAT
        )
        self.delete_list_button.grid(row=0, column=1, padx=5, pady=5)

        self.search_button = tk.Button(
            self.przyciski_frame, text="Szukaj listy", width=15, command=self.szukaj_listy,
            bg="#2196F3", fg="white", activebackground="#0b7dda", relief=tk.FLAT
        )
        self.search_button.grid(row=1, column=0, padx=5, pady=5)

        self.save_button = tk.Button(
            self.przyciski_frame, text="Zapisz do pliku", width=15, command=self.zapisz_do_pliku,
            bg="#9C27B0", fg="white", activebackground="#7b1fa2", relief=tk.FLAT
        )
        self.save_button.grid(row=1, column=1, padx=5, pady=5)

        self.listbox = tk.Listbox(root, font=("Arial", 12), height=15, bg="white", selectbackground="#c0d6e4")
        self.listbox.pack(pady=10, fill=tk.BOTH, expand=True, padx=10)

        self.listbox.bind('<Double-1>', lambda event: self.wyswielt_i_edytuj_liste(event))
        self.listbox.bind('<space>', lambda event: self.wyswielt_i_edytuj_liste(event))

        self.wczytaj_liste()
        self.odswiez_liste()

        self.root.protocol("WM_DELETE_WINDOW", self.zamknij_okno)


    # Funkcjonalności

    def dodaj_liste(self):
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
        # print("usun_liste_ok")
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

    def szukaj_listy(self):
        zapytanie = simpledialog.askstring("Szukaj", "Wpisz co najmniej 3 znaki (nazwa lub pozycja)")
        while len(zapytanie.strip()) < 3:
            messagebox.showwarning("Błąd", "Wprowadź co najmniej 3 znaki.")
            zapytanie = simpledialog.askstring("Szukaj", "Wpisz co najmniej 3 znaki (nazwa lub pozycja)")
            if zapytanie is None:
                return

        zapytanie = zapytanie.lower().strip()
        wyniki = []

        for tytul, pozycje in self.listy.items():
            if zapytanie in tytul.lower() or any(zapytanie in p.lower() for p in pozycje):
                wyniki.append(tytul)

        if not wyniki:
            messagebox.showinfo("Brak wyników", "Nie znaleziono pasujących list.")
            return

        # Okno z wynikami
        wynik_okno = tk.Toplevel(self.root)
        wynik_okno.title(f"Wyniki wyszukiwania: {zapytanie}")
        wynik_okno.resizable(False, False)
        self.ustaw_okno(400, 250, 0, 80, wynik_okno)
        # wynik_okno.transient(self.root)
        # wynik_okno.grab_set()
        wynik_okno.focus_force()

        wynik_listbox = tk.Listbox(wynik_okno, width=50, height=10, font=("Helvetica", 12))
        wynik_listbox.pack(padx=10, pady=10)

        for tytul in wyniki:
            wynik_listbox.insert(tk.END, tytul)

        wynik_listbox.bind("<Double-1>", lambda event: self.wyswielt_i_edytuj_liste(event))
        wynik_listbox.bind("<space>", lambda event: self.wyswielt_i_edytuj_liste(event))

        zamknij_btn = tk.Button(wynik_okno, text="Zamknij", command=wynik_okno.destroy)
        zamknij_btn.pack(pady=(0, 10))

    def zapisz_do_pliku(self):
        sciezka = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Pliki tekstowe", "*.txt")])
        if sciezka:
            with open(sciezka, 'w', encoding='utf-8') as f:
                for tytul, pozycje in self.listy.items():
                    f.write(f"{tytul}:{','.join(pozycje)}\n")
            messagebox.showinfo("Zapisano", f"Zapisano do {sciezka}")

    def wyswielt_i_edytuj_liste(self, event=None, tytul=None):
        if event:
            widget = event.widget
            wybor = widget.curselection()
            if not wybor:
                return
            tytul = widget.get(wybor[0])
        if tytul is None:
            return

        okno = Toplevel(self.root)
        okno.title(f"Lista: {tytul}")
        okno.resizable(False, False)
        self.ustaw_okno(300, 225, 0, 100, okno)
        okno.focus_force()

        oryginalne = list(self.listy[tytul])

        lista = tk.Listbox(okno, selectmode=tk.SINGLE, width=50)
        lista.pack(padx=10, pady=10)

        for pozycja in self.listy[tytul]:
            lista.insert(tk.END, pozycja)

        def zapisz():
            nowe = lista.get(0, tk.END)
            self.listy[tytul] = [p.strip() for p in nowe if p.strip()]
            self.odswiez_liste()
            okno.destroy()

        def dodaj():
            nowa = simpledialog.askstring("Dodaj pozycje", "Wpisz nowe pozycje  po przecinku:", parent=okno)
            if nowa:
                for pozycja in nowa.split(','):
                    p = pozycja.strip()
                    if p:
                        lista.insert(tk.END, p)

        def usun():
            zaznaczony = lista.curselection()
            if not zaznaczony:
                return
            lista.delete(zaznaczony[0])
            if lista.size() > 0:
                nowy = min(zaznaczony[0], lista.size() - 1)
                lista.select_set(nowy)
                lista.activate(nowy)

        def zamknij_okno():
            aktualne = [lista.get(i) for i in range(lista.size())]
            if aktualne != oryginalne:
                if messagebox.askyesno("Niezapisane zmiany", "Masz niezapisane zmiany. Czy chcesz je zapisać?"):
                    zapisz()
            okno.destroy()


        przyciski = tk.Frame(okno)
        przyciski.pack(pady=5)

        tk.Button(przyciski, text="Dodaj", command=dodaj).pack(side=tk.LEFT, padx=5)
        tk.Button(przyciski, text="Usuń zaznaczony", command=usun).pack(side=tk.LEFT, padx=5)
        tk.Button(przyciski, text="Zapisz i zamknij", command=zapisz).pack(side=tk.LEFT, padx=5)

        okno.protocol("WM_DELETE_WINDOW", zamknij_okno)

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

    def ustaw_okno(self, okno_szerokosc: int, okno_wysokosc: int, x: int, y: int, okno):
        x += (okno.winfo_screenwidth() // 2) - (okno_szerokosc // 2)
        y += (okno.winfo_screenheight() // 2) - (okno_wysokosc // 2)

        okno.geometry(f"{okno_szerokosc}x{okno_wysokosc}+{x}+{y}")


    def zamknij_okno(self):
        self.zapisz_liste()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    AplikacjaListaZakupow(root)
    root.mainloop()