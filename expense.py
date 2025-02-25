import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns

# Constants
DATABASE_NAME = "expense.db"
TABLE_NAME = "expenses"
CATEGORY_OPTIONS = ["Food", "Transport", "Entertainment", "Utilities", "Healthcare", "Other"]

# Database Functions
def initialize_database():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Category TEXT NOT NULL,
            Amount REAL NOT NULL,
            Date TEXT NOT NULL,
            Description TEXT
        )
    """)
    conn.commit()
    conn.close()

def load_data_from_database():
    conn = sqlite3.connect(DATABASE_NAME)
    data = pd.read_sql_query(f"SELECT * FROM {TABLE_NAME}", conn)
    conn.close()
    return data

def add_data_to_database(category, amount, date, description):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute(f"""
        INSERT INTO {TABLE_NAME} (Category, Amount, Date, Description)
        VALUES (?, ?, ?, ?)
    """, (category, amount, date, description))
    conn.commit()
    conn.close()

def clear_all_data():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM {TABLE_NAME}")
    conn.commit()
    conn.close()

initialize_database()

st.title("Personal Expense Tracker")

with st.sidebar:
    st.header("Add Section")
    category = st.selectbox("Select Category", CATEGORY_OPTIONS)
    date = st.date_input("Date")
    amount = st.number_input("Amount", min_value=0.0, step=0.01)
    description = st.text_area("Description")
    if st.button("Add Expense"):
        if category and amount > 0 and description:
            add_data_to_database(category, amount, date, description)
            st.success("Expense added successfully!")
            st.rerun()

st.header("Expenses Table")
data = load_data_from_database()

if not data.empty:
    data['Date'] = pd.to_datetime(data['Date'])
    st.dataframe(data)  # Display the table directly

    if st.button("Clear Data"):  # Only Clear Data button
        clear_all_data()
        st.rerun()

# Visualization Section
st.header("Expense Analysis")
if st.button("Visualize"):
    if not data.empty:
        data['Month'] = data['Date'].dt.to_period('M')  # Convert date to month period

        # 1. Expenses by Category (Pie Chart)
        category_expenses = data.groupby('Category')['Amount'].sum()
        fig1, ax1 = plt.subplots()
        ax1.pie(category_expenses, labels=category_expenses.index, autopct='%1.1f%%', startangle=90)
        ax1.axis('equal')
        st.pyplot(fig1)

        # 2. Monthly Expenses (Line Chart)
        monthly_expenses = data.groupby('Month')['Amount'].sum()
        fig2, ax2 = plt.subplots()
        ax2.plot(monthly_expenses.index.astype(str), monthly_expenses.values, marker='o')
        ax2.set_xlabel("Month")
        ax2.set_ylabel("Total Expenses")
        ax2.set_title("Monthly Expense Analysis")
        ax2.grid(True)
        st.pyplot(fig2)

        # 3. Expenses by Category (Bar Chart)
        fig3, ax3 = plt.subplots()
        sns.barplot(x=category_expenses.index, y=category_expenses.values, ax=ax3)
        ax3.set_xlabel("Category")
        ax3.set_ylabel("Total Expenses")
        ax3.set_title("Expenses by Category")
        st.pyplot(fig3)
    else:
        st.write("No expenses recorded yet for visualization.")
