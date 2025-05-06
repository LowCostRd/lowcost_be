import re
import os
from ..repository.user_repository import *
from ..exception.copy_exception import CopyException
from ..constant.error_message import *
from dotenv import load_dotenv


def check_if_email_address_exist(email_address : str):

    user = get_user_by_email_address(email_address)

    if user :
        raise CopyException(email_address_exist,409)

def validate_email(email_address : str):
    load_dotenv()
    email_format = os.getenv("EMAIL_REGEX")
    email_regex = rf"{email_format}"

    if not re.match(email_regex,email_address):
        raise CopyException(invalid_email_format, 400)



  

