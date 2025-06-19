#Budujemy na tym pliku, tu działa autozapis do .txt
# ostatni edit: Krzychu 19.06.2025
# zmiany:
# - poprawione wyszukiwanie po nazwie produktu (trzeba wpisać min 3 znaki)
#   (zmiany w funkcjach 'dodaj_liste' i 'okno_listy zakupow')
# - poprawiony interfejs graficzny - wyświetlanie okna na środku, kolorki itd
#   (zmiana w funkcji 'init')

import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
import os

# Plik do automatycznego zapisu
PLIK = "listy_zakupow.txt"

class AplikacjaListaZakupow:
    def __init__(self, root):
        # Ustawienie rozmiaru i wyśrodkowanie okna (edit: 19.06 KB)
        szerokosc_okna = 600
        wysokosc_okna = 400
        ekran_szer = root.winfo_screenwidth()
        ekran_wys = root.winfo_screenheight()
        x = (ekran_szer // 2) - (szerokosc_okna // 2)
        y = (ekran_wys // 2) - (wysokosc_okna // 2)
        root.geometry(f"{szerokosc_okna}x{wysokosc_okna}+{x}+{y}")

        self.root = root
        self.root.title("Lista Zakupów")

        self.listy = {}  # Słownik przechowujący listy zakupów

        # Interfejs użytkownika (buttony)
        self.title_entry = tk.Entry(root, font=("Helvetica", 12))
        self.title_entry.pack()

        self.add_list_button = tk.Button(root, text="Dodaj listę", command=self.dodaj_liste,
                                 bg="#4CAF50", fg="white", font=("Helvetica", 11), relief="flat")
        self.add_list_button.pack()

        self.search_button = tk.Button(root, text="Szukaj listy", command=self.szukaj_listy,
                               bg="#2196F3", fg="white", font=("Helvetica", 11), relief="flat")
        self.search_button.pack()

        self.save_button = tk.Button(root, text="Zapisz do pliku", command=self.zapisz_do_pliku,
                             bg="#FF9800", fg="white", font=("Helvetica", 11), relief="flat")
        self.save_button.pack()

        self.listbox = tk.Listbox(root, font=("Helvetica", 12), bg="white", fg="black",
                          selectbackground="#90CAF9", selectforeground="black", height=10)
        self.listbox.pack()
        self.listbox.bind('<Double-1>', self.edytuj_lub_usun_liste)

        self.wczytaj_liste()
        self.odswiez_liste()

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # Kolor tła głównego okna
        self.root.configure(bg="#f0f4f8")

        # Funkcjonalności (funkcje listy zakupów)
    def dodaj_liste(self):
        self.okno_listy_zakupow()

    def okno_listy_zakupow(self, tytul_poczatkowy="", pozycje_poczatkowe=None):
        is_edit = bool(tytul_poczatkowy)
        okno = tk.Toplevel(self.root)
        okno.title("Edytuj listę" if is_edit else "Nowa lista")

        tk.Label(okno, text="Tytuł listy:").pack(pady=(10, 0))
        entry_tytul = tk.Entry(okno, width=40)
        entry_tytul.pack(pady=5)
        entry_tytul.insert(0, tytul_poczatkowy)

        tk.Label(okno, text="Składniki:").pack(pady=(10, 0))
        lista_box = tk.Listbox(okno, width=40, height=10, font=("Helvetica", 12))
        lista_box.pack(padx=10, pady=5)

        if pozycje_poczatkowe:
            for p in pozycje_poczatkowe:
                lista_box.insert(tk.END, p)

        frame_input = tk.Frame(okno)
        frame_input.pack()

        entry_skladnik = tk.Entry(frame_input, width=30)
        entry_skladnik.pack(side=tk.LEFT, padx=5)

        def dodaj_skladnik():
            tekst = entry_skladnik.get().strip()
            if tekst:
                lista_box.insert(tk.END, tekst)
                entry_skladnik.delete(0, tk.END)

        def usun_skladnik():
            zaznaczony = lista_box.curselection()
            for i in reversed(zaznaczony):
                lista_box.delete(i)

        tk.Button(frame_input, text="Dodaj", command=dodaj_skladnik).pack(side=tk.LEFT)
        tk.Button(okno, text="Usuń zaznaczony", command=usun_skladnik).pack(pady=5)

        def zapisz():
            tytul = entry_tytul.get().strip()
            if not tytul:
                messagebox.showwarning("Błąd", "Tytuł nie może być pusty")
                return

            pozycje = [lista_box.get(i) for i in range(lista_box.size())]
            if not pozycje:
                messagebox.showwarning("Błąd", "Lista nie może być pusta")
                return

            if not is_edit and tytul in self.listy:
                messagebox.showwarning("Błąd", "Lista o takim tytule już istnieje")
                return

            self.listy[tytul] = pozycje
            self.odswiez_liste()
            okno.destroy()

        tk.Button(okno, text="Zapisz", command=zapisz).pack(pady=10)


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

        # Okno z wynikami
        wynik_okno = tk.Toplevel(self.root)
        wynik_okno.title("Wyniki wyszukiwania")

        wynik_listbox = tk.Listbox(wynik_okno, width=50, height=10, font=("Helvetica", 12))
        wynik_listbox.pack(padx=10, pady=10)

        for tytul in wyniki:
            wynik_listbox.insert(tk.END, tytul)

        def pokaz_skladniki(event):
            wybor = wynik_listbox.curselection()
            if not wybor:
                return
            tytul = wynik_listbox.get(wybor)
            skladniki = self.listy[tytul]

            # nowe okno z widokiem składników
            skladnik_okno = tk.Toplevel(wynik_okno)
            skladnik_okno.title(f"Lista: {tytul}")

            label = tk.Label(skladnik_okno, text=f"Składniki listy: {tytul}", font=("Helvetica", 14, "bold"))
            label.pack(pady=(10, 5))

            lista_skladnikow = tk.Listbox(skladnik_okno, width=40, height=len(skladniki), font=("Helvetica", 12))
            lista_skladnikow.pack(padx=10, pady=5)

            for item in skladniki:
                lista_skladnikow.insert(tk.END, item)

            def edytuj():
                nowe_pozycje = simpledialog.askstring("Edytuj pozycje", "Nowe pozycje oddzielone przecinkami",
                                                       initialvalue=", ".join(self.listy[tytul]))
                if nowe_pozycje:
                    self.listy[tytul] = [p.strip() for p in nowe_pozycje.split(',')]
                    self.odswiez_liste()
                    skladnik_okno.destroy()
                    wynik_okno.destroy()
                    messagebox.showinfo("Zmieniono", f"Zaktualizowano listę: {tytul}")

            btn_frame = tk.Frame(skladnik_okno)
            btn_frame.pack(pady=10)

            tk.Button(btn_frame, text="Edytuj", command=edytuj).pack(side=tk.LEFT, padx=5)
            tk.Button(btn_frame, text="Zamknij", command=skladnik_okno.destroy).pack(side=tk.LEFT, padx=5)

        wynik_listbox.bind("<Double-1>", pokaz_skladniki)



    def zapisz_do_pliku(self):
        sciezka = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Pliki tekstowe", "*.txt")])
        if sciezka:
            with open(sciezka, 'w', encoding='utf-8') as f:
                for tytul, pozycje in self.listy.items():
                    f.write(f"{tytul}:{','.join(pozycje)}\n")
            messagebox.showinfo("Zapisano", f"Zapisano do {sciezka}")

    def edytuj_lub_usun_liste(self, event):
        wybor = self.listbox.curselection()
        if not wybor:
            return
        tytul = self.listbox.get(wybor)

        akcja = messagebox.askquestion("Edycja lub usunięcie", "Czy chcesz edytować tę listę? (Nie = usuń)")
        if akcja == 'yes':
            self.okno_listy_zakupow(tytul_poczatkowy=tytul, pozycje_poczatkowe=self.listy[tytul])
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

