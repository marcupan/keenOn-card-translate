import grpc
from translation_pb2 import TranslationResponse
import translation_pb2_grpc


class TranslationService(translation_pb2_grpc.TranslationServiceServicer):
    def Translate(self, request, context):
        chinese_word = request.chinese_word
        if not chinese_word:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details('Chinese word is required')
            return TranslationResponse()

        translation_uk = "text"
        individual_translations = []

        return TranslationResponse(
            translation=translation_uk,
            individual_translations=individual_translations
        )
