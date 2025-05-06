from unittest import TestCase
from unittest.mock import patch
from app.validation.validate_email_address import check_if_email_address_exist, CopyException

class TestEmailCheck(TestCase):

    @patch('app.validation.validate_email_address.get_user_by_email_address')
    def test_email_exists_raises_exception(self, mock_get_user):
        mock_get_user.return_value = {'email_address': 'test@email.com'}

        with self.assertRaises(CopyException) as context:
            check_if_email_address_exist('test@email.com')

        self.assertEqual(context.exception.message, 'email address exist.')
        self.assertEqual(context.exception.code, 409)

    @patch('app.validation.validate_email_address.get_user_by_email_address')
    def test_email_does_not_exist(self, mock_get_user):
        mock_get_user.return_value = None

        try:
            check_if_email_address_exist('new@example.com')
        except Exception as e:
            self.fail(f"check_if_email_address_exist raised {e} unexpectedly!")
