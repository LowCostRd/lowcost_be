import uuid
from datetime import datetime
from .enum.user_role import UserRole

class User:
    def __init__(self, first_name, last_name, email_address, phone_number, password, role:UserRole, organization_name=None):
        
        self._id = str(uuid.uuid4())
        self.first_name = first_name
        self.last_name = last_name
        self.email_address = email_address
        self.phone_number = phone_number
        self.password = password
        self.role = role
        self.organization_name = organization_name or ""
        self.created_at = datetime.now()
        self.is_verified = False

    def to_dict(self):
        return {
            "_id": self._id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email_address": self.email_address,
            "phone_number": self.phone_number,
            "password": self.password,
            "role" : self.role.value,
            "organization_name": self.organization_name,
            "is_verified" : self.is_verified,
            "created_at": self.created_at,
        }
