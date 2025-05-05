from ..exception.copy_exception import CopyException
from ..models.enum.user_role import UserRole
from ..constant.error_message import *

def validate_registration_field(data: dict):
    required_fields = ['first_name', 'last_name', 'email_address', 'phone_number', 'password', 'role']

    missing_fields = [field for field in required_fields if not data.get(field) or not str(data[field]).strip()]
    
    if missing_fields:
       raise CopyException(required_field["required_field"](missing_fields[0]),400)

def validate_user_role(data:dict):
     try:
            role = UserRole(data["role"].lower())
            return role
     except ValueError:
            raise CopyException(role_not_valid,400)
   