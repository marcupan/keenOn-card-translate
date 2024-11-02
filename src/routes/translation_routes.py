from flask import Blueprint, request, jsonify
from src.utils.translate_processing import translate_text, translate_individual_characters

translation_bp = Blueprint('translation_bp', __name__)


@translation_bp.route('/generate-translate', methods=['POST'])
def translate_route():
    data = request.get_json()
    chinese_word = data.get('chinese_word')
    if not chinese_word:
        return jsonify(error="Chinese word is required"), 400

    # TODO: Remove when API ready
    # translation_uk = translate_text(chinese_word)
    # individual_translations = translate_individual_characters(chinese_word)

    translation_uk = "text"
    individual_translations = []

    return jsonify({
        "translation": translation_uk,
        "individual_translations": individual_translations,
    })
