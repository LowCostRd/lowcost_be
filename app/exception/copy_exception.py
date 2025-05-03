from datetime import datetime

class CopyException(Exception):
    def __init__(self, message:str, code:int):
        super().__init__(message)
        self.message = message
        self.code = code 
        self.timestamp = datetime.now() 
    
    def to_dict(self):
        return {
            "error_message": self.message,
            "status_code": self.code,
            "time_stamp": self.timestamp.isoformat()
        }
