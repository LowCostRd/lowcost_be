from unittest import TestCase
from unittest.mock import patch, MagicMock
from app.exception.copy_exception import CopyException
from app.services.user_authentication_service import UserAuthenticationService
from app.models.enum.user_role import UserRole
from app.constant.error_message import *


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
       

        mock_validate_user_role.return_value = UserRole.ORGANIZATION
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

 
    def test_empty_first_name_field(self):
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

        expected_message = "first_name is required."

        with self.assertRaises(CopyException) as context:
            service.registration(data)

        self.assertEqual(context.exception.args[0], expected_message)
        self.assertEqual(context.exception.code, 400)

    def test_null_first_name_field(self):
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

        expected_message = "first_name is required."

        with self.assertRaises(CopyException) as context:
            service.registration(data)

        self.assertEqual(context.exception.args[0], expected_message)
        self.assertEqual(context.exception.code, 400)

    def test_Null_first_name_field(self):
        service = UserAuthenticationService()
        data = {
            "first_name": "Null",
            "last_name": "last name",
            "email_address": "test@gmail.com",
            "phone_number": "090789393",
            "password": "password@234",
            "role": "organization",
            "organization_name": "name"
        }

        expected_message = "first_name is required."

        with self.assertRaises(CopyException) as context:
            service.registration(data)

        self.assertEqual(context.exception.args[0], expected_message)
        self.assertEqual(context.exception.code, 400)
    
    def test_empty_last_name_field(self):
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

        expected_message = "last_name is required."

        with self.assertRaises(CopyException) as context:
            service.registration(data)

        self.assertEqual(context.exception.args[0], expected_message)
        self.assertEqual(context.exception.code, 400)
    
    def test_null_last_name_field(self):
        service = UserAuthenticationService()
        data = {
            "first_name": "first name",
            "last_name": "null",
            "email_address": "test@gmail.com",
            "phone_number": "090789393",
            "password": "password@234",
            "role": "organization",
            "organization_name": "name"
        }

        expected_message = "last_name is required."

        with self.assertRaises(CopyException) as context:
            service.registration(data)

        self.assertEqual(context.exception.args[0], expected_message)
        self.assertEqual(context.exception.code, 400)
    
    def test_Null_last_name_field(self):
        service = UserAuthenticationService()
        data = {
            "first_name": "first name",
            "last_name": "Null",
            "email_address": "test@gmail.com",
            "phone_number": "090789393",
            "password": "password@234",
            "role": "organization",
            "organization_name": "name"
        }

        expected_message = "last_name is required."

        with self.assertRaises(CopyException) as context:
            service.registration(data)

        self.assertEqual(context.exception.args[0], expected_message)
        self.assertEqual(context.exception.code, 400)
    
    def test_empty_email_address_field(self):
        service = UserAuthenticationService()
        data = {
            "first_name": "first name",
            "last_name": "last name",
            "email_address": " ",
            "phone_number": "090789393",
            "password": "password@234",
            "role": "organization",
            "organization_name": "name"
        }

        expected_message = "email_address is required."

        with self.assertRaises(CopyException) as context:
            service.registration(data)

        self.assertEqual(context.exception.args[0], expected_message)
        self.assertEqual(context.exception.code, 400)
    
    def test_null_email_address_field(self):
        service = UserAuthenticationService()
        data = {
            "first_name": "first name",
            "last_name": "last name",
            "email_address": "null",
            "phone_number": "090789393",
            "password": "password@234",
            "role": "organization",
            "organization_name": "name"
        }

        expected_message = "email_address is required."

        with self.assertRaises(CopyException) as context:
            service.registration(data)

        self.assertEqual(context.exception.args[0], expected_message)
        self.assertEqual(context.exception.code, 400)
    
    def test_Null_email_address_field(self):
        service = UserAuthenticationService()
        data = {
            "first_name": "first name",
            "last_name": "last name",
            "email_address": "Null",
            "phone_number": "090789393",
            "password": "password@234",
            "role": "organization",
            "organization_name": "name"
        }

        expected_message = "email_address is required."

        with self.assertRaises(CopyException) as context:
            service.registration(data)

        self.assertEqual(context.exception.args[0], expected_message)
        self.assertEqual(context.exception.code, 400)

    def test_empty_phone_number_field(self):
        service = UserAuthenticationService()
        data = {
            "first_name": "first name",
            "last_name": "last name",
            "email_address": "email@gmail.com",
            "phone_number": " ",
            "password": "password@234",
            "role": "organization",
            "organization_name": "name"
        }

        expected_message = "phone_number is required."

        with self.assertRaises(CopyException) as context:
            service.registration(data)

        self.assertEqual(context.exception.args[0], expected_message)
        self.assertEqual(context.exception.code, 400)
    
    def test_null_phone_number_field(self):
        service = UserAuthenticationService()
        data = {
            "first_name": "first name",
            "last_name": "last name",
            "email_address": "email@gmail.com",
            "phone_number": "null",
            "password": "password@234",
            "role": "organization",
            "organization_name": "name"
        }

        expected_message = "phone_number is required."

        with self.assertRaises(CopyException) as context:
            service.registration(data)

        self.assertEqual(context.exception.args[0], expected_message)
        self.assertEqual(context.exception.code, 400)
    
    def test_Null_phone_number_field(self):
        service = UserAuthenticationService()
        data = {
            "first_name": "first name",
            "last_name": "last name",
            "email_address": "email@gmail.com",
            "phone_number": "Null",
            "password": "password@234",
            "role": "organization",
            "organization_name": "name"
        }

        expected_message = "phone_number is required."

        with self.assertRaises(CopyException) as context:
            service.registration(data)

        self.assertEqual(context.exception.args[0], expected_message)
        self.assertEqual(context.exception.code, 400)
    
    def test_empty_password_field(self):
        service = UserAuthenticationService()
        data = {
            "first_name": "first name",
            "last_name": "last name",
            "email_address": "email@gmail.com",
            "phone_number": "0907839939",
            "password": " ",
            "role": "organization",
            "organization_name": "name"
        }

        expected_message = "password is required."

        with self.assertRaises(CopyException) as context:
            service.registration(data)

        self.assertEqual(context.exception.args[0], expected_message)
        self.assertEqual(context.exception.code, 400)

    def test_null_password_field(self):
        service = UserAuthenticationService()
        data = {
            "first_name": "first name",
            "last_name": "last name",
            "email_address": "email@gmail.com",
            "phone_number": "0907839939",
            "password": "null",
            "role": "organization",
            "organization_name": "name"
        }

        expected_message = "password is required."

        with self.assertRaises(CopyException) as context:
            service.registration(data)

        self.assertEqual(context.exception.args[0], expected_message)
        self.assertEqual(context.exception.code, 400)
    
    def test_Null_password_field(self):
        service = UserAuthenticationService()
        data = {
            "first_name": "first name",
            "last_name": "last name",
            "email_address": "email@gmail.com",
            "phone_number": "0907839939",
            "password": "Null",
            "role": "organization",
            "organization_name": "name"
        }

        expected_message = "password is required."

        with self.assertRaises(CopyException) as context:
            service.registration(data)

        self.assertEqual(context.exception.args[0], expected_message)
        self.assertEqual(context.exception.code, 400)
    
    def test_empty_role_field(self):
        service = UserAuthenticationService()
        data = {
            "first_name": "first name",
            "last_name": "last name",
            "email_address": "email@gmail.com",
            "phone_number": "0907839939",
            "password": "password@123",
            "role": " ",
            "organization_name": "name"
        }

        expected_message = "role is required."

        with self.assertRaises(CopyException) as context:
            service.registration(data)

        self.assertEqual(context.exception.args[0], expected_message)
        self.assertEqual(context.exception.code, 400)

    def test_null_role_field(self):
        service = UserAuthenticationService()
        data = {
            "first_name": "first name",
            "last_name": "last name",
            "email_address": "email@gmail.com",
            "phone_number": "0907839939",
            "password": "password@123",
            "role": "null",
            "organization_name": "name"
        }

        expected_message = "role is required."

        with self.assertRaises(CopyException) as context:
            service.registration(data)

        self.assertEqual(context.exception.args[0], expected_message)
        self.assertEqual(context.exception.code, 400)
    
    def test_Null_role_field(self):
        service = UserAuthenticationService()
        data = {
            "first_name": "first name",
            "last_name": "last name",
            "email_address": "email@gmail.com",
            "phone_number": "0907839939",
            "password": "password@123",
            "role": "Null",
            "organization_name": "name"
        }

        expected_message = "role is required."

        with self.assertRaises(CopyException) as context:
            service.registration(data)

        self.assertEqual(context.exception.args[0], expected_message)
        self.assertEqual(context.exception.code, 400)
    
    def test_empty_organization_field_if_role_is_organization(self):
        service = UserAuthenticationService()
        data = {
            "first_name": "first name",
            "last_name": "last name",
            "email_address": "email@gmail.com",
            "phone_number": "0907839939",
            "password": "password@123",
            "role": "organization",
            "organization_name": " "
        }

        expected_message = "organization name is required."

        with self.assertRaises(CopyException) as context:
            service.registration(data)

        self.assertEqual(context.exception.args[0], expected_message)
        self.assertEqual(context.exception.code, 400)
    
    def test_null_organization_field_if_role_is_organization(self):
        service = UserAuthenticationService()
        data = {
            "first_name": "first name",
            "last_name": "last name",
            "email_address": "email@gmail.com",
            "phone_number": "0907839939",
            "password": "password@123",
            "role": "organization",
            "organization_name": "null"
        }

        expected_message = "organization name is required."

        with self.assertRaises(CopyException) as context:
            service.registration(data)

        self.assertEqual(context.exception.args[0], expected_message)
        self.assertEqual(context.exception.code, 400)
    
    def test_Null_organization_field_if_role_is_organization(self):
        service = UserAuthenticationService()
        data = {
            "first_name": "first name",
            "last_name": "last name",
            "email_address": "email@gmail.com",
            "phone_number": "0907839939",
            "password": "password@123",
            "role": "organization",
            "organization_name": "Null"
        }

        expected_message = "organization name is required."

        with self.assertRaises(CopyException) as context:
            service.registration(data)

        self.assertEqual(context.exception.args[0], expected_message)
        self.assertEqual(context.exception.code, 400)

    
    def test_invalid_email_format(self):
        service = UserAuthenticationService()
        data = {
            "first_name": "first name",
            "last_name": "last name",
            "email_address": "wrong email",
            "phone_number": "0907839939",
            "password": "password@123",
            "role": "organization",
            "organization_name": "name"
        }

        expected_message = invalid_email_format

        with self.assertRaises(CopyException) as context:
            service.registration(data)

        self.assertEqual(context.exception.args[0], expected_message)
        self.assertEqual(context.exception.code, 400)
    
    def test_invalid_password_format(self):
        service = UserAuthenticationService()
        data = {
            "first_name": "first name",
            "last_name": "last name",
            "email_address": "test@email.com",
            "phone_number": "0907839939",
            "password": "wrong password",
            "role": "organization",
            "organization_name": "name"
        }

        expected_message = password_not_valid

        with self.assertRaises(CopyException) as context:
            service.registration(data)

        self.assertEqual(context.exception.args[0], expected_message)
        self.assertEqual(context.exception.code, 400)

    
    def test_invalid_role(self):
        service = UserAuthenticationService()
        data = {
            "first_name": "first name",
            "last_name": "last name",
            "email_address": "test@email.com",
            "phone_number": "0907839939",
            "password": "password@123",
            "role": "invalid role",
            "organization_name": "name"
        }

        expected_message = role_not_valid

        with self.assertRaises(CopyException) as context:
            service.registration(data)

        self.assertEqual(context.exception.args[0], expected_message)
        self.assertEqual(context.exception.code, 400)
    
    @patch("app.services.user_authentication_service.hash_password")
    @patch("app.services.user_authentication_service.EmailOTPService.send_and_store_otp")
    @patch("app.services.user_authentication_service.mongo")
    @patch("app.services.user_authentication_service.check_if_email_address_exist")
    @patch("app.services.user_authentication_service.validate_password")
    @patch("app.services.user_authentication_service.validate_email")
    @patch("app.services.user_authentication_service.validate_registration_field")
    @patch("app.services.user_authentication_service.validate_user_role")
    def test_registration_is_successful_if_role_is_personal_and_no_organization_field_is_provided(
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
            "role": "personal",
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
    @patch("app.services.user_authentication_service.validate_user_role")
    def test_registration_is_successful_if_role_is_personal_and_organization_field_is_provided_but_empty(
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
            "role": "personal",
            "organization_name" : ""
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
    @patch("app.services.user_authentication_service.validate_user_role")
    def test_registration_is_successful_if_role_is_personal_and_organization_field_is_provided_but_is_null(
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
            "role": "personal",
            "organization_name" : "null"
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
    @patch("app.services.user_authentication_service.validate_user_role")
    def test_registration_is_successful_if_role_is_personal_and_organization_field_is_provided_but_is_Null(
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
            "role": "personal",
            "organization_name" : "Null"
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

 
 