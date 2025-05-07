from unittest import TestCase
from unittest.mock import patch, MagicMock
from app.exception.copy_exception import CopyException
from app.services.user_authentication_service import UserAuthenticationService
from app.models.enum.user_role import UserRole
from app.constant.error_message import required_field
class UserAuthenticationTest(TestCase):
    @patch("app.services.user_authentication_service.hash_password")
    @patch("app.services.user_authentication_service.EmailOTPService.send_and_store_otp")
    @patch("app.services.user_authentication_service.mongo")
    @patch("app.services.user_authentication_service.check_if_email_address_exist")
    @patch("app.services.user_authentication_service.validate_password")
    @patch("app.services.user_authentication_service.validate_email")
    @patch("app.services.user_authentication_service.validate_registration_field")
    @patch("app.services.user_authentication_service.validate_user_role")
    def test_successful_registration(
        self,
        mock_validate_user_role,
        mock_validate_registration_field,
        mock_validate_email,
        mock_validate_password,
        mock_check_email,
        mock_mongo,
        mock_send_otp,
        mock_hash_password,
    ):
        service = UserAuthenticationService()
        data = {
            "first_name": "testing first name",
            "last_name": "last name",
            "email_address": "test@gmail.com",
            "phone_number": "090789393",
            "password": "password@234",
            "role": "organization",
            "organization_name": "name"
        }
       

        mock_validate_user_role.return_value = UserRole.PERSONAL
        mock_hash_password.return_value = data["password"]
        mock_collection = MagicMock()
        mock_mongo.db.users = mock_collection

        

        service.registration(data)
        mock_validate_password.assert_called_once_with(data["password"]) 
        mock_validate_registration_field.assert_called_once_with(data)
        mock_validate_email.assert_called_once_with(data["email_address"])
        mock_check_email.assert_called_once_with(data["email_address"])
        mock_hash_password.assert_called_once_with(data["password"])
        mock_collection.insert_one.assert_called_once()
        mock_send_otp.assert_called_once_with(data["email_address"])

 
    @patch("app.services.user_authentication_service.hash_password")
    @patch("app.services.user_authentication_service.EmailOTPService.send_and_store_otp")
    @patch("app.services.user_authentication_service.mongo")
    @patch("app.services.user_authentication_service.check_if_email_address_exist")
    @patch("app.services.user_authentication_service.validate_password")
    @patch("app.services.user_authentication_service.validate_email")
    @patch("app.services.user_authentication_service.validate_registration_field")
    def test_empty_first_name_field(
        self,
        mock_validate_registration_field,
        mock_validate_email,
        mock_validate_password,
        mock_check_email,
        mock_mongo,
        mock_send_otp,
        mock_hash_password,
    ):
        service = UserAuthenticationService()
        data = {
            "first_name": "",
            "last_name": "last name",
            "email_address": "test@gmail.com",
            "phone_number": "090789393",
            "password": "password@234",
            "role": "organization",
            "organization_name": "name"
        }


        mock_validate_registration_field.side_effect = CopyException(
            required_field["required_field"]("first name"),400
        )

        with self.assertRaises(CopyException) as context:
            service.registration(data)

        self.assertEqual(context.exception.message, required_field["required_field"]("first name"))
        self.assertEqual(context.exception.code, 400)
 
    @patch("app.services.user_authentication_service.hash_password")
    @patch("app.services.user_authentication_service.EmailOTPService.send_and_store_otp")
    @patch("app.services.user_authentication_service.mongo")
    @patch("app.services.user_authentication_service.check_if_email_address_exist")
    @patch("app.services.user_authentication_service.validate_password")
    @patch("app.services.user_authentication_service.validate_email")
    @patch("app.services.user_authentication_service.validate_registration_field")
    def test_null_first_name_field(
        self,
        mock_validate_registration_field,
        mock_validate_email,
        mock_validate_password,
        mock_check_email,
        mock_mongo,
        mock_send_otp,
        mock_hash_password,
    ):
        service = UserAuthenticationService()
        data = {
            "first_name": "null",
            "last_name": "last name",
            "email_address": "test@gmail.com",
            "phone_number": "090789393",
            "password": "password@234",
            "role": "organization",
            "organization_name": "name"
        }


        mock_validate_registration_field.side_effect = CopyException(
            required_field["required_field"]("first name"),400
        )

        with self.assertRaises(CopyException) as context:
            service.registration(data)

        self.assertEqual(context.exception.message, required_field["required_field"]("first name"))
        self.assertEqual(context.exception.code, 400)
 
    @patch("app.services.user_authentication_service.hash_password")
    @patch("app.services.user_authentication_service.EmailOTPService.send_and_store_otp")
    @patch("app.services.user_authentication_service.mongo")
    @patch("app.services.user_authentication_service.check_if_email_address_exist")
    @patch("app.services.user_authentication_service.validate_password")
    @patch("app.services.user_authentication_service.validate_email")
    @patch("app.services.user_authentication_service.validate_registration_field")
    def test_Null_first_name_field(
        self,
        mock_validate_registration_field,
        mock_validate_email,
        mock_validate_password,
        mock_check_email,
        mock_mongo,
        mock_send_otp,
        mock_hash_password,
    ):
        service = UserAuthenticationService()
        data = {
            "first_name": "null",
            "last_name": "last name",
            "email_address": "test@gmail.com",
            "phone_number": "090789393",
            "password": "password@234",
            "role": "organization",
            "organization_name": "name"
        }


        mock_validate_registration_field.side_effect = CopyException(
            required_field["required_field"]("first name"),400
        )

        with self.assertRaises(CopyException) as context:
            service.registration(data)

        self.assertEqual(context.exception.message, required_field["required_field"]("first name"))
        self.assertEqual(context.exception.code, 400)
    
    @patch("app.services.user_authentication_service.hash_password")
    @patch("app.services.user_authentication_service.EmailOTPService.send_and_store_otp")
    @patch("app.services.user_authentication_service.mongo")
    @patch("app.services.user_authentication_service.check_if_email_address_exist")
    @patch("app.services.user_authentication_service.validate_password")
    @patch("app.services.user_authentication_service.validate_email")
    @patch("app.services.user_authentication_service.validate_registration_field")
    def test_empty_last_name_field(
        self,
        mock_validate_registration_field,
        mock_validate_email,
        mock_validate_password,
        mock_check_email,
        mock_mongo,
        mock_send_otp,
        mock_hash_password,
    ):
        service = UserAuthenticationService()
        data = {
            "first_name": "first name",
            "last_name": " ",
            "email_address": "test@gmail.com",
            "phone_number": "090789393",
            "password": "password@234",
            "role": "organization",
            "organization_name": "name"
        }


        mock_validate_registration_field.side_effect = CopyException(
            required_field["required_field"]("last name"),400
        )

        with self.assertRaises(CopyException) as context:
            service.registration(data)

        self.assertEqual(context.exception.message, required_field["required_field"]("last name"))
        self.assertEqual(context.exception.code, 400)
