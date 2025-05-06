from datetime import datetime, timedelta
import uuid


class Otp:
    def __init__(self,email, otp,expiring_minutes):
        self.id = uuid.uuid4
        self.email = email
        self.otp = otp
        self.created_at = datetime.now()
        self.expires_at = datetime.now() + timedelta(minutes=expiring_minutes)
    
    def to_dict(self):
        return {
            "email_address": self.email,
            "otp": self.otp,
            "created_at": self.created_at,
            "expires_at": self.expires_at
        }