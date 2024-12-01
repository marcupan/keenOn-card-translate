import grpc
import openai
from src.proto import translation_pb2, translation_pb2_grpc
from src.config import Config
from src.utils.logger import logger


class TranslationService(translation_pb2_grpc.TranslationServiceServicer):
    def __init__(self):
        openai.api_key = Config.OPENAI_API_KEY

    def Translate(self, request, context):
        chinese_word = request.chinese_word
        translations = []
        example_sentences = []

        try:
            # Use OpenAI to get translation and example sentences
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user",
                     "content": f"Translate the following Chinese word: '{chinese_word}'. Provide the translation, each character's meaning, and two example sentences using the word."}
                ],
                max_tokens=150
            )
            response_text = response.choices[0].message['content'].strip().split('\n')

            # Parse response
            translation = response_text[0]
            translations = response_text[1:len(chinese_word) + 1]
            example_sentences = response_text[len(chinese_word) + 1:]

        except Exception as e:
            logger.error(f"Translation failed: {str(e)}")
            context.set_details(f'Translation failed: {str(e)}')
            context.set_code(grpc.StatusCode.INTERNAL)
            return translation_pb2.TranslationResponse()

        return translation_pb2.TranslationResponse(
            translation=translation,
            individual_translations=translations,
            example_sentences=example_sentences
        )
