from datetime import datetime, timezone

class EmailDeliveryException(Exception):
    def __init__(self, email_address: str):
        super().__init__("Failed to deliver email after multiple attempts")
        self.email_address = email_address
        self.timestamp = datetime.now(timezone.utc)

    def to_dict(self):
        return {
            "success": True,   
            "email_sent": False,
            "error_message": "Registration successful but we couldn't send the OTP email after multiple attempts. "
                             "Please verify your internet connection and use the resend OTP option.",
            "status_code": 201,
            "time_stamp": self.timestamp.isoformat()
        }