# Library Management System

A simple library management system with a MySQL database backend and Tkinter GUI.

## Features

- View all books in the library
- Add new books to the library
- Edit existing book details
- Delete books from the library
- Search for books by title, author, or genre

## Setup Instructions

### 1. Install Required Packages

```bash
pip install mysql-connector-python
```

### 2. Database Setup

1. Make sure MySQL server is installed and running
2. Import the database schema using the provided SQL script:

```bash
mysql -u root -p < schema.sql
```

Or manually run the SQL commands in the `schema.sql` file.

### 3. Configuration

Edit the `config.ini` file to match your MySQL database settings:

```ini
[database]
host = localhost
user = your_username
password = your_password
database = librarydb
```

## Running the Application

```bash
python library_app.py
```

or use the new version with more features:

```bash
python library_app_new.py
```

## Project Structure

- `library_app.py` - Original Tkinter GUI application
- `library_app_new.py` - Enhanced version with additional features
- `database.py` - Database connection and operations module
- `schema.sql` - SQL script to create database tables and sample data
- `config.ini` - Database connection configuration
- `requirements.txt` - Python dependencies

