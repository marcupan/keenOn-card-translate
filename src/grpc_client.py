import grpc
from proto.translation_pb2 import TranslationRequest
from proto.translation_pb2_grpc import TranslationServiceStub

def run():
    with grpc.insecure_channel('localhost:<GRPC_PORT>') as channel:
        stub = TranslationServiceStub(channel)
        request = TranslationRequest(chinese_word='你好')
        response = stub.Translate(request)
        print("Translation:", response.translation)
        print("Individual Translations:", response.individual_translations)

if __name__ == '__main__':
    run()
