import tkinter as tk
from tkinter import simpledialog, messagebox
import os
import subprocess

SZABLON_KODU = '''from tkinter import *
from tkinter import messagebox

def newTask():
    task = my_entry.get()
    if task != "":
        lb.insert(END, task)
        my_entry.delete(0, "end")
    else:
        messagebox.showwarning("warning", "Please enter some task.")

def deleteTask():
    lb.delete(ANCHOR)

ws = Tk()
ws.geometry('500x450+500+200')
ws.title('{tytul}')
ws.config(bg='#223441')
ws.resizable(width=False, height=False)

frame = Frame(ws)
frame.pack(pady=10)

lb = Listbox(
    frame,
    width=25,
    height=8,
    font=('Times', 18),
    bd=0,
    fg='#464646',
    highlightthickness=0,
    selectbackground='#a6a6a6',
    activestyle="none",
)
lb.pack(side=LEFT, fill=BOTH)

task_list = [
    'Eat apple',
    'drink water',
    'go gym',
    'write software',
    'write documentation',
    'take a nap',
    'Learn something',
    'paint canvas'
]

for item in task_list:
    lb.insert(END, item)

sb = Scrollbar(frame)
sb.pack(side=RIGHT, fill=BOTH)

lb.config(yscrollcommand=sb.set)
sb.config(command=lb.yview)

my_entry = Entry(ws, font=('times', 24))
my_entry.pack(pady=20)

button_frame = Frame(ws)
button_frame.pack(pady=20)

addTask_btn = Button(
    button_frame,
    text='Add Task',
    font=('times 14'),
    bg='#c5f776',
    padx=20,
    pady=10,
    command=newTask
)
addTask_btn.pack(fill=BOTH, expand=True, side=LEFT)

delTask_btn = Button(
    button_frame,
    text='Delete Task',
    font=('times 14'),
    bg='#ff8b61',
    padx=20,
    pady=10,
    command=deleteTask
)
delTask_btn.pack(fill=BOTH, expand=True, side=LEFT)

ws.mainloop()
'''

def odswiez_liste():
    listbox.delete(0, tk.END)
    for plik in os.listdir("."):
        if plik.startswith("lista_") and plik.endswith(".py"):
            listbox.insert(tk.END, plik)

def utworz_liste():
    nazwa = simpledialog.askstring("Nowa lista", "Podaj nazwę listy:")
    if not nazwa:
        return
    filename = f"lista_{nazwa}.py"
    if os.path.exists(filename):
        messagebox.showwarning("Błąd", "Taki plik już istnieje!")
        return
    with open(filename, "w", encoding="utf-8") as f:
        f.write(SZABLON_KODU.format(tytul=nazwa))
    odswiez_liste()

def usun_liste():
    selected = listbox.get(tk.ACTIVE)
    if selected:
        confirm = messagebox.askyesno("Potwierdź", f"Usunąć plik {selected}?")
        if confirm:
            os.remove(selected)
            odswiez_liste()

def uruchom_liste():
    selected = listbox.get(tk.ACTIVE)
    if selected:
        subprocess.Popen(["python", selected])

# GUI zarządcy
root = tk.Tk()
root.title("Zarządca list zadań")

listbox = tk.Listbox(root, width=40)
listbox.pack(pady=5)

tk.Button(root, text="➕ Utwórz nową listę", command=utworz_liste).pack(fill="x")
tk.Button(root, text="▶️ Uruchom zaznaczoną", command=uruchom_liste).pack(fill="x")
tk.Button(root, text="🗑 Usuń zaznaczoną", command=usun_liste).pack(fill="x")

odswiez_liste()
root.mainloop()
