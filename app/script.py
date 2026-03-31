from .extensions import mongo

def insert_users():
    users = mongo.db.users
    if users.count_documents({}) == 0:
        default_user = {
            "full_name": "default full name",
            "email_address": "default1@gmail.com",
            "password": "default@2025",
            "role": "medical director",
        }
        users.insert_one(default_user)
        print("Seeded default user.")
    else:
        print("Users already exist. Skipping seeding.")
