import tkinter as tk
from tkinter import *
from tkinter import messagebox, ttk
import psycopg2

def create_table():
    conn = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="1234"
    )
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS books (id Serial PRIMARY KEY, name VARCHAR(255), author VARCHAR(255), fiction_or_nonfiction VARCHAR(255))"
    )
    conn.commit()
    cursor.close()
    conn.close()

def check_duplicate(name):
    conn = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="1234"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books WHERE LOWER(name)=LOWER(%s) OR name LIKE LOWER(%s)", (name, f"{name}%"))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result is not None

def add_book(name, author, fiction_or_nonfiction):
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="postgres",
            user="postgres",
            password="1234"
        )
        cursor = conn.cursor()
        cursor.execute("INSERT INTO books (name, author, fiction_or_nonfiction) VALUES (%s, %s, %s)", (name, author, fiction_or_nonfiction))
        conn.commit()
    except Exception as e:
        print(f"An error occurred while adding the book: {e}")
    finally:
        cursor.close()
        conn.close()



def add_book_to_db():
    book_name = book_name_entry.get()
    book_author = book_author_entry.get()
    fiction_or_nonfiction = combo_fiction_or_nonfiction.get()
    
    if book_name == "" or book_author == "":
        messagebox.showerror("Empty", "Enter all Details")
        book_name_entry.delete(0, tk.END)
        book_author_entry.delete(0, tk.END)
        combo_fiction_or_nonfiction.current(0)
        combo_fiction_or_nonfiction.set("") 
    
    elif combo_fiction_or_nonfiction == "":
        messagebox.showerror("Empty", "Select Fiction or Non-Fiction")
        book_name_entry.delete(0, tk.END)
        book_author_entry.delete(0, tk.END)
        combo_fiction_or_nonfiction.current(0)
        combo_fiction_or_nonfiction.set("") 
    
    
    elif check_duplicate(book_name):
        messagebox.showerror("Error", "A book with this name already exists.") 
        book_name_entry.delete(0, tk.END)
        book_author_entry.delete(0, tk.END)
        combo_fiction_or_nonfiction.current(0)
        combo_fiction_or_nonfiction.set("") 
        
    else:
        add_book(book_name, book_author, fiction_or_nonfiction)
        book_name_entry.delete(0, tk.END)
        book_author_entry.delete(0, tk.END)
        combo_fiction_or_nonfiction.current(0)
        combo_fiction_or_nonfiction.set("") 


def clear_box():
    fiction_or_nonfiction.set("")



create_table()
root = tk.Tk()
root.title("Books Manager")
root.geometry = ("400x200")
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

book_name_entry = ttk.Entry(mainframe, width=20)
book_name_entry.grid(column=2, row=1, sticky=(tk.W, tk.E))

book_author_entry = ttk.Entry(mainframe, width=20)
book_author_entry.grid(column=2, row=2, sticky=(tk.W, tk.E))

fiction_or_nonfiction = tk.StringVar()
combo_fiction_or_nonfiction = ttk.Combobox(mainframe, values=["Fiction", "Non-Fiction"], textvariable=fiction_or_nonfiction, width=20)
combo_fiction_or_nonfiction.grid(column=2, row=3, sticky=(tk.W, tk.E))


ttk.Label(mainframe, text="Book Name :").grid(column=1, row=1, sticky=tk.W)
ttk.Label(mainframe, text="Author :").grid(column=1, row=2, sticky=tk.W)
ttk.Label(mainframe, text="Genre :").grid(column=1, row=3, sticky=tk.W)

ttk.Button(mainframe, text="Add Book", command=lambda:[add_book_to_db(), clear_box()]).grid(column=2, row=4, pady=5)

for child in mainframe.winfo_children(): 
    child.grid_configure(padx=5, pady=5)

book_name_entry.focus()
root.mainloop()
