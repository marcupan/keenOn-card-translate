import grpc
import openai
import json
from src.proto import translation_pb2, translation_pb2_grpc
from src.config import Config
from src.utils.logger import logger

class TranslationService(translation_pb2_grpc.TranslationServiceServicer):
    def __init__(self):
        openai.api_key = Config.OPENAI_API_KEY
        self.openai_timeout = 60

    def Translate(self, request, context):
        chinese_word = request.chinese_word
        individual_translations = []
        example_sentences = []
        translation = ""

        try:
            prompt_content = f"""
            Translate the following Chinese word: '{chinese_word}'.
            Provide the response as a JSON object with the following keys:
            - "translation": The English translation (string).
            - "breakdown": An array of strings, where each string describes a character and its meaning.
            - "examples": An array of strings, containing two example sentences using the word.

            Example JSON format:
            {{
              "translation": "Hello",
              "breakdown": ["你 (nǐ): you", "好 (hǎo): good"],
              "examples": ["你好吗？ (Nǐ hǎo ma?) - How are you?", "他是一个好人。(Tā shì yī ge hǎo rén.) - He is a good person."]
            }}

            Generate the JSON for the word '{chinese_word}':
            """

            logger.info(f"Sending request to OpenAI for word: {chinese_word}")
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that provides translations in JSON format."},
                    {"role": "user", "content": prompt_content}
                ],
                max_tokens=400,
                temperature=0.5,
                request_timeout=self.openai_timeout
            )
            raw_response_text = response.choices[0].message['content'].strip()
            logger.info(f"Raw response from OpenAI:\n{raw_response_text}")

            try:
                json_start = raw_response_text.find('{')
                json_end = raw_response_text.rfind('}') + 1
                if json_start != -1 and json_end != -1:
                    json_string = raw_response_text[json_start:json_end]
                    parsed_data = json.loads(json_string)
                else:
                    raise ValueError("Could not find JSON object in the response")

                translation = parsed_data.get("translation", "")
                individual_translations = parsed_data.get("breakdown", [])
                example_sentences = parsed_data.get("examples", [])

                if not translation:
                    logger.warning("Translation field was empty in the parsed JSON.")
                if not individual_translations:
                    logger.warning("Breakdown field was empty in the parsed JSON.")
                if not example_sentences:
                    logger.warning("Examples field was empty in the parsed JSON.")


            except (json.JSONDecodeError, ValueError, KeyError) as e:
                logger.error(f"Failed to parse JSON response from OpenAI: {str(e)}. Raw response was: {raw_response_text}")
                context.set_details(f'Failed to parse OpenAI response: {str(e)}')
                context.set_code(grpc.StatusCode.INTERNAL)
                return translation_pb2.TranslationResponse()


        except openai.error.Timeout as e:
            logger.error(f"OpenAI request timed out: {str(e)}")
            context.set_details(f'OpenAI request timed out: {str(e)}')
            context.set_code(grpc.StatusCode.DEADLINE_EXCEEDED)
            return translation_pb2.TranslationResponse()
        except openai.error.OpenAIError as e:
            logger.error(f"OpenAI API error: {str(e)}")
            context.set_details(f'OpenAI API error: {str(e)}')
            context.set_code(grpc.StatusCode.INTERNAL)
            return translation_pb2.TranslationResponse()
        except Exception as e:
            logger.error(f"Translation failed unexpectedly: {str(e)}", exc_info=True)
            context.set_details(f'Internal server error during translation: {str(e)}')
            context.set_code(grpc.StatusCode.INTERNAL)
            return translation_pb2.TranslationResponse()

        logger.info(f"Successfully translated '{chinese_word}'. Sending response.")
        return translation_pb2.TranslationResponse(
            translation=translation,
            individual_translations=individual_translations,
            example_sentences=example_sentences
        )
