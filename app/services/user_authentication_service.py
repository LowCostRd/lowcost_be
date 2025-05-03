from ..interfaces.user_authentication import UserAuthentication
from ..models.user import User
from .. import mongo
from ..validation.field_validation import *
from ..constant.success_message import *
from ..validation.validate_email_address import check_if_email_address_exist


class UserAuthenticationService(UserAuthentication):
     def registration(self, data: dict) -> dict:
         validate_registration_field(data)
         role = validate_user_role(data)
         check_if_email_address_exist(data.get("email_address"))
         data["role"] = role
         user = User(**data)
         mongo.db.users.insert_one(user.to_dict())
         return {registration_message}
