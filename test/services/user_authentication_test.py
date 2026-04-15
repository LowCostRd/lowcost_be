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
            "full_name": "first name",
            "email_address": "test@gmail.com",
            "password": "password@234",
            "role": "other",
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
            "full_name": "",
            "email_address": "test@gmail.com",
            "password": "password@234",
            "role": "other",
        }

        expected_message = "full_name is required."

        with self.assertRaises(CopyException) as context:
            service.registration(data)

        self.assertEqual(context.exception.args[0], expected_message)
        self.assertEqual(context.exception.code, 400)

    def test_null_full_name_field(self):
        service = UserAuthenticationService()
        data = {
            "full_name": "null",
            "email_address": "test@gmail.com",
            "password": "password@234",
            "role": "other",
        }

        expected_message = "full_name is required."

        with self.assertRaises(CopyException) as context:
            service.registration(data)

        self.assertEqual(context.exception.args[0], expected_message)
        self.assertEqual(context.exception.code, 400)

    def test_Null_first_name_field(self):
        service = UserAuthenticationService()
        data = {
            "full_name": "Null",
            "email_address": "test@gmail.com",
            "password": "password@234",
            "role": "organization",
        }

        expected_message = "full_name is required."

        with self.assertRaises(CopyException) as context:
            service.registration(data)

        self.assertEqual(context.exception.args[0], expected_message)
        self.assertEqual(context.exception.code, 400)
    
    
    def test_empty_email_address_field(self):
        service = UserAuthenticationService()
        data = {
            "full_name": "full name",
            "email_address": " ",
            "password": "password@234",
            "role": "other",
        }

        expected_message = "email_address is required."

        with self.assertRaises(CopyException) as context:
            service.registration(data)

        self.assertEqual(context.exception.args[0], expected_message)
        self.assertEqual(context.exception.code, 400)
    
    def test_null_email_address_field(self):
        service = UserAuthenticationService()
        data = {
            "full_name": "full name",
            "email_address": "null",
            "password": "password@234",
            "role": "other",
        }

        expected_message = "email_address is required."

        with self.assertRaises(CopyException) as context:
            service.registration(data)

        self.assertEqual(context.exception.args[0], expected_message)
        self.assertEqual(context.exception.code, 400)
    
    def test_Null_email_address_field(self):
        service = UserAuthenticationService()
        data = {
            "full_name": "full name",
            "email_address": "Null",
            "password": "password@234",
            "role": "other",
        }

        expected_message = "email_address is required."

        with self.assertRaises(CopyException) as context:
            service.registration(data)

        self.assertEqual(context.exception.args[0], expected_message)
        self.assertEqual(context.exception.code, 400)

   
    
    def test_empty_password_field(self):
        service = UserAuthenticationService()
        data = {
            "full_name": "full name",
            "email_address": "email@gmail.com",
            "password": " ",
            "role": "other",
        }

        expected_message = "password is required."

        with self.assertRaises(CopyException) as context:
            service.registration(data)

        self.assertEqual(context.exception.args[0], expected_message)
        self.assertEqual(context.exception.code, 400)

    def test_null_password_field(self):
        service = UserAuthenticationService()
        data = {
            "full_name": "full name",
            "email_address": "email@gmail.com",
            "phone_number": "0907839939",
            "password": "null",
            "role": "other",
    
        }

        expected_message = "password is required."

        with self.assertRaises(CopyException) as context:
            service.registration(data)

        self.assertEqual(context.exception.args[0], expected_message)
        self.assertEqual(context.exception.code, 400)
    
    def test_Null_password_field(self):
        service = UserAuthenticationService()
        data = {
            "full_name": "full name",
            "email_address": "email@gmail.com",
            "phone_number": "0907839939",
            "password": "Null",
            "role": "other",
        }

        expected_message = "password is required."

        with self.assertRaises(CopyException) as context:
            service.registration(data)

        self.assertEqual(context.exception.args[0], expected_message)
        self.assertEqual(context.exception.code, 400)
    
    def test_empty_role_field(self):
        service = UserAuthenticationService()
        data = {
            "full_name": "full name",
            "email_address": "email@gmail.com",
            "password": "password@123",
            "role": " ",
        }

        expected_message = "role is required."

        with self.assertRaises(CopyException) as context:
            service.registration(data)

        self.assertEqual(context.exception.args[0], expected_message)
        self.assertEqual(context.exception.code, 400)

    def test_null_role_field(self):
        service = UserAuthenticationService()
        data = {
            "full_name": "full name",
            "email_address": "email@gmail.com",
            "password": "password@123",
            "role": "null",
        }

        expected_message = "role is required."

        with self.assertRaises(CopyException) as context:
            service.registration(data)

        self.assertEqual(context.exception.args[0], expected_message)
        self.assertEqual(context.exception.code, 400)
    
    def test_Null_role_field(self):
        service = UserAuthenticationService()
        data = {
            "full_name": "full name",
            "email_address": "email@gmail.com",
            "password": "password@123",
            "role": "Null",
        }

        expected_message = "role is required."

        with self.assertRaises(CopyException) as context:
            service.registration(data)

        self.assertEqual(context.exception.args[0], expected_message)
        self.assertEqual(context.exception.code, 400)
    
   
    def test_invalid_email_format(self):
        service = UserAuthenticationService()
        data = {
            "full_name": "full name",
            "email_address": "wrong email",
            "password": "password@123",
            "role": "other",
        }

        expected_message = invalid_email_format

        with self.assertRaises(CopyException) as context:
            service.registration(data)

        self.assertEqual(context.exception.args[0], expected_message)
        self.assertEqual(context.exception.code, 400)
    
    def test_invalid_password_format(self):
        service = UserAuthenticationService()
        data = {
            "full_name": "full name",
            "email_address": "test@email.com",
            "phone_number": "0907839939",
            "password": "wrong password",
            "role": "other",
        }

        expected_message = password_not_valid

        with self.assertRaises(CopyException) as context:
            service.registration(data)

        self.assertEqual(context.exception.args[0], expected_message)
        self.assertEqual(context.exception.code, 400)

    
    def test_invalid_role(self):
        service = UserAuthenticationService()
        data = {
            "full_name": "full name",
            "email_address": "test@email.com",
            "password": "password@123",
            "role": "invalid role",
        }

        expected_message = role_not_valid

        with self.assertRaises(CopyException) as context:
            service.registration(data)

        self.assertEqual(context.exception.args[0], expected_message)
        self.assertEqual(context.exception.code, 400)
    
    @patch("app.services.user_authentication_service.mongo")
    @patch("app.services.user_authentication_service.check_if_user_exist")
    @patch("app.services.user_authentication_service.validate_number_of_practitioners")
    @patch("app.services.user_authentication_service.validate_practice_details_field")
    def test_successful_register_practice_details(
        self,
        mock_validate_practice_details_field,
        mock_validate_number_of_practitioners,
        mock_check_if_user_exist,
        mock_mongo,
    ):
        service = UserAuthenticationService()
        data = {
            "user_id": "67f2b4e8a1c9d23f4e5b6789",
            "main_phone_number": "+2348012345678",
            "website": "https://www.mypractice.com",
            "number_of_practitioners": "6-15 Practitioners",
            "insurance_plans": ["Blue Cross Blue Shield", "Aetna", "Cigna"],
        }

        mock_validate_number_of_practitioners.return_value = MagicMock(value="6-15 Practitioners")
        mock_collection = MagicMock()
        mock_mongo.db.practice_details = mock_collection

        service.register_practice_details(data)

        mock_validate_practice_details_field.assert_called_once_with(data)
        mock_validate_number_of_practitioners.assert_called_once_with(data)
        mock_check_if_user_exist.assert_called_once_with(data["user_id"])
        mock_collection.insert_one.assert_called_once()

    def test_empty_user_id_field(self):
        service = UserAuthenticationService()
        data = {
            "user_id": "",
            "main_phone_number": "+2348012345678",
            "website": "https://www.mypractice.com",
            "number_of_practitioners": "6-15 Practitioners",
            "insurance_plans": ["Aetna"],
        }

        with self.assertRaises(CopyException) as context:
            service.register_practice_details(data)

        self.assertEqual(context.exception.args[0], "user_id is required.")
        self.assertEqual(context.exception.code, 400)

    def test_empty_main_phone_number_field(self):
        service = UserAuthenticationService()
        data = {
            "user_id": "67f2b4e8a1c9d23f4e5b6789",
            "main_phone_number": "",
            "website": "https://www.mypractice.com",
            "number_of_practitioners": "6-15 Practitioners",
            "insurance_plans": ["Aetna"],
        }

        with self.assertRaises(CopyException) as context:
            service.register_practice_details(data)

        self.assertEqual(context.exception.args[0], "main_phone_number is required.")
        self.assertEqual(context.exception.code, 400)

    def test_invalid_main_phone_number_format(self):
        service = UserAuthenticationService()
        data = {
            "user_id": "67f2b4e8a1c9d23f4e5b6789",
            "main_phone_number": "abc123",
            "website": "https://www.mypractice.com",
            "number_of_practitioners": "6-15 Practitioners",
            "insurance_plans": ["Aetna"],
        }

        with self.assertRaises(CopyException) as context:
            service.register_practice_details(data)

        self.assertEqual(context.exception.args[0], "Number must be a valid numeric value")
        self.assertEqual(context.exception.code, 400)

    def test_empty_number_of_practitioners_field(self):
        service = UserAuthenticationService()
        data = {
            "user_id": "67f2b4e8a1c9d23f4e5b6789",
            "main_phone_number": "+2348012345678",
            "website": "https://www.mypractice.com",
            "number_of_practitioners": "",
            "insurance_plans": ["Aetna"],
        }

        with self.assertRaises(CopyException) as context:
            service.register_practice_details(data)

        self.assertEqual(context.exception.args[0], "number_of_practitioners is required.")
        self.assertEqual(context.exception.code, 400)

    def test_invalid_number_of_practitioners(self):
        service = UserAuthenticationService()
        data = {
            "user_id": "67f2b4e8a1c9d23f4e5b6789",
            "main_phone_number": "+2348012345678",
            "website": "https://www.mypractice.com",
            "number_of_practitioners": "invalid value",
            "insurance_plans": ["Aetna"],
        }

        with self.assertRaises(CopyException) as context:
            service.register_practice_details(data)

        self.assertEqual(context.exception.args[0], number_of_practitioners_not_valid)
        self.assertEqual(context.exception.code, 400)

    def test_empty_insurance_plans_field(self):
        service = UserAuthenticationService()
        data = {
            "user_id": "67f2b4e8a1c9d23f4e5b6789",
            "main_phone_number": "+2348012345678",
            "website": "https://www.mypractice.com",
            "number_of_practitioners": "6-15 Practitioners",
            "insurance_plans": [],
        }

        with self.assertRaises(CopyException) as context:
            service.register_practice_details(data)

        self.assertEqual(context.exception.args[0], "insurance_plans is required.")
        self.assertEqual(context.exception.code, 400)

    def test_insurance_plans_not_a_list(self):
        service = UserAuthenticationService()
        data = {
            "user_id": "67f2b4e8a1c9d23f4e5b6789",
            "main_phone_number": "+2348012345678",
            "website": "https://www.mypractice.com",
            "number_of_practitioners": "6-15 Practitioners",
            "insurance_plans": "Aetna",
        }

        with self.assertRaises(CopyException) as context:
            service.register_practice_details(data)

        self.assertEqual(context.exception.args[0], "insurance_plans must be a list")
        self.assertEqual(context.exception.code, 400)

    def test_null_number_of_practitioners_field(self):
        service = UserAuthenticationService()
        data = {
            "user_id": "67f2b4e8a1c9d23f4e5b6789",
            "main_phone_number": "+2348012345678",
            "website": "https://www.mypractice.com",
            "number_of_practitioners": "null",
            "insurance_plans": ["Aetna"],
        }

        with self.assertRaises(CopyException) as context:
            service.register_practice_details(data)

        self.assertEqual(context.exception.args[0], "number_of_practitioners is required.")
        self.assertEqual(context.exception.code, 400)

    @patch("app.services.user_authentication_service.check_if_user_exist")
    @patch("app.services.user_authentication_service.validate_practice_details_field")
    @patch("app.services.user_authentication_service.validate_number_of_practitioners")
    def test_user_does_not_exist(
        self,
        mock_validate_number_of_practitioners,
        mock_validate_practice_details_field,
        mock_check_if_user_exist,
    ):
        service = UserAuthenticationService()
        data = {
            "user_id": "nonexistent_user_id",
            "main_phone_number": "+2348012345678",
            "website": "https://www.mypractice.com",
            "number_of_practitioners": "6-15 Practitioners",
            "insurance_plans": ["Aetna"],
        }

        mock_validate_number_of_practitioners.return_value = MagicMock(value="6-15 Practitioners")
        mock_check_if_user_exist.side_effect = CopyException("User does not exist.", 404)

        with self.assertRaises(CopyException) as context:
            service.register_practice_details(data)

        self.assertEqual(context.exception.args[0], "User does not exist.")
        self.assertEqual(context.exception.code, 404)
    