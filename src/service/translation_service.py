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
        individual_translations = []
        example_sentences = []
        translation = ""

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user",
                     "content": f"Translate the following Chinese word: '{chinese_word}'. Provide the word's English translation, a breakdown of each character with meanings, and two example sentences using the word."}
                ],
                max_tokens=300
            )
            response_text = response.choices[0].message['content'].strip().split('\n')

            parsing_mode = None
            for line in response_text:
                line = line.strip()
                if line.startswith("Translation:"):
                    translation = line.split(': ')[-1].strip()
                    parsing_mode = None  # Reset parsing mode after translation
                elif line.startswith("Breakdown:"):
                    parsing_mode = "individual_translations"
                elif line.startswith("Example sentences:"):
                    parsing_mode = "example_sentences"
                elif parsing_mode == "individual_translations" and line:
                    individual_translations.append(line)
                elif parsing_mode == "example_sentences" and line:
                    example_sentences.append(line)

        except Exception as e:
            logger.error(f"Translation failed: {str(e)}")
            context.set_details(f'Translation failed: {str(e)}')
            context.set_code(grpc.StatusCode.INTERNAL)
            return translation_pb2.TranslationResponse()

        return translation_pb2.TranslationResponse(
            translation=translation,
            individual_translations=individual_translations,
            example_sentences=example_sentences
        )
