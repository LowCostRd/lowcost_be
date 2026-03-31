from ..constant.error_message import *
from app.exception.copy_exception import CopyException
from app.repository.user_repository import get_user_by_id


def check_if_user_exist(user_id : str):

    user = get_user_by_id(user_id)

    if not user:
            raise CopyException(user_not_found, 404)
    
    if not user.get("is_verified"):
        raise CopyException(user_is_not_verified, 400)
