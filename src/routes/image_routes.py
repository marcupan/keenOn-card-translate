from flask import Blueprint, request, jsonify, send_file
from src.utils.image_processing import generate_image

image_bp = Blueprint('image_bp', __name__)


@image_bp.route('/generate', methods=['POST'])
def generate_image_route():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify(error="Prompt is required"), 400

    image_file = generate_image(prompt)
    if not image_file:
        return jsonify(error="Failed to generate image"), 500

    return send_file(image_file, mimetype='image/png')
