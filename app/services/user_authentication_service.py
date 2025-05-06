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


         if role == UserRole.ORGANIZATION:
           validate_organization_name(data)
   
         
         validate_email(email_address)
         validate_password(password)
         check_if_email_address_exist(email_address)

         hashed_password = hash_password(password)
     

         data["role"] = role
         data["password"] = hashed_password
         user = User(**data)
         mongo.db.users.insert_one(user.to_dict())

         EmailOTPService.send_and_store_otp(email_address)





         
