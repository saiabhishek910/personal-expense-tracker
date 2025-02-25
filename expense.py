import streamlit as st
import pandas as pd
import sqlite3

# Database setup
def init_db():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS expenses (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        category TEXT,
                        amount REAL,
                        date TEXT,
                        description TEXT)''')
    conn.commit()
    conn.close()

# Function to load data from database
def load_data():
    conn = sqlite3.connect("expenses.db")
    df = pd.read_sql("SELECT * FROM expenses", conn)
    conn.close()
    return df

# Function to add expense
def add_expense(category, amount, date, description):
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO expenses (category, amount, date, description) VALUES (?, ?, ?, ?)",
                   (category, amount, date, description))
    conn.commit()
    conn.close()

# Function to update an expense
def update_expense(expense_id, category, amount, date, description):
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE expenses SET category=?, amount=?, date=?, description=? WHERE id=?",
                   (category, amount, date, description, expense_id))
    conn.commit()
    conn.close()

# Function to delete an expense
def delete_expense(expense_id):
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM expenses WHERE id=?", (expense_id,))
    conn.commit()
    conn.close()

# Initialize database
init_db()

# Streamlit UI
st.title("Personal Expense Tracker")

# Sidebar - Add Expense
with st.sidebar:
    st.header("Add Expense")
    category = st.selectbox("Category", ["Food", "Transport", "Entertainment", "Utilities", "Healthcare", "Other"])
    amount = st.number_input("Amount", min_value=0.0, step=0.01)
    date = st.date_input("Date")
    description = st.text_area("Description")
    if st.button("Add Expense"):
        if category and amount > 0 and description:
            add_expense(category, amount, date, description)
            st.success("Expense added successfully!")
            st.experimental_rerun()
        else:
            st.error("Please fill in all fields.")

# Load data
expenses = load_data()

# Display Expenses Table
st.header("Expense Records")
if not expenses.empty:
    for index, row in expenses.iterrows():
        col1, col2, col3, col4, col5, col6, col7 = st.columns([1, 2, 2, 2, 3, 1, 1])
        col1.write(row['id'])
        col2.write(row['category'])
        col3.write(row['amount'])
        col4.write(row['date'])
        col5.write(row['description'])
        if col6.button("Edit", key=f"edit_{row['id']}"):
            st.session_state['edit_id'] = row['id']
            st.session_state['edit_category'] = row['category']
            st.session_state['edit_amount'] = row['amount']
            st.session_state['edit_date'] = row['date']
            st.session_state['edit_description'] = row['description']
        if col7.button("Remove", key=f"remove_{row['id']}"):
            delete_expense(row['id'])
            st.experimental_rerun()

# Edit Expense Section
if 'edit_id' in st.session_state:
    st.header("Edit Expense")
    new_category = st.selectbox("Category", ["Food", "Transport", "Entertainment", "Utilities", "Healthcare", "Other"],
                                index=["Food", "Transport", "Entertainment", "Utilities", "Healthcare", "Other"].index(st.session_state['edit_category']))
    new_amount = st.number_input("Amount", min_value=0.0, step=0.01, value=st.session_state['edit_amount'])
    new_date = st.date_input("Date", value=pd.to_datetime(st.session_state['edit_date']))
    new_description = st.text_area("Description", value=st.session_state['edit_description'])
    if st.button("Update Expense"):
        update_expense(st.session_state['edit_id'], new_category, new_amount, new_date, new_description)
        del st.session_state['edit_id']
        st.experimental_rerun()

# Clear all data button
if st.button("Clear All Data"):
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM expenses")
    conn.commit()
    conn.close()
    st.experimental_rerun()
