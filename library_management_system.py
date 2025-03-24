"""
Simplified Library Management System
"""

import datetime


class Book:
    def __init__(self, book_id, title, author, genre, publication_year, is_available=True):
        # Basic validation
        if not isinstance(publication_year, int):
            raise ValueError("Publication year must be an integer")
        
        current_year = datetime.datetime.now().year
        if publication_year > current_year:
            raise ValueError("Publication year cannot be in the future")
            
        self.__book_id = book_id
        self.__title = title
        self.__author = author
        self.__genre = genre
        self.__publication_year = publication_year
        self.__is_available = is_available
    
    @property
    def book_id(self): return self.__book_id
    
    @property
    def title(self): return self.__title
    
    @property
    def author(self): return self.__author
    
    @property
    def genre(self): return self.__genre
    
    @property
    def publication_year(self): return self.__publication_year
    
    @property
    def is_available(self): return self.__is_available
    
    @is_available.setter
    def is_available(self, value): self.__is_available = value
    
    def checkout(self):
        if not self.__is_available: return False
        self.__is_available = False
        return True
    
    def return_to_library(self):
        if self.__is_available: return False
        self.__is_available = True
        return True
    
    def display_info(self):
        availability = "Available" if self.__is_available else "Checked Out"
        return f"{self.__book_id} | {self.__title} by {self.__author} | {self.__genre} | {self.__publication_year} | {availability}"


class FictionBook(Book):
    def __init__(self, book_id, title, author, genre, publication_year, fiction_type, is_available=True):
        super().__init__(book_id, title, author, genre, publication_year, is_available)
        self.__fiction_type = fiction_type
    
    @property
    def fiction_type(self): return self.__fiction_type
    
    def display_info(self):
        basic_info = super().display_info()
        return f"{basic_info} | Type: {self.__fiction_type}"


class NonFictionBook(Book):
    def __init__(self, book_id, title, author, genre, publication_year, subject, is_available=True):
        super().__init__(book_id, title, author, genre, publication_year, is_available)
        self.__subject = subject
    
    @property
    def subject(self): return self.__subject
    
    def display_info(self):
        basic_info = super().display_info()
        return f"{basic_info} | Subject: {self.__subject}"


class Member:
    def __init__(self, member_id, name, email, books_borrowed=None):
        # Simple email validation
        if not '@' in email or not '.' in email.split('@')[1]:
            raise ValueError("Invalid email format")
            
        self.__member_id = member_id
        self.__name = name
        self.__email = email
        self.__books_borrowed = books_borrowed if books_borrowed is not None else []
    
    @property
    def member_id(self): return self.__member_id
    
    @property
    def name(self): return self.__name
    
    @property
    def email(self): return self.__email
    
    @property
    def books_borrowed(self): return self.__books_borrowed.copy()
    
    def borrow_book(self, book):
        if len(self.__books_borrowed) >= 3:
            print("Maximum borrowing limit (3) reached")
            return False
        
        if not book.is_available:
            print(f"Book '{book.title}' is not available")
            return False
        
        if book.checkout():
            self.__books_borrowed.append(book.book_id)
            return True
        return False
    
    def return_book(self, book):
        if book.book_id not in self.__books_borrowed: return False
        
        if book.return_to_library():
            self.__books_borrowed.remove(book.book_id)
            return True
        return False
    
    def display_info(self):
        return f"{self.__member_id} | {self.__name} | {self.__email} | Books borrowed: {len(self.__books_borrowed)}"


class Library:
    book_count = 0
    member_count = 0
    
    def __init__(self, name, address):
        self.__name = name
        self.__address = address
        self.__books = {}
        self.__members = {}
    
    @property
    def name(self): return self.__name
    
    @property
    def address(self): return self.__address
    
    @staticmethod
    def get_book_count(): return Library.book_count
    
    @staticmethod
    def get_member_count(): return Library.member_count
    
    def add_book(self, book):
        if book.book_id in self.__books: return False
        
        self.__books[book.book_id] = book
        Library.book_count += 1
        return True
    
    def add_member(self, member):
        if member.member_id in self.__members: return False
        
        self.__members[member.member_id] = member
        Library.member_count += 1
        return True
    
    def checkout_book(self, book_id, member_id):
        if book_id not in self.__books:
            print(f"Book with ID {book_id} not found")
            return False
        
        if member_id not in self.__members:
            print(f"Member with ID {member_id} not found")
            return False
        
        book = self.__books[book_id]
        member = self.__members[member_id]
        
        return member.borrow_book(book)
    
    def return_book(self, book_id, member_id):
        if book_id not in self.__books:
            print(f"Book with ID {book_id} not found")
            return False
        
        if member_id not in self.__members:
            print(f"Member with ID {member_id} not found")
            return False
        
        book = self.__books[book_id]
        member = self.__members[member_id]
        
        return member.return_book(book)
    
    def get_available_books(self):
        return {book_id: book for book_id, book in self.__books.items() if book.is_available}
    
    def search_book_by_title(self, title):
        if title is None:
            raise ValueError("Search title cannot be None")
            
        title = title.lower()
        return {book_id: book for book_id, book in self.__books.items() 
                if title in book.title.lower()}
    
    def search_book_by_author(self, author):
        if author is None:
            raise ValueError("Search author cannot be None")
        
        author = author.lower()
        return {book_id: book for book_id, book in self.__books.items() 
                if author in book.author.lower().split()}
    
    def get_book(self, book_id): return self.__books.get(book_id)
    
    def get_member(self, member_id): return self.__members.get(member_id)
    
    def get_all_books(self): return self.__books.copy()
    
    def get_all_members(self): return self.__members.copy()


def main():
    library = Library("City Public Library", "123 Main St, Anytown")
    
    # Add initial books
    library.add_book(FictionBook("B001", "To Kill a Mockingbird", "Harper Lee", "Fiction", 1960, "Novel"))
    library.add_book(FictionBook("B002", "1984", "George Orwell", "Fiction", 1949, "Novel"))
    library.add_book(NonFictionBook("B003", "A Brief History of Time", "Stephen Hawking", "Non-Fiction", 1988, "Physics"))
    library.add_book(NonFictionBook("B004", "Sapiens", "Yuval Noah Harari", "Non-Fiction", 2011, "History"))
    
    # Add initial members
    library.add_member(Member("M001", "John Smith", "john@example.com"))
    library.add_member(Member("M002", "Jane Doe", "jane@example.com"))
    
    while True:
        print("\n===== LIBRARY MANAGEMENT SYSTEM =====")
        print(f"Library Name: {library.name}")
        print(f"Address: {library.address}")
        print(f"Total Books: {Library.get_book_count()}")
        print(f"Total Members: {Library.get_member_count()}")
        print("\nMenu:")
        print("1. Add New Book")
        print("2. Add New Member")
        print("3. Checkout Book")
        print("4. Return Book")
        print("5. Display All Books")
        print("6. Display All Members")
        print("7. Search for Books")
        print("0. Exit")
        
        try:
            choice = int(input("\nEnter your choice (0-7): "))
            
            if choice == 1:
                # Add new book
                book_id = input("Enter book ID: ")
                title = input("Enter title: ")
                author = input("Enter author: ")
                genre = input("Enter genre: ")
                
                try:
                    publication_year = int(input("Enter publication year: "))
                except ValueError:
                    print("Invalid year. Using current year.")
                    publication_year = datetime.datetime.now().year
                
                book_type = input("Enter book type (F for Fiction, N for Non-Fiction): ").upper()
                
                if book_type == 'F':
                    fiction_type = input("Enter fiction type: ")
                    book = FictionBook(book_id, title, author, genre, publication_year, fiction_type)
                elif book_type == 'N':
                    subject = input("Enter subject: ")
                    book = NonFictionBook(book_id, title, author, genre, publication_year, subject)
                else:
                    print("Invalid book type. Adding as base Book type.")
                    book = Book(book_id, title, author, genre, publication_year)
                
                if library.add_book(book):
                    print(f"Book {book_id} added successfully.")
                else:
                    print(f"Book with ID {book_id} already exists.")
            
            elif choice == 2:
                # Add new member
                member_id = input("Enter member ID: ")
                name = input("Enter name: ")
                email = input("Enter email: ")
                
                try:
                    member = Member(member_id, name, email)
                    if library.add_member(member):
                        print(f"Member {member_id} added successfully.")
                    else:
                        print(f"Member with ID {member_id} already exists.")
                except ValueError as e:
                    print(f"Invalid member data: {e}")
            
            elif choice == 3:
                # Checkout book
                book_id = input("Enter book ID: ")
                member_id = input("Enter member ID: ")
                
                if library.checkout_book(book_id, member_id):
                    print(f"Book {book_id} checked out successfully to member {member_id}.")
                else:
                    print("Checkout failed.")
            
            elif choice == 4:
                # Return book
                book_id = input("Enter book ID: ")
                member_id = input("Enter member ID: ")
                
                if library.return_book(book_id, member_id):
                    print(f"Book {book_id} returned successfully by member {member_id}.")
                else:
                    print("Return failed.")
            
            elif choice == 5:
                # Display all books
                books = library.get_all_books()
                
                if books:
                    print("\nCurrent Book Collection:")
                    for book in books.values():
                        print(book.display_info())
                else:
                    print("No books found.")
            
            elif choice == 6:
                # Display all members
                members = library.get_all_members()
                
                if members:
                    print("\nLibrary Members:")
                    for member in members.values():
                        print(member.display_info())
                else:
                    print("No members found.")
            
            elif choice == 7:
                # Search for books
                print("\nSearch Options:")
                print("1. Search by Title")
                print("2. Search by Author")
                print("3. Show Available Books")
                
                search_choice = int(input("Enter search option (1-3): "))
                
                if search_choice == 1:
                    title = input("Enter title keyword: ")
                    books = library.search_book_by_title(title)
                elif search_choice == 2:
                    author = input("Enter author keyword: ")
                    books = library.search_book_by_author(author)
                elif search_choice == 3:
                    books = library.get_available_books()
                else:
                    print("Invalid search option.")
                    continue
                
                if books:
                    print("\nSearch Results:")
                    for book in books.values():
                        print(book.display_info())
                else:
                    print("No matching books found.")
            
            elif choice == 0:
                # Exit
                print("Thank you for using the Library Management System.")
                break
            
            else:
                print("Invalid choice. Please enter a number between 0 and 7.")
        
        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()