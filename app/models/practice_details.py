from datetime import datetime
import uuid

from app.models.enum.number_of_practitioners import NumberOfPractitioners


class PracticeDetails:
    def __init__(self,user_id,main_phone_number,website,number_of_practitioners: NumberOfPractitioners,insurance_plans:None):
         self._id = str(uuid.uuid4())
         self.user_id = user_id
         self.main_phone_number = main_phone_number
         self.website = website
         self.number_of_practitioners = number_of_practitioners
         self.insurance_plans = insurance_plans or []
         self.created_at = datetime.now()

    
    def to_dict(self):
        return {
            "_id": self._id,
            "user_id": self.user_id,
            "main_phone_number": self.main_phone_number,
            "website": self.website,
            "number_of_practitioners": self.number_of_practitioners.value,
            "insurance_plans": self.insurance_plans,
            "created_at": self.created_at

        }