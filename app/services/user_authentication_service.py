from venv import logger

from app.exception.email_delivery_exception import EmailDeliveryException
import logging
import time
from app.models.compliance import Compliance
from app.models.practice_details import PracticeDetails
from app.models.practice_identity import PracticeIdentity
from app.utils.network_utils import has_internet_connection
from app.exception.email_delivery_exception import EmailDeliveryException
from datetime import datetime


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MAX_RETRIES = 3
RETRY_DELAY = 2

from ..interfaces.user_authentication import UserAuthentication
from ..models.user import User
from .. import mongo
from ..validation.field_validation import *
from ..constant.success_message import *
from ..validation.validate_email_address import *
from ..validation.validate_user import *
from ..validation.validate_practise_identity import *
from ..models.enum.user_role import UserRole
from ..bycrypt import  hash_password
from .email_otp_service import EmailOTPService
from ..repository.user_repository import *



class UserAuthenticationService(UserAuthentication):
     
     def registration(self, data: dict) -> dict:
        email_address = data.get("email_address").strip().lower()
        password = data.get('password')

      
        validate_registration_field(data)
        role = validate_user_role(data)
        validate_email(email_address)
        validate_password(password)

       
        existing_user_doc = mongo.db.users.find_one({"email_address": email_address})

        if existing_user_doc:
            if existing_user_doc.get("is_verified"):
                raise CopyException(account_exist, 404) 

            hashed_password = hash_password(password)
            mongo.db.users.update_one(
                {"email_address": email_address},
                {
                    "$set": {
                        "full_name": data.get("full_name"),
                        "password": hashed_password,
                        "role": role.value,
                        "updated_at": datetime.now()
                    }
                }
            )
        else:
            
            hashed_password = hash_password(password)
            data["role"] = role
            data["password"] = hashed_password
            
            user = User(**data)
            mongo.db.users.insert_one(user.to_dict())

    
        self._attempt_send_otp(email_address)
    

     def register_practice_identity(self, data: dict) -> dict:
   
        validate_practice_field(data)

        user_id = data.get("user_id")
        check_if_user_exist(user_id)

       
        existing = mongo.db.practice_identities.find_one({"user_id": user_id})


        practice_identity = PracticeIdentity(
            user_id=user_id,
            name=data.get("name"),
            number=data.get("number"),
            country=data.get("country"),
            logo=data.get("logo"),
            state=data.get("state"),
            _id=existing["_id"] if existing else None,
            created_at=existing["created_at"] if existing else None
        )

       
        mongo.db.practice_identities.update_one(
            {"user_id": user_id},
            {"$set": practice_identity.to_dict()},
            upsert=True
        )



    
     def register_practice_details(self, data: dict) -> dict:
   
         validate_practice_details_field(data)
         number_of_practitioners = validate_number_of_practitioners(data)

         user_id = data.get("user_id")
         main_phone_number = data.get("main_phone_number")
         website = data.get("website")
         data["number_of_practitioners"] = number_of_practitioners
         insurance_plans = data.get("insurance_plans", [])


         check_if_user_exist(user_id)

         practice_details = PracticeDetails(
             user_id=user_id,
             main_phone_number=main_phone_number,
             website=website,
             number_of_practitioners=number_of_practitioners,
             insurance_plans=insurance_plans
         )

         mongo.db.practice_details.insert_one(practice_details.to_dict())
    
    
     def compliance_agreement(self, data: dict) -> dict:
       validate_agreement_field(data)

       user_id = data.get("user_id")
       business_associate_agreement = data.get("business_associate_agreement")
       terms_of_service = data.get("terms_of_service")
       data_processing_agreement = data.get("data_processing_agreement")
       practice_information_accuracy = data.get("practice_information_accuracy")

       check_if_user_exist(user_id)

       compliance = Compliance(
           user_id=user_id,
           business_associate_agreement=business_associate_agreement,
           terms_of_service=terms_of_service,
           data_processing_agreement=data_processing_agreement,
           practice_information_accuracy=practice_information_accuracy
           )
        
       mongo.db.compliance.insert_one(compliance.to_dict())
    
     def get_user_by_email_address(self, email_address: str) -> dict:
     
        if not email_address or not isinstance(email_address, str):
            raise CopyException("Email address is required", 400)

        validate_email(email_address)

        user = get_user_by_email_address(email_address)   

        if not user:
            raise CopyException(user_not_found, 404)   

        return user
    
     def get_user_by_id(self, user_id: str) -> dict:
     
        if not user_id or not isinstance(user_id, str):
            raise CopyException("User id is required", 400)


        user = get_user_by_id(user_id)   

        if not user:
            raise CopyException(user_not_found, 404)   

        return user


     def _attempt_send_otp(self, email_address: str) -> None:
       for attempt in range(1, MAX_RETRIES + 1):
        if not has_internet_connection():
            logger.warning(f"No internet connection. Attempt {attempt}/{MAX_RETRIES}. Retrying in {RETRY_DELAY}s...")
            time.sleep(RETRY_DELAY)
            continue

        try:
            EmailOTPService.send_and_store_otp(email_address)
            return 
        except Exception as e:
            logger.error(f"OTP send failed for {email_address} on attempt {attempt}/{MAX_RETRIES}: {e}")
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_DELAY)

  
       raise EmailDeliveryException(email_address)
     
    




         
