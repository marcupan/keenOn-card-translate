import grpc

from src.proto.translation_pb2 import TranslationResponse
from src.proto.translation_pb2_grpc import TranslationServiceServicer


class TranslationService(TranslationServiceServicer):
    def Translate(self, request, context):
        chinese_word = request.chinese_word
        if not chinese_word:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details('Chinese word is required')
            return TranslationResponse()  # Return an empty response in case of error

        # Mock translation logic for testing purposes
        translation_uk = "text"  # Placeholder for the actual translation
        individual_translations = []  # Placeholder list for individual character translations

        # Properly create and return the TranslationResponse
        return TranslationResponse(
            translation=translation_uk,
            individual_translations=individual_translations
        )
