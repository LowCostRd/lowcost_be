from flask import Blueprint,request,jsonify

from app.utils.success_builder import build_response
from ..services.email_otp_service import EmailOTPService
from ..constant.success_message import otp_verification_message



email_verification_bp = Blueprint('email_verification', __name__)
email_otp_service = EmailOTPService()

@email_verification_bp.route("/v1/api/verify_otp",methods=['POST'])
def verify_user_otp():
    data = request.get_json()
    email_otp_service.check_if_otp_is_verify_and_update_user_is_verified(data)
    json_response =  build_response(otp_verification_message,200)
    return jsonify(json_response),200

@email_verification_bp.route("/v1/api/resend_otp",methods=['PATCH'])
def resend_otp():
    data = request.get_json()
    response = email_otp_service.resend_otp(data)
    json_response = build_response(response,200)
    return jsonify(json_response),200




