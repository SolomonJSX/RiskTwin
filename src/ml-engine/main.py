import logging
import warnings
from concurrent import futures
import grpc

warnings.filterwarnings('ignore', category=UserWarning, module='sklearn')

from app.proto import ml_inference_pb2_grpc
from app.infrastructure.deep_learning.deep_scoring_model import DeepCrossAttentionScoringModel
from app.infrastructure.xai.deep_cross_attention_explainer import DeepCrossAttentionExplainabilityEngine
from app.infrastructure.optimization.ortools_restructuring import OrToolsRestructuringOptimizer
from app.grpc_server.services import ScoringGrpcService, OptimizerGrpcService


def serve(port: int = 50051):
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )
    logger = logging.getLogger("RiskTwin.MlEngine")

    # Инициализация глубокой нейросети PyTorch и XAI движка на основе матриц кросс-внимания
    scoring_model = DeepCrossAttentionScoringModel()
    xai_engine = DeepCrossAttentionExplainabilityEngine(scoring_model)
    optimizer = OrToolsRestructuringOptimizer()

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    ml_inference_pb2_grpc.add_ScoringServiceServicer_to_server(
        ScoringGrpcService(scoring_model, xai_engine), server
    )
    ml_inference_pb2_grpc.add_RestructuringOptimizerServiceServicer_to_server(
    OptimizerGrpcService(optimizer, scoring_model, xai_engine), server
)

    server_address = f"0.0.0.0:{port}"
    server.add_insecure_port(server_address)
    logger.info(f"RiskTwin ML Inference Engine started successfully on gRPC port {port}")
    
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()