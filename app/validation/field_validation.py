from ..exception.copy_exception import CopyException
from ..models.enum.user_role import UserRole
from ..constant.error_message import *

def validate_registration_field(data: dict):
    required_fields = ['first_name', 'last_name', 'email_address', 'phone_number', 'password', 'role']

    for field in required_fields:
            if not data.get(field):
                raise CopyException(required_field["required_field"](field),400)

def validate_user_role(data:dict):
     try:
            role = UserRole(data["role"].lower())
            return role
     except ValueError:
            raise CopyException(role_not_valid,400)
   