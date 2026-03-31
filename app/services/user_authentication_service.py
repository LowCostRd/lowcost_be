from venv import logger

from app.exception.email_delivery_exception import EmailDeliveryException
import logging
import time
from app.utils.network_utils import has_internet_connection
from app.exception.email_delivery_exception import EmailDeliveryException

logger = logging.getLogger(__name__)

MAX_RETRIES = 3
RETRY_DELAY = 2

from ..interfaces.user_authentication import UserAuthentication
from ..models.user import User
from .. import mongo
from ..validation.field_validation import *
from ..constant.success_message import *
from ..validation.validate_email_address import *
from ..models.enum.user_role import UserRole
from ..bycrypt import  hash_password
from .email_otp_service import EmailOTPService


class UserAuthenticationService(UserAuthentication):
     def registration(self, data: dict) -> dict:
         email_address = data.get("email_address")
         password = data.get('password')


         validate_registration_field(data)
         role = validate_user_role(data)
  
         
         validate_email(email_address)
         validate_password(password)
         check_if_email_address_exist(email_address)

         hashed_password = hash_password(password)
     

         data["role"] = role
         data["password"] = hashed_password
         user = User(**data)
         mongo.db.users.insert_one(user.to_dict())

         self._attempt_send_otp(email_address)

    

     def _attempt_send_otp(self, email_address: str) -> None:
       for attempt in range(1, MAX_RETRIES + 1):
        if not has_internet_connection():
            logger.warning(f"No internet connection. Attempt {attempt}/{MAX_RETRIES}. Retrying in {RETRY_DELAY}s...")
            time.sleep(RETRY_DELAY)
            continue

        try:
            EmailOTPService.send_and_store_otp(email_address)
            return  # ✅ success, exit early
        except Exception as e:
            logger.error(f"OTP send failed for {email_address} on attempt {attempt}/{MAX_RETRIES}: {e}")
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_DELAY)

    # All retries exhausted
       raise EmailDeliveryException(email_address)




         
