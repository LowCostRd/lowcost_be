from ..constant.error_message import *
from app.exception.copy_exception import CopyException
from app.repository.practice_identity_repository import find_identity_by_user_id


def check_if_practice_identity_exists(user_id: str):
    identity = find_identity_by_user_id(user_id)

    if identity:
        raise CopyException(practice_identity_found_by_user, 409)