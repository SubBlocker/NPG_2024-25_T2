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

        # Interfejs użytkownika

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
    def dodaj_liste(self):
        tytul = simpledialog.askstring("Nowa lista", "Podaj nazwę listy:")
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
        
        
        

    def szukaj_listy(self):         #to możemy poprawić żeby actually szukało
        nazwa = simpledialog.askstring("Szukaj", "Podaj nazwę listy")
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

