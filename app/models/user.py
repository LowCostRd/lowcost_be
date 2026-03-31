import uuid
from datetime import datetime
from .enum.job_title import JobTitle

class User:
    def __init__(self, full_name,email_address,password, role:JobTitle):
        
        self._id = str(uuid.uuid4())
        self.full_name = full_name
        self.email_address = email_address
        self.password = password
        self.role = role
        self.created_at = datetime.now()
        self.is_verified = False

    def to_dict(self):
        return {
            "_id": self._id,
            "full_name": self.full_name,
            "email_address": self.email_address,
            "password": self.password,
            "role" : self.role.value,
            "is_verified" : self.is_verified,
            "created_at": self.created_at,
        }
