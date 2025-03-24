import pytest
import datetime
from test.TestUtils import TestUtils
from library_management_system import Book, FictionBook, NonFictionBook, Member, Library

class TestExceptional:
    """Test cases for exceptional conditions in the library system."""
    
    def test_exception_handling(self):
        """Test all exception handling across the library management system."""
        try:
            # Book validation exceptions
            future_year = datetime.datetime.now().year + 10
            try:
                Book("B001", "Future Book", "Author", "Fiction", future_year)
                assert False, "Future publication year should be rejected"
            except ValueError:
                pass  # Expected behavior
                
            try:
                Book("B002", "String Year", "Author", "Fiction", "2023")
                assert False, "Non-integer publication year should be rejected"
            except ValueError:
                pass  # Expected behavior
            
            # Member validation exceptions
            for invalid_email in ["invalidemail.com", "invalid@"]:
                try:
                    Member("M001", "Invalid Email", invalid_email)
                    assert False, f"Invalid email '{invalid_email}' should be rejected"
                except ValueError:
                    pass  # Expected behavior
                
            # Library search validation
            library = Library("Search Library", "Search St")
            
            try:
                library.search_book_by_title(None)
                assert False, "Search with None title should be rejected"
            except ValueError:
                pass  # Expected behavior
                
            try:
                library.search_book_by_author(None)
                assert False, "Search with None author should be rejected"
            except ValueError:
                pass  # Expected behavior
                
            # Empty string searches (should not raise exceptions)
            result = library.search_book_by_title("")
            assert result == {}, "Search with empty title should return empty dict"
            
            result = library.search_book_by_author("")
            assert result == {}, "Search with empty author should return empty dict"
            
            # Book checkout operation exceptions
            checked_out_book = Book("B001", "Unavailable Book", "Author", "Fiction", 2020, False)
            member = Member("M001", "Test Member", "test@example.com")
            
            result = member.borrow_book(checked_out_book)
            assert result == False, "Borrowing unavailable book should fail"
            
            # Exceed borrowing limit
            books = [Book(f"B{i}", f"Book {i}", "Author", "Fiction", 2020) for i in range(2, 6)]
            
            member.borrow_book(books[0])
            member.borrow_book(books[1])
            member.borrow_book(books[2])
            
            result = member.borrow_book(books[3])
            assert result == False, "Exceeding borrowing limit should fail"
            
            # Library checkout/return exceptions
            lib = Library("Test Library", "Test St")
            
            # Missing book during return
            book = Book("B101", "Test Book", "Author", "Fiction", 2020)
            member2 = Member("M101", "Test Member", "test@example.com")
            
            lib.add_book(book)
            lib.add_member(member2)
            
            # Check out the book
            assert lib.checkout_book("B101", "M101") is True
            
            # Try to return with missing book ID
            assert lib.return_book("INVALID", "M101") is False
            
            # Library checkout exceptions
            new_library = Library("Operations Library", "Operations St")
            
            # Checkout with missing book
            result = new_library.checkout_book("NONEXISTENT", "M001")
            assert result is False, "Checkout with non-existent book should return False"
            
            # Checkout with missing member
            book2 = Book("B011", "Exists", "Author", "Fiction", 2020)
            new_library.add_book(book2)
            
            result = new_library.checkout_book("B011", "NONEXISTENT")
            assert result is False, "Checkout with non-existent member should return False"
            
            # Checkout with book already checked out
            member3 = Member("M007", "Exists", "exists@example.com")
            new_library.add_member(member3)
            
            # Check out the book
            new_library.checkout_book("B011", "M007")
            
            # Try to check out again
            result = new_library.checkout_book("B011", "M007")
            assert result is False, "Checkout of already checked out book should return False"
                
            TestUtils.yakshaAssert("test_exception_handling", True, "exceptional")
        except Exception as e:
            TestUtils.yakshaAssert("test_exception_handling", False, "exceptional")
            raise e