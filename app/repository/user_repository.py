from .. import mongo

def get_user_by_email_address(email_address:str):
    user = mongo.db.users.find_one({"email_address": email_address})
    return user