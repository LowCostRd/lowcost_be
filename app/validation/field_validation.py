import os
import re
from ..exception.copy_exception import CopyException
from ..models.enum.job_title import JobTitle
from ..constant.error_message import *
from dotenv import load_dotenv

def validate_registration_field(data: dict):
    required_fields = ['full_name', 'email_address', 'password', 'role']

    missing_fields = [field for field in required_fields if not data.get(field) or not str(data[field]).strip() or str(data[field]).strip().lower() == "null"]
    
    if missing_fields:
       raise CopyException(required_field["required_field"](missing_fields[0]),400)

def validate_user_role(data:dict):
     try:
            role = JobTitle(data["role"].lower())
            return role
     except ValueError:
            raise CopyException(role_not_valid,400)

def validate_password(password:str):
     load_dotenv()
     password_format = os.getenv("PASSWORD_REGEX")
     password_regex = rf'{password_format}'

     if not re.match(password_regex,password):
          raise CopyException(password_not_valid ,400)

def validate_organization_name(data: dict):
    organization_name = data.get("organization_name")
    if not organization_name or not organization_name.strip() or organization_name.strip().lower() == "null": 
        raise CopyException(organization_name_required, 400)

def verify_otp_field(email,otp):
    if not email or not otp or not email.strip() or not otp.strip() or email.strip().lower() == "null" or otp.lower() == "null":
        raise CopyException(email_and_otp_required,400)

          
          
     

     
   