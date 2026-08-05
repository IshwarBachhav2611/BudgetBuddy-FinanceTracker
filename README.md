# BudgetBuddy - Personal Finance Tracker

BudgetBuddy is a full-stack personal finance management web application built using Django. It helps users manage their daily finances by tracking income, expenses, monthly budgets, savings, and financial reports through a clean and user-friendly interface.

The application is designed to provide users with complete control over their financial activities while maintaining secure authentication, real-time budget monitoring, notifications, activity logging, and analytical reports.

---

## Project Overview

Managing personal finances manually is time-consuming and often leads to poor budgeting decisions. BudgetBuddy simplifies financial management by allowing users to organize all their financial records in one place.

The application enables users to:

- Manage multiple income sources
- Track daily expenses
- Set monthly budgets
- Monitor savings
- Receive budget notifications
- View financial reports
- Maintain complete activity history
- Access their data securely from anywhere

---

# Features

## Authentication

- User Registration
- Secure Login
- Logout
- Profile Management
- Edit Profile
- Change Password

---

## Dashboard

- Personalized dashboard
- Current Month Income
- Current Month Expense
- Monthly Budget
- Total Savings
- Recent Income Records
- Recent Expense Records
- Budget Alerts
- Quick Action Buttons

---

## Income Management

- Add Income
- Edit Income
- Delete Income
- View Income History
- Income Categories
- Payment Methods
- Date-wise Income Records

---

## Expense Management

- Add Expense
- Edit Expense
- Delete Expense
- Expense Categories
- Payment Methods
- Expense History
- Date-wise Tracking

---

## Budget Management

- Create Monthly Budget
- Update Budget
- Budget Utilization
- Budget Monitoring
- Budget Remaining
- Budget Exceeded Detection

---

## Reports

- Income Summary
- Expense Summary
- Savings Summary
- Monthly Financial Analysis

---

## Notifications

- Budget Warning Notifications
- Budget Exceeded Notifications
- Mark Notification as Read
- Delete Notifications
- View Notification History

---

## Activity Logs

- User Login
- User Logout
- Income Activities
- Expense Activities
- Budget Activities
- Notification Activities

---

## REST API

- Django REST Framework Integration
- API Endpoints for Application Data

---

# Technology Stack

## Frontend

- HTML5
- CSS3
- Bootstrap 5
- Bootstrap Icons
- JavaScript

---

## Backend

- Python 3
- Django 6
- Django REST Framework

---

## Databases

### Local Development

- PostgreSQL

### Production

- Render PostgreSQL

### Activity Logging

- MongoDB Atlas

---

## Deployment

- Render

---

## Static Files

- WhiteNoise

---

## Version Control

- Git
- GitHub

---

# Project Structure

```text
BudgetBuddy
│
├── apps
│   ├── accounts
│   ├── dashboard
│   ├── income
│   ├── expense
│   ├── budgets
│   ├── reports
│   ├── notifications
│   ├── api
│   └── activity_logs
│
├── BudgetBuddy
│
├── templates
│
├── static
│
├── media
│
├── requirements.txt
│
├── manage.py
│
└── README.md
```

---

# Application Workflow

```text
                 User

                   │
                   ▼

          Register / Login

                   │
                   ▼

              Dashboard

        ┌──────────┼──────────┐
        ▼          ▼          ▼

    Income      Expense     Budget

        └──────────┼──────────┘
                   │
                   ▼

          Financial Reports

                   │
                   ▼

           Notifications

                   │
                   ▼

            Activity Logs

                   │
          ┌────────┴─────────┐
          ▼                  ▼

 Render PostgreSQL      MongoDB Atlas
```

---

# Database Flow

```text
User Action

      │

      ▼

Django View

      │

      ▼

Business Logic

      │

      ▼

PostgreSQL Database

      │

      ▼

Updated Dashboard
```

---

# Deployment Architecture

```text
Client Browser

      │

      ▼

Render Web Service

      │

      ▼

Django Application

      │

      ├──────────────► Render PostgreSQL

      │

      └──────────────► MongoDB Atlas
```

---

# Local Development

### Clone Repository

```bash
git clone <repository-url>
```

---

### Create Virtual Environment

```bash
python -m venv venv
```

---

### Activate Virtual Environment

Windows

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
source venv/bin/activate
```

---

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

### Apply Migrations

```bash
python manage.py makemigrations

python manage.py migrate
```

---

### Run Development Server

```bash
python manage.py runserver
```

---

# Environment Variables

Create a `.env` file in the project root.

```env
SECRET_KEY=

DEBUG=

ALLOWED_HOSTS=

DB_NAME=

DB_USER=

DB_PASSWORD=

DB_HOST=

DB_PORT=

MONGO_URI=
```

---

## Live Demo

**Application URL**

https://budgetbuddy-financetracker.onrender.com/

**Platform**

- Backend: Django
- Hosting: Render
- Database: Render PostgreSQL
- Activity Logs: MongoDB Atlas

> **Note:** The application is hosted on Render's free tier. The first request after a period of inactivity may take 30–60 seconds while the server wakes up.

---

# Real World Use Cases

- Personal Expense Tracking
- Monthly Budget Planning
- Salary Management
- Student Expense Management
- Family Budget Monitoring
- Small Business Financial Tracking
- Freelancers Income Management
- Financial Record Keeping

---

# Future Enhancements

- Excel Report Export
- Email Notifications
- AI Financial Insights
- Expense Prediction
- Bill Scanner
- Multi Currency Support
- Dark Mode
- Mobile Application

---

# Learning Outcomes

This project demonstrates practical implementation of:

- Django Web Development
- Django Authentication
- PostgreSQL Integration
- MongoDB Integration
- REST API Development
- CRUD Operations
- Database Relationships
- User Authentication
- Deployment on Render
- Git & GitHub
- Responsive UI Design
- MVC (MVT) Architecture
- Environment Configuration
- Production Deployment

---

# License

This project is developed for educational and learning purposes.

---

# Author

**Ishwar Bachhav**

Personal Finance Management System using Django

GitHub: https://github.com/IshwarBachhav2611

---
