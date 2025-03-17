import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
import sqlite3

# Create or connect to the database
conn = sqlite3.connect("tasks.db")
cursor = conn.cursor()

# Create tasks table if not exists
cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task TEXT NOT NULL,
        category TEXT,
        due_date TEXT,
        status TEXT DEFAULT 'Pending'
    )
''')
conn.commit()


root = tk.Tk()
root.title("Advanced To-Do List")
root.geometry("600x400")
root.resizable(False, False)


tk.Label(root, text="Task:", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5, sticky="w")
task_entry = tk.Entry(root, font=("Arial", 12), width=40)
task_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Category:", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5, sticky="w")
category_entry = ttk.Combobox(root, values=["Work", "Personal", "Urgent", "Others"], font=("Arial", 12), width=18)
category_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Due Date:", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=5, sticky="w")
due_date_entry = DateEntry(root, font=("Arial", 12), width=18, date_pattern="yyyy-mm-dd")
due_date_entry.grid(row=2, column=1, padx=10, pady=5)


def add_task():
    task = task_entry.get()
    category = category_entry.get()
    due_date = due_date_entry.get()
    
    if task.strip() == "":
        messagebox.showwarning("Warning", "Task cannot be empty!")
        return

    cursor.execute("INSERT INTO tasks (task, category, due_date) VALUES (?, ?, ?)", (task, category, due_date))
    conn.commit()
    task_entry.delete(0, tk.END)
    load_tasks()


def load_tasks():
    task_list.delete(*task_list.get_children())  # Clear previous entries
    cursor.execute("SELECT id, task, category, due_date, status FROM tasks")
    for row in cursor.fetchall():
        task_list.insert("", "end", values=row)


def complete_task():
    selected_item = task_list.selection()
    if not selected_item:
        messagebox.showwarning("Warning", "Please select a task to mark as completed!")
        return

    task_id = task_list.item(selected_item)['values'][0]
    cursor.execute("UPDATE tasks SET status = 'Completed' WHERE id = ?", (task_id,))
    conn.commit()
    load_tasks()


def delete_task():
    selected_item = task_list.selection()
    if not selected_item:
        messagebox.showwarning("Warning", "Please select a task to delete!")
        return

    task_id = task_list.item(selected_item)['values'][0]
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    load_tasks()


tk.Button(root, text="Add Task", command=add_task, font=("Arial", 12), bg="green", fg="white").grid(row=3, column=0, padx=10, pady=10)
tk.Button(root, text="Complete Task", command=complete_task, font=("Arial", 12), bg="blue", fg="white").grid(row=3, column=1, padx=10, pady=10)
tk.Button(root, text="Delete Task", command=delete_task, font=("Arial", 12), bg="red", fg="white").grid(row=3, column=2, padx=10, pady=10)


task_list = ttk.Treeview(root, columns=("ID", "Task", "Category", "Due Date", "Status"), show="headings")
task_list.heading("ID", text="ID")
task_list.heading("Task", text="Task")
task_list.heading("Category", text="Category")
task_list.heading("Due Date", text="Due Date")
task_list.heading("Status", text="Status")
task_list.column("ID", width=30)
task_list.column("Task", width=200)
task_list.column("Category", width=100)
task_list.column("Due Date", width=100)
task_list.column("Status", width=80)
task_list.grid(row=4, column=0, columnspan=3, padx=10, pady=10)
load_tasks()


root.mainloop()
conn.close()
