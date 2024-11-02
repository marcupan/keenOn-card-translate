from flask import Flask
from concurrent import futures
import grpc
import translation_pb2
import translation_pb2_grpc
from services.translation_service import TranslationService
from grpc_reflection.v1alpha import reflection
from config import Config

app = Flask(__name__)

grpc_server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
translation_pb2_grpc.add_TranslationServiceServicer_to_server(TranslationService(), grpc_server)

SERVICE_NAMES = (
    translation_pb2.DESCRIPTOR.services_by_name['TranslationService'].full_name,
    reflection.SERVICE_NAME,
)
reflection.enable_server_reflection(SERVICE_NAMES, grpc_server)


def start_grpc_server():
    grpc_server.add_insecure_port(f'[::]:{Config.GRPC_RUN_PORT}')
    grpc_server.start()


if __name__ == '__main__':
    start_grpc_server()
    app.run(debug=True, host='0.0.0.0', port=Config.FLASK_RUN_PORT)
