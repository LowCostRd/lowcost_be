from unittest import TestCase
from unittest.mock import patch
from app.validation.validate_email_address import *
from app.constant.error_message import email_address_exist

class TestEmailCheck(TestCase):

    @patch('app.validation.validate_email_address.get_user_by_email_address')
    def test_email_exists_raises_exception(self, mock_get_user):
        mock_get_user.return_value = {'email_address': 'test@email.com'}

        with self.assertRaises(CopyException) as context:
            check_if_email_address_exist('test@email.com')

        self.assertEqual(context.exception.message, email_address_exist)
        self.assertEqual(context.exception.code, 409)

    @patch('app.validation.validate_email_address.get_user_by_email_address')
    def test_email_does_not_exist(self, mock_get_user):
        mock_get_user.return_value = None

        try:
            check_if_email_address_exist('new@example.com')
        except Exception as e:
            self.fail(f"check_if_email_address_exist raised {e} unexpectedly!")
    
    def test_empty_email_address(self):
        with self.assertRaises(CopyException):
            validate_email_not_empty("")
    
    def test_null_email_address(self):
        with self.assertRaises(CopyException):
            validate_email_not_empty("null")
    
    def test_Null_email_address(self):
        with self.assertRaises(CopyException):
            validate_email_not_empty("Null")

    def test_invalid_email_format(self):
        with self.assertRaises(CopyException):
            validate_email("invalid format")
    
    def test_valid_email_format(self):
        try:
            validate_email("valid@valid.com")
        except CopyException as e:
            self.fail(e.message)
            


