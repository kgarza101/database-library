import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error

class LibraryBookApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Book Records")
        self.root.geometry("900x600")
        
        # For accessing MySQL database
        self.db_config = {
            'host': 'localhost',
            'user': 'root', # use MySQL username
            'password': 'password', # use MySQL password (change before uploading to github)
            'database': 'librarydb.mwb'
        }
        
        self.widgets()
        self.load_books()
    
    # Desktop widgets    
    def widgets(self):
        title_label = tk.Label(
            self.root,
            text = "Library Book Records",
            font = ("Arial", 20, "bold"),
            pady = 20,
            bg = "#2c3e50",
            fg = "white"
        )
        
        title_label.pack(fill = tk.X)
        search_frame = tk.Frame(self.root, pady=15, bg = "#ecf0f1")
        search_frame.pack(fill = tk.X, padx = 20)
        
        tk.Label(
            search_frame,
            text = "Search: ",
            font = ("Arial", 11),
            bg = "#ecf0f1"
        ).pack(side = tk.LEFT, padx=5)
        
        self.search_var = tk.StringVar()
        self.search_var.trace('w', lambda *args: self.search_books())
        search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_var,
            width = 35,
            font = ("Arial", 10)
        )
        
        search_entry.pack(side = tk.LEFT, padx = 5)
        
        tk.Button(
            search_frame,
            text = "Refresh",
            command=self.load_books,
            bg = "#27ae60",
            fg = "white",    
            padx = 15,
            pady = 5,
            font = ("Arial", 10, "bold"),
            cursor = "hand2"
        ).pack(side = tk.LEFT, padx = 5)
        
        tk.Button(
            search_frame, 
            text = "Clear Search", 
            command = self.clear_search,
            bg = "#3498db",
            fg = "white",
            padx = 15,
            pady = 5,
            font = ("Arial", 10, "bold"),
            cursor = "hand2"
        ).pack(side = tk.LEFT, padx = 5)        
        
        # Desktop column 
        tree_frame = tk.Frame(self.root)
        tree_frame.pack(fill = tk.BOTH, expand = True, padx = 20, pady = 10)
        
        # Scrollbar in desktop
        vsb = ttk.Scrollbar(tree_frame, orient = "vertical")
        vsb.pack(side = tk.RIGHT, fill = tk.Y)
       
        hsb = ttk.Scrollbar(tree_frame, orient = "horizontal")
        hsb.pack(side = tk.BOTTOM, fill = tk.X) 
        
        # Styling column
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                       background = "#ffffff",
                       foreground = "black",
                       rowheight = 25,
                       fieldbackground = "#ffffff",
                       font = ("Arial", 10))
        style.map("Treeview", background=[("selected", "#3498db")])
        style.configure("Treeview.Heading",
                        font=("Arial", 11, "bold"),
                        background = "#34495e",
                        foreground = "white")
        
        self.tree = ttk.Treeview(
            tree_frame,
            columns=("ID", "Title", "Author", "Genre"),
            show = "headings",
            yscrollcommand = vsb.set,
            xscrollcommand = hsb.set            
        )
        
        vsb.config(command = self.tree.yview)
        hsb.config(command = self.tree.xview)
        
        # Column headings
        self.tree.heading("ID", text = "Book ID")
        self.tree.heading("Title", text = "Title")
        self.tree.heading("Author", text = "Author")
        self.tree.heading("Genre", text = "Genre")
        
        # Column widths
        self.tree.column("ID", width = 80, anchor = tk.CENTER)
        self.tree.column("Title", width = 350, anchor = tk.W)
        self.tree.column("Author", width = 200, anchor = tk.W)
        self.tree.column("Genre", width = 150, anchor = tk.W)
        
        # Row colors
        self.tree.tag_configure("oddrow", background = "#f8f9fa")
        self.tree.tag_configure("evenrow", background = "#ffffff")
        self.tree.pack(fill = tk.BOTH, expand = True)
        
        self.status_label = tk.Label(
            self.root,
            text = "Ready",
            bd = 1,
            relief = tk.SUNKEN,
            anchor = tk.W,
            bg="#ecf0f1",
            font=("Arial", 9)
        )
        
        self.status_label.pack(side = tk.BOTTOM, fill = tk.X)
    
    # Will load books from SQL database    
    def load_books(self):
        """Load all books from database"""
        try:
            for item in self.tree.get_children():
                self.tree.delete(item)
                
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()
            query = """
                SELECT book_id, title, author, genre
                FROM books
                ORDER BY title
            """
            cursor.execute(query)
            books = cursor.fetchall()
            
            for index, book in enumerate(books):
                tag = "evenrow" if index % 2 == 0 else "oddrow"
                self.tree.insert("", tk.END, values = book, tags = (tag,))
            
            self.status_label.config(text=f"✓ Loaded {len(books)} books")
            
            cursor.close()
            conn.close()
            
        except Error as e:
            messagebox.showerror("Database Error", f"Error loading books: {e}")
            self.status_label.config(text = "✗ Error loading books")
    
    def search_books(self):
        """Search books based on search term"""
        search_term = self.search_var.get().strip()
        
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        if not search_term:
            self.load_books()
            return
        
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()
            query = """
                SELECT book_id, title, author, genre
                FROM books
                WHERE title LIKE %s OR author LIKE %s OR genre LIKE %s
                ORDER BY title
            """
            search_pattern = f"%{search_term}%"
            cursor.execute(query, (search_pattern, search_pattern, search_pattern))
            books = cursor.fetchall()
            
            for index, book in enumerate(books):
                tag = "evenrow" if index % 2 == 0 else "oddrow"
                self.tree.insert("", tk.END, values = book, tags = (tag,))
            
            self.status_label.config(text=f"✓ Found {len(books)} books matching '{search_term}'")
            
            cursor.close()
            conn.close()
            
        except Error as e:
            messagebox.showerror("Database Error", f"Error searching for books: {e}")
            self.status_label.config(text = "✗ Error searching for books")
    
    def clear_search(self):
        self.search_var.set("")
        self.load_books()

if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryBookApp(root)
    root.mainloop()