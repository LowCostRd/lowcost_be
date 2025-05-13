import os
import random
from datetime import datetime, timedelta
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from app.exception.copy_exception import CopyException
from app.repository.user_repository import *
from app.validation.field_validation import verify_otp_field
from .. import mongo
from dotenv import load_dotenv
from ..repository.otp_repository import *
from ..constant.error_message import *
from app.models.otp import Otp
from app.validation.validate_email_address import *
from app.constant.success_message import otp_resent


class EmailOTPService:
    load_dotenv()
    OTP_LENGTH = int(os.getenv('OTP_LENGTH'))
    OTP_EXPIRY_MINUTES = int(os.getenv('OTP_EXPIRY_MINUTES'))
    FROM_EMAIL = os.getenv('FROM_EMAIL')

    @classmethod
    def generate_otp(cls) -> str:
        return ''.join([str(random.randint(0, 9)) for _ in range(cls.OTP_LENGTH)])
       

    @classmethod
    def store_otp(cls, email: str, otp: str):
        minutes=cls.OTP_EXPIRY_MINUTES
        otp = Otp(email,otp,minutes)
        mongo.db.otps.insert_one(otp.to_dict())

    @classmethod
    def send_otp_email(cls, to_email: str, otp: str):
        with open("templates/otp_email_template.html", "r") as file:
            template = file.read()
            html_content = template.replace("{{ otp }}", otp).replace("{{ expiry }}", str(cls.OTP_EXPIRY_MINUTES))

        message = Mail(
            from_email=cls.FROM_EMAIL,
            to_emails=to_email,
            subject='Your OTP Code',
            html_content= html_content)
        try:
            load_dotenv()
            sg = SendGridAPIClient(api_key=os.getenv('SENDGRID_API_KEY'))
            response = sg.send(message)
            if response.status_code not in range(200, 300):
                raise CopyException(otp_failed_to_send, response.status_code)
        except Exception as e:
            raise CopyException(email_failed_to_send_otp, e.code)

    @classmethod
    def send_and_store_otp(cls, email: str):
        otp = cls.generate_otp()
        cls.store_otp(email, otp)
        cls.send_otp_email(email, otp)
    
    @classmethod
    def verify_otp(cls, email: str, otp: str) -> bool:
        record = find_otp_by_otp_and_email(email,otp)

        if not record:
            return False

        if record.get("expires_at") < datetime.now():
            return False
        
        delete_otp(record)
        
        return True
    
    @classmethod
    def check_if_otp_is_verify_and_update_user_is_verified(cls,data:dict):
     email = data.get("email_address")
     otp = data.get("otp")

     verify_otp_field(email,otp)
     is_verified = EmailOTPService.verify_otp(email, otp)

     if not is_verified:
        raise CopyException(invalid_otp,400)
    
     update_user_to_verified(email)

    @classmethod
    def resend_otp(cls, data)->str:
        email_address = data.get("email_address")
    
        validate_email_not_empty(email_address)
        validate_email(email_address)

        user = get_user_by_email_address(email_address)

        if not user:
            raise CopyException(user_not_found, 404)

        if user.get("is_verified") is False:
            EmailOTPService.send_and_store_otp(email_address)
            return  f"{ otp_resent["message"](email_address)}"
       
        else:
            raise CopyException(user_is_verified,409)
        

         

