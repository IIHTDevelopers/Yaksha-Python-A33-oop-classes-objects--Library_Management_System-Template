import pytest
import datetime
from test.TestUtils import TestUtils
from library_management_system import Book, FictionBook, NonFictionBook, Member, Library

class TestBoundary:
    """Test cases for boundary conditions in the library system."""
    
    def test_system_boundaries(self):
        """Test all boundary conditions for the library management system."""
        try:
            # Book year boundary tests
            current_year = datetime.datetime.now().year
            book1 = Book("B001", "Current Year", "Author", "Fiction", current_year)
            assert book1.publication_year == current_year
            
            book2 = Book("B002", "Ancient Book", "Ancient Author", "History", 1)
            assert book2.publication_year == 1
            
            book3 = Book("B003", "Year Zero", "Author Zero", "Fiction", 0)
            assert book3.publication_year == 0
            
            # Member borrowing limit tests
            member = Member("M001", "Max Borrower", "max@example.com")
            books = [
                Book(f"B00{i}", f"Book {i}", "Author", "Fiction", 2020) 
                for i in range(4, 8)
            ]
            
            # Borrow up to the limit
            assert member.borrow_book(books[0]) == True
            assert member.borrow_book(books[1]) == True
            assert member.borrow_book(books[2]) == True
            
            # Try to exceed limit
            assert member.borrow_book(books[3]) == False
            
            # Return and borrow again
            assert member.return_book(books[1]) == True
            assert member.borrow_book(books[3]) == True
            
            # Test books_borrowed list immutability
            predefined_books = ["B101", "B102"]
            member2 = Member("M101", "Pre Member", "pre@example.com", predefined_books)
            assert member2.books_borrowed == predefined_books
            assert member2.books_borrowed is not predefined_books  # Should be a copy
            
            # Test modifying the returned list doesn't affect original
            borrowed_copy = member2.books_borrowed
            borrowed_copy.append("B103")
            assert "B103" not in member2.books_borrowed
            
            # Empty library tests
            library = Library("Empty Library", "Empty St")
            assert len(library.get_all_books()) == 0
            assert len(library.get_available_books()) == 0
            assert library.search_book_by_title("any") == {}
            assert library.search_book_by_author("any") == {}
            assert library.get_book("B001") is None
            assert len(library.get_all_members()) == 0
            assert library.get_member("M001") is None
            
            # Library checkout boundary tests
            test_library = Library("Test Library", "Test St")
            book = Book("B001", "Test Book", "Author", "Fiction", 2020)
            member = Member("M001", "Test Member", "test@example.com")
            
            test_library.add_book(book)
            test_library.add_member(member)
            
            # Test various input combinations
            assert test_library.checkout_book("INVALID", "M001") is False
            assert test_library.checkout_book("B001", "INVALID") is False
            assert test_library.checkout_book("INVALID", "INVALID") is False
            
            # Valid checkout and repeat attempt
            assert test_library.checkout_book("B001", "M001") is True
            assert test_library.checkout_book("B001", "M001") is False  # Already checked out
            
            TestUtils.yakshaAssert("test_system_boundaries", True, "boundary")
        except Exception as e:
            TestUtils.yakshaAssert("test_system_boundaries", False, "boundary")
            raise e