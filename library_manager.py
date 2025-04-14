import json
import os
from typing import Dict, List, Any, Union

class LibraryManager:
    def __init__(self, filename: str = "library.txt"):
        self.filename = filename
        self.library: List[Dict[str, Any]] = []
        self.load_library()
    
    def add_book(self, title: str, author: str, year: int, genre: str, read: bool) -> None:
        """Add a new book to the library."""
        book = {
            "title": title,
            "author": author,
            "year": year,
            "genre": genre,
            "read": read
        }
        self.library.append(book)
        print("Book added successfully!")
    
    def remove_book(self, title: str) -> bool:
        """Remove a book from the library by title."""
        initial_count = len(self.library)
        self.library = [book for book in self.library if book["title"].lower() != title.lower()]
        
        if len(self.library) < initial_count:
            print("Book removed successfully!")
            return True
        else:
            print(f"No book with title '{title}' found in the library.")
            return False
    
    def search_by_title(self, title: str) -> List[Dict[str, Any]]:
        """Search for books by title (partial match)."""
        return [book for book in self.library if title.lower() in book["title"].lower()]
    
    def search_by_author(self, author: str) -> List[Dict[str, Any]]:
        """Search for books by author (partial match)."""
        return [book for book in self.library if author.lower() in book["author"].lower()]
    
    def display_books(self, books: List[Dict[str, Any]] = None) -> None:
        """Display a list of books in a formatted way."""
        if books is None:
            books = self.library
        
        if not books:
            print("No books to display.")
            return
        
        print("Your Library:")
        for i, book in enumerate(books, 1):
            read_status = "Read" if book["read"] else "Unread"
            print(f"{i}. {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {read_status}")
    
    def display_statistics(self) -> None:
        """Display statistics about the library."""
        total_books = len(self.library)
        if total_books == 0:
            print("Library is empty. No statistics available.")
            return
        
        read_books = sum(1 for book in self.library if book["read"])
        read_percentage = (read_books / total_books) * 100 if total_books > 0 else 0
        
        print(f"Total books: {total_books}")
        print(f"Percentage read: {read_percentage:.1f}%")
    
    def save_library(self) -> None:
        """Save the library to a file."""
        try:
            with open(self.filename, 'w') as file:
                json.dump(self.library, file)
            print(f"Library saved to {self.filename}.")
        except Exception as e:
            print(f"Error saving library: {e}")
    
    def load_library(self) -> None:
        """Load the library from a file if it exists."""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as file:
                    self.library = json.load(file)
                print(f"Library loaded from {self.filename}.")
            except Exception as e:
                print(f"Error loading library: {e}")
                self.library = []
        else:
            print("No existing library file found. Starting with an empty library.")
            self.library = []

def get_integer_input(prompt: str, min_value: int = None, max_value: int = None) -> int:
    """Get an integer input from the user within a specified range."""
    while True:
        try:
            value = int(input(prompt))
            if min_value is not None and value < min_value:
                print(f"Please enter a number greater than or equal to {min_value}.")
                continue
            if max_value is not None and value > max_value:
                print(f"Please enter a number less than or equal to {max_value}.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number.")

def get_yes_no_input(prompt: str) -> bool:
    """Get a yes/no input from the user and return as boolean."""
    while True:
        response = input(prompt).lower()
        if response in ["yes", "y"]:
            return True
        elif response in ["no", "n"]:
            return False
        else:
            print("Please enter 'yes' or 'no'.")

def display_menu() -> None:
    """Display the main menu options."""
    print("\nWelcome to your Personal Library Manager!")
    print("1. Add a book")
    print("2. Remove a book")
    print("3. Search for a book")
    print("4. Display all books")
    print("5. Display statistics")
    print("6. Save to File and Exit")

def main() -> None:
    """Main function to run the Personal Library Manager."""
    library_manager = LibraryManager()
    
    while True:
        display_menu()
        choice = get_integer_input("Enter your choice: ", 1, 6)
        
        if choice == 1:  # Add a book
            title = input("Enter the book title: ")
            author = input("Enter the author: ")
            year = get_integer_input("Enter the publication year: ", 0)
            genre = input("Enter the genre: ")
            read = get_yes_no_input("Have you read this book? (yes/no): ")
            library_manager.add_book(title, author, year, genre, read)
        
        elif choice == 2:  # Remove a book
            title = input("Enter the title of the book to remove: ")
            library_manager.remove_book(title)
        
        elif choice == 3:  # Search for a book
            print("Search by:")
            print("1. Title")
            print("2. Author")
            search_choice = get_integer_input("Enter your choice: ", 1, 2)
            
            if search_choice == 1:
                title = input("Enter the title: ")
                results = library_manager.search_by_title(title)
                print("Matching Books:")
                library_manager.display_books(results)
            else:
                author = input("Enter the author: ")
                results = library_manager.search_by_author(author)
                print("Matching Books:")
                library_manager.display_books(results)
        
        elif choice == 4:  # Display all books
            library_manager.display_books()
        
        elif choice == 5:  # Display statistics
            library_manager.display_statistics()
        
        elif choice == 6:  # Exit
            library_manager.save_library()
            print("Library saved to file. Goodbye!")
            break

if __name__ == "__main__":
    main()