"""
Functional tests for the Library Management System.
"""

import pytest
import datetime
import importlib
import os
from test.TestUtils import TestUtils

# Utility functions for resilient testing
def check_file_exists(filename):
    """Check if a file exists in the current directory."""
    return os.path.exists(filename)

def safely_import_module(module_name):
    """Safely import a module, returning None if import fails."""
    try:
        return importlib.import_module(module_name)
    except ImportError:
        return None

def check_class_exists(module, class_name):
    """Check if a class exists in a module."""
    return hasattr(module, class_name) and isinstance(getattr(module, class_name), type)

def check_function_exists(obj, function_name):
    """Check if a function/method exists in an object or class."""
    return hasattr(obj, function_name) and callable(getattr(obj, function_name))

def safely_create_instance(module, class_name, *args, **kwargs):
    """Safely create an instance of a class, handling missing classes gracefully."""
    if module is None or not check_class_exists(module, class_name):
        return None
    try:
        cls = getattr(module, class_name)
        return cls(*args, **kwargs)
    except (AttributeError, NameError, ImportError, SyntaxError, TypeError):
        # These are "broken implementation" errors - return None
        return None
    except Exception:
        # All other exceptions should be re-raised as they indicate proper validation
        raise

def safely_call_method(obj, method_name, *args, **kwargs):
    """Safely call a method, handling missing methods gracefully but allowing proper exceptions."""
    if obj is None or not check_function_exists(obj, method_name):
        return None
    try:
        result = getattr(obj, method_name)(*args, **kwargs)
        return result if result is not None else True
    except (AttributeError, NameError, ImportError, SyntaxError):
        # These are "broken implementation" errors - return None
        return None
    except Exception:
        # All other exceptions should be re-raised
        raise

def safely_get_attribute(obj, attr_name):
    """Safely get an attribute, returning None if it doesn't exist."""
    if obj is None:
        return None
    try:
        return getattr(obj, attr_name)
    except (AttributeError, NameError):
        return None

class TestFunctional:
    """Test class for functional tests of the Library Management System."""
    
    def setup_method(self):
        """Setup test data before each test method."""
        # Import the module under test
        self.module_obj = safely_import_module("skeleton")
        
        # Test object for assertions
        self.test_obj = TestUtils()
    
    def test_book_functionality(self):
        """Test book creation, properties, checkout and return functionality."""
        # Check if module exists
        if self.module_obj is None:
            self.test_obj.yakshaAssert("test_book_functionality", False, "functional")
            pytest.fail("Could not import skeleton module.")
            return
        
        # Check Book class exists
        if not check_class_exists(self.module_obj, "Book"):
            self.test_obj.yakshaAssert("test_book_functionality", False, "functional")
            pytest.fail("Book class not found in module.")
            return
        
        # Create a list to collect errors
        errors = []
        
        try:
            # Test basic book creation and property access
            book = safely_create_instance(self.module_obj, "Book", "B001", "Test Book", "Test Author", "Fiction", 2020, True)
            
            if book is None:
                errors.append("Could not create Book instance - constructor failed")
            else:
                # Test book properties
                book_id = safely_get_attribute(book, "book_id")
                if book_id is None:
                    errors.append("Book.book_id property not found")
                elif book_id != "B001":
                    errors.append(f"Book.book_id returned {book_id}, expected 'B001'")
                
                title = safely_get_attribute(book, "title")
                if title is None:
                    errors.append("Book.title property not found")
                elif title != "Test Book":
                    errors.append(f"Book.title returned {title}, expected 'Test Book'")
                
                author = safely_get_attribute(book, "author")
                if author is None:
                    errors.append("Book.author property not found")
                elif author != "Test Author":
                    errors.append(f"Book.author returned {author}, expected 'Test Author'")
                
                genre = safely_get_attribute(book, "genre")
                if genre is None:
                    errors.append("Book.genre property not found")
                elif genre != "Fiction":
                    errors.append(f"Book.genre returned {genre}, expected 'Fiction'")
                
                pub_year = safely_get_attribute(book, "publication_year")
                if pub_year is None:
                    errors.append("Book.publication_year property not found")
                elif pub_year != 2020:
                    errors.append(f"Book.publication_year returned {pub_year}, expected 2020")
                
                is_available = safely_get_attribute(book, "is_available")
                if is_available is None:
                    errors.append("Book.is_available property not found")
                elif is_available != True:
                    errors.append(f"Book.is_available returned {is_available}, expected True")
                
                # Test checkout
                checkout_result = safely_call_method(book, "checkout")
                if checkout_result is None:
                    errors.append("Book.checkout method not implemented or failed")
                elif checkout_result != True:
                    errors.append(f"Book.checkout returned {checkout_result}, expected True")
                else:
                    # Check is_available was updated
                    is_available = safely_get_attribute(book, "is_available")
                    if is_available is None:
                        errors.append("Book.is_available property not found after checkout")
                    elif is_available != False:
                        errors.append(f"Book.is_available after checkout returned {is_available}, expected False")
                
                # Test return
                return_result = safely_call_method(book, "return_to_library")
                if return_result is None:
                    errors.append("Book.return_to_library method not implemented or failed")
                elif return_result != True:
                    errors.append(f"Book.return_to_library returned {return_result}, expected True")
                else:
                    # Check is_available was updated
                    is_available = safely_get_attribute(book, "is_available")
                    if is_available is None:
                        errors.append("Book.is_available property not found after return")
                    elif is_available != True:
                        errors.append(f"Book.is_available after return returned {is_available}, expected True")
                
                # Test failed checkout
                if checkout_result:
                    # Checkout book again
                    safely_call_method(book, "checkout")
                    second_checkout = safely_call_method(book, "checkout")
                    if second_checkout is None:
                        errors.append("Book.checkout method failed on second attempt")
                    elif second_checkout != False:
                        errors.append(f"Book.checkout on already checked out book returned {second_checkout}, expected False")
            
            # Final result checking
            if errors:
                self.test_obj.yakshaAssert("test_book_functionality", False, "functional")
                pytest.fail("\n".join(errors))
            else:
                self.test_obj.yakshaAssert("test_book_functionality", True, "functional")
                
        except Exception as e:
            self.test_obj.yakshaAssert("test_book_functionality", False, "functional")
            pytest.fail(f"Book functionality test failed: {str(e)}")
    
    def test_book_inheritance(self):
        """Test book inheritance for fiction and non-fiction books."""
        # Check if module exists
        if self.module_obj is None:
            self.test_obj.yakshaAssert("test_book_inheritance", False, "functional")
            pytest.fail("Could not import skeleton module.")
            return
        
        # Check required classes exist
        required_classes = ["Book", "FictionBook", "NonFictionBook"]
        missing_classes = []
        for class_name in required_classes:
            if not check_class_exists(self.module_obj, class_name):
                missing_classes.append(class_name)
        
        if missing_classes:
            error_msg = f"Missing required classes: {', '.join(missing_classes)}"
            self.test_obj.yakshaAssert("test_book_inheritance", False, "functional")
            pytest.fail(error_msg)
            return
        
        # Create a list to collect errors
        errors = []
        
        try:
            # Test fiction book
            fiction_book = safely_create_instance(self.module_obj, "FictionBook", 
                                               "B003", "Fiction", "Author", "Fantasy", 2022, "Novel")
            
            if fiction_book is None:
                errors.append("Could not create FictionBook instance - constructor failed")
            else:
                # Test inheritance properties
                book_id = safely_get_attribute(fiction_book, "book_id")
                if book_id is None:
                    errors.append("FictionBook.book_id property not found")
                elif book_id != "B003":
                    errors.append(f"FictionBook.book_id returned {book_id}, expected 'B003'")
                
                title = safely_get_attribute(fiction_book, "title")
                if title is None:
                    errors.append("FictionBook.title property not found")
                elif title != "Fiction":
                    errors.append(f"FictionBook.title returned {title}, expected 'Fiction'")
                
                # Test subclass specific property
                fiction_type = safely_get_attribute(fiction_book, "fiction_type")
                if fiction_type is None:
                    errors.append("FictionBook.fiction_type property not found")
                elif fiction_type != "Novel":
                    errors.append(f"FictionBook.fiction_type returned {fiction_type}, expected 'Novel'")
                
                # Test display_info method
                display_info = safely_call_method(fiction_book, "display_info")
                if display_info is None:
                    errors.append("FictionBook.display_info method not implemented or failed")
                elif not isinstance(display_info, str):
                    errors.append(f"FictionBook.display_info returned {type(display_info)}, expected string")
                elif "Novel" not in display_info:
                    errors.append(f"FictionBook.display_info should include 'Novel', got '{display_info}'")
            
            # Test non-fiction book
            non_fiction = safely_create_instance(self.module_obj, "NonFictionBook", 
                                              "B004", "Science", "Scientist", "Science", 2023, "Physics")
            
            if non_fiction is None:
                errors.append("Could not create NonFictionBook instance - constructor failed")
            else:
                # Test inheritance properties
                book_id = safely_get_attribute(non_fiction, "book_id")
                if book_id is None:
                    errors.append("NonFictionBook.book_id property not found")
                elif book_id != "B004":
                    errors.append(f"NonFictionBook.book_id returned {book_id}, expected 'B004'")
                
                title = safely_get_attribute(non_fiction, "title")
                if title is None:
                    errors.append("NonFictionBook.title property not found")
                elif title != "Science":
                    errors.append(f"NonFictionBook.title returned {title}, expected 'Science'")
                
                # Test subclass specific property
                subject = safely_get_attribute(non_fiction, "subject")
                if subject is None:
                    errors.append("NonFictionBook.subject property not found")
                elif subject != "Physics":
                    errors.append(f"NonFictionBook.subject returned {subject}, expected 'Physics'")
                
                # Test display_info method
                display_info = safely_call_method(non_fiction, "display_info")
                if display_info is None:
                    errors.append("NonFictionBook.display_info method not implemented or failed")
                elif not isinstance(display_info, str):
                    errors.append(f"NonFictionBook.display_info returned {type(display_info)}, expected string")
                elif "Physics" not in display_info:
                    errors.append(f"NonFictionBook.display_info should include 'Physics', got '{display_info}'")
            
            # Final result checking
            if errors:
                self.test_obj.yakshaAssert("test_book_inheritance", False, "functional")
                pytest.fail("\n".join(errors))
            else:
                self.test_obj.yakshaAssert("test_book_inheritance", True, "functional")
                
        except Exception as e:
            self.test_obj.yakshaAssert("test_book_inheritance", False, "functional")
            pytest.fail(f"Book inheritance test failed: {str(e)}")
    
    def test_member_functionality(self):
        """Test member creation, properties, and book borrowing/returning."""
        # Check if module exists
        if self.module_obj is None:
            self.test_obj.yakshaAssert("test_member_functionality", False, "functional")
            pytest.fail("Could not import skeleton module.")
            return
        
        # Check required classes exist
        required_classes = ["Book", "Member"]
        missing_classes = []
        for class_name in required_classes:
            if not check_class_exists(self.module_obj, class_name):
                missing_classes.append(class_name)
        
        if missing_classes:
            error_msg = f"Missing required classes: {', '.join(missing_classes)}"
            self.test_obj.yakshaAssert("test_member_functionality", False, "functional")
            pytest.fail(error_msg)
            return
        
        # Create a list to collect errors
        errors = []
        
        try:
            # Test member creation
            member = safely_create_instance(self.module_obj, "Member", 
                                         "M001", "Test Member", "test@example.com")
            
            if member is None:
                errors.append("Could not create Member instance - constructor failed")
            else:
                # Test member properties
                member_id = safely_get_attribute(member, "member_id")
                if member_id is None:
                    errors.append("Member.member_id property not found")
                elif member_id != "M001":
                    errors.append(f"Member.member_id returned {member_id}, expected 'M001'")
                
                name = safely_get_attribute(member, "name")
                if name is None:
                    errors.append("Member.name property not found")
                elif name != "Test Member":
                    errors.append(f"Member.name returned {name}, expected 'Test Member'")
                
                email = safely_get_attribute(member, "email")
                if email is None:
                    errors.append("Member.email property not found")
                elif email != "test@example.com":
                    errors.append(f"Member.email returned {email}, expected 'test@example.com'")
                
                books_borrowed = safely_get_attribute(member, "books_borrowed")
                if books_borrowed is None:
                    errors.append("Member.books_borrowed property not found")
                elif not isinstance(books_borrowed, list):
                    errors.append(f"Member.books_borrowed returned {type(books_borrowed)}, expected list")
                elif len(books_borrowed) != 0:
                    errors.append(f"New member books_borrowed should be empty, got {books_borrowed}")
                
                # Test borrow and return
                book = safely_create_instance(self.module_obj, "Book", 
                                           "B005", "Borrow Test", "Author", "Fiction", 2021, True)
                
                if book is None:
                    errors.append("Could not create Book instance for borrowing test")
                else:
                    # Test borrow_book method
                    result = safely_call_method(member, "borrow_book", book)
                    if result is None:
                        errors.append("Member.borrow_book method not implemented or failed")
                    elif result != True:
                        errors.append(f"Member.borrow_book returned {result}, expected True")
                    else:
                        # Check book was marked unavailable
                        is_available = safely_get_attribute(book, "is_available")
                        if is_available is None:
                            errors.append("Book.is_available property not found after borrowing")
                        elif is_available != False:
                            errors.append(f"Book.is_available after borrowing returned {is_available}, expected False")
                        
                        # Check book was added to borrowed list
                        books_borrowed = safely_get_attribute(member, "books_borrowed")
                        if books_borrowed is None:
                            errors.append("Member.books_borrowed property not found after borrowing")
                        elif not isinstance(books_borrowed, list):
                            errors.append(f"Member.books_borrowed after borrowing returned {type(books_borrowed)}, expected list")
                        elif "B005" not in books_borrowed and book.book_id not in books_borrowed:
                            errors.append(f"Book ID not found in Member.books_borrowed after borrowing, got {books_borrowed}")
                    
                    # Test return_book method
                    result = safely_call_method(member, "return_book", book)
                    if result is None:
                        errors.append("Member.return_book method not implemented or failed")
                    elif result != True:
                        errors.append(f"Member.return_book returned {result}, expected True")
                    else:
                        # Check book was marked available
                        is_available = safely_get_attribute(book, "is_available")
                        if is_available is None:
                            errors.append("Book.is_available property not found after returning")
                        elif is_available != True:
                            errors.append(f"Book.is_available after returning returned {is_available}, expected True")
                        
                        # Check book was removed from borrowed list
                        books_borrowed = safely_get_attribute(member, "books_borrowed")
                        if books_borrowed is None:
                            errors.append("Member.books_borrowed property not found after returning")
                        elif not isinstance(books_borrowed, list):
                            errors.append(f"Member.books_borrowed after returning returned {type(books_borrowed)}, expected list")
                        elif "B005" in books_borrowed or book.book_id in books_borrowed:
                            errors.append(f"Book ID still in Member.books_borrowed after returning, got {books_borrowed}")
            
            # Final result checking
            if errors:
                self.test_obj.yakshaAssert("test_member_functionality", False, "functional")
                pytest.fail("\n".join(errors))
            else:
                self.test_obj.yakshaAssert("test_member_functionality", True, "functional")
                
        except Exception as e:
            self.test_obj.yakshaAssert("test_member_functionality", False, "functional")
            pytest.fail(f"Member functionality test failed: {str(e)}")
    
    def test_library_creation_and_adding(self):
        """Test library creation, properties, and adding books and members."""
        # Check if module exists
        if self.module_obj is None:
            self.test_obj.yakshaAssert("test_library_creation_and_adding", False, "functional")
            pytest.fail("Could not import skeleton module.")
            return
        
        # Check required classes exist
        required_classes = ["Library", "Book", "Member"]
        missing_classes = []
        for class_name in required_classes:
            if not check_class_exists(self.module_obj, class_name):
                missing_classes.append(class_name)
        
        if missing_classes:
            error_msg = f"Missing required classes: {', '.join(missing_classes)}"
            self.test_obj.yakshaAssert("test_library_creation_and_adding", False, "functional")
            pytest.fail(error_msg)
            return
        
        # Create a list to collect errors
        errors = []
        
        try:
            # Test library creation
            library = safely_create_instance(self.module_obj, "Library", 
                                          "Test Library", "123 Test St")
            
            if library is None:
                errors.append("Could not create Library instance - constructor failed")
            else:
                # Test library properties
                name = safely_get_attribute(library, "name")
                if name is None:
                    errors.append("Library.name property not found")
                elif name != "Test Library":
                    errors.append(f"Library.name returned {name}, expected 'Test Library'")
                
                address = safely_get_attribute(library, "address")
                if address is None:
                    errors.append("Library.address property not found")
                elif address != "123 Test St":
                    errors.append(f"Library.address returned {address}, expected '123 Test St'")
                
                # Get initial book count
                Library = getattr(self.module_obj, "Library")
                initial_book_count = safely_get_attribute(Library, "book_count")
                if initial_book_count is None:
                    errors.append("Library.book_count static property not found")
                elif not isinstance(initial_book_count, int):
                    errors.append(f"Library.book_count returned {type(initial_book_count)}, expected int")
                
                # Test adding books
                book1 = safely_create_instance(self.module_obj, "Book", 
                                            "B006", "Book 1", "Author 1", "Fiction", 2020, True)
                book2 = safely_create_instance(self.module_obj, "Book", 
                                            "B007", "Book 2", "Author 2", "Science", 2021, True)
                
                if book1 is None or book2 is None:
                    if book1 is None:
                        errors.append("Could not create first Book instance for library test")
                    if book2 is None:
                        errors.append("Could not create second Book instance for library test")
                else:
                    # Test add_book method
                    result1 = safely_call_method(library, "add_book", book1)
                    if result1 is None:
                        errors.append("Library.add_book method not implemented or failed")
                    elif result1 != True:
                        errors.append(f"Library.add_book returned {result1}, expected True")
                    
                    result2 = safely_call_method(library, "add_book", book2)
                    if result2 is None:
                        errors.append("Library.add_book method failed on second book")
                    elif result2 != True:
                        errors.append(f"Library.add_book for second book returned {result2}, expected True")
                    
                    # Check book count increased
                    if initial_book_count is not None:
                        new_book_count = safely_get_attribute(Library, "book_count")
                        if new_book_count is None:
                            errors.append("Library.book_count static property not found after adding books")
                        elif new_book_count != initial_book_count + 2:
                            errors.append(f"Library.book_count after adding two books returned {new_book_count}, expected {initial_book_count + 2}")
                    
                    # Test duplicate addition
                    dup_result = safely_call_method(library, "add_book", book1)
                    if dup_result is None:
                        errors.append("Library.add_book method failed on duplicate book")
                    elif dup_result != False:
                        errors.append(f"Library.add_book for duplicate book returned {dup_result}, expected False")
                    
                    # Test get_book method
                    book_result1 = safely_call_method(library, "get_book", "B006")
                    if book_result1 is None:
                        errors.append("Library.get_book method not implemented or failed")
                    elif book_result1 != book1:
                        errors.append("Library.get_book did not return the correct book instance")
                    
                    book_result2 = safely_call_method(library, "get_book", "B007")
                    if book_result2 is None:
                        errors.append("Library.get_book method failed for second book")
                    elif book_result2 != book2:
                        errors.append("Library.get_book did not return the correct second book instance")
                
                # Get initial member count
                initial_member_count = safely_get_attribute(Library, "member_count")
                if initial_member_count is None:
                    errors.append("Library.member_count static property not found")
                elif not isinstance(initial_member_count, int):
                    errors.append(f"Library.member_count returned {type(initial_member_count)}, expected int")
                
                # Test adding members
                member1 = safely_create_instance(self.module_obj, "Member", 
                                              "M003", "Member 1", "member1@example.com")
                member2 = safely_create_instance(self.module_obj, "Member", 
                                              "M004", "Member 2", "member2@example.com")
                
                if member1 is None or member2 is None:
                    if member1 is None:
                        errors.append("Could not create first Member instance for library test")
                    if member2 is None:
                        errors.append("Could not create second Member instance for library test")
                else:
                    # Test add_member method
                    result1 = safely_call_method(library, "add_member", member1)
                    if result1 is None:
                        errors.append("Library.add_member method not implemented or failed")
                    elif result1 != True:
                        errors.append(f"Library.add_member returned {result1}, expected True")
                    
                    result2 = safely_call_method(library, "add_member", member2)
                    if result2 is None:
                        errors.append("Library.add_member method failed on second member")
                    elif result2 != True:
                        errors.append(f"Library.add_member for second member returned {result2}, expected True")
                    
                    # Check member count increased
                    if initial_member_count is not None:
                        new_member_count = safely_get_attribute(Library, "member_count")
                        if new_member_count is None:
                            errors.append("Library.member_count static property not found after adding members")
                        elif new_member_count != initial_member_count + 2:
                            errors.append(f"Library.member_count after adding two members returned {new_member_count}, expected {initial_member_count + 2}")
                    
                    # Test duplicate addition
                    dup_result = safely_call_method(library, "add_member", member1)
                    if dup_result is None:
                        errors.append("Library.add_member method failed on duplicate member")
                    elif dup_result != False:
                        errors.append(f"Library.add_member for duplicate member returned {dup_result}, expected False")
                    
                    # Test get_member method
                    member_result1 = safely_call_method(library, "get_member", "M003")
                    if member_result1 is None:
                        errors.append("Library.get_member method not implemented or failed")
                    elif member_result1 != member1:
                        errors.append("Library.get_member did not return the correct member instance")
                    
                    member_result2 = safely_call_method(library, "get_member", "M004")
                    if member_result2 is None:
                        errors.append("Library.get_member method failed for second member")
                    elif member_result2 != member2:
                        errors.append("Library.get_member did not return the correct second member instance")
            
            # Final result checking
            if errors:
                self.test_obj.yakshaAssert("test_library_creation_and_adding", False, "functional")
                pytest.fail("\n".join(errors))
            else:
                self.test_obj.yakshaAssert("test_library_creation_and_adding", True, "functional")
                
        except Exception as e:
            self.test_obj.yakshaAssert("test_library_creation_and_adding", False, "functional")
            pytest.fail(f"Library creation and adding test failed: {str(e)}")
    
    def test_library_checkout_return(self):
        """Test library checkout and return process."""
        # Check if module exists
        if self.module_obj is None:
            self.test_obj.yakshaAssert("test_library_checkout_return", False, "functional")
            pytest.fail("Could not import skeleton module.")
            return
        
        # Check required classes exist
        required_classes = ["Library", "Book", "Member"]
        missing_classes = []
        for class_name in required_classes:
            if not check_class_exists(self.module_obj, class_name):
                missing_classes.append(class_name)
        
        if missing_classes:
            error_msg = f"Missing required classes: {', '.join(missing_classes)}"
            self.test_obj.yakshaAssert("test_library_checkout_return", False, "functional")
            pytest.fail(error_msg)
            return
        
        # Create a list to collect errors
        errors = []
        
        try:
            # Create library, book, and member
            library = safely_create_instance(self.module_obj, "Library", 
                                          "Checkout Library", "Checkout St")
            book = safely_create_instance(self.module_obj, "Book", 
                                       "B008", "Checkout Book", "Author", "Fiction", 2020)
            member = safely_create_instance(self.module_obj, "Member", 
                                         "M005", "Member", "member@example.com")
            
            if library is None or book is None or member is None:
                if library is None:
                    errors.append("Could not create Library instance for checkout test")
                if book is None:
                    errors.append("Could not create Book instance for checkout test")
                if member is None:
                    errors.append("Could not create Member instance for checkout test")
            else:
                # Add book and member to library
                add_book_result = safely_call_method(library, "add_book", book)
                add_member_result = safely_call_method(library, "add_member", member)
                
                if add_book_result is None or add_member_result is None:
                    if add_book_result is None:
                        errors.append("Library.add_book method not implemented or failed in checkout test")
                    if add_member_result is None:
                        errors.append("Library.add_member method not implemented or failed in checkout test")
                else:
                    # Test checkout
                    checkout_result = safely_call_method(library, "checkout_book", "B008", "M005")
                    # Test checkout
                    checkout_result = safely_call_method(library, "checkout_book", "B008", "M005")
                    if checkout_result is None:
                        errors.append("Library.checkout_book method not implemented or failed")
                    elif checkout_result != True:
                        errors.append(f"Library.checkout_book returned {checkout_result}, expected True")
                    else:
                        # Verify book is now unavailable
                        is_available = safely_get_attribute(book, "is_available")
                        if is_available is None:
                            errors.append("Book.is_available property not found after checkout")
                        elif is_available != False:
                            errors.append(f"Book.is_available after checkout returned {is_available}, expected False")
                        
                        # Verify book is in member's borrowed list
                        books_borrowed = safely_get_attribute(member, "books_borrowed")
                        if books_borrowed is None:
                            errors.append("Member.books_borrowed property not found after checkout")
                        elif not isinstance(books_borrowed, list):
                            errors.append(f"Member.books_borrowed after checkout returned {type(books_borrowed)}, expected list")
                        elif "B008" not in books_borrowed and book.book_id not in books_borrowed:
                            errors.append(f"Book ID not found in Member.books_borrowed after checkout, got {books_borrowed}")
                        
                        # Test return
                        return_result = safely_call_method(library, "return_book", "B008", "M005")
                        if return_result is None:
                            errors.append("Library.return_book method not implemented or failed")
                        elif return_result != True:
                            errors.append(f"Library.return_book returned {return_result}, expected True")
                        else:
                            # Verify book is now available
                            is_available = safely_get_attribute(book, "is_available")
                            if is_available is None:
                                errors.append("Book.is_available property not found after return")
                            elif is_available != True:
                                errors.append(f"Book.is_available after return returned {is_available}, expected True")
                            
                            # Verify book is not in member's borrowed list
                            books_borrowed = safely_get_attribute(member, "books_borrowed")
                            if books_borrowed is None:
                                errors.append("Member.books_borrowed property not found after return")
                            elif not isinstance(books_borrowed, list):
                                errors.append(f"Member.books_borrowed after return returned {type(books_borrowed)}, expected list")
                            elif "B008" in books_borrowed or book.book_id in books_borrowed:
                                errors.append(f"Book ID still in Member.books_borrowed after return, got {books_borrowed}")
            
            # Final result checking
            if errors:
                self.test_obj.yakshaAssert("test_library_checkout_return", False, "functional")
                pytest.fail("\n".join(errors))
            else:
                self.test_obj.yakshaAssert("test_library_checkout_return", True, "functional")
                
        except Exception as e:
            self.test_obj.yakshaAssert("test_library_checkout_return", False, "functional")
            pytest.fail(f"Library checkout and return test failed: {str(e)}")
    
    def test_library_search_functions(self):
        """Test library search and filter functions."""
        # Check if module exists
        if self.module_obj is None:
            self.test_obj.yakshaAssert("test_library_search_functions", False, "functional")
            pytest.fail("Could not import skeleton module.")
            return
        
        # Check Library class exists
        if not check_class_exists(self.module_obj, "Library"):
            self.test_obj.yakshaAssert("test_library_search_functions", False, "functional")
            pytest.fail("Library class not found in module.")
            return
        
        # Create a list to collect errors
        errors = []
        
        try:
            # Create library and books for search
            library = safely_create_instance(self.module_obj, "Library", 
                                          "Search Library", "Search St")
            
            if library is None:
                errors.append("Could not create Library instance for search test")
            else:
                # Create book instances
                book_data = [
                    ("B009", "Python Programming", "John Smith", "Programming", 2020, True),
                    ("B010", "Advanced Python", "Jane Doe", "Programming", 2021, False),
                    ("B011", "Java Basics", "John Smith", "Programming",2022, True),
                    ("B012", "Database Systems", "Alice Johnson", "Technology", 2019, True)
                ]
                
                books = []
                for book_args in book_data:
                    book = safely_create_instance(self.module_obj, "Book", *book_args)
                    if book is not None:
                        books.append(book)
                        safely_call_method(library, "add_book", book)
                
                if len(books) < 4:
                    errors.append(f"Could not create all books for search test, created {len(books)} out of 4")
                elif not check_function_exists(library, "search_book_by_title") or not check_function_exists(library, "search_book_by_author"):
                    if not check_function_exists(library, "search_book_by_title"):
                        errors.append("Library.search_book_by_title method not found")
                    if not check_function_exists(library, "search_book_by_author"):
                        errors.append("Library.search_book_by_author method not found")
                else:
                    # Test search by title
                    title_results = safely_call_method(library, "search_book_by_title", "python")
                    if title_results is None:
                        errors.append("Library.search_book_by_title method failed")
                    elif not isinstance(title_results, dict):
                        errors.append(f"Library.search_book_by_title returned {type(title_results)}, expected dict")
                    elif len(title_results) != 2:
                        errors.append(f"Library.search_book_by_title('python') returned {len(title_results)} results, expected 2")
                    elif "B009" not in title_results or "B010" not in title_results:
                        errors.append(f"Library.search_book_by_title('python') missing expected results, got {list(title_results.keys())}")
                    
                    # Test search by author
                    author_results = safely_call_method(library, "search_book_by_author", "john")
                    if author_results is None:
                        errors.append("Library.search_book_by_author method failed")
                    elif not isinstance(author_results, dict):
                        errors.append(f"Library.search_book_by_author returned {type(author_results)}, expected dict")
                    elif len(author_results) != 2:
                        errors.append(f"Library.search_book_by_author('john') returned {len(author_results)} results, expected 2")
                    elif "B009" not in author_results or "B011" not in author_results:
                        errors.append(f"Library.search_book_by_author('john') missing expected results, got {list(author_results.keys())}")
                    
                    # Test available books
                    available_results = safely_call_method(library, "get_available_books")
                    if available_results is None:
                        errors.append("Library.get_available_books method failed")
                    elif not isinstance(available_results, dict):
                        errors.append(f"Library.get_available_books returned {type(available_results)}, expected dict")
                    elif len(available_results) != 3:
                        errors.append(f"Library.get_available_books returned {len(available_results)} results, expected 3")
                    elif "B010" in available_results:
                        errors.append(f"Library.get_available_books should not include unavailable book B010")
            
            # Final result checking
            if errors:
                self.test_obj.yakshaAssert("test_library_search_functions", False, "functional")
                pytest.fail("\n".join(errors))
            else:
                self.test_obj.yakshaAssert("test_library_search_functions", True, "functional")
                
        except Exception as e:
            self.test_obj.yakshaAssert("test_library_search_functions", False, "functional")
            pytest.fail(f"Library search functions test failed: {str(e)}")
    
    def test_integrated_library_functions(self):
        """Test integrated library functionality with multiple operations."""
        # Check if module exists
        if self.module_obj is None:
            self.test_obj.yakshaAssert("test_integrated_library_functions", False, "functional")
            pytest.fail("Could not import skeleton module.")
            return
        
        # Check required classes exist
        required_classes = ["Library", "Book", "FictionBook", "NonFictionBook", "Member"]
        missing_classes = []
        for class_name in required_classes:
            if not check_class_exists(self.module_obj, class_name):
                missing_classes.append(class_name)
        
        if missing_classes:
            error_msg = f"Missing required classes: {', '.join(missing_classes)}"
            self.test_obj.yakshaAssert("test_integrated_library_functions", False, "functional")
            pytest.fail(error_msg)
            return
        
        # Create a list to collect errors
        errors = []
        
        try:
            # Create integrated library system
            library = safely_create_instance(self.module_obj, "Library", 
                                          "Integrated Library", "Integration St")
            
            if library is None:
                errors.append("Could not create Library instance for integrated test")
            else:
                # Add different book types
                fiction = safely_create_instance(self.module_obj, "FictionBook", 
                                             "B101", "Adventure Story", "Famous Author", "Fiction", 2018, "Adventure")
                non_fiction = safely_create_instance(self.module_obj, "NonFictionBook", 
                                                  "B102", "History of Science", "Scholar", "Non-Fiction", 2019, "History")
                
                if fiction is None or non_fiction is None:
                    if fiction is None:
                        errors.append("Could not create FictionBook instance for integrated test")
                    if non_fiction is None:
                        errors.append("Could not create NonFictionBook instance for integrated test")
                else:
                    fiction_add = safely_call_method(library, "add_book", fiction)
                    non_fiction_add = safely_call_method(library, "add_book", non_fiction)
                    
                    if fiction_add is None or non_fiction_add is None:
                        if fiction_add is None:
                            errors.append("Library.add_book method failed for fiction book")
                        if non_fiction_add is None:
                            errors.append("Library.add_book method failed for non-fiction book")
                    else:
                        # Add members
                        member1 = safely_create_instance(self.module_obj, "Member", 
                                                      "M101", "Regular User", "user@example.com")
                        member2 = safely_create_instance(self.module_obj, "Member", 
                                                      "M102", "Frequent User", "frequent@example.com")
                        
                        if member1 is None or member2 is None:
                            if member1 is None:
                                errors.append("Could not create first Member instance for integrated test")
                            if member2 is None:
                                errors.append("Could not create second Member instance for integrated test")
                        else:
                            member1_add = safely_call_method(library, "add_member", member1)
                            member2_add = safely_call_method(library, "add_member", member2)
                            
                            if member1_add is None or member2_add is None:
                                if member1_add is None:
                                    errors.append("Library.add_member method failed for first member")
                                if member2_add is None:
                                    errors.append("Library.add_member method failed for second member")
                            else:
                                # Test checkout and return process
                                checkout_result = safely_call_method(library, "checkout_book", "B101", "M101")
                                if checkout_result is None:
                                    errors.append("Library.checkout_book method failed in integrated test")
                                elif checkout_result != True:
                                    errors.append(f"Library.checkout_book returned {checkout_result}, expected True")
                                else:
                                    # Check book availability after checkout
                                    is_available = safely_get_attribute(fiction, "is_available")
                                    if is_available is None:
                                        errors.append("Book.is_available property not found after integrated checkout")
                                    elif is_available != False:
                                        errors.append(f"Book.is_available after integrated checkout returned {is_available}, expected False")
                                    
                                    # Test returning book
                                    return_result = safely_call_method(library, "return_book", "B101", "M101")
                                    if return_result is None:
                                        errors.append("Library.return_book method failed in integrated test")
                                    elif return_result != True:
                                        errors.append(f"Library.return_book returned {return_result}, expected True")
                                    else:
                                        # Check book availability after return
                                        is_available = safely_get_attribute(fiction, "is_available")
                                        if is_available is None:
                                            errors.append("Book.is_available property not found after integrated return")
                                        elif is_available != True:
                                            errors.append(f"Book.is_available after integrated return returned {is_available}, expected True")
                                        
                                        # Test search after more operations
                                        fiction2 = safely_create_instance(self.module_obj, "FictionBook", 
                                                                      "B103", "Mystery Novel", "Famous Author", "Fiction", 2020, "Mystery")
                                        
                                        if fiction2 is None:
                                            errors.append("Could not create second FictionBook for integrated test")
                                        else:
                                            fiction2_add = safely_call_method(library, "add_book", fiction2)
                                            
                                            if fiction2_add is None:
                                                errors.append("Library.add_book method failed for second fiction book")
                                            else:
                                                # Test author search
                                                author_results = safely_call_method(library, "search_book_by_author", "famous")
                                                if author_results is None:
                                                    errors.append("Library.search_book_by_author method failed in integrated test")
                                                elif not isinstance(author_results, dict):
                                                    errors.append(f"Library.search_book_by_author in integrated test returned {type(author_results)}, expected dict")
                                                elif len(author_results) != 2:
                                                    errors.append(f"Library.search_book_by_author('famous') returned {len(author_results)} results, expected 2")
                                                elif "B101" not in author_results or "B103" not in author_results:
                                                    errors.append(f"Library.search_book_by_author('famous') missing expected results, got {list(author_results.keys())}")
                                                
                                                # Test available books
                                                available_results = safely_call_method(library, "get_available_books")
                                                if available_results is None:
                                                    errors.append("Library.get_available_books method failed in integrated test")
                                                elif not isinstance(available_results, dict):
                                                    errors.append(f"Library.get_available_books in integrated test returned {type(available_results)}, expected dict")
                                                elif "B101" not in available_results or "B102" not in available_results or "B103" not in available_results:
                                                    errors.append(f"Library.get_available_books missing expected books, got {list(available_results.keys())}")
            
            # Final result checking
            if errors:
                self.test_obj.yakshaAssert("test_integrated_library_functions", False, "functional")
                pytest.fail("\n".join(errors))
            else:
                self.test_obj.yakshaAssert("test_integrated_library_functions", True, "functional")
                
        except Exception as e:
            self.test_obj.yakshaAssert("test_integrated_library_functions", False, "functional")
            pytest.fail(f"Integrated library functions test failed: {str(e)}")


if __name__ == '__main__':
    pytest.main(['-v'])