import pytest
from test.TestUtils import TestUtils
from library_management_system import Book, FictionBook, NonFictionBook, Member, Library
import datetime

class TestFunctional:
    """Test cases for functional requirements of the library system."""
    
    def test_book_functionality(self):
        """Test book creation, properties, checkout and return functionality."""
        try:
            # Test basic book creation and property access
            book = Book("B001", "Test Book", "Test Author", "Fiction", 2020, True)
            assert book.book_id == "B001"
            assert book.title == "Test Book"
            assert book.author == "Test Author"
            assert book.genre == "Fiction"
            assert book.publication_year == 2020
            assert book.is_available == True
            
            # Test checkout
            assert book.checkout() == True
            assert book.is_available == False
            
            # Test return
            assert book.return_to_library() == True
            assert book.is_available == True
            
            # Test failed checkout
            book.checkout()
            assert book.checkout() == False  # Already checked out
            
            TestUtils.yakshaAssert("test_book_functionality", True, "functional")
        except Exception as e:
            TestUtils.yakshaAssert("test_book_functionality", False, "functional")
            raise e
    
    def test_book_inheritance(self):
        """Test book inheritance for fiction and non-fiction books."""
        try:
            # Test fiction book
            fiction_book = FictionBook("B003", "Fiction", "Author", "Fantasy", 2022, "Novel")
            assert fiction_book.book_id == "B003"
            assert fiction_book.title == "Fiction"
            assert fiction_book.fiction_type == "Novel"
            assert "Novel" in fiction_book.display_info()
            
            # Test non-fiction book
            non_fiction = NonFictionBook("B004", "Science", "Scientist", "Science", 2023, "Physics")
            assert non_fiction.book_id == "B004"
            assert non_fiction.title == "Science"
            assert non_fiction.subject == "Physics"
            assert "Physics" in non_fiction.display_info()
            
            TestUtils.yakshaAssert("test_book_inheritance", True, "functional")
        except Exception as e:
            TestUtils.yakshaAssert("test_book_inheritance", False, "functional")
            raise e
    
    def test_member_functionality(self):
        """Test member creation, properties, and book borrowing/returning."""
        try:
            # Test member creation
            member = Member("M001", "Test Member", "test@example.com")
            assert member.member_id == "M001"
            assert member.name == "Test Member"
            assert member.email == "test@example.com"
            assert len(member.books_borrowed) == 0
            
            # Test borrow and return
            book = Book("B005", "Borrow Test", "Author", "Fiction", 2021, True)
            result = member.borrow_book(book)
            assert result == True
            assert book.is_available == False
            assert book.book_id in member.books_borrowed
            
            result = member.return_book(book)
            assert result == True
            assert book.is_available == True
            assert book.book_id not in member.books_borrowed
            
            TestUtils.yakshaAssert("test_member_functionality", True, "functional")
        except Exception as e:
            TestUtils.yakshaAssert("test_member_functionality", False, "functional")
            raise e
    
    def test_library_creation_and_adding(self):
        """Test library creation, properties, and adding books and members."""
        try:
            # Test library creation
            library = Library("Test Library", "123 Test St")
            assert library.name == "Test Library"
            assert library.address == "123 Test St"
            
            # Test adding books
            initial_book_count = Library.book_count
            book1 = Book("B006", "Book 1", "Author 1", "Fiction", 2020, True)
            book2 = Book("B007", "Book 2", "Author 2", "Science", 2021, True)
            
            assert library.add_book(book1) == True
            assert library.add_book(book2) == True
            assert Library.book_count == initial_book_count + 2
            assert library.add_book(book1) == False  # Test duplicate addition
            assert library.get_book("B006") == book1
            assert library.get_book("B007") == book2
            
            # Test adding members
            initial_member_count = Library.member_count
            member1 = Member("M003", "Member 1", "member1@example.com")
            member2 = Member("M004", "Member 2", "member2@example.com")
            
            assert library.add_member(member1) == True
            assert library.add_member(member2) == True
            assert Library.member_count == initial_member_count + 2
            assert library.add_member(member1) == False  # Test duplicate addition
            assert library.get_member("M003") == member1
            assert library.get_member("M004") == member2
            
            TestUtils.yakshaAssert("test_library_creation_and_adding", True, "functional")
        except Exception as e:
            TestUtils.yakshaAssert("test_library_creation_and_adding", False, "functional")
            raise e
    
    def test_library_checkout_return(self):
        """Test library checkout and return process."""
        try:
            library = Library("Checkout Library", "Checkout St")
            book = Book("B008", "Checkout Book", "Author", "Fiction", 2020)
            member = Member("M005", "Member", "member@example.com")
            
            library.add_book(book)
            library.add_member(member)
            
            # Test checkout
            checkout_result = library.checkout_book("B008", "M005")
            assert checkout_result is True
            assert not book.is_available
            assert book.book_id in member.books_borrowed
            
            # Test return
            return_result = library.return_book("B008", "M005")
            assert return_result is True
            assert book.is_available
            assert book.book_id not in member.books_borrowed
            
            TestUtils.yakshaAssert("test_library_checkout_return", True, "functional")
        except Exception as e:
            TestUtils.yakshaAssert("test_library_checkout_return", False, "functional")
            raise e
    
    def test_library_search_functions(self):
        """Test library search and filter functions."""
        try:
            library = Library("Search Library", "Search St")
            
            # Add books for search testing
            books = [
                Book("B009", "Python Programming", "John Smith", "Programming", 2020),
                Book("B010", "Advanced Python", "Jane Doe", "Programming", 2021, False),
                Book("B011", "Java Basics", "John Smith", "Programming", 2022),
                Book("B012", "Database Systems", "Alice Johnson", "Technology", 2019)
            ]
            
            for book in books:
                library.add_book(book)
            
            # Test search by title
            results = library.search_book_by_title("python")
            assert len(results) == 2
            assert "B009" in results
            assert "B010" in results
            
            # Test search by author
            results = library.search_book_by_author("john")
            assert len(results) == 2
            assert "B009" in results
            assert "B011" in results
            
            # Test available books
            results = library.get_available_books()
            assert len(results) == 3
            assert "B010" not in results
            
            TestUtils.yakshaAssert("test_library_search_functions", True, "functional")
        except Exception as e:
            TestUtils.yakshaAssert("test_library_search_functions", False, "functional")
            raise e
            
    def test_integrated_library_functions(self):
        """Test integrated library functionality with multiple operations."""
        try:
            library = Library("Integrated Library", "Integration St")
            
            # Test adding different book types
            fiction = FictionBook("B101", "Adventure Story", "Famous Author", "Fiction", 2018, "Adventure")
            non_fiction = NonFictionBook("B102", "History of Science", "Scholar", "Non-Fiction", 2019, "History")
            
            library.add_book(fiction)
            library.add_book(non_fiction)
            
            # Add members
            member1 = Member("M101", "Regular User", "user@example.com")
            member2 = Member("M102", "Frequent User", "frequent@example.com")
            
            library.add_member(member1)
            library.add_member(member2)
            
            # Test checkout and return process
            checkout_result = library.checkout_book("B101", "M101")
            assert checkout_result is True
            assert not fiction.is_available
            
            # Simulate returning book
            return_result = library.return_book("B101", "M101")
            assert return_result is True
            assert fiction.is_available
            
            # Test search functionality after multiple operations
            fiction2 = FictionBook("B103", "Mystery Novel", "Famous Author", "Fiction", 2020, "Mystery")
            library.add_book(fiction2)
            
            results = library.search_book_by_author("famous")
            assert len(results) == 2
            assert "B101" in results
            assert "B103" in results
            
            # Test available books after operations
            available = library.get_available_books()
            assert "B101" in available
            assert "B102" in available
            assert "B103" in available
            
            TestUtils.yakshaAssert("test_integrated_library_functions", True, "functional")
        except Exception as e:
            TestUtils.yakshaAssert("test_integrated_library_functions", False, "functional")
            raise e