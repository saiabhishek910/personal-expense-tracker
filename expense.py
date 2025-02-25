import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Database connection
DB_NAME = "expenses.db"

# Function to initialize database
def initialize_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT,
            amount REAL,
            date TEXT,
            description TEXT
        )
    """)
    conn.commit()
    conn.close()

# Function to add expense to database
def add_expense(category, amount, date, description):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO expenses (category, amount, date, description) VALUES (?, ?, ?, ?)", 
              (category, amount, date, description))
    conn.commit()
    conn.close()

# Function to retrieve all expenses
def get_expenses():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql("SELECT * FROM expenses", conn)
    conn.close()
    return df

# Function to delete an expense
def delete_expense(expense_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM expenses WHERE id=?", (expense_id,))
    conn.commit()
    conn.close()

# Function to update an expense
def update_expense(expense_id, category, amount, date, description):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        UPDATE expenses
        SET category=?, amount=?, date=?, description=?
        WHERE id=?
    """, (category, amount, date, description, expense_id))
    conn.commit()
    conn.close()

# Function to clear all expenses
def clear_expenses():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM expenses")
    conn.commit()
    conn.close()

# Initialize database
initialize_db()

# Page Title
st.title("Personal Expense Tracker (Database Version)")

# Sidebar Section - Add Expense
with st.sidebar:
    st.header("Add Expense")

    category_options = ["Food", "Transport", "Entertainment", "Utilities", "Healthcare", "Other"]
    category = st.selectbox("Category", category_options)
    amount = st.number_input("Amount", min_value=0.0, step=0.01)
    date = st.date_input("Date")
    description = st.text_area("Description")

    if st.button("Add Expense"):
        if category and amount > 0 and description:
            add_expense(category, amount, date.strftime('%Y-%m-%d'), description)
            st.success("Expense added successfully!")
            st.rerun()

# Main Section - Display Table
st.header("Expenses Table")

data = get_expenses()

if not data.empty:
    # Add Edit and Remove buttons
    data["Edit"] = [st.button(f"✏️ Edit {i}", key=f"edit_{i}") for i in data["id"]]
    data["Remove"] = [st.button(f"❌ Remove {i}", key=f"remove_{i}") for i in data["id"]]

    st.dataframe(data)

    # Handling Edit and Remove
    for i in data["id"]:
        if st.session_state.get(f"edit_{i}", False):
            expense = data[data["id"] == i].iloc[0]
            new_category = st.selectbox("Edit Category", category_options, index=category_options.index(expense["category"]))
            new_amount = st.number_input("Edit Amount", min_value=0.0, step=0.01, value=expense["amount"])
            new_date = st.date_input("Edit Date", value=datetime.strptime(expense["date"], '%Y-%m-%d'))
            new_description = st.text_area("Edit Description", value=expense["description"])

            if st.button("Update Expense"):
                update_expense(i, new_category, new_amount, new_date.strftime('%Y-%m-%d'), new_description)
                st.success("Expense updated successfully!")
                st.rerun()

        if st.session_state.get(f"remove_{i}", False):
            delete_expense(i)
            st.success("Expense removed successfully!")
            st.rerun()
else:
    st.info("No expenses recorded.")

# Clear All Expenses Button
if st.button("Clear Data"):
    clear_expenses()
    st.success("All expenses cleared!")
    st.rerun()

# Visualization Section
st.header("Visualize Expenses")

if st.button("Visualize"):
    if not data.empty:
        # Expense by Category
        st.subheader("Expense by Category")
        category_expense = data.groupby("category")["amount"].sum().reset_index()
        fig1, ax1 = plt.subplots()
        ax1.pie(category_expense["amount"], labels=category_expense["category"], autopct="%1.1f%%", startangle=90)
        ax1.axis("equal")
        st.pyplot(fig1)

        # Monthly Expense Trend
        st.subheader("Monthly Expense Trend")
        data["date"] = pd.to_datetime(data["date"])
        data["month"] = data["date"].dt.to_period("M").astype(str)
        monthly_expense = data.groupby("month")["amount"].sum().reset_index()
        fig2, ax2 = plt.subplots()
        sns.lineplot(data=monthly_expense, x="month", y="amount", marker="o", ax=ax2)
        ax2.set_title("Monthly Expense Trend")
        plt.xticks(rotation=45)
        st.pyplot(fig2)

        # Bar Chart of Categories
        st.subheader("Bar Chart of Expenses by Category")
        fig3, ax3 = plt.subplots()
        sns.barplot(data=category_expense, x="category", y="amount", palette="viridis", ax=ax3)
        ax3.set_title("Expenses by Category")
        plt.xticks(rotation=45)
        st.pyplot(fig3)
    else:
        st.warning("No data available to visualize. Please add expenses first.")
