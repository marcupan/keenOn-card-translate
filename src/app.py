from threading import Thread
from concurrent import futures
import grpc

from flask import Flask
from grpc_reflection.v1alpha import reflection

from config import Config
from services.translation_service import TranslationService
from src.proto import translation_pb2_grpc, translation_pb2

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
    grpc_thread = Thread(target=start_grpc_server)
    grpc_thread.start()
    app.run(debug=True, host='0.0.0.0', port=Config.FLASK_RUN_PORT)
