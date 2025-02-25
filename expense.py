import streamlit as st
import pandas as pd
import os
from openpyxl import Workbook, load_workbook
import matplotlib.pyplot as plt
import seaborn as sns

# Constants
FILE_NAME = "expense.xlsx"
REQUIRED_COLUMNS = ["Category", "Amount", "Date", "Description"]

def initialize_excel_file():
    if not os.path.exists(FILE_NAME):
        wb = Workbook()
        ws = wb.active
        ws.append(REQUIRED_COLUMNS)
        wb.save(FILE_NAME)

def load_data_from_excel():
    initialize_excel_file()
    data = pd.read_excel(FILE_NAME)
    data = data.dropna(subset=REQUIRED_COLUMNS).reset_index()
    return data

def add_data_to_excel(category, amount, date, description):
    initialize_excel_file()
    wb = load_workbook(FILE_NAME)
    ws = wb.active
    ws.append([category, amount, date, description])
    wb.save(FILE_NAME)

def update_data_in_excel(index, category, amount, date, description):
    data = load_data_from_excel()
    if index in data.index:
        data.loc[index] = [index, category, amount, date, description]
        data.to_excel(FILE_NAME, index=False)

def remove_data_from_excel(index):
    data = load_data_from_excel()
    data = data.drop(index=index)
    data.to_excel(FILE_NAME, index=False)

def clear_all_data():
    initialize_excel_file()
    wb = Workbook()
    ws = wb.active
    ws.append(REQUIRED_COLUMNS)
    wb.save(FILE_NAME)

initialize_excel_file()

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
            add_data_to_excel(category, amount, date, description)
            st.success("Expense added successfully!")
            st.rerun()


st.header("Expenses Table")
data = load_data_from_excel()
if not data.empty:
    data["Edit"] = [st.button(f"✏️ Edit {i}", key=f"edit_{i}") for i in data.index]
    data["Remove"] = [st.button(f"❌ Remove {i}", key=f"remove_{i}") for i in data.index]
    st.dataframe(data)

    for i in data.index:
        if st.session_state.get(f"edit_{i}", False):
            st.session_state["edit_index"] = i
        if st.session_state.get(f"remove_{i}", False):
            remove_data_from_excel(i)
            st.rerun()


    
    if "edit_index" in st.session_state:
        i = st.session_state["edit_index"]
        with st.expander("Edit Expense"):
            category_edit = st.selectbox("Category", category_options, index=category_options.index(data.loc[i, "Category"]))
            date_edit = st.date_input("Date", data.loc[i, "Date"])
            amount_edit = st.number_input("Amount", min_value=0.0, step=0.01, value=data.loc[i, "Amount"])
            description_edit = st.text_area("Description", data.loc[i, "Description"])
            if st.button("Update Expense"):
                update_data_in_excel(i, category_edit, amount_edit, date_edit, description_edit)
                del st.session_state["edit_index"]
                st.rerun()

    
    if st.button("Clear Data"):
        clear_all_data()
        st.rerun()

