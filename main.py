import tkinter as tk
from tkinter import ttk
import mysql.connector

root = tk.Tk()
root.title("Students")
root.geometry("1200x600")
add_window = None
details_window = None
name_entry = None
surname_entry = None
birth_entry = None
id_entry = None
yearstudy_entry = None
way_entry = None


def open_details_window(event):

    selected_item = treeview.focus()

    global details_window, id_entry, name_entry, surname_entry, birth_entry, yearstudy_entry, way_entry
    if selected_item:
        item_data = treeview.item(selected_item)
        item_values = item_data["values"]

        details_window = tk.Toplevel(root)
        details_window.title("Szczegóły")

        id_label = ttk.Label(details_window, text="ID:")
        id_label.pack()
        id_entry = ttk.Entry(details_window)
        id_entry.insert(0, item_values[0])
        id_entry.config(state="disabled")
        id_entry.pack()

        name_label = ttk.Label(details_window, text="Imie:")
        name_label.pack()
        name_entry = ttk.Entry(details_window)
        name_entry.insert(0, item_values[1])
        name_entry.pack()

        surname_label = ttk.Label(details_window, text="Nazwisko:")
        surname_label.pack()
        surname_entry = ttk.Entry(details_window)
        surname_entry.insert(0, item_values[2])
        surname_entry.pack()

        birth_label = ttk.Label(details_window, text="Data Urodzenia:")
        birth_label.pack()
        birth_entry = ttk.Entry(details_window)
        birth_entry.insert(0, item_values[3])
        birth_entry.pack()

        category_label = ttk.Label(details_window, text="Rok Studiow:")
        category_label.pack()
        category_entry = ttk.Entry(details_window)
        category_entry.insert(0, item_values[4])
        category_entry.pack()

        way_label = ttk.Label(details_window, text="Kierunek studiow:")
        way_label.pack()
        way_entry = ttk.Entry(details_window)
        way_entry.insert(0, item_values[5])
        way_entry.pack()

        #update_button = ttk.Button(details_window, text="Aktualizuj", command=update_record)
        update_button = ttk.Button(details_window, text="Aktualizuj",
                                   command=lambda: update_data(item_values[0], name_entry.get(), surname_entry.get(),
                                                               birth_entry.get(), category_entry.get(),
                                                               way_entry.get()))
        update_button.pack()

        delete_button = ttk.Button(details_window, text="Usuń", command=delete_record)
        delete_button.pack()


def fetch_data():
    mydb = mysql.connector.connect(host="localhost", port="3306", user="root", password="zaq1@WSX", database="books")
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM student")
    result = mycursor.fetchall()
    mycursor.close()
    mydb.close()
    return result


def load_data():
    data = fetch_data()
    treeview.delete(*treeview.get_children())
    for row in data:
        treeview.insert("", "end", values=(row[0], row[1], row[2], row[3], row[4], row[5]))


def open_new_student_window():
    global add_window, name_entry, surname_entry, birth_entry, yearstudy_entry, tstudy_entry

    add_window = tk.Toplevel(root)
    add_window.title("Dodaj nowego studenta")

    name_label = ttk.Label(add_window, text="Imie:")
    name_label.pack()
    name_entry = ttk.Entry(add_window)
    name_entry.pack()

    surname_label = ttk.Label(add_window, text="Nazwisko:")
    surname_label.pack()
    surname_entry = ttk.Entry(add_window)
    surname_entry.pack()

    birth_label = ttk.Label(add_window, text="Data urodzenia:")
    birth_label.pack()
    birth_entry = ttk.Entry(add_window)
    birth_entry.pack()

    yearstudy_label = ttk.Label(add_window, text="Rok studiow:")
    yearstudy_label.pack()
    yearstudy_entry = ttk.Entry(add_window)
    yearstudy_entry.pack()

    tstudy_label = ttk.Label(add_window, text="Kierunek studiow:")
    tstudy_label.pack()
    tstudy_entry = ttk.Entry(add_window)
    tstudy_entry.pack()

    add_button = ttk.Button(add_window, text="Dodaj", command=add_new)
    add_button.pack()


def add_new():
    global name_entry, surname_entry, birth_entry, yearstudy_entry, tstudy_entry

    new_imie = name_entry.get()
    new_nazwisko = surname_entry.get()
    new_dataurodzenia = birth_entry.get()
    new_rokstudiow = yearstudy_entry.get()
    new_kierunekstudiow = tstudy_entry.get()

    mydb = mysql.connector.connect(
        host="localhost",
        port="3306",
        user="root",
        password="zaq1@WSX",
        database="books"
    )

    mycursor = mydb.cursor()
    sql = "INSERT INTO student (imie, nazwisko, dataurodzenia, rokstudiow, kierunekstudiow) VALUES (%s, %s, %s, %s, %s)"
    params = (new_imie, new_nazwisko, new_dataurodzenia, new_rokstudiow, new_kierunekstudiow)
    mycursor.execute(sql, params)

    mydb.commit()
    mycursor.close()
    mydb.close()

    load_data()
    add_window.destroy()





def update_data(id, name, surname, birthdate,year, way):
    mydb = mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        password="zaq1@WSX",
        database="books"
    )
    mycursor = mydb.cursor()

    sql = "UPDATE student SET imie = %s, nazwisko = %s, dataurodzenia = %s,  rokstudiow= %s , kierunekstudiow=%s WHERE id = %s"
    params = (name, surname, birthdate,year,way, id)
    mycursor.execute(sql, params)

    mydb.commit()
    mycursor.close()
    mydb.close()

    load_data()



def delete_record():
    global id_entry

    mydb = mysql.connector.connect(
        host="localhost",
        port="3306",
        user="root",
        password="zaq1@WSX",
        database="books"
    )

    mycursor = mydb.cursor()
    sql = "DELETE FROM student WHERE id = %s"
    params = (id_entry.get(),)
    mycursor.execute(sql, params)

    mydb.commit()
    mycursor.close()
    mydb.close()

    load_data()
    details_window.destroy()


label = tk.Label(root, text="usuwanie studentow:")

label = tk.Label(root, text="Wyswietlanie studentów:")
label.pack()
treeview = ttk.Treeview(root)
treeview["columns"] = ("id", "imie", "nazwisko", "dataurodzenia", "rokstudiow", "kierunekstudiow")
treeview.column("#0", width=0)
treeview.heading("id", text="ID")
treeview.heading("imie", text="Imie")
treeview.heading("nazwisko", text="Nazwisko")
treeview.heading("dataurodzenia", text="Data urodzenia")
treeview.heading("rokstudiow", text="Rok studiow")
treeview.heading("kierunekstudiow", text="Kierunek studiow")
treeview.bind("<Double-1>", open_details_window)
treeview.pack()

add_new_book_button = tk.Button(root, text="Dodaj nowego studenta", command=open_new_student_window)
add_new_book_button.pack()

load_data()
root.mainloop()
