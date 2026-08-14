from datetime import datetime
import uuid

from app.models.enum.number_of_practitioners import NumberOfPractitioners


class Waitlist:
    def __init__(self,name,role,email_address,hospital_name,country,specialty, number_of_practitioners: NumberOfPractitioners,challenge:None, _id=None, created_at=None):
         self._id = _id or str(uuid.uuid4())
         self.name= name
         self.role = role
         self.email_address = email_address
         self.hospital_name = hospital_name
         self.country = country
         self.specialty = specialty
         self.number_of_practitioners = number_of_practitioners
         self.challenge = challenge or []
         self.created_at = created_at or datetime.now()
         self.updated_at = datetime.now()

    
    def to_dict(self):
        return {
            "_id": self._id,
            "name" : self.name,
            "role" : self.role,
            "email_address" : self.email_address,
            "hospital_name" : self.hospital_name,
            "country" : self.country,
            "specialty" : self.specialty,
            "number_of_practitioners": self.number_of_practitioners.value,
            "challenge": self.challenge,
            "created_at": self.created_at,
            "updated_at": self.updated_at

        }