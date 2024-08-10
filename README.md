# Bookstore Project

## Overview
This project is a Django-based backend application for managing a bookstore. It provides functionalities for managing books, customers, and orders.

## Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- PostgreSQL (or another database of your choice)
- Django
- Django REST framework
- Django Filter

## Setting Up the Project Locally

### 1. Clone the Repository
```bash
git clone https://github.com/your_username/bookstore.git
cd bookstore
```

### 2. Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables
Create a .env file in the root of your project and add the following environment variables:
```bash
DEBUG=True
DATABASE_NAME=bookstore_db
DATABASE_USER=postgres
DATABASE_PASSWORD=root
DATABASE_HOST=localhost
DATABASE_PORT=5432
# 'percentage' or 'flat'
DISCOUNT_TYPE=percentage
# value: e.g., 10% or a flat amount like $10
DISCOUNT_VALUE=10.00
```

### 5. Database Setup

#### 5.1. Create the Database
Using PostgreSQL, we can create a new database using the following command:
```bash
psql -U username -c "CREATE DATABASE your_db_name;"
```
#### 5.2. Run Migrations
Apply the migrations to set up the database schema:
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Run the Development Server
```bash
python manage.py runserver
```

### Running Tests
```bash
python manage.py test
```

### API Endpoints
Books

    GET /api/books/ - List all books
    POST /api/books/ - Create a new book

Orders

    POST /api/orders/ - Create a new order

Customers

    GET /api/customers/ - List all customers
    POST /api/customers/ - Create a new customer

