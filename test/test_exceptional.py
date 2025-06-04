import unittest
import os
import importlib
import sys
import io
import contextlib
import datetime
from test.TestUtils import TestUtils

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
    if not check_class_exists(module, class_name):
        return None
    try:
        with contextlib.redirect_stdout(io.StringIO()):
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
        with contextlib.redirect_stdout(io.StringIO()):
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
        with contextlib.redirect_stdout(io.StringIO()):
            return getattr(obj, attr_name)
    except (AttributeError, NameError):
        return None

def check_raises(func, args, expected_exception=Exception):
    """Check if a function raises an expected exception."""
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            func(*args)
        return False
    except expected_exception:
        return True
    except Exception:
        return False

def load_module_dynamically():
    """Load the student's module for testing"""
    module_obj = safely_import_module("skeleton")
    if module_obj is None:
        module_obj = safely_import_module("solution")
    return module_obj

class TestExceptionHandling(unittest.TestCase):
    def setUp(self):
        """Standard setup for all test methods"""
        self.test_obj = TestUtils()
        self.module_obj = load_module_dynamically()
    
    def test_comprehensive_exceptions(self):
        """Test exception handling across the library management system."""
        try:
            # Check if module can be imported
            if self.module_obj is None:
                self.test_obj.yakshaAssert("TestExceptionHandling", False, "exception")
                print("TestExceptionHandling = Failed")
                return
            
            errors = []
            
            # Test Book class validation exceptions
            if check_class_exists(self.module_obj, "Book"):
                try:
                    # Test future publication year validation
                    future_year = datetime.datetime.now().year + 10
                    book_cls = getattr(self.module_obj, "Book")
                    
                    if not check_raises(lambda: book_cls("B001", "Future Book", "Author", "Fiction", future_year), [], ValueError):
                        errors.append("Book constructor should raise ValueError for future publication year")
                    
                    # Test non-integer publication year
                    if not check_raises(lambda: book_cls("B002", "String Year", "Author", "Fiction", "2023"), [], (ValueError, TypeError)):
                        errors.append("Book constructor should raise ValueError/TypeError for non-integer publication year")
                    
                    # Test negative publication year
                    if not check_raises(lambda: book_cls("B003", "Negative Year", "Author", "Fiction", -100), [], ValueError):
                        # This may or may not be implemented, so don't fail if it's not
                        pass
                    
                except Exception as e:
                    errors.append(f"Error testing Book validation exceptions: {str(e)}")
            else:
                errors.append("Book class not found")
            
            # Test Member class validation exceptions
            if check_class_exists(self.module_obj, "Member"):
                try:
                    member_cls = getattr(self.module_obj, "Member")
                    
                    # Test invalid email formats
                    invalid_emails = ["invalidemail.com", "invalid@", "@invalid.com", "invalid@.com", ""]
                    for invalid_email in invalid_emails:
                        if not check_raises(lambda: member_cls("M001", "Invalid Email", invalid_email), [], ValueError):
                            errors.append(f"Member constructor should raise ValueError for invalid email: {invalid_email}")
                            break  # Only report one invalid email error
                    
                    # Test empty name
                    if not check_raises(lambda: member_cls("M002", "", "valid@email.com"), [], ValueError):
                        # This validation might not be implemented, so don't fail the test
                        pass
                    
                except Exception as e:
                    errors.append(f"Error testing Member validation exceptions: {str(e)}")
            else:
                errors.append("Member class not found")
            
            # Test Library search validation exceptions
            if check_class_exists(self.module_obj, "Library"):
                try:
                    library = safely_create_instance(self.module_obj, "Library", "Search Library", "Search St")
                    if library is not None:
                        # Test search with None values
                        if check_function_exists(library, "search_book_by_title"):
                            search_title_method = getattr(library, "search_book_by_title")
                            if not check_raises(lambda: search_title_method(None), [], ValueError):
                                errors.append("search_book_by_title should raise ValueError for None input")
                        else:
                            errors.append("search_book_by_title method not found")
                        
                        if check_function_exists(library, "search_book_by_author"):
                            search_author_method = getattr(library, "search_book_by_author")
                            if not check_raises(lambda: search_author_method(None), [], ValueError):
                                errors.append("search_book_by_author should raise ValueError for None input")
                        else:
                            errors.append("search_book_by_author method not found")
                        
                        # Test empty string searches (should NOT raise exceptions)
                        if check_function_exists(library, "search_book_by_title"):
                            try:
                                result = safely_call_method(library, "search_book_by_title", "")
                                if result is None:
                                    errors.append("search_book_by_title method not implemented properly")
                                elif not isinstance(result, dict):
                                    errors.append("search_book_by_title should return empty dict for empty string")
                            except Exception:
                                errors.append("search_book_by_title should not raise exception for empty string")
                        
                        if check_function_exists(library, "search_book_by_author"):
                            try:
                                result = safely_call_method(library, "search_book_by_author", "")
                                if result is None:
                                    errors.append("search_book_by_author method not implemented properly")
                                elif not isinstance(result, dict):
                                    errors.append("search_book_by_author should return empty dict for empty string")
                            except Exception:
                                errors.append("search_book_by_author should not raise exception for empty string")
                    else:
                        errors.append("Library instance could not be created")
                except Exception as e:
                    errors.append(f"Error testing Library search validation: {str(e)}")
            else:
                errors.append("Library class not found")
            
            # Test book checkout operation exceptions
            if check_class_exists(self.module_obj, "Book") and check_class_exists(self.module_obj, "Member"):
                try:
                    # Test borrowing unavailable book
                    checked_out_book = safely_create_instance(self.module_obj, "Book", "B001", "Unavailable Book", "Author", "Fiction", 2020, False)
                    member = safely_create_instance(self.module_obj, "Member", "M001", "Test Member", "test@example.com")
                    
                    if checked_out_book is not None and member is not None:
                        result = safely_call_method(member, "borrow_book", checked_out_book)
                        if result is None:
                            errors.append("Member.borrow_book method not implemented")
                        elif result != False:
                            errors.append("Member.borrow_book should return False for unavailable book")
                        
                        # Test exceeding borrowing limit
                        if check_function_exists(member, "borrow_book"):
                            books = []
                            for i in range(2, 6):
                                book = safely_create_instance(self.module_obj, "Book", f"B{i}", f"Book {i}", "Author", "Fiction", 2020)
                                if book is not None:
                                    books.append(book)
                            
                            if len(books) >= 4:
                                # Borrow 3 books (maximum limit)
                                for i in range(3):
                                    safely_call_method(member, "borrow_book", books[i])
                                
                                # Try to borrow 4th book
                                result = safely_call_method(member, "borrow_book", books[3])
                                if result != False:
                                    errors.append("Member.borrow_book should return False when exceeding borrowing limit")
                    else:
                        if checked_out_book is None:
                            errors.append("Could not create Book instance for checkout testing")
                        if member is None:
                            errors.append("Could not create Member instance for checkout testing")
                except Exception as e:
                    errors.append(f"Error testing book checkout exceptions: {str(e)}")
            
            # Test Library checkout/return operation exceptions
            if check_class_exists(self.module_obj, "Library") and check_class_exists(self.module_obj, "Book") and check_class_exists(self.module_obj, "Member"):
                try:
                    lib = safely_create_instance(self.module_obj, "Library", "Test Library", "Test St")
                    book = safely_create_instance(self.module_obj, "Book", "B101", "Test Book", "Author", "Fiction", 2020)
                    member = safely_create_instance(self.module_obj, "Member", "M101", "Test Member", "test@example.com")
                    
                    if lib is not None and book is not None and member is not None:
                        # Add book and member to library
                        safely_call_method(lib, "add_book", book)
                        safely_call_method(lib, "add_member", member)
                        
                        # Check out the book
                        checkout_result = safely_call_method(lib, "checkout_book", "B101", "M101")
                        if checkout_result == True:
                            # Try to return with missing book ID
                            if check_function_exists(lib, "return_book"):
                                return_result = safely_call_method(lib, "return_book", "INVALID", "M101")
                                if return_result != False:
                                    errors.append("Library.return_book should return False for invalid book ID")
                            else:
                                errors.append("Library.return_book method not found")
                        else:
                            if checkout_result is None:
                                errors.append("Library.checkout_book method not implemented")
                            else:
                                errors.append("Could not checkout book for return testing")
                        
                        # Test checkout with missing book/member
                        new_library = safely_create_instance(self.module_obj, "Library", "Operations Library", "Operations St")
                        if new_library is not None:
                            # Checkout with missing book
                            result = safely_call_method(new_library, "checkout_book", "NONEXISTENT", "M001")
                            if result != False:
                                errors.append("Library.checkout_book should return False for non-existent book")
                            
                            # Checkout with missing member
                            book2 = safely_create_instance(self.module_obj, "Book", "B011", "Exists", "Author", "Fiction", 2020)
                            if book2 is not None:
                                safely_call_method(new_library, "add_book", book2)
                                result = safely_call_method(new_library, "checkout_book", "B011", "NONEXISTENT")
                                if result != False:
                                    errors.append("Library.checkout_book should return False for non-existent member")
                                
                                # Test checkout of already checked out book
                                member3 = safely_create_instance(self.module_obj, "Member", "M007", "Exists", "exists@example.com")
                                if member3 is not None:
                                    safely_call_method(new_library, "add_member", member3)
                                    
                                    # Check out the book
                                    first_checkout = safely_call_method(new_library, "checkout_book", "B011", "M007")
                                    if first_checkout == True:
                                        # Try to check out again
                                        second_checkout = safely_call_method(new_library, "checkout_book", "B011", "M007")
                                        if second_checkout != False:
                                            errors.append("Library.checkout_book should return False for already checked out book")
                    else:
                        if lib is None:
                            errors.append("Could not create Library instance for operation testing")
                        if book is None:
                            errors.append("Could not create Book instance for operation testing")
                        if member is None:
                            errors.append("Could not create Member instance for operation testing")
                except Exception as e:
                    errors.append(f"Error testing Library operation exceptions: {str(e)}")
            
            # Test inheritance-specific exceptions (if implemented)
            if check_class_exists(self.module_obj, "FictionBook"):
                try:
                    # Test FictionBook with invalid parameters
                    fiction_cls = getattr(self.module_obj, "FictionBook")
                    # Most validation should be in base Book class, so just test creation
                    fiction_book = safely_create_instance(self.module_obj, "FictionBook", "FB001", "Fiction Test", "Author", "Fiction", 2020, "Novel")
                    if fiction_book is None:
                        errors.append("FictionBook could not be created - check inheritance")
                except Exception as e:
                    errors.append(f"Error testing FictionBook: {str(e)}")
            
            if check_class_exists(self.module_obj, "NonFictionBook"):
                try:
                    # Test NonFictionBook with invalid parameters
                    nonfiction_cls = getattr(self.module_obj, "NonFictionBook")
                    nonfiction_book = safely_create_instance(self.module_obj, "NonFictionBook", "NF001", "NonFiction Test", "Author", "NonFiction", 2020, "Science")
                    if nonfiction_book is None:
                        errors.append("NonFictionBook could not be created - check inheritance")
                except Exception as e:
                    errors.append(f"Error testing NonFictionBook: {str(e)}")
            
            # Final assertion
            if errors:
                self.test_obj.yakshaAssert("TestExceptionHandling", False, "exception")
                print("TestExceptionHandling = Failed")
            else:
                self.test_obj.yakshaAssert("TestExceptionHandling", True, "exception")
                print("TestExceptionHandling = Passed")
                
        except Exception as e:
            self.test_obj.yakshaAssert("TestExceptionHandling", False, "exception")
            print("TestExceptionHandling = Failed")

if __name__ == '__main__':
    unittest.main()