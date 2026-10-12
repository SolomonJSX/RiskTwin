import os

KAFKA_BROKER = os.getenv("KAFKA_BROKER", "localhost:9092")
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))

TOPIC_TRANSACTIONS = "banking.transactions.v1"
TOPIC_TELEMETRY = "banking.telemetry.v1"
