# PocketPilot

PocketPilot is a desktop personal finance management application built with Python and Kivy. It helps users record income and expenses, track transaction history, manage financial preferences, and understand their spending through visual analytics and financial insights.

---

## Overview

PocketPilot is designed as a simple and user-friendly personal finance manager.

Users can:

- Record income and expenses
- Categorize transactions
- Add descriptions to transactions
- View transaction history
- Edit and delete transactions
- Track their current balance
- Analyse spending by category
- Compare income and expenses
- View financial insights
- Change application theme
- Change currency
- Manage account settings

The application uses a local SQLite database to store user and transaction information.

---

## Features

### User Authentication

- User registration
- Login system
- Password-protected accounts
- User session handling

### Transaction Management

- Add income
- Add expenses
- Select transaction categories
- Add descriptions
- Edit transactions
- Delete transactions
- Automatic balance calculation

### Transaction History

The History screen displays:

- Transaction category
- Amount
- Description
- Date
- Income or expense indication
- Edit option
- Delete option

### Financial Analytics

PocketPilot provides visual analytics including:

- Expense breakdown
- Income vs Expense comparison
- Category-wise spending
- Highest spending category

Charts are generated using Matplotlib.

### Financial Insights

The Analytics screen provides:

- Total income
- Total expenses
- Savings rate
- Highest spending category
- Highest spending amount
- Current balance
- Number of transactions
- Number of expense categories

PocketPilot also generates a rule-based financial insight based on the user's financial data.

Note: The current financial insight system is rule-based and is not an AI model.

### Theme Support

PocketPilot supports:

- Light Mode
- Dark Mode
- Theme persistence

### Currency Support

Users can select their preferred currency for displaying financial values.

### Settings

The Settings screen provides:

- Edit Profile
- Change Password
- Theme
- Currency
- About PocketPilot
- Logout

---

## Screenshots

Screenshots of the following screens will be added:

- Login
- Home Dashboard
- Add Transaction
- Transaction History
- Analytics
- Settings

---

## Tech Stack

| Technology | Purpose |
|------------|---------|
| Python | Core application development |
| Kivy | Desktop UI framework |
| KivyMD | Material Design UI components |
| SQLite | Local database |
| Matplotlib | Financial charts and visualization |
| Git | Version control |
| GitHub | Source code hosting |

---

## Project Structure

```text
PocketPilot/
|
+-- assets/
|
+-- data/
|
+-- kv/
|
+-- screens/
|
+-- widget/
|
+-- charts.py
+-- database.py
+-- main.py
+-- requirements.txt
+-- .gitignore
+-- README.md