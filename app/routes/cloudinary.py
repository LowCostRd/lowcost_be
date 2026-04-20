from flask import Blueprint, request, jsonify
from ..services.cloudinary_service import CloudinaryService
from ..utils.success_builder import build_response
from ..constant.success_message import *


cloudinary_bp = Blueprint('cloudinary', __name__)
cloudinary_service = CloudinaryService()

@cloudinary_bp.route('/v1/api/delete-image', methods=['POST'])
def delete_organization_logo():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body is required"}), 400

    try:
        cloudinary_service.delete_image(data)
        json_response = build_response(delete_image_message, 201)
        return jsonify(json_response), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500