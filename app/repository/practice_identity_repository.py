from .. import mongo


def find_identity_by_user_id(user_id):
    return mongo.db.practice_identities.find_one({
        "user_id": user_id
    })
