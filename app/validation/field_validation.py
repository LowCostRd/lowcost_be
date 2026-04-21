import os
import re

from app.models.enum.number_of_practitioners import NumberOfPractitioners
from ..exception.copy_exception import CopyException
from ..models.enum.job_title import JobTitle
from ..constant.error_message import *
from dotenv import load_dotenv
from .. import mongo

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


def validate_business_number(number: str, current_user_id: str):

    existing_identity = mongo.db.practice_identities.find_one({"number": number})
    
    if existing_identity:
        if existing_identity.get("user_id") != current_user_id:
            raise CopyException(reg_number_exist, 409)


def validate_practice_field(data: dict):
    required_fields = ['user_id', 'name', 'number', 'country', 'state']

    missing_fields = [field for field in required_fields if not data.get(field) or not str(data[field]).strip() or str(data[field]).strip().lower() == "null"]
    
    if missing_fields:
       raise CopyException(required_field["required_field"](missing_fields[0]), 400)
    
    validate_business_number(data.get("number"), data.get("user_id"))

     

def validate_number(value):
    if not value or not str(value).strip() or str(value).strip().lower() == "null":
        raise CopyException("Number is required", 400)

    cleaned = str(value).strip()
    
    number_to_check = cleaned[1:] if cleaned.startswith("+") else cleaned
    
    if not number_to_check.isdigit():
        raise CopyException("Number must be a valid numeric value", 400)
    
    if len(cleaned) < 7 or len(cleaned) > 15:
        raise CopyException("Number must be between 7 and 15 digits", 400)
     

def validate_number_of_practitioners(data:dict):
     try:
            number_of_practitioners = NumberOfPractitioners(data["number_of_practitioners"])
            return number_of_practitioners
     except ValueError:
            raise CopyException(number_of_practitioners_not_valid,400)  


def validate_practice_details_field(data: dict):
    required_fields = ['user_id', 'main_phone_number', 'number_of_practitioners', 'insurance_plans']

    missing_fields = [field for field in required_fields if not data.get(field) or not str(data[field]).strip() or str(data[field]).strip().lower() == "null"]
    
    if missing_fields:
        raise CopyException(required_field["required_field"](missing_fields[0]), 400)

    insurance_plans = data.get("insurance_plans")
    if not isinstance(insurance_plans, list):
        raise CopyException("insurance_plans must be a list", 400)
    
    if len(insurance_plans) == 0:
        raise CopyException("insurance_plans cannot be empty", 400)

    validate_number(data.get("main_phone_number"))


def validate_agreement_field(data: dict):
    required_fields = ['user_id', 'business_associate_agreement', 'terms_of_service', 'data_processing_agreement', 'practice_information_accuracy']
    required_agreement_fields = ['business_associate_agreement', 'terms_of_service', 'data_processing_agreement','practice_information_accuracy']

    missing_fields = [field for field in required_fields if field not in data]
    
    if missing_fields:
        raise CopyException(required_field["required_field"](missing_fields[0]), 400)

    for field in required_fields[1:]:
        if not isinstance(data[field], bool):
            raise CopyException(f"{field} must be a boolean value", 400)

   
    for field in required_agreement_fields:
        if not data[field]:
            raise CopyException(f"{field} must be true", 400)