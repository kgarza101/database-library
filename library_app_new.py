import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import os
from database import DatabaseConnection

class LibraryBookApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Book Records")
        self.root.geometry("900x600")
        
        # Initialize database connection
        self.db = DatabaseConnection(config_file='config.ini')
        
        self.create_widgets()
        self.load_books()
    
    # Desktop widgets    
    def create_widgets(self):
        # Main title
        title_label = tk.Label(
            self.root,
            text = "Library Book Records",
            font = ("Arial", 20, "bold"),
            pady = 20,
            bg = "#2c3e50",
            fg = "white"
        )
        title_label.pack(fill = tk.X)
        
        # Button frame (top)
        button_frame = tk.Frame(self.root, bg = "#ecf0f1")
        button_frame.pack(fill = tk.X, padx = 20, pady = 5)
        
        # Add book button
        tk.Button(
            button_frame,
            text = "Add Book",
            command = self.add_book_dialog,
            bg = "#2ecc71",
            fg = "white",
            padx = 15,
            pady = 5,
            font = ("Arial", 10, "bold"),
            cursor = "hand2"
        ).pack(side = tk.LEFT, padx = 5)
        
        # Edit book button
        tk.Button(
            button_frame,
            text = "Edit Book",
            command = self.edit_book_dialog,
            bg = "#f39c12",
            fg = "white",
            padx = 15,
            pady = 5,
            font = ("Arial", 10, "bold"),
            cursor = "hand2"
        ).pack(side = tk.LEFT, padx = 5)
        
        # Delete book button
        tk.Button(
            button_frame,
            text = "Delete Book",
            command = self.delete_book,
            bg = "#e74c3c",
            fg = "white",
            padx = 15,
            pady = 5,
            font = ("Arial", 10, "bold"),
            cursor = "hand2"
        ).pack(side = tk.LEFT, padx = 5)
        
        # Search frame
        search_frame = tk.Frame(self.root, pady=10, bg = "#ecf0f1")
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
        
        # Tree frame for book display
        tree_frame = tk.Frame(self.root)
        tree_frame.pack(fill = tk.BOTH, expand = True, padx = 20, pady = 10)
        
        # Scrollbars
        vsb = ttk.Scrollbar(tree_frame, orient = "vertical")
        vsb.pack(side = tk.RIGHT, fill = tk.Y)
       
        hsb = ttk.Scrollbar(tree_frame, orient = "horizontal")
        hsb.pack(side = tk.BOTTOM, fill = tk.X) 
        
        # Styling
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
        
        # Create Treeview
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
        
        # Status bar
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
        
        # Double click to edit
        self.tree.bind("<Double-1>", lambda event: self.edit_book_dialog())
    
    # Database operations
    def load_books(self):
        """Load all books from database"""
        try:
            # Clear the treeview
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Connect to database and get books
            self.db.connect()
            books = self.db.get_all_books()
            
            if books:
                for index, book in enumerate(books):
                    tag = "evenrow" if index % 2 == 0 else "oddrow"
                    self.tree.insert("", tk.END, values=book, tags=(tag,))
                
                self.status_label.config(text=f"✓ Loaded {len(books)} books")
            else:
                self.status_label.config(text="No books found in database")
                
        except Exception as e:
            messagebox.showerror("Database Error", f"Error loading books: {e}")
            self.status_label.config(text="✗ Error loading books")
        finally:
            self.db.disconnect()
    
    def search_books(self):
        """Search books based on search term"""
        search_term = self.search_var.get().strip()
        
        # Clear the treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        if not search_term:
            self.load_books()
            return
        
        try:
            # Connect to database and search books
            self.db.connect()
            books = self.db.search_books(search_term)
            
            if books:
                for index, book in enumerate(books):
                    tag = "evenrow" if index % 2 == 0 else "oddrow"
                    self.tree.insert("", tk.END, values=book, tags=(tag,))
                
                self.status_label.config(text=f"✓ Found {len(books)} books matching '{search_term}'")
            else:
                self.status_label.config(text=f"No books found matching '{search_term}'")
                
        except Exception as e:
            messagebox.showerror("Database Error", f"Error searching for books: {e}")
            self.status_label.config(text="✗ Error searching for books")
        finally:
            self.db.disconnect()
    
    def clear_search(self):
        """Clear search and reload all books"""
        self.search_var.set("")
        self.load_books()
        
    def add_book_dialog(self):
        """Open dialog to add a new book"""
        # Create a custom dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Book")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Form fields
        tk.Label(dialog, text="Title:", anchor="w").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        title_var = tk.StringVar()
        tk.Entry(dialog, textvariable=title_var, width=30).grid(row=0, column=1, padx=10, pady=10)
        
        tk.Label(dialog, text="Author:", anchor="w").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        author_var = tk.StringVar()
        tk.Entry(dialog, textvariable=author_var, width=30).grid(row=1, column=1, padx=10, pady=10)
        
        tk.Label(dialog, text="Genre:", anchor="w").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        genre_var = tk.StringVar()
        tk.Entry(dialog, textvariable=genre_var, width=30).grid(row=2, column=1, padx=10, pady=10)
        
        tk.Label(dialog, text="Publication Year:", anchor="w").grid(row=3, column=0, padx=10, pady=10, sticky="w")
        year_var = tk.StringVar()
        tk.Entry(dialog, textvariable=year_var, width=30).grid(row=3, column=1, padx=10, pady=10)
        
        tk.Label(dialog, text="ISBN:", anchor="w").grid(row=4, column=0, padx=10, pady=10, sticky="w")
        isbn_var = tk.StringVar()
        tk.Entry(dialog, textvariable=isbn_var, width=30).grid(row=4, column=1, padx=10, pady=10)
        
        # Submit button
        def submit_book():
            title = title_var.get().strip()
            author = author_var.get().strip()
            genre = genre_var.get().strip()
            year = year_var.get().strip()
            isbn = isbn_var.get().strip()
            
            if not title or not author or not genre:
                messagebox.showerror("Input Error", "Title, Author and Genre are required fields")
                return
                
            try:
                year = int(year) if year else None
            except ValueError:
                messagebox.showerror("Input Error", "Publication Year must be a number")
                return
                
            # Add to database
            try:
                self.db.connect()
                book_id = self.db.add_book(title, author, genre, year, isbn)
                
                if book_id:
                    messagebox.showinfo("Success", "Book added successfully")
                    dialog.destroy()
                    self.load_books()
                else:
                    messagebox.showerror("Database Error", "Failed to add book")
            except Exception as e:
                messagebox.showerror("Database Error", f"Error adding book: {e}")
            finally:
                self.db.disconnect()
                
        # Button frame
        button_frame = tk.Frame(dialog)
        button_frame.grid(row=5, column=0, columnspan=2, pady=20)
        
        tk.Button(
            button_frame,
            text="Add Book",
            command=submit_book,
            bg="#2ecc71",
            fg="white",
            padx=15,
            pady=5
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            button_frame,
            text="Cancel",
            command=dialog.destroy,
            bg="#e74c3c",
            fg="white",
            padx=15,
            pady=5
        ).pack(side=tk.LEFT, padx=5)
    
    def edit_book_dialog(self):
        """Open dialog to edit selected book"""
        selected_item = self.tree.selection()
        
        if not selected_item:
            messagebox.showinfo("No Selection", "Please select a book to edit")
            return
            
        # Get book data from selection
        book_data = self.tree.item(selected_item[0], 'values')
        book_id = book_data[0]
        
        # Create a custom dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Book")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Form fields with pre-filled data
        tk.Label(dialog, text="Title:", anchor="w").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        title_var = tk.StringVar(value=book_data[1])
        tk.Entry(dialog, textvariable=title_var, width=30).grid(row=0, column=1, padx=10, pady=10)
        
        tk.Label(dialog, text="Author:", anchor="w").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        author_var = tk.StringVar(value=book_data[2])
        tk.Entry(dialog, textvariable=author_var, width=30).grid(row=1, column=1, padx=10, pady=10)
        
        tk.Label(dialog, text="Genre:", anchor="w").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        genre_var = tk.StringVar(value=book_data[3])
        tk.Entry(dialog, textvariable=genre_var, width=30).grid(row=2, column=1, padx=10, pady=10)
        
        # Try to get additional info from database
        try:
            self.db.connect()
            query = "SELECT publication_year, isbn FROM books WHERE book_id = %s"
            result = self.db.execute_query(query, (book_id,))
            if result and len(result[0]) >= 2:
                year_value = result[0][0] if result[0][0] else ""
                isbn_value = result[0][1] if result[0][1] else ""
            else:
                year_value = ""
                isbn_value = ""
            self.db.disconnect()
        except:
            year_value = ""
            isbn_value = ""
            
        tk.Label(dialog, text="Publication Year:", anchor="w").grid(row=3, column=0, padx=10, pady=10, sticky="w")
        year_var = tk.StringVar(value=str(year_value))
        tk.Entry(dialog, textvariable=year_var, width=30).grid(row=3, column=1, padx=10, pady=10)
        
        tk.Label(dialog, text="ISBN:", anchor="w").grid(row=4, column=0, padx=10, pady=10, sticky="w")
        isbn_var = tk.StringVar(value=isbn_value)
        tk.Entry(dialog, textvariable=isbn_var, width=30).grid(row=4, column=1, padx=10, pady=10)
        
        # Submit button
        def update_book():
            title = title_var.get().strip()
            author = author_var.get().strip()
            genre = genre_var.get().strip()
            year = year_var.get().strip()
            isbn = isbn_var.get().strip()
            
            if not title or not author or not genre:
                messagebox.showerror("Input Error", "Title, Author and Genre are required fields")
                return
                
            try:
                year = int(year) if year else None
            except ValueError:
                messagebox.showerror("Input Error", "Publication Year must be a number")
                return
                
            # Update database
            try:
                self.db.connect()
                success = self.db.update_book(book_id, title, author, genre, year, isbn)
                
                if success:
                    messagebox.showinfo("Success", "Book updated successfully")
                    dialog.destroy()
                    self.load_books()
                else:
                    messagebox.showerror("Database Error", "Failed to update book")
            except Exception as e:
                messagebox.showerror("Database Error", f"Error updating book: {e}")
            finally:
                self.db.disconnect()
                
        # Button frame
        button_frame = tk.Frame(dialog)
        button_frame.grid(row=5, column=0, columnspan=2, pady=20)
        
        tk.Button(
            button_frame,
            text="Update Book",
            command=update_book,
            bg="#f39c12",
            fg="white",
            padx=15,
            pady=5
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            button_frame,
            text="Cancel",
            command=dialog.destroy,
            bg="#e74c3c",
            fg="white",
            padx=15,
            pady=5
        ).pack(side=tk.LEFT, padx=5)
        
    def delete_book(self):
        """Delete selected book"""
        selected_item = self.tree.selection()
        
        if not selected_item:
            messagebox.showinfo("No Selection", "Please select a book to delete")
            return
            
        # Get book data from selection
        book_data = self.tree.item(selected_item[0], 'values')
        book_id = book_data[0]
        book_title = book_data[1]
        
        # Confirm deletion
        if not messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{book_title}'?"):
            return
            
        # Delete from database
        try:
            self.db.connect()
            if self.db.delete_book(book_id):
                self.tree.delete(selected_item)
                self.status_label.config(text=f"✓ Book '{book_title}' deleted")
            else:
                messagebox.showerror("Database Error", "Failed to delete book")
        except Exception as e:
            messagebox.showerror("Database Error", f"Error deleting book: {e}")
        finally:
            self.db.disconnect()

if __name__ == "__main__":
    # Check if database config exists, if not create a default one
    if not os.path.exists('config.ini'):
        with open('config.ini', 'w') as f:
            f.write('[database]\n')
            f.write('host = localhost\n')
            f.write('user = root\n')
            f.write('password = password\n')
            f.write('database = librarydb\n')
    
    root = tk.Tk()
    app = LibraryBookApp(root)
    root.mainloop()