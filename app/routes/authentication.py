from flask import Blueprint,request,jsonify
from ..services.user_authentication_service import UserAuthenticationService
from ..utils.success_builder import build_response
from ..constant.success_message import *


auth_bp = Blueprint('authentication', __name__)
user_service = UserAuthenticationService()

@auth_bp.route('/register',methods=['POST'])
def register_user():
    data = request.get_json()
    user_service.registration(data)
    json_response =  build_response(registration_message,201)
    return jsonify(json_response), 201



@auth_bp.route('/register_practice_identity',methods=['POST'])
def register_practice_identity():
    data = request.get_json()
    user_service.register_practice_identity(data)
    json_response =  build_response(practice_identity_registration_message,201)
    return jsonify(json_response), 201


    
