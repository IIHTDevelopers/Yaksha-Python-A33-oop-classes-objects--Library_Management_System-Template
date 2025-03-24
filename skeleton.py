"""
Simplified Library Management System

This module implements a library management system that tracks
books, library members, and borrowing operations using object-oriented programming.

TODO: Implement all the classes and methods following the specifications
"""

# DO NOT MODIFY THE IMPORT
import datetime


class Book:
    """Base class representing a book in the library."""
    
    def __init__(self, book_id, title, author, genre, publication_year, is_available=True):
        """
        Initialize a Book object.
        
        Args:
            book_id: Unique identifier for the book
            title: Title of the book
            author: Author of the book
            genre: Genre of the book
            publication_year: Year the book was published
            is_available: Whether the book is available for checkout
        """
        # Validate publication_year
        if not isinstance(publication_year, int):
            raise ValueError("Publication year must be an integer")
        
        current_year = datetime.datetime.now().year
        if publication_year > current_year:
            raise ValueError("Publication year cannot be in the future")
            
        # TODO: Initialize all the private attributes
        # HINT: Use double underscore prefix for private attributes (e.g., self.__book_id)
        # WRITE IMPLEMENTATION HERE
        pass
    
    @property
    def book_id(self):
        """Get the book ID."""
        # TODO: Return the book_id
        # WRITE IMPLEMENTATION HERE
        pass
    
    @property
    def title(self):
        """Get the book title."""
        # TODO: Return the title
        # WRITE IMPLEMENTATION HERE
        pass
    
    @property
    def author(self):
        """Get the book author."""
        # TODO: Return the author
        # WRITE IMPLEMENTATION HERE
        pass
    
    @property
    def genre(self):
        """Get the book genre."""
        # TODO: Return the genre
        # WRITE IMPLEMENTATION HERE
        pass
    
    @property
    def publication_year(self):
        """Get the book publication year."""
        # TODO: Return the publication_year
        # WRITE IMPLEMENTATION HERE
        pass
    
    @property
    def is_available(self):
        """Get the book availability status."""
        # TODO: Return the is_available status
        # WRITE IMPLEMENTATION HERE
        pass
    
    @is_available.setter
    def is_available(self, value):
        """Set the book availability status."""
        # TODO: Set the is_available status
        # WRITE IMPLEMENTATION HERE
        pass
    
    def checkout(self):
        """
        Mark the book as checked out.
        
        Returns:
            bool: True if checkout successful, False otherwise
        """
        # TODO: Implement checkout logic
        # HINT: Only successful if book is currently available
        # WRITE IMPLEMENTATION HERE
        pass
    
    def return_to_library(self):
        """
        Mark the book as returned to the library.
        
        Returns:
            bool: True if return successful, False otherwise
        """
        # TODO: Implement return logic
        # HINT: Only successful if book is currently checked out
        # WRITE IMPLEMENTATION HERE
        pass
    
    def display_info(self):
        """
        Display book information.
        
        Returns:
            str: Formatted string with book information
        """
        # TODO: Return formatted string with book information
        # HINT: Include book_id, title, author, genre, publication_year, and availability status
        # WRITE IMPLEMENTATION HERE
        pass


class FictionBook(Book):
    """Class representing a fiction book, inherits from Book."""
    
    def __init__(self, book_id, title, author, genre, publication_year, fiction_type, is_available=True):
        """
        Initialize a FictionBook object.
        
        Args:
            book_id: Unique identifier for the book
            title: Title of the book
            author: Author of the book
            genre: Genre of the book
            publication_year: Year the book was published
            fiction_type: Type of fiction (e.g., Novel, Short Story)
            is_available: Whether the book is available for checkout
        """
        # TODO: Call the parent class constructor and initialize additional attributes
        # HINT: Use super().__init__() to call parent constructor
        # WRITE IMPLEMENTATION HERE
        pass
    
    @property
    def fiction_type(self):
        """Get the fiction type."""
        # TODO: Return the fiction_type
        # WRITE IMPLEMENTATION HERE
        pass
    
    def display_info(self):
        """
        Display fiction book information.
        
        Returns:
            str: Formatted string with fiction book information
        """
        # TODO: Override the display_info method to include fiction-specific information
        # HINT: Use super().display_info() to get basic book information
        # WRITE IMPLEMENTATION HERE
        pass


class NonFictionBook(Book):
    """Class representing a non-fiction book, inherits from Book."""
    
    def __init__(self, book_id, title, author, genre, publication_year, subject, is_available=True):
        """
        Initialize a NonFictionBook object.
        
        Args:
            book_id: Unique identifier for the book
            title: Title of the book
            author: Author of the book
            genre: Genre of the book
            publication_year: Year the book was published
            subject: Subject of the book
            is_available: Whether the book is available for checkout
        """
        # TODO: Call the parent class constructor and initialize additional attributes
        # HINT: Use super().__init__() to call parent constructor
        # WRITE IMPLEMENTATION HERE
        pass
    
    @property
    def subject(self):
        """Get the subject."""
        # TODO: Return the subject
        # WRITE IMPLEMENTATION HERE
        pass
    
    def display_info(self):
        """
        Display non-fiction book information.
        
        Returns:
            str: Formatted string with non-fiction book information
        """
        # TODO: Override the display_info method to include non-fiction-specific information
        # HINT: Use super().display_info() to get basic book information
        # WRITE IMPLEMENTATION HERE
        pass


class Member:
    """Class representing a library member."""
    
    def __init__(self, member_id, name, email, books_borrowed=None):
        """
        Initialize a Member object.
        
        Args:
            member_id: Unique identifier for the member
            name: Name of the member
            email: Email address of the member
            books_borrowed: List of books borrowed by the member
        """
        # Validate email format
        if not '@' in email or not '.' in email.split('@')[1]:
            raise ValueError("Invalid email format")
            
        # TODO: Initialize all attributes
        # HINT: Handle default value for books_borrowed
        # WRITE IMPLEMENTATION HERE
        pass
    
    @property
    def member_id(self):
        """Get the member ID."""
        # TODO: Return the member_id
        # WRITE IMPLEMENTATION HERE
        pass
    
    @property
    def name(self):
        """Get the member name."""
        # TODO: Return the name
        # WRITE IMPLEMENTATION HERE
        pass
    
    @property
    def email(self):
        """Get the member email."""
        # TODO: Return the email
        # WRITE IMPLEMENTATION HERE
        pass
    
    @property
    def books_borrowed(self):
        """Get the list of books borrowed by the member."""
        # TODO: Return a copy of the books_borrowed list
        # HINT: Use the copy() method to avoid returning a reference to the original list
        # WRITE IMPLEMENTATION HERE
        pass
    
    def borrow_book(self, book):
        """
        Borrow a book.
        
        Args:
            book: Book object to borrow
            
        Returns:
            bool: True if borrow successful, False otherwise
        """
        # TODO: Implement borrow logic
        # HINT: Check if member has reached maximum book limit (3)
        # HINT: Check if the book is available
        # HINT: Use book.checkout() method
        # WRITE IMPLEMENTATION HERE
        pass
    
    def return_book(self, book):
        """
        Return a borrowed book.
        
        Args:
            book: Book object to return
            
        Returns:
            bool: True if return successful, False otherwise
        """
        # TODO: Implement return logic
        # HINT: Check if the member has borrowed this book
        # HINT: Use book.return_to_library() method
        # WRITE IMPLEMENTATION HERE
        pass
    
    def display_info(self):
        """
        Display member information.
        
        Returns:
            str: Formatted string with member information
        """
        # TODO: Return formatted string with member information
        # HINT: Include member_id, name, email, and number of books borrowed
        # WRITE IMPLEMENTATION HERE
        pass


# DO NOT MODIFY THESE CLASS VARIABLES
class Library:
    """Class representing a library system."""
    
    book_count = 0  # Class variable to track total books
    member_count = 0  # Class variable to track total members
    
    def __init__(self, name, address):
        """
        Initialize a Library object.
        
        Args:
            name: Name of the library
            address: Address of the library
        """
        # TODO: Initialize all attributes
        # HINT: Create dictionaries to store books and members
        # WRITE IMPLEMENTATION HERE
        pass
    
    @property
    def name(self):
        """Get the library name."""
        # TODO: Return the name
        # WRITE IMPLEMENTATION HERE
        pass
    
    @property
    def address(self):
        """Get the library address."""
        # TODO: Return the address
        # WRITE IMPLEMENTATION HERE
        pass
    
    @staticmethod
    def get_book_count():
        """
        Get the total number of books.
        
        Returns:
            int: Total number of books
        """
        # TODO: Return the book_count class variable
        # WRITE IMPLEMENTATION HERE
        pass
    
    @staticmethod
    def get_member_count():
        """
        Get the total number of members.
        
        Returns:
            int: Total number of members
        """
        # TODO: Return the member_count class variable
        # WRITE IMPLEMENTATION HERE
        pass
    
    def add_book(self, book):
        """
        Add a book to the library.
        
        Args:
            book: Book object to add
            
        Returns:
            bool: True if addition successful, False otherwise
        """
        # TODO: Implement add book logic
        # HINT: Check if book already exists before adding
        # HINT: Increment book_count class variable
        # WRITE IMPLEMENTATION HERE
        pass
    
    def add_member(self, member):
        """
        Add a member to the library.
        
        Args:
            member: Member object to add
            
        Returns:
            bool: True if addition successful, False otherwise
        """
        # TODO: Implement add member logic
        # HINT: Check if member already exists before adding
        # HINT: Increment member_count class variable
        # WRITE IMPLEMENTATION HERE
        pass
    
    def checkout_book(self, book_id, member_id):
        """
        Check out a book to a member.
        
        Args:
            book_id: ID of the book to check out
            member_id: ID of the member checking out the book
            
        Returns:
            bool: True if checkout successful, False otherwise
        """
        # TODO: Implement checkout logic
        # HINT: Check if book and member exist
        # HINT: Use member.borrow_book() method
        # WRITE IMPLEMENTATION HERE
        pass
    
    def return_book(self, book_id, member_id):
        """
        Return a book to the library.
        
        Args:
            book_id: ID of the book to return
            member_id: ID of the member returning the book
            
        Returns:
            bool: True if return successful, False otherwise
        """
        # TODO: Implement return logic
        # HINT: Check if book and member exist
        # HINT: Use member.return_book() method
        # WRITE IMPLEMENTATION HERE
        pass
    
    def get_available_books(self):
        """
        Get all available books.
        
        Returns:
            dict: Dictionary of available books
        """
        # TODO: Return a dictionary of all available books
        # HINT: Use dictionary comprehension
        # WRITE IMPLEMENTATION HERE
        pass
    
    def search_book_by_title(self, title):
        """
        Search for books by title.
        
        Args:
            title: Title to search for
            
        Returns:
            dict: Dictionary of matching books
        """
        # Check for None
        if title is None:
            raise ValueError("Search title cannot be None")
            
        # TODO: Return a dictionary of books with matching titles
        # HINT: Use dictionary comprehension and case-insensitive search
        # WRITE IMPLEMENTATION HERE
        pass
    
    def search_book_by_author(self, author):
        """
        Search for books by author.
        
        Args:
            author: Author to search for
            
        Returns:
            dict: Dictionary of matching books
        """
        # Check for None
        if author is None:
            raise ValueError("Search author cannot be None")
            
        # TODO: Return a dictionary of books with matching authors
        # HINT: Use the partial word matching for author search
        # WRITE IMPLEMENTATION HERE
        pass
    
    def get_book(self, book_id):
        """
        Get a book by ID.
        
        Args:
            book_id: ID of the book to get
            
        Returns:
            Book: Book object if found, None otherwise
        """
        # TODO: Return the book with the given ID or None if not found
        # WRITE IMPLEMENTATION HERE
        pass
    
    def get_member(self, member_id):
        """
        Get a member by ID.
        
        Args:
            member_id: ID of the member to get
            
        Returns:
            Member: Member object if found, None otherwise
        """
        # TODO: Return the member with the given ID or None if not found
        # WRITE IMPLEMENTATION HERE
        pass
    
    def get_all_books(self):
        """
        Get all books.
        
        Returns:
            dict: Dictionary of all books
        """
        # TODO: Return a copy of the books dictionary
        # WRITE IMPLEMENTATION HERE
        pass
    
    def get_all_members(self):
        """
        Get all members.
        
        Returns:
            dict: Dictionary of all members
        """
        # TODO: Return a copy of the members dictionary
        # WRITE IMPLEMENTATION HERE
        pass


def main():
    """Main function to run the library management system."""
    # TODO: Implement the main function
    # HINT: Create a library and implement a menu-driven interface with the following options:
    # 1. Add New Book
    # 2. Add New Member
    # 3. Checkout Book
    # 4. Return Book
    # 5. Display All Books
    # 6. Display All Members
    # 7. Search for Books
    # 0. Exit
    # WRITE IMPLEMENTATION HERE
    pass


# DO NOT MODIFY THIS CODE
if __name__ == "__main__":
    main()