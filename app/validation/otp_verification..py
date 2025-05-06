from app.exception.copy_exception import CopyException
from app.services.email_otp_service import EmailOTPService
from ..constant.error_message import invalid_otp


email_otp_service = EmailOTPService()

def check_if_otp_is_verified(email,otp):
    is_verified = EmailOTPService.verify_otp(email, otp)

    if not is_verified:
        raise CopyException(invalid_otp,400)