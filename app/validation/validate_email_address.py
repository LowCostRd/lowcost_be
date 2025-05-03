from ..repository.user_repository import *
from ..exception.copy_exception import CopyException
from ..constant.error_message import email_address_exist


def check_if_email_address_exist(email_address : str):
    user = get_user_by_email_address(email_address)

    if user :
        raise CopyException(email_address_exist,409) 