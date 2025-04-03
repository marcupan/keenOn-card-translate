from concurrent import futures
import grpc
from src.proto import translation_pb2_grpc, translation_pb2
from src.service.translation_service import TranslationService
from src.config import Config
from src.utils.logger import logger

from grpc_reflection.v1alpha import reflection


def serve():
    server_options = [
        ('grpc.keepalive_time_ms', 10000),
        ('grpc.keepalive_timeout_ms', 5000),
        ('grpc.keepalive_permit_without_calls', True),
        ('grpc.http2.min_time_between_pings_ms', 10000),
        ('grpc.http2.min_ping_interval_without_data_ms', 5000),
        ('grpc.http2.max_pings_without_data', 0),
    ]

    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10),
        options=server_options
    )

    translation_pb2_grpc.add_TranslationServiceServicer_to_server(TranslationService(), server)

    port = Config.PORT
    server.add_insecure_port(f'[::]:{port}')

    service_names = (
        translation_pb2.DESCRIPTOR.services_by_name['TranslationService'].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(service_names, server)

    logger.info(f"Starting gRPC server on port {port} with keepalive options...")

    server.start()
    logger.info("Server started. Waiting for termination...")
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
