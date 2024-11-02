import requests
from src.config import Config


def translate_text(chinese_word):
    api_key = Config.HUGGINGFACE_API_KEY
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {"inputs": chinese_word}
    response = requests.post("https://api-inference.huggingface.co/models/Helsinki-NLP/opus-mt-zh-en", headers=headers,
                             json=payload)

    if response.status_code != 200:
        print(f"Failed to translate Chinese to English: {response.status_code} {response.text}")
        return None

    translation_en = response.json()[0]['translation_text']
    uk_payload = {"inputs": translation_en}
    uk_response = requests.post("https://api-inference.huggingface.co/models/Helsinki-NLP/opus-mt-en-uk",
                                headers=headers, json=uk_payload)

    if uk_response.status_code != 200:
        print(f"Failed to translate English to Ukrainian: {uk_response.status_code} {uk_response.text}")
        return None

    return uk_response.json()[0]['translation_text']


def translate_individual_characters(chinese_word):
    api_key = Config.HUGGINGFACE_API_KEY
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    individual_translations = []

    for char in chinese_word:
        char_payload = {"inputs": char}
        char_response = requests.post("https://api-inference.huggingface.co/models/Helsinki-NLP/opus-mt-zh-en",
                                      headers=headers, json=char_payload)
        if char_response.status_code == 200:
            char_translation = char_response.json()[0]['translation_text']
            uk_payload = {"inputs": char_translation}
            uk_response = requests.post("https://api-inference.huggingface.co/models/Helsinki-NLP/opus-mt-en-uk",
                                        headers=headers, json=uk_payload)
            if uk_response.status_code == 200:
                uk_translation = uk_response.json()[0]['translation_text']
                individual_translations.append({"character": char, "translation": uk_translation})
            else:
                print(
                    f"Failed to translate individual character to Ukrainian: {uk_response.status_code} {uk_response.text}")
                individual_translations.append({"character": char, "translation": char_translation})
        else:
            print(
                f"Failed to translate individual character to English: {char_response.status_code} {char_response.text}")
            individual_translations.append({"character": char, "translation": "Translation failed"})

    return individual_translations
