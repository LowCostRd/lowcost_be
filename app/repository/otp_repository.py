from .. import mongo

def find_otp_by_otp_and_email(email,otp):
   return mongo.db.otps.find_one({
            "email_address": email,
            "otp": otp
        })
    
def delete_otp(record):
    mongo.db.otps.delete_one({"_id": record["_id"]})