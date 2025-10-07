-- Database creation and setup for Library Management System
-- This script creates the database and necessary tables for the library application

-- Create the database if it doesn't exist
CREATE DATABASE IF NOT EXISTS librarydb;

-- Use the database
USE librarydb;

-- Create the books table
CREATE TABLE IF NOT EXISTS books (
    book_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255) NOT NULL,
    genre VARCHAR(100) NOT NULL,
    publication_year INT,
    isbn VARCHAR(20),
    available BOOLEAN DEFAULT TRUE,
    added_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample data
INSERT INTO books (title, author, genre, publication_year, isbn) VALUES
('To Kill a Mockingbird', 'Harper Lee', 'Fiction', 1960, '978-0446310789'),
('1984', 'George Orwell', 'Dystopian', 1949, '978-0451524935'),
('Pride and Prejudice', 'Jane Austen', 'Romance', 1813, '978-0141439518'),
('The Great Gatsby', 'F. Scott Fitzgerald', 'Fiction', 1925, '978-0743273565'),
('The Hobbit', 'J.R.R. Tolkien', 'Fantasy', 1937, '978-0547928227'),
('The Catcher in the Rye', 'J.D. Salinger', 'Fiction', 1951, '978-0316769488'),
('To the Lighthouse', 'Virginia Woolf', 'Fiction', 1927, '978-0156907392'),
('Brave New World', 'Aldous Huxley', 'Dystopian', 1932, '978-0060850524'),
('The Lord of the Rings', 'J.R.R. Tolkien', 'Fantasy', 1954, '978-0618640157'),
('Jane Eyre', 'Charlotte Brontë', 'Gothic Fiction', 1847, '978-0141441146');

-- Create an index for faster searching
CREATE INDEX idx_title ON books(title);
CREATE INDEX idx_author ON books(author);
CREATE INDEX idx_genre ON books(genre);

-- Display the data to verify
SELECT * FROM books;