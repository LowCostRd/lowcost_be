from .extensions import mongo

def insert_users():
    users = mongo.db.users
    if users.count_documents({}) == 0:
        default_user = {
            "first_name": "default first name",
            "last_name": "default last name",
            "email_address": "default1@gmail.com",
            "phone_number": "090789393",
            "password": "default@2025",
            "role": "personal",
            "organization_name": "default organization name"
        }
        users.insert_one(default_user)
        print("Seeded default user.")
    else:
        print("Users already exist. Skipping seeding.")
