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
            # Special case for get_book and get_member methods
            if method_name in ["get_book", "get_member"]:
                return result  # Return None as is for these methods
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

def load_module_dynamically():
    """Load the student's module for testing"""
    module_obj = safely_import_module("skeleton")
    if module_obj is None:
        module_obj = safely_import_module("solution")
    return module_obj

class TestSystemBoundaries(unittest.TestCase):
    def setUp(self):
        """Standard setup for all test methods"""
        self.test_obj = TestUtils()
        self.module_obj = load_module_dynamically()
    
    def test_system_boundaries(self):
        """Test all boundary conditions for the library management system."""
        try:
            # Check if module can be imported
            if self.module_obj is None:
                self.test_obj.yakshaAssert("TestSystemBoundaries", False, "boundary")
                print("TestSystemBoundaries = Failed")
                return
            
            errors = []
            
            # Test Book class boundary cases
            if check_class_exists(self.module_obj, "Book"):
                try:
                    current_year = datetime.datetime.now().year
                    
                    # Test current year boundary
                    book1 = safely_create_instance(self.module_obj, "Book", "B001", "Current Year", "Author", "Fiction", current_year)
                    if book1 is None:
                        errors.append("Book class not properly implemented - constructor failed")
                    else:
                        year = safely_get_attribute(book1, "publication_year")
                        if year != current_year:
                            errors.append(f"Book publication_year property not working correctly - expected {current_year}, got {year}")
                    
                    # Test ancient year boundary (year 1)
                    book2 = safely_create_instance(self.module_obj, "Book", "B002", "Ancient Book", "Ancient Author", "History", 1)
                    if book2 is not None:
                        year = safely_get_attribute(book2, "publication_year")
                        if year != 1:
                            errors.append(f"Book should handle year 1 - expected 1, got {year}")
                    
                    # Test year zero boundary
                    book3 = safely_create_instance(self.module_obj, "Book", "B003", "Year Zero", "Author Zero", "Fiction", 0)
                    if book3 is not None:
                        year = safely_get_attribute(book3, "publication_year")
                        if year != 0:
                            errors.append(f"Book should handle year 0 - expected 0, got {year}")
                    
                except Exception as e:
                    errors.append(f"Error testing Book boundary cases: {str(e)}")
            else:
                errors.append("Book class not found")
            
            # Test Member class borrowing limit boundaries
            if check_class_exists(self.module_obj, "Member") and check_class_exists(self.module_obj, "Book"):
                try:
                    # Create member for borrowing limit tests
                    member = safely_create_instance(self.module_obj, "Member", "M001", "Max Borrower", "max@example.com")
                    if member is None:
                        errors.append("Member class not properly implemented - constructor failed")
                    else:
                        # Create test books
                        books = []
                        for i in range(4, 8):
                            book = safely_create_instance(self.module_obj, "Book", f"B00{i}", f"Book {i}", "Author", "Fiction", 2020)
                            if book is not None:
                                books.append(book)
                        
                        if len(books) >= 4:
                            # Test borrowing up to limit (3 books)
                            borrow_results = []
                            for i in range(3):
                                result = safely_call_method(member, "borrow_book", books[i])
                                borrow_results.append(result)
                            
                            # Check if borrow_book method exists and works
                            if None in borrow_results[:3]:
                                errors.append("Member.borrow_book method not properly implemented")
                            elif not all(result == True for result in borrow_results[:3]):
                                errors.append("Member should be able to borrow up to 3 books")
                            
                            # Test exceeding limit
                            exceed_result = safely_call_method(member, "borrow_book", books[3])
                            if exceed_result is None:
                                errors.append("Member.borrow_book method not properly implemented for limit test")
                            elif exceed_result != False:
                                errors.append("Member should not be able to borrow more than 3 books")
                            
                            # Test return and borrow again
                            if safely_call_method(member, "return_book", books[1]) == True:
                                final_borrow = safely_call_method(member, "borrow_book", books[3])
                                if final_borrow != True:
                                    errors.append("Member should be able to borrow after returning a book")
                            else:
                                if check_function_exists(member, "return_book"):
                                    errors.append("Member.return_book method not working correctly")
                                else:
                                    errors.append("Member.return_book method not found")
                        else:
                            errors.append("Could not create enough books for borrowing limit test")
                    
                    # Test books_borrowed list immutability
                    predefined_books = ["B101", "B102"]
                    member2 = safely_create_instance(self.module_obj, "Member", "M101", "Pre Member", "pre@example.com", predefined_books)
                    if member2 is not None:
                        borrowed_list = safely_get_attribute(member2, "books_borrowed")
                        if borrowed_list is None:
                            errors.append("Member.books_borrowed property not found")
                        elif borrowed_list == predefined_books and borrowed_list is not predefined_books:
                            # Test that modifying returned list doesn't affect original
                            borrowed_copy = safely_get_attribute(member2, "books_borrowed")
                            if borrowed_copy is not None and isinstance(borrowed_copy, list):
                                borrowed_copy.append("B103")
                                new_borrowed = safely_get_attribute(member2, "books_borrowed")
                                if new_borrowed is not None and "B103" in new_borrowed:
                                    errors.append("books_borrowed should return a copy, not the original list")
                        elif borrowed_list != predefined_books:
                            errors.append("Member should preserve predefined books_borrowed list")
                    
                except Exception as e:
                    errors.append(f"Error testing Member boundary cases: {str(e)}")
            else:
                if not check_class_exists(self.module_obj, "Member"):
                    errors.append("Member class not found")
                if not check_class_exists(self.module_obj, "Book"):
                    errors.append("Book class not found for Member testing")
            
            # Test Library class empty state and operations
            if check_class_exists(self.module_obj, "Library"):
                try:
                    # Test empty library
                    library = safely_create_instance(self.module_obj, "Library", "Empty Library", "Empty St")
                    if library is None:
                        errors.append("Library class not properly implemented - constructor failed")
                    else:
                        # Test empty library methods
                        all_books = safely_call_method(library, "get_all_books")
                        if all_books is None:
                            errors.append("Library.get_all_books method not implemented")
                        elif not isinstance(all_books, dict) or len(all_books) != 0:
                            errors.append("Empty library should return empty dictionary for get_all_books")
                        
                        available_books = safely_call_method(library, "get_available_books")
                        if available_books is None:
                            errors.append("Library.get_available_books method not implemented")
                        elif not isinstance(available_books, dict) or len(available_books) != 0:
                            errors.append("Empty library should return empty dictionary for get_available_books")
                        
                        # Test search methods on empty library
                        title_search = safely_call_method(library, "search_book_by_title", "any")
                        if title_search is None:
                            errors.append("Library.search_book_by_title method not implemented")
                        elif not isinstance(title_search, dict) or len(title_search) != 0:
                            errors.append("Empty library search_book_by_title should return empty dictionary")
                        
                        author_search = safely_call_method(library, "search_book_by_author", "any")
                        if author_search is None:
                            errors.append("Library.search_book_by_author method not implemented")
                        elif not isinstance(author_search, dict) or len(author_search) != 0:
                            errors.append("Empty library search_book_by_author should return empty dictionary")
                        
                        # Test get methods on empty library
                        book_result = safely_call_method(library, "get_book", "B001")
                        if book_result is not None:
                            errors.append("Empty library get_book should return None")
                        
                        all_members = safely_call_method(library, "get_all_members")
                        if all_members is None:
                            errors.append("Library.get_all_members method not implemented")
                        elif not isinstance(all_members, dict) or len(all_members) != 0:
                            errors.append("Empty library should return empty dictionary for get_all_members")
                        
                        member_result = safely_call_method(library, "get_member", "M001")
                        if member_result is not None:
                            errors.append("Empty library get_member should return None")
                    
                    # Test library checkout boundary conditions
                    test_library = safely_create_instance(self.module_obj, "Library", "Test Library", "Test St")
                    if test_library is not None and check_class_exists(self.module_obj, "Book") and check_class_exists(self.module_obj, "Member"):
                        book = safely_create_instance(self.module_obj, "Book", "B001", "Test Book", "Author", "Fiction", 2020)
                        member = safely_create_instance(self.module_obj, "Member", "M001", "Test Member", "test@example.com")
                        
                        if book is not None and member is not None:
                            # Add book and member to library
                            add_book_result = safely_call_method(test_library, "add_book", book)
                            add_member_result = safely_call_method(test_library, "add_member", member)
                            
                            if add_book_result is None:
                                errors.append("Library.add_book method not implemented")
                            elif add_member_result is None:
                                errors.append("Library.add_member method not implemented")
                            else:
                                # Test invalid checkout combinations
                                invalid_book_checkout = safely_call_method(test_library, "checkout_book", "INVALID", "M001")
                                if invalid_book_checkout is None:
                                    errors.append("Library.checkout_book method not implemented")
                                elif invalid_book_checkout != False:
                                    errors.append("Library.checkout_book should return False for invalid book ID")
                                
                                invalid_member_checkout = safely_call_method(test_library, "checkout_book", "B001", "INVALID")
                                if invalid_member_checkout != False:
                                    errors.append("Library.checkout_book should return False for invalid member ID")
                                
                                invalid_both_checkout = safely_call_method(test_library, "checkout_book", "INVALID", "INVALID")
                                if invalid_both_checkout != False:
                                    errors.append("Library.checkout_book should return False for invalid book and member IDs")
                                
                                # Test valid checkout and repeated attempt
                                valid_checkout = safely_call_method(test_library, "checkout_book", "B001", "M001")
                                if valid_checkout != True:
                                    errors.append("Library.checkout_book should return True for valid checkout")
                                else:
                                    # Try to checkout same book again
                                    repeat_checkout = safely_call_method(test_library, "checkout_book", "B001", "M001")
                                    if repeat_checkout != False:
                                        errors.append("Library.checkout_book should return False for already checked out book")
                        else:
                            if book is None:
                                errors.append("Could not create Book instance for Library testing")
                            if member is None:
                                errors.append("Could not create Member instance for Library testing")
                    
                except Exception as e:
                    errors.append(f"Error testing Library boundary cases: {str(e)}")
            else:
                errors.append("Library class not found")
            
            # Final assertion
            if errors:
                self.test_obj.yakshaAssert("TestSystemBoundaries", False, "boundary")
                print("TestSystemBoundaries = Failed")
            else:
                self.test_obj.yakshaAssert("TestSystemBoundaries", True, "boundary")
                print("TestSystemBoundaries = Passed")
                
        except Exception as e:
            self.test_obj.yakshaAssert("TestSystemBoundaries", False, "boundary")
            print("TestSystemBoundaries = Failed")

if __name__ == '__main__':
    unittest.main()