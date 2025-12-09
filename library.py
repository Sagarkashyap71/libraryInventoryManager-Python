# ---------------------------------------------
# LIBRARY INVENTORY MANAGER - MINI PROJECT
# Name: Sagar Singh
# Course: B.Tech CSE
# Title: Library Inventory Manager
# ---------------------------------------------

import json
import logging
from pathlib import Path

# ---------------------------------------------
# Logging Setup
# ---------------------------------------------
logging.basicConfig(
    filename="library.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ---------------------------------------------
# Task 1: BOOK CLASS
# ---------------------------------------------
class Book:
    def __init__(self, title, author, isbn, status="available"):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.status = status  # available / issued

    def __str__(self):
        return f"{self.title} | {self.author} | ISBN: {self.isbn} | Status: {self.status}"

    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "status": self.status
        }

    def issue(self):
        if self.status == "issued":
            return False
        self.status = "issued"
        return True

    def return_book(self):
        if self.status == "available":
            return False
        self.status = "available"
        return True

    def is_available(self):
        return self.status == "available"


# ----------------------------------------------------
# Task 2 + 3: INVENTORY MANAGER with ABSOLUTE JSON PATH
# ----------------------------------------------------
class LibraryInventory:
    def __init__(self):
        # ABSOLUTE PATH → Works in terminal + right click run
        self.file_path = Path(__file__).resolve().parent / "library_books.json"
        self.books = []
        self.load_books()

    # Add Book
    def add_book(self, book: Book):
        self.books.append(book)
        logging.info(f"Book added: {book.title}")

    # Search by title
    def search_by_title(self, title):
        return [b for b in self.books if title.lower() in b.title.lower()]

    # Search by ISBN
    def search_by_isbn(self, isbn):
        for b in self.books:
            if b.isbn == isbn:
                return b
        return None

    # Display all books
    def display_all(self):
        if not self.books:
            print("No books available in the inventory.")
            return
        print("\n----- BOOK INVENTORY -----")
        for b in self.books:
            print(b)

    # Save to JSON
    def save_books(self):
        try:
            with open(self.file_path, "w") as f:
                json.dump([b.to_dict() for b in self.books], f, indent=4)
        except Exception as e:
            logging.error("Error saving books: " + str(e))

    # Load from JSON
    def load_books(self):
        try:
            if not self.file_path.exists():
                self.save_books()
                return

            with open(self.file_path, "r") as f:
                data = json.load(f)

                for item in data:
                    book = Book(
                        item["title"], item["author"],
                        item["isbn"], item["status"]
                    )
                    self.books.append(book)

        except json.JSONDecodeError:
            logging.error("JSON corrupted. Resetting...")
            self.save_books()
        except Exception as e:
            logging.error("Error loading books: " + str(e))


# ---------------------------------------------
# Task 4: MENU-DRIVEN CLI
# ---------------------------------------------
def menu():
    print("\n========== LIBRARY INVENTORY MANAGER ==========")
    print("1. Add Book")
    print("2. Issue Book")
    print("3. Return Book")
    print("4. View All Books")
    print("5. Search Book")
    print("6. Exit")
    return input("Enter your choice: ")


def main():
    inventory = LibraryInventory()

    while True:
        choice = menu()

        # Add Book
        if choice == "1":
            title = input("Enter Book Title: ")
            author = input("Enter Author: ")
            isbn = input("Enter ISBN: ")

            book = Book(title, author, isbn)
            inventory.add_book(book)
            inventory.save_books()
            print("Book Added Successfully!")

        # Issue Book
        elif choice == "2":
            isbn = input("Enter ISBN to issue: ")
            book = inventory.search_by_isbn(isbn)

            if book and book.issue():
                inventory.save_books()
                print("Book Issued Successfully!")
            else:
                print("Cannot issue. Book not available or invalid ISBN.")

        # Return Book
        elif choice == "3":
            isbn = input("Enter ISBN to return: ")
            book = inventory.search_by_isbn(isbn)

            if book and book.return_book():
                inventory.save_books()
                print("Book Returned Successfully!")
            else:
                print("Cannot return. Book already available or invalid ISBN.")

        # View All Books
        elif choice == "4":
            inventory.display_all()

        # Search
        elif choice == "5":
            query = input("Enter Title/ISBN to search: ")

            # Search by ISBN
            book = inventory.search_by_isbn(query)
            if book:
                print("Book Found:")
                print(book)
                continue

            # Search by title
            results = inventory.search_by_title(query)
            if results:
                print("Matching Books:")
                for b in results:
                    print(b)
            else:
                print("No book found.")

        # Exit
        elif choice == "6":
            print("Exiting Library Manager...")
            break

        else:
            print("Invalid Choice! Try Again.")


# Run Program
if __name__ == "__main__":
    main()
