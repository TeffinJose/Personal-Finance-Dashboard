import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class PersonalFinanceTracker:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Personal Finance Tracker")
        self.root.geometry("800x600")
        self.root.configure(bg="#63afde")  # Light blue background

 
        # Load user data
        self.users_file = "users.json"
        self.expenses_file = "expenses.json"
        self.load_data()
        
        self.current_user = None
        self.show_login_screen()


    def load_data(self):
        # Load users
        if os.path.exists(self.users_file):
            with open(self.users_file, 'r') as f:
                self.users = json.load(f)
        else:
            self.users = {}
            
        # Load expenses
        if os.path.exists(self.expenses_file):
            with open(self.expenses_file, 'r') as f:
                self.expenses = json.load(f)
        else:
            self.expenses = {}
            
    def save_data(self):
        # Save users
        with open(self.users_file, 'w') as f:
            json.dump(self.users, f)
            
        # Save expenses
        with open(self.expenses_file, 'w') as f:
            json.dump(self.expenses, f)
            
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()
            
    def show_login_screen(self):
        self.clear_window()
        
        frame = ttk.Frame(self.root, padding="20")
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        ttk.Label(frame, text="Enter Username:").grid(row=0, column=0, pady=5)
        username = ttk.Entry(frame)
        username.grid(row=0, column=1, pady=5)
        
        ttk.Label(frame, text="Enter Password:").grid(row=1, column=0, pady=5)
        password = ttk.Entry(frame, show="*")
        password.grid(row=1, column=1, pady=5)
        
        ttk.Button(frame, text="Login", command=lambda: self.login(username.get(), password.get())).grid(row=2, column=0, pady=10)
        ttk.Button(frame, text="Register", command=lambda: self.show_register_screen()).grid(row=2, column=1, pady=10)

    def show_Register_screen(self):
        self.clear_window()

        frame=ttk.Frame(self.root, padding="20")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        ttk.Label(frame, text="Enter Username").grid(row=0,column=0, pady=5)
        username = ttk.Entry(frame, show="*")
        username.grid(row=0, column=1, pady=5)

        ttk.Label(frame,text="Enter Password").grid(row=1,column=0,pady=5)
        password = ttk.Entry(frame,show="*")
        password.grid(row=1, column=1, pady=5)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = PersonalFinanceTracker()
    app.run()