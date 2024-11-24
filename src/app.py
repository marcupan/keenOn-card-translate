from concurrent import futures
import grpc
from proto import translation_pb2
from proto import translation_pb2_grpc
import openai
import os
from grpc_reflection.v1alpha import reflection
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class TranslationService(translation_pb2_grpc.TranslationServiceServicer):
    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")

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
                    {"role": "user", "content": f"Translate the following Chinese word: '{chinese_word}'. Provide the translation, each character's meaning, and two example sentences using the word."}
                ],
                max_tokens=150
            )
            response_text = response.choices[0].message['content'].strip().split('\n')

            # Parse response
            translation = response_text[0]
            translations = response_text[1:len(chinese_word) + 1]
            example_sentences = response_text[len(chinese_word) + 1:]

        except Exception as e:
            context.set_details(f'Translation failed: {str(e)}')
            context.set_code(grpc.StatusCode.INTERNAL)
            return translation_pb2.TranslationResponse()

        return translation_pb2.TranslationResponse(
            translation=translation,
            individual_translations=translations,
            example_sentences=example_sentences
        )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    translation_pb2_grpc.add_TranslationServiceServicer_to_server(TranslationService(), server)
    port = os.getenv("TRANSLATION_SERVICE_PORT", "50051")
    server.add_insecure_port(f'[::]:{port}')

    # Add reflection support
    SERVICE_NAMES = (
        translation_pb2.DESCRIPTOR.services_by_name['TranslationService'].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)

    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
