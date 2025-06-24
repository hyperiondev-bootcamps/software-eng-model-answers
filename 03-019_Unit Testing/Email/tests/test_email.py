"""
In this practical task, you are going to write unit tests for one of your
previous practical tasks. Here is an example using the OOP Classes task.

If you would like to run all tests, you can use the following command in your terminal:
    python -m unittest discover -s tests

Alternatively, you can run a specific test file with a command similar to this:
    python -m unittest tests/test_email.py
"""

# Import the unittest module, provides the framework for creating unit tests
import unittest

# Import the Email class from the email module
# This is the class we are going to test
from email_module import Email

# Define a test class that inherits from unittest.TestCase, which provides
# various assert methods for testing
class TestEmail(unittest.TestCase):
    """TestEmail class to access our functions"""

    # A unit test method that tests the initialization of the Email object
    # ensure your functions start with "test" to ensure they are recognised
    def test_email_initialization(self):
        """Test for email initialization"""
        # Create an instance of the Email class with specific test data
        test_email = Email(
            "test@example.com", "Test Subject", "This is a test email."
        )

        # Assert that the email_address attribute was correctly initialized
        self.assertEqual(test_email.email_address, "test@example.com")
        # Assert that the subject_line attribute was correctly initialized
        self.assertEqual(test_email.subject_line, "Test Subject")
        # Assert that the email_content attribute was correctly initialized
        self.assertEqual(test_email.email_content, "This is a test email.")
        # Assert that the email is marked as unread upon initialization
        self.assertFalse(test_email.has_been_read)

    # Unit test method that tests the functionality of marking an email as read
    def test_mark_as_read(self):
        """Test for marking an email as read"""
        # Create an instance of the Email class with specific test data
        test_email = Email(
            "test@example.com", "Test Subject", "This is a test email."
        )

        # Assert that the email is initially unread
        self.assertFalse(test_email.has_been_read)

        # Call the method to mark the email as read
        test_email.mark_as_read()

        # Assert that the email is now marked as read
        self.assertTrue(test_email.has_been_read)

    # A unit test method that tests the ability to list unread emails from a
    # collection of emails
    def test_list_unread_emails(self):
        """Test the listing of unread emails"""
        # Create multiple instances of the Email class with different data
        first_email = Email("test1@example.com", "Subject 1", "Content 1")
        second_email = Email("test2@example.com", "Subject 2", "Content 2")
        third_email = Email("test3@example.com", "Subject 3", "Content 3")

        # Mark one of the emails as read
        second_email.mark_as_read()

        # Simulate an inbox with a list of these email objects
        inbox = [first_email, second_email, third_email]

        # Define a helper function that returns a list of unread emails from
        # the inbox
        def get_unread_emails(inbox):
            """Helper function to retrieve unread emails"""
            # Use a list comprehension to filter out unread emails
            return [email for email in inbox if not email.has_been_read]

        # Call the helper function to retrieve unread emails
        unread_emails = get_unread_emails(inbox)

        # Assert that there are exactly 2 unread emails
        self.assertEqual(len(unread_emails), 2)
        # Assert that email_1 is in the list of unread emails
        self.assertIn(first_email, unread_emails)
        # Assert that email_3 is in the list of unread emails
        self.assertIn(third_email, unread_emails)
        # Assert that email_2 is not in the list of unread emails because it
        # was marked as read
        self.assertNotIn(second_email, unread_emails)


# The entry point of the script. If this script is run directly, it will
# execute the unit tests
if __name__ == "__main__":
    unittest.main()
