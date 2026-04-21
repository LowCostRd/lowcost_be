import uuid
from datetime import datetime
from .enum.job_title import JobTitle

class User:
    def __init__(self, full_name, email_address, password, role: JobTitle, is_verified=False, _id=None, created_at=None):
        self._id = _id or str(uuid.uuid4())
        self.full_name = full_name
        self.email_address = email_address
        self.password = password
        self.role = role
        self.is_verified = is_verified
        self.created_at = created_at or datetime.now()
        self.updated_at = datetime.now()

    def to_dict(self):
        return {
            "_id": self._id,
            "full_name": self.full_name,
            "email_address": self.email_address,
            "password": self.password,
            "role": self.role.value if isinstance(self.role, JobTitle) else self.role,
            "is_verified": self.is_verified,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }