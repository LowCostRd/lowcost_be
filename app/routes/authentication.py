from flask import Blueprint,request,jsonify
from ..services.user_authentication_service import UserAuthenticationService
from ..utils.success_builder import build_response
from ..constant.success_message import *


auth_bp = Blueprint('authentication', __name__)
user_service = UserAuthenticationService()

@auth_bp.route('/v1/api/register',methods=['POST'])
def register_user():
    data = request.get_json()
    user_service.registration(data)
    json_response =  build_response(registration_message,201)
    return jsonify(json_response), 201



@auth_bp.route('/v1/api/register_practice_identity',methods=['POST'])
def register_practice_identity():
    data = request.get_json()
    user_service.register_practice_identity(data)
    json_response =  build_response(practice_identity_registration_message,201)
    return jsonify(json_response), 201



@auth_bp.route('/v1/ap1/register_practice_details',methods=['POST'])
def register_practice_details():
    data = request.get_json()
    user_service.register_practice_details(data)
    json_response =  build_response(practice_details_registration_message,201)
    return jsonify(json_response), 201


@auth_bp.route('/v1/api/register_compliance',methods=['POST'])
def register_compliance():
    data = request.get_json()
    user_service.compliance_agreement(data)
    json_response =  build_response(compliance_registration_message,201)
    return jsonify(json_response), 201


@auth_bp.route('/v1/api/users/by-email',methods=['GET'])
def get_user_by_email_address():
    data = request.get_json()
    email_address = data.get("email_address") if data else None
    user = user_service.get_user_by_email_address(email_address)
    json_response =  build_response(user, 200)
    return jsonify(json_response), 200