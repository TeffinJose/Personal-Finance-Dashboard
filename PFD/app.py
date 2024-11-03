from flask import Flask, render_template, request, redirect, url_for, flash, session
import json
import os
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import io
import base64

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change to a secure key in production

# Load user and expenses data
def load_data():
    users_file = "users.json"
    expenses_file = "expenses.json"
    
    if os.path.exists(users_file):
        with open(users_file, 'r') as f:
            users = json.load(f)
    else:
        users = {}
    
    if os.path.exists(expenses_file):
        with open(expenses_file, 'r') as f:
            expenses = json.load(f)
    else:
        expenses = {}
    
    return users, expenses

# Save user and expenses data
def save_data(users, expenses):
    with open("users.json", 'w') as f:
        json.dump(users, f)
        
    with open("expenses.json", 'w') as f:
        json.dump(expenses, f)

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    users, expenses = load_data()
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if username in users:
            flash("Username already exists!", "error")
            return redirect(url_for('register'))
        
        if password != confirm_password:
            flash("Passwords do not match!", "error")
            return redirect(url_for('register'))
        
        users[username] = password
        expenses[username] = []
        save_data(users, expenses)
        flash("Registration successful!", "success")
        return redirect(url_for('home'))

    return render_template('register.html')

@app.route('/login', methods=['POST'])
def login():
    users, expenses = load_data()
    username = request.form['username']
    password = request.form['password']
    
    if username in users and users[username] == password:
        session['username'] = username
        return redirect(url_for('expenses'))
    
    flash("Invalid credentials", "error")
    return redirect(url_for('home'))

@app.route('/expenses', methods=['GET', 'POST'])
def expenses():
    users, expenses = load_data()
    
    if 'username' not in session:
        return redirect(url_for('home'))
    
    username = session['username']
    
    if request.method == 'POST':
        category = request.form['category']
        amount = request.form['amount']
        description = request.form['description']
        
        try:
            amount = float(amount)
        except ValueError:
            flash("Please enter a valid amount", "error")
            return redirect(url_for('expenses'))
        
        expense = {
            "category": category,
            "amount": amount,
            "description": description,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        expenses[username].append(expense)
        save_data(users, expenses)
        flash("Expense added successfully!", "success")
        return redirect(url_for('expenses'))
    
    user_expenses = expenses.get(username, [])
    pie_chart_url = create_pie_chart(user_expenses)
    return render_template('expenses.html', user_expenses=user_expenses, pie_chart_url=pie_chart_url)

def create_pie_chart(user_expenses):
    if not user_expenses:
        return None
    
    category_totals = {}
    for expense in user_expenses:
        category = expense['category']
        amount = expense['amount']
        category_totals[category] = category_totals.get(category, 0) + amount
    
    labels = list(category_totals.keys())
    sizes = list(category_totals.values())

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%')
    ax.set_title('Expenses by Category')

    # Save the pie chart to a BytesIO object and encode it to base64
    img = io.BytesIO()
    FigureCanvas(fig).print_png(img)
    img.seek(0)
    return base64.b64encode(img.getvalue()).decode()

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)
