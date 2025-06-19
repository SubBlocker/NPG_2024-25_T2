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

        self.listy = {}  # Słownik przechowujący listy zakupów

        # Interfejs użytkownika (buttony)
        self.title_entry = tk.Entry(root)
        self.title_entry.pack()

        self.add_list_button = tk.Button(root, text="Dodaj listę", command=self.dodaj_liste)
        self.add_list_button.pack()

        self.search_button = tk.Button(root, text="Szukaj listy", command=self.szukaj_listy)
        self.search_button.pack()

        self.save_button = tk.Button(root, text="Zapisz do pliku", command=self.zapisz_do_pliku)
        self.save_button.pack()

        self.listbox = tk.Listbox(root)
        self.listbox.pack()
        self.listbox.bind('<Double-1>', self.edytuj_lub_usun_liste)

        self.wczytaj_liste()
        self.odswiez_liste()

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # Funkcjonalności (funkcje listy zakupów)
    def dodaj_liste(self):          #możemy zrobić wyskakujące okienko zamiast paska na górze
        tytul = self.title_entry.get().strip()
        if not tytul:
            messagebox.showwarning("Błąd", "Podaj tytuł listy")
            return

        if tytul in self.listy:
            messagebox.showwarning("Błąd", "Lista o tym tytule już istnieje")
            return

        pozycje = simpledialog.askstring("Pozycje", "Wprowadź pozycje oddzielone przecinkami")
        if pozycje:
            self.listy[tytul] = [p.strip() for p in pozycje.split(',')]
            self.odswiez_liste()

    def szukaj_listy(self):
        zapytanie = simpledialog.askstring("Szukaj", "Wpisz co najmniej 3 znaki (nazwa lub pozycja)")
        if not zapytanie or len(zapytanie.strip()) < 3:
            messagebox.showwarning("Błąd", "Wprowadź co najmniej 3 znaki.")
            return

        zapytanie = zapytanie.lower().strip()
        wyniki = []

        for tytul, pozycje in self.listy.items():
            if zapytanie in tytul.lower() or any(zapytanie in p.lower() for p in pozycje):
                wyniki.append(tytul)

        if not wyniki:
            messagebox.showinfo("Brak wyników", "Nie znaleziono pasujących list.")
            return

        # Nowe okno z wynikami
        wynik_okno = tk.Toplevel(self.root)
        wynik_okno.title("Wyniki wyszukiwania")

        wynik_listbox = tk.Listbox(wynik_okno, width=50)
        wynik_listbox.pack(padx=10, pady=10)
        for tytul in wyniki:
            wynik_listbox.insert(tk.END, tytul)

        def edytuj_po_kliknieciu(event):
            wybor = wynik_listbox.curselection()
            if not wybor:
                return
            tytul = wynik_listbox.get(wybor)

            nowe_pozycje = simpledialog.askstring(
                "Edytuj pozycje",
                "Nowe pozycje oddzielone przecinkami",
                initialvalue=", ".join(self.listy[tytul])
            )
            if nowe_pozycje is not None:
                self.listy[tytul] = [p.strip() for p in nowe_pozycje.split(',')]
                self.odswiez_liste()
                messagebox.showinfo("Zmieniono", f"Zaktualizowano listę: {tytul}")
                wynik_okno.destroy()

        wynik_listbox.bind("<Double-1>", edytuj_po_kliknieciu)


    def zapisz_do_pliku(self):
        sciezka = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Pliki tekstowe", "*.txt")])
        if sciezka:
            with open(sciezka, 'w', encoding='utf-8') as f:
                for tytul, pozycje in self.listy.items():
                    f.write(f"{tytul}:{','.join(pozycje)}\n")
            messagebox.showinfo("Zapisano", f"Zapisano do {sciezka}")

    def edytuj_lub_usun_liste(self, event):     #to należy zmienić żeby nie usuwało
        wybor = self.listbox.curselection()
        if not wybor:
            return
        tytul = self.listbox.get(wybor)

        akcja = messagebox.askquestion("Edycja lub usunięcie", "Czy chcesz edytować tę listę? (Nie = usuń)")
        if akcja == 'yes':
            nowe_pozycje = simpledialog.askstring("Edytuj pozycje", "Nowe pozycje oddzielone przecinkami", 
                initialvalue=", ".join(self.listy[tytul]))
            if nowe_pozycje:
                self.listy[tytul] = [p.strip() for p in nowe_pozycje.split(',')]
        else:
            del self.listy[tytul]
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
    app = AplikacjaListaZakupow(root)
    root.mainloop()

