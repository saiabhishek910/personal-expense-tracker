# Personal Expense Tracker

## Overview
The **Personal Expense Tracker** is a Streamlit-based web application that helps users track and visualize their expenses efficiently. The application allows users to log their daily expenses, categorize them, and analyze spending patterns through interactive visualizations.

## Features
- **Expense Management:**
  - Add expenses with details like category, amount, date, and description.
  - View all recorded expenses in a structured table.
  - Clear all data when needed.
- **Data Persistence:**
  - Uses SQLite database for efficient data storage.
- **Expense Analysis & Visualization:**
  - View expenses as a **pie chart** based on categories.
  - Track **monthly expenses** with a **line chart**.
  - Analyze category-wise spending using a **bar chart**.
  - Visualizations appear only after clicking the **"Visualize"** button.

## Technologies Used
- **Python** (Backend logic)
- **Streamlit** (UI Framework)
- **SQLite** (Database)
- **Pandas** (Data manipulation)
- **Matplotlib & Seaborn** (Data visualization)

## Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/expense-tracker.git
   cd expense-tracker
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Run the application:
   ```sh
   streamlit run expense.py
   ```

## How to Use
1. **Add Expenses:** Fill in the category, date, amount, and description fields in the sidebar and click "Add Expense".
2. **View Expenses:** The expenses table displays all recorded expenses.
3. **Clear Data:** Click "Clear Data" to remove all records.
4. **Analyze Spending:** Click "Visualize" to see expense trends using pie, line, and bar charts.

## Screenshots
![image](https://github.com/user-attachments/assets/aaa1f7cd-505c-4d45-9b5b-50d29567f89e)
![image](https://github.com/user-attachments/assets/0112cadf-2e36-4cfb-a234-9172191ffdde)


## License
This project is licensed under the MIT License.

## Author
[Abhishek Kollipara](https://github.com/saiabhishek910)

