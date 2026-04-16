from .. import mongo

def get_user_by_email_address(email_address:str):
    user = mongo.db.users.find_one({"email_address": email_address}, {"password": 0})
    return user

def update_user_to_verified(email:str):
     mongo.db.users.update_one(
        {"email_address": email},
        {"$set": {"is_verified": True}}
    )

def get_user_by_id(user_id: str):
    user = mongo.db.users.find_one({"_id": user_id}, {"password": 0} )
    return user