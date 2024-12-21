from concurrent import futures
import grpc
from proto import translation_pb2_grpc, translation_pb2
from service.translation_service import TranslationService
from config import Config
from grpc_reflection.v1alpha import reflection
from utils.logger import logger

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    translation_pb2_grpc.add_TranslationServiceServicer_to_server(TranslationService(), server)
    port = Config.PORT
    server.add_insecure_port(f'[::]:{port}')

    # Add reflection support
    SERVICE_NAMES = (
        translation_pb2.DESCRIPTOR.services_by_name['TranslationService'].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)

    logger.info(f"Starting gRPC server on port {port}...")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
