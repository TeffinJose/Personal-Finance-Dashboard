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
        ttk.Button(frame, text="Register", command=lambda: self.show_Register_screen()).grid(row=2, column=1, pady=10)

    def show_Register_screen(self):
        self.clear_window()

        frame=ttk.Frame(self.root, padding="20")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        ttk.Label(frame, text="Enter Username").grid(row=0,column=0, pady=5)
        username = ttk.Entry(frame)
        username.grid(row=0, column=1, pady=5)

        ttk.Label(frame,text="Enter Password").grid(row=1,column=0,pady=5)
        password = ttk.Entry(frame,show="*")
        password.grid(row=1, column=1, pady=5)

        ttk.Label(frame, text="Confirm Password:").grid(row=2, column=0, pady=5)
        confirm_password = ttk.Entry(frame, show="*")
        confirm_password.grid(row=2, column=1, pady=5)

        ttk.Button(frame, text="Register",
                   command=lambda: self.register(username.get(), password.get(), confirm_password.get())
                 ).grid(row=3, column=0,columnspan=2, pady=10)
        
                
        ttk.Button(frame, text="Back to Login", 
                  command=self.show_login_screen
                 ).grid(row=4, column=0, columnspan=2, pady=5)
        
    def register(self, username, password, confirm_password):
        if not username or not password:
            messagebox.showerror("Error","Please do fill all the fields")
            return

        if password != confirm_password:
            messagebox.showerror("Error","Passwords don't match!")
            return
        
        if username in self.users:
            messagebox.showerror("Error","Username already exists!")
            return
        
        self.users[username] = password
        self.expenses[username]=[]
        self.save_data()
        messagebox.showinfo("Success!","Registration Successful!")
        self.show_login_screen()

    def login(self, username, password):
        if username in self.users and self.users[username] == password:
            self.current_user = username
            self.show_expense_screen()
        else:
            messagebox.showerror("Error","Invalid credentials!")

    def show_expense_screen(self):
        self.clear_window()

        #creating the main frame
        main_frame = ttk.Frame(self.root, padding = 20)
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
     
        #section to enter expenses
        entry_frame = ttk.Label(main_frame, text="Add Expenses",padding = 20)
        entry_frame.grid(row=0,column=0,padx=0,pady=5, sticky=(tk.W, tk.E))  

        catergories = ['Food','Transportation','Bills','Utilities','Shopping','Healthcare','Entertainment','Others']

        ttk.Label(entry_frame, text="Category: ").grid(row=0, column=0, pady=5)
        category_var = ttk.Combobox(entry_frame, values=categories)
        category_var.grid(row=0, column=1, pady=5)

        ttk.Label(entry_frame,text="Amount: ").grid(row=1,column=0,pady=5)
        amount_var = ttk.Combobox(entry_frame)
        amount_var.grid(row=1,column=1,pady=5)

        ttk.Label(entry_frame, text="Description").grid(row=2, column=0, pady=5)
        description_var = ttk.Combobox(entry_frame)
        description_var.grid(row=2,column=1,pady=5)

        ttk.Button(entry_frame, text="Add Expense", 
                  command=lambda: self.add_expense(category_var.get(), amount_var.get(), desc_var.get())
                 ).grid(row=3, column=0, columnspan=2, pady=10)
        
        #Visualization frame
        viz_frame = ttk.LabelFrame(main_frame, text="Finance Analysis", padding="0")
        viz_frame.grid(row=1, column=0,padx = 5, pady = 5, sticky=(tk.W, tk.E))

        self.plot_expenses(viz_frame)

        

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = PersonalFinanceTracker()
    app.run()