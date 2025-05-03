from flask import Blueprint,request,jsonify
from ..services.user_authentication_service import UserAuthenticationService
from ..exception.copy_exception import CopyException

auth_bp = Blueprint('authentication', __name__)
user_service = UserAuthenticationService()

@auth_bp.route('/register',methods=['POST'])
def register_user():
    data = request.get_json()

    try:
        response = user_service.registration(data)
        return jsonify(response), 201
    except CopyException as e:
        return jsonify(e.to_dict()), 400

    
