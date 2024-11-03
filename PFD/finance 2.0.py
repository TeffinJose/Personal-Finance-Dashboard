import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class ExpenseTracker:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Expense Tracker")
        self.root.geometry("800x600")
        self.root.configure(bg="#63afde") 
        
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
        
        ttk.Label(frame, text="Username:").grid(row=0, column=0, pady=5)
        username = ttk.Entry(frame)
        username.grid(row=0, column=1, pady=5)
        
        ttk.Label(frame, text="Password:").grid(row=1, column=0, pady=5)
        password = ttk.Entry(frame, show="*")
        password.grid(row=1, column=1, pady=5)
        
        ttk.Button(frame, text="Login", command=lambda: self.login(username.get(), password.get())).grid(row=2, column=0, pady=10)
        ttk.Button(frame, text="Register", command=lambda: self.show_register_screen()).grid(row=2, column=1, pady=10)
        
    def show_register_screen(self):
        self.clear_window()
        
        frame = ttk.Frame(self.root, padding="20")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        ttk.Label(frame, text="Enter Username:").grid(row=0, column=0, pady=5)
        username = ttk.Entry(frame)
        username.grid(row=0, column=1, pady=5)
        
        ttk.Label(frame, text="Enter Password:").grid(row=1, column=0, pady=5)
        password = ttk.Entry(frame, show="*")
        password.grid(row=1, column=1, pady=5)
        
        ttk.Label(frame, text="Confirm Password:").grid(row=2, column=0, pady=5)
        confirm_password = ttk.Entry(frame, show="*")
        confirm_password.grid(row=2, column=1, pady=5)
        
        ttk.Button(frame, text="Register", 
                  command=lambda: self.register(username.get(), password.get(), confirm_password.get())
                 ).grid(row=3, column=0, columnspan=2, pady=10)
        
        ttk.Button(frame, text="Back to Login", 
                  command=self.show_login_screen
                 ).grid(row=4, column=0, columnspan=2, pady=5)
        
    def register(self, username, password, confirm_password):
        if not username or not password:
            messagebox.showerror("Error", "Please fill all fields")
            return
            
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords not Matching!")
            return
            
        if username in self.users:
            messagebox.showerror("Error", "Username already exists!")
            return
            
        self.users[username] = password
        self.expenses[username] = []
        self.save_data()
        messagebox.showinfo("Success", "Registration successful!")
        self.show_login_screen()
        
    def login(self, username, password):
        if username in self.users and self.users[username] == password:
            self.current_user = username
            self.show_expense_screen()
        else:
            messagebox.showerror("Error", "Invalid credentials")
            
    def show_expense_screen(self):
        self.clear_window()

        # Parent frame to center the main content within the window
        parent_frame = ttk.Frame(self.root)
        parent_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)  # Center the parent frame

        # Main frame inside the centered parent frame
        main_frame = ttk.Frame(parent_frame, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Expense entry section
        entry_frame = ttk.LabelFrame(main_frame, text="Add Expense", padding="8")
        entry_frame.grid(row=0, column=0, padx=5, pady=5, sticky=(tk.W, tk.E))

        categories = ['Food', 'Transportation', 'Housing', 'Utilities', 'Entertainment', 'Shopping', 'Healthcare', 'Other']

        ttk.Label(entry_frame, text="Category:").grid(row=0, column=0, pady=3)
        category_var = ttk.Combobox(entry_frame, values=categories)
        category_var.grid(row=0, column=1, pady=3)

        ttk.Label(entry_frame, text="Amount:").grid(row=1, column=0, pady=3)
        amount_var = ttk.Entry(entry_frame)
        amount_var.grid(row=1, column=1, pady=3)

        ttk.Label(entry_frame, text="Description:").grid(row=2, column=0, pady=3)
        desc_var = ttk.Entry(entry_frame)
        desc_var.grid(row=2, column=1, pady=3)

        ttk.Button(entry_frame, text="Add Expense", 
                command=lambda: self.add_expense(category_var.get(), amount_var.get(), desc_var.get())
                ).grid(row=3, column=0, columnspan=2, pady=8)

        # Visualization section
        viz_frame = ttk.LabelFrame(main_frame, text="Expense Analysis", padding="8")
        viz_frame.grid(row=1, column=0, padx=5, pady=5, sticky=(tk.W, tk.E))

        self.plot_expenses(viz_frame)

        # Savings recommendations section
        rec_frame = ttk.LabelFrame(main_frame, text="Savings Recommendations", padding="8")
        rec_frame.grid(row=2, column=0, padx=5, pady=5, sticky=(tk.W, tk.E))

        self.show_recommendations(rec_frame)

        # Logout button
        ttk.Button(main_frame, text="Logout", 
                command=self.show_login_screen
                ).grid(row=3, column=0, pady=8)

        
    def add_expense(self, category, amount, description):
        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount")
            return
            
        if not category:
            messagebox.showerror("Error", "Please select a category")
            return
            
        expense = {
            "category": category,
            "amount": amount,
            "description": description,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        self.expenses[self.current_user].append(expense)
        self.save_data()
        messagebox.showinfo("Success", "Expense added successfully!")
        self.show_expense_screen()
        
    def plot_expenses(self, frame):
        if not self.expenses[self.current_user]:
            ttk.Label(frame, text="No expenses recorded yet").grid(row=0, column=0)
            return
            
        # Calculate total expenses by category
        category_totals = {}
        for expense in self.expenses[self.current_user]:
            category = expense['category']
            amount = expense['amount']
            category_totals[category] = category_totals.get(category, 0) + amount
            
        # Create pie chart
        fig, ax = plt.subplots(figsize=(6, 4))
        labels = list(category_totals.keys())
        sizes = list(category_totals.values())
        
        ax.pie(sizes, labels=labels, autopct='%1.1f%%')
        ax.set_title('Expenses by Category')
        
        canvas = FigureCanvasTkAgg(fig, frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0)
        
    def show_recommendations(self, frame):
        if not self.expenses[self.current_user]:
            ttk.Label(frame, text="Add expenses to get savings recommendations").grid(row=0, column=0)
            return
            
        # Calculate category percentages
        total_expenses = sum(expense['amount'] for expense in self.expenses[self.current_user])
        category_percentages = {}
        for expense in self.expenses[self.current_user]:
            category = expense['category']
            amount = expense['amount']
            category_percentages[category] = category_percentages.get(category, 0) + (amount / total_expenses * 100)
            
        # Define recommended percentages
        recommended = {
            'Housing': 30,
            'Food': 15,
            'Transportation': 10,
            'Utilities': 10,
            'Entertainment': 5,
            'Shopping': 10,
            'Healthcare': 10,
            'Other': 10
        }
        
        # Generate recommendations
        text = "Savings Recommendations:\n\n"
        for category, percentage in category_percentages.items():
            if category in recommended and percentage > recommended[category]:
                diff = percentage - recommended[category]
                text += f"• Consider reducing {category} expenses by {diff:.1f}%\n"
                text += f"  (Current: {percentage:.1f}%, Recommended: {recommended[category]}%)\n\n"
                
        ttk.Label(frame, text=text).grid(row=0, column=0, sticky=tk.W)
        
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = ExpenseTracker()
    app.run()