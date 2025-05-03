import uuid
from datetime import datetime

class User:
    def __init__(self, first_name, last_name, email_address, phone_number, password, organization_name=None):
        self._id = str(uuid.uuid4())
        self.first_name = first_name
        self.last_name = last_name
        self.email_address = email_address
        self.phone_number = phone_number
        self.password = password
        self.organization_name = organization_name or ""
        self.created_at = datetime.now()

    def to_dict(self):
        return {
            "_id": self._id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email_address": self.email_address,
            "phone_number": self.phone_number,
            "password": self.password,
            "organization_name": self.organization_name,
            "created_at": self.created_at
        }
