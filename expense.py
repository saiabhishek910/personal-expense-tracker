import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns

# Constants
DATABASE_NAME = "expense.db"
TABLE_NAME = "expenses"
REQUIRED_COLUMNS = ["Category", "Amount", "Date", "Description"]

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

def update_data_in_database(id, category, amount, date, description):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute(f"""
        UPDATE {TABLE_NAME}
        SET Category = ?, Amount = ?, Date = ?, Description = ?
        WHERE id = ?
    """, (category, amount, date, description, id))
    conn.commit()
    conn.close()

def remove_data_from_database(id):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM {TABLE_NAME} WHERE id = ?", (id,))
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
    category_options = ["Food", "Transport", "Entertainment", "Utilities", "Healthcare", "Other"]
    category = st.selectbox("Select Category", category_options)
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
    for i, row in data.iterrows():
        col1, col2, col3 = st.columns([8, 1, 1])
        col1.write(row.to_dict())  # Display the row data
        if col2.button("Edit", key=f"edit_{row['id']}"):  # Use id for key
            st.session_state["edit_id"] = row['id']  # Store the id
        if col3.button("Remove", key=f"remove_{row['id']}"): # Use id for key
            remove_data_from_database(row['id'])
            st.rerun()

    if "edit_id" in st.session_state:
        edit_id = st.session_state["edit_id"]
        edit_row = data[data['id'] == edit_id].iloc[0] # Get the row for editing

        with st.expander("Edit Expense"):
            category_edit = st.selectbox("Category", category_options, index=category_options.index(edit_row["Category"]))
            date_edit = st.date_input("Date", pd.to_datetime(edit_row["Date"])) # convert to datetime object
            amount_edit = st.number_input("Amount", min_value=0.0, step=0.01, value=edit_row["Amount"])
            description_edit = st.text_area("Description", edit_row["Description"])
            if st.button("Update Expense"):
                update_data_in_database(edit_id, category_edit, amount_edit, date_edit, description_edit)
                del st.session_state["edit_id"]
                st.rerun()

    if st.button("Clear Data"):
        clear_all_data()
        st.rerun()
