from datetime import datetime
import uuid


class PracticeIdentity:
    def __init__(self,user_id,name,number,country,logo,state):
        self._id = str(uuid.uuid4())
        self.user_id = user_id
        self.name = name
        self.number = number
        self.country = country
        self.logo = logo
        self.state = state
        self.created_at = datetime.now()

    def to_dict(self):
        return {
            "_id": self._id,
            "user_id": self.user_id,
            "name": self.name,
            "number": self.number,
            "country": self.country,
            "logo": self.logo,
            "state": self.state,
            "created_at": self.created_at
        }