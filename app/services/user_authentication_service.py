from ..interfaces.user_authentication import UserAuthentication
from ..models.user import User
from .. import mongo
from ..validation.field_validation import *
from ..constant.success_message import *
from ..validation.validate_email_address import *
from ..models.enum.user_role import UserRole


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


         data["role"] = role
         user = User(**data)
         mongo.db.users.insert_one(user.to_dict())
         return {registration_message}
