# Splitwise Project

# Architecture Diagram

                   +----------------------+
                   |                      |
                   |  Splitwise Web App   |
                   |                      |
                   +----------|-----------+
                              |
                   +----------|-----------+
                   |                      |
                   |   Django Framework   |
                   |                      |
                   +--|---------------|--+
                      |               |
              +-------|------+ +-------|------+
              |               | |               |
              |  User 1       | |  User 2       |
              |               | |               |
              | +---------+   | | +---------+   |
              | |   UI    |   | | |   UI    |   |
              | +----|----+   | | +----|----+   |
              |      |        | |      |        |
              | +----v----+   | | +----v----+   |
              | | Views  |   | | | Views  |   |
              | +----|----+   | | +----|----+   |
              |      |        | |      |        |
              | +----v----+   | | +----v----+   |
              | | Models |   | | | Models |   |
              | +----|----+   | | +----|----+   |
              |      |        | |      |        |
              +------|--------+ +------|--------+
                     |               |
                     |               |
           +---------|------+ +-------|------+
           |               | |               |
           |   User N      | |   User N+1    |
           |               | |               |
           | +---------+   | | +---------+   |
           | |   UI    |   | | |   UI    |   |
           | +----|----+   | | +----|----+   |
           |      |        | |      |        |
           | +----v----+   | | +----v----+   |
           | | Views  |   | | | Views  |   |
           | +----|----+   | | +----|----+   |
           |      |        | |      |        |
           | +----v----+   | | +----v----+   |
           | | Models |   | | | Models |   |
           | +----|----+   | | +----|----+   |
           |      |        | |      |        |
           +------|--------+ +------|--------+
                  |                 |
                  |                 |
       +----------|----+   +--------|------+
       |               |   |               |
       |    Database   |   |    Celery     |
       |               |   | (Background   |
       |  (PostgreSQL) |   |   Task Queue) |
       |               |   |               |
       +---------------+   +---------------+


## Overview

Splitwise is an expense sharing application that allows users to track and split expenses among friends and housemates. This project is built using Django and provides a simple and efficient way to manage shared expenses and balances between users.

## System Architecture

The Splitwise project follows a typical web application architecture with the following components:

- Django Web Application: This is the core of the project, handling user authentication, expense creation, and balance calculations.

- Database: The project uses a relational database to store user data, expenses, and balances.

- Celery: Celery is used for background task processing, such as sending asynchronous emails for expense notifications.

## Database Schema

The database schema is designed to store user information, expenses, expense shares, and balances. Here is an overview of the key tables:

- User: Stores user information, including their username, email, and mobile number.

- Expense: Contains details of each expense, including its description, amount, and creator.

- ExpenseShare: Associates users with expenses and specifies their share in the expense.

- Balance: Tracks the balances between users, showing who owes money to whom.

## Getting Started

To run the Splitwise project locally, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/splitwise.git
   cd splitwise
   ```

2. Create a virtual environment and install the dependencies:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use 'venv\Scripts\activate'
   pip install -r requirements.txt
   ```

3. Set up the database:

   ```bash
   python manage.py migrate
   ```

4. Create a superuser account:

   ```bash
   python manage.py createsuperuser
   ```

5. Start the development server:

   ```bash
   python manage.py runserver
   ```

6. Access the application in your web browser at `http://localhost:8000`.

## API Endpoints

Splitwise provides the following HTTP API endpoints:

- `/expenses/add_expense/`: Add a new expense.
- `/expenses/view_expenses/`: View a list of all expenses.
- `/balances/`: View balances for all users.

Please refer to the API documentation for more details on how to use these endpoints.

## Weekly Balance Email

A scheduled task sends a weekly balance email to users, summarizing the total amount they owe to others. This task is run using Celery and Celery Beat.

## Optional Features

The project includes optional features such as adding expense names, notes, and images, splitting by share, and showing a user's passbook.

## Contribute

We welcome contributions to the Splitwise project. Feel free to fork the repository, make changes, and create a pull request.

## Issues and Bug Reports

If you encounter any issues or want to report a bug, please open an issue on the project's GitHub repository.

