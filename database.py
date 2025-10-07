import mysql.connector
from mysql.connector import Error
import configparser
import os

class DatabaseConnection:
    """
    A class to handle database connection and operations for the library application.
    """
    
    def __init__(self, config_file='config.ini'):
        """
        Initialize the database connection using the config file
        
        Args:
            config_file (str): Path to the configuration file
        """
        self.connection = None
        self.config_file = config_file
        self.db_config = self._read_config()
        
    def _read_config(self):
        """Read database configuration from config file"""
        config = configparser.ConfigParser()
        
        # Check if config file exists
        if not os.path.exists(self.config_file):
            # Use default configuration
            return {
                'host': 'localhost',
                'user': 'root',
                'password': 'password',
                'database': 'librarydb'
            }
        
        # Read configuration file
        config.read(self.config_file)
        return {
            'host': config['database']['host'],
            'user': config['database']['user'],
            'password': config['database']['password'],
            'database': config['database']['database']
        }
        
    def connect(self):
        """Establish a database connection"""
        try:
            self.connection = mysql.connector.connect(**self.db_config)
            return True
        except Error as e:
            print(f"Error connecting to MySQL database: {e}")
            return False
            
    def disconnect(self):
        """Close the database connection"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            
    def execute_query(self, query, params=None):
        """
        Execute a query with optional parameters
        
        Args:
            query (str): SQL query to execute
            params (tuple, optional): Parameters for the query
            
        Returns:
            list: Query results or None if error
        """
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect()
                
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
                
            # Check if query is a SELECT statement
            if query.strip().upper().startswith("SELECT"):
                result = cursor.fetchall()
            else:
                self.connection.commit()
                result = cursor.rowcount
                
            cursor.close()
            return result
            
        except Error as e:
            print(f"Error executing query: {e}")
            return None
            
    def get_all_books(self):
        """Get all books from the database"""
        query = """
            SELECT book_id, title, author, genre
            FROM books
            ORDER BY title
        """
        return self.execute_query(query)
        
    def search_books(self, search_term):
        """
        Search for books by title, author, or genre
        
        Args:
            search_term (str): Term to search for
            
        Returns:
            list: Matching books
        """
        query = """
            SELECT book_id, title, author, genre
            FROM books
            WHERE title LIKE %s OR author LIKE %s OR genre LIKE %s
            ORDER BY title
        """
        search_pattern = f"%{search_term}%"
        return self.execute_query(query, (search_pattern, search_pattern, search_pattern))
        
    def add_book(self, title, author, genre, publication_year=None, isbn=None):
        """
        Add a new book to the database
        
        Args:
            title (str): Book title
            author (str): Book author
            genre (str): Book genre
            publication_year (int, optional): Year of publication
            isbn (str, optional): ISBN number
            
        Returns:
            int: ID of the new book or None if error
        """
        query = """
            INSERT INTO books (title, author, genre, publication_year, isbn)
            VALUES (%s, %s, %s, %s, %s)
        """
        params = (title, author, genre, publication_year, isbn)
        
        if self.execute_query(query, params) is not None:
            # Get the last inserted ID
            return self.execute_query("SELECT LAST_INSERT_ID()")[0][0]
        return None
        
    def update_book(self, book_id, title, author, genre, publication_year=None, isbn=None):
        """
        Update an existing book
        
        Args:
            book_id (int): ID of the book to update
            title (str): Book title
            author (str): Book author
            genre (str): Book genre
            publication_year (int, optional): Year of publication
            isbn (str, optional): ISBN number
            
        Returns:
            bool: True if successful, False otherwise
        """
        query = """
            UPDATE books
            SET title = %s, author = %s, genre = %s, publication_year = %s, isbn = %s
            WHERE book_id = %s
        """
        params = (title, author, genre, publication_year, isbn, book_id)
        
        return self.execute_query(query, params) is not None
        
    def delete_book(self, book_id):
        """
        Delete a book by ID
        
        Args:
            book_id (int): ID of the book to delete
            
        Returns:
            bool: True if successful, False otherwise
        """
        query = """
            DELETE FROM books
            WHERE book_id = %s
        """
        return self.execute_query(query, (book_id,)) is not None