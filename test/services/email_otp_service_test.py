import os
from unittest import TestCase
from unittest.mock import patch, mock_open, MagicMock
from app.exception.copy_exception import CopyException
from app.services.email_otp_service import EmailOTPService
from dotenv import load_dotenv
from datetime import datetime, timedelta


class EmailOtpServiceTest(TestCase):
    def test_generate_otp(self):
        load_dotenv()
        OTP_LENGTH = int(os.getenv('OTP_LENGTH'))
        email_otp_service = EmailOTPService()
        otp = email_otp_service.generate_otp()
        self.assertEqual(len(otp),OTP_LENGTH)
    
    @patch("app.services.email_otp_service.mongo")
    def test_store_otp(self,mock_mongo):
        data = {
                  "email_address" : "test@gmail.com",
                  "otp" : "123456"
               }
 
        mock_collection = MagicMock()
        mock_mongo.db.otps = mock_collection
        
        email_otp_service = EmailOTPService()

        email_otp_service.store_otp(data["email_address"],data["otp"])

        mock_collection.insert_one.assert_called_once()
    
    
    @patch("app.services.email_otp_service.load_dotenv") 
    @patch("app.services.email_otp_service.SendGridAPIClient")
    @patch("app.services.email_otp_service.os.getenv")
    @patch("builtins.open", new_callable=mock_open, read_data="<html>{{ otp }} expires in {{ expiry }} minutes</html>")
    def test_send_otp_email_success(self, mock_file, mock_getenv, mock_sendgrid_client, mock_dotenv):
        mock_getenv.return_value = "fake-api-key"

        mock_send_instance = MagicMock()
        mock_send_instance.send.return_value.status_code = 202
        mock_sendgrid_client.return_value = mock_send_instance
        email_otp_service = EmailOTPService()
        email_otp_service.send_otp_email("test@example.com", "123456")

        mock_file.assert_any_call("templates/otp_email_template.html", "r")
        mock_send_instance.send.assert_called_once()

  
    @patch("app.services.email_otp_service.SendGridAPIClient")
    @patch("app.services.email_otp_service.os.getenv")
    def test_send_otp_email_failure(self,mock_getenv, mock_sendgrid_client):
        mock_getenv.return_value = "fake-api-key"

        mock_send_instance = MagicMock()
        mock_send_instance.send.return_value.status_code = 500
        mock_sendgrid_client.return_value = mock_send_instance

        email_otp_service = EmailOTPService()


        with self.assertRaises(CopyException):
            email_otp_service.send_otp_email("test@example.com", "123456")
    
    @patch("app.services.email_otp_service.EmailOTPService.send_otp_email")
    @patch("app.services.email_otp_service.EmailOTPService.store_otp")
    @patch("app.services.email_otp_service.EmailOTPService.generate_otp")
    @patch("app.services.email_otp_service.os.getenv")
    @patch("app.services.email_otp_service.SendGridAPIClient")
    def test_send_and_store_otp(
        self,
        mock_sendgrid_client,
        mock_getenv,
        mock_generate_otp,
        mock_store_otp,
        mock_send_otp_email,
    ):
        mock_generate_otp.return_value = "123456"
        mock_store_otp.return_value = {
            "email_address": "test@gmail.com",
            "otp": "123456"
        }
        mock_getenv.return_value = "fake-api-key"

        mock_send_instance = MagicMock()
        mock_send_instance.send.return_value.status_code = 202
        mock_sendgrid_client.return_value = mock_send_instance

        email_otp_service = EmailOTPService()
        email_otp_service.send_and_store_otp("test@gmail.com")

        mock_generate_otp.assert_called_once()
        mock_store_otp.assert_called_once_with("test@gmail.com", "123456")
        mock_send_otp_email.assert_called_once_with("test@gmail.com", "123456")
    
   
    @patch("app.services.email_otp_service.find_otp_by_otp_and_email")
    @patch("app.repository.otp_repository.mongo")
    def test_verify_otp(self, mock_mongo,mock_find_otp_by_otp_and_email):
        future_time = datetime.now() + timedelta(minutes=5)
        data = {
            "_id": "some_dummy_id", 
            "email_address": "test@gmail.com",
            "otp": "3456789",
            "expires_at": future_time
        }

        mock_find_otp_by_otp_and_email.return_value = data
        mock_mongo.db.otps.delete_one.return_value = None 

        email_otp_service = EmailOTPService()
        result = email_otp_service.verify_otp(data["email_address"], data["otp"])

        mock_find_otp_by_otp_and_email.assert_called_once_with(data["email_address"], data["otp"])
        assert result is True 
    
    @patch("app.services.email_otp_service.find_otp_by_otp_and_email")
    def test_verify_otp_when_time_has_expired(self,mock_find_otp_by_otp_and_email):
        future_time = datetime.now() - timedelta(minutes=5)
        data = {
            "_id": "some_dummy_id", 
            "email_address": "test@gmail.com",
            "otp": "3456789",
            "expires_at": future_time
        }

        mock_find_otp_by_otp_and_email.return_value = data
       

        email_otp_service = EmailOTPService()
        result = email_otp_service.verify_otp(data["email_address"], data["otp"])

        mock_find_otp_by_otp_and_email.assert_called_once_with(data["email_address"], data["otp"])
        assert result is False 
    
        
    @patch("app.services.email_otp_service.update_user_to_verified")
    @patch("app.services.email_otp_service.EmailOTPService.verify_otp")
    @patch("app.services.email_otp_service.verify_otp_field")
    def test_check_if_otp_is_verify_and_update_user_is_verified_success(
            self,
            mock_verify_otp_field,
            mock_verify_otp,
            mock_update_user_to_verified,
        ):
            data = {
                "email_address": "test@gmail.com",
                "otp": "2345678"
            }
            mock_verify_otp.return_value = True

            EmailOTPService.check_if_otp_is_verify_and_update_user_is_verified(data)

            mock_verify_otp_field.assert_called_once_with("test@gmail.com", "2345678")
            mock_verify_otp.assert_called_once_with("test@gmail.com", "2345678")
            mock_update_user_to_verified.assert_called_once_with("test@gmail.com")
    


    @patch("app.services.email_otp_service.EmailOTPService.verify_otp")
    def test_check_if_otp_is_verify_and_update_user_is_verified_failure(
            self,
            mock_verify_otp,
        ):
            data = {
                "email_address": "test@gmail.com",
                "otp": "2345678"
            }
            mock_verify_otp.return_value = False

            with self.assertRaises(CopyException):
             EmailOTPService.check_if_otp_is_verify_and_update_user_is_verified(data)
    

    def test_check_if_otp_is_verify_and_update_user_is_verified_when_email_address_is_not_provided_will_fail(
            self,
        ):
            data = {
                "email_address": "",
                "otp": "2345678"
            }

            with self.assertRaises(CopyException):
             EmailOTPService.check_if_otp_is_verify_and_update_user_is_verified(data)


    def test_check_if_otp_is_verify_and_update_user_is_verified_when_email_address_is_not_provided_will_fail_key2(
            self,
        ):
            data = {
                "otp": "2345678"
            }

            with self.assertRaises(CopyException):
             EmailOTPService.check_if_otp_is_verify_and_update_user_is_verified(data)


    def test_check_if_otp_is_verify_and_update_user_is_verified_when_email_address_is_null_will_fail(
            self,
        ):
            data = {
                "email_address": "null",
                "otp": "2345678"
            }

            with self.assertRaises(CopyException):
             EmailOTPService.check_if_otp_is_verify_and_update_user_is_verified(data)
 
    def test_check_if_otp_is_verify_and_update_user_is_verified_when_email_address_is_Null_will_fail(
            self,
        ):
            data = {
                "email_address": "Null",
                "otp": "2345678"
            }

            with self.assertRaises(CopyException):
             EmailOTPService.check_if_otp_is_verify_and_update_user_is_verified(data)

    def test_check_if_otp_is_verify_and_update_user_is_verified_when_otp_is_not_provided_will_fail(
            self,
        ):
            data = {
                "email_address": "test@gmail.com",
                "otp": ""
            }

            with self.assertRaises(CopyException):
             EmailOTPService.check_if_otp_is_verify_and_update_user_is_verified(data)
    
    def test_check_if_otp_is_verify_and_update_user_is_verified_when_otp_key_and_value_is_not_provided_will_fail(
            self,
        ):
            data = {
                "email_address": "test@gmail.com",
            }

            with self.assertRaises(CopyException):
             EmailOTPService.check_if_otp_is_verify_and_update_user_is_verified(data)

    def test_check_if_otp_is_verify_and_update_user_is_verified_when_otp_is_null_will_fail(
            self,
        ):
            data = {
                "email_address": "test@gmail.com",
                "otp": "null"
            }

            with self.assertRaises(CopyException):
             EmailOTPService.check_if_otp_is_verify_and_update_user_is_verified(data)

    def test_check_if_otp_is_verify_and_update_user_is_verified_when_otp_is_Null_will_fail(
            self,
        ):
            data = {
                "email_address": "test@gmail.com",
                "otp": "Null"
            }

            with self.assertRaises(CopyException):
             EmailOTPService.check_if_otp_is_verify_and_update_user_is_verified(data)
    

    @patch("app.services.email_otp_service.get_user_by_email_address")
    @patch("app.services.email_otp_service.EmailOTPService.send_and_store_otp")
    @patch("app.services.email_otp_service.validate_email_not_empty")
    @patch("app.services.email_otp_service.validate_email")
    def test_resend_otp(self,mock_db,mock_send_otp,mock_validate_email_not_empty,mock_validate_email):
        pass





