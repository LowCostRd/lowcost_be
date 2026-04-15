from datetime import datetime
import uuid


class Compliance:
    def __init__(self, user_id, business_associate_agreement: bool, terms_of_service: bool, data_processing_agreement: bool, practice_information_accuracy: bool):
        self._id = str(uuid.uuid4())
        self.user_id = user_id
        self.business_associate_agreement = business_associate_agreement
        self.terms_of_service = terms_of_service
        self.data_processing_agreement = data_processing_agreement
        self.practice_information_accuracy = practice_information_accuracy
        self.created_at = datetime.now()

    def to_dict(self):
        return {
            "_id": self._id,
            "user_id": self.user_id,
            "business_associate_agreement": self.business_associate_agreement,
            "terms_of_service": self.terms_of_service,
            "data_processing_agreement": self.data_processing_agreement,
            "practice_information_accuracy": self.practice_information_accuracy,
            "created_at": self.created_at
        }