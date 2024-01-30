import sqlite3
import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import messagebox

conn = sqlite3.connect('database.db')
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS sites (url TEXT)')
conn.commit()
def add_site():
    site_url = entry_url.get()
    if not site_url:
        messagebox.showwarning("Warning", "Введіть URL сайту")
        return
    c.execute('INSERT INTO sites (url) VALUES (?)', (site_url,))
    conn.commit()
    entry_url.delete(0, tk.END)
    update_sites_list()
def clear_database():
    c.execute('DELETE FROM sites')
    conn.commit()
    update_sites_list()
def update_sites_list():
    sites_listbox.delete(0, tk.END)
    c.execute('SELECT * FROM sites')
    for row in c.fetchall():
        sites_listbox.insert(tk.END, row[0])
def search():
    query = entry_search.get()
    if not query:
        messagebox.showwarning("Warning", "Введіть дані для пошуку")
        return
    c.execute('SELECT * FROM sites')
    results = []
    for row in c.fetchall():
        site_url = row[0]
        try:
            response = requests.get(site_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            matches = soup.text.lower().count(query.lower())
            results.append((site_url, matches))
        except requests.RequestException:
            continue
    results.sort(key=lambda x: x[1], reverse=True)
    result_text.config(state=tk.NORMAL)
    result_text.delete(1.0, tk.END)
    for result in results:
        result_text.insert(tk.END, f"{result[0]} - Збігів: {result[1]}\n")
    result_text.config(state=tk.DISABLED)
root = tk.Tk()
root.title("Пошук на сторінках")
frame_add = tk.Frame(root)
frame_add.pack(pady=10)
label_url = tk.Label(frame_add, text="URL сайту:")
label_url.grid(row=0, column=0, padx=5)
entry_url = tk.Entry(frame_add, width=30)
entry_url.grid(row=0, column=1, padx=5)
btn_add_site = tk.Button(frame_add, text="Додати сайт", command=add_site)
btn_add_site.grid(row=0, column=2, padx=5)
frame_database = tk.Frame(root)
frame_database.pack(pady=10)
btn_clear_database = tk.Button(frame_database, text="Очистити базу даних", command=clear_database)
btn_clear_database.grid(row=0, column=0, padx=5)
btn_update_list = tk.Button(frame_database, text="Оновити список сайтів", command=update_sites_list)
btn_update_list.grid(row=0, column=1, padx=5)
frame_sites_list = tk.Frame(root)
frame_sites_list.pack(pady=10)
sites_listbox = tk.Listbox(frame_sites_list, width=50, height=10)
sites_listbox.grid(row=0, column=0, padx=5)
frame_search = tk.Frame(root)
frame_search.pack(pady=10)
label_search = tk.Label(frame_search, text="Пошук:")
label_search.grid(row=0, column=0, padx=5)
entry_search = tk.Entry(frame_search, width=30)
entry_search.grid(row=0, column=1, padx=5)
btn_search = tk.Button(frame_search, text="Пошук", command=search)
btn_search.grid(row=0, column=2, padx=5)
frame_results = tk.Frame(root)
frame_results.pack(pady=10)
result_text = tk.Text(frame_results, width=50, height=10, state=tk.DISABLED)
result_text.grid(row=0, column=0, padx=5)
update_sites_list()
root.mainloop()