from flask import Blueprint,request,jsonify
from ..models.user import User
from .. import mongo

auth_bp = Blueprint('authentication', __name__)

@auth_bp.route('/register',methods=['POST'])
def register_user():
    data = request.get_json()

    required_fields = ['first_name', 'last_name', 'email_address', 'phone_number', 'password']

    for field in required_fields:
        if not data.get(field):
            return jsonify({"error": f"{field} is required"}), 400
        
    user = User(**data)
    result = mongo.db.users.insert_one(user.to_dict())

    
    return jsonify({"id": str(result.inserted_id)}), 201