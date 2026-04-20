from flask import Flask, request, jsonify
import cloudinary
import cloudinary.uploader
from ..interfaces.cloudinary import Cloudinary
import os


class CloudinaryService(Cloudinary):
    def __init__(self):
        cloudinary.config(
            cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
            api_key=os.getenv("CLOUDINARY_API_KEY"),
            api_secret=os.getenv("CLOUDINARY_API_SECRET"),
            secure=True
        )
    def delete_image(self, data):
        public_id = data.get('public_id')

        if not public_id:
            raise ValueError("public_id is required")
           
        result = cloudinary.uploader.destroy(public_id)
        return result
    

# @app.route('/api/delete-image', methods=['POST'])
# def delete_image():
#   data = request.get_json()
#   public_id = data.get('public_id')

#   if not public_id:
#     return jsonify({'error': 'public_id is required'}), 400

#   try:
#     result = cloudinary.uploader.destroy(public_id)
#     return jsonify({'result': result}), 200
#   except Exception as e:
#     return jsonify({'error': str(e)}), 500