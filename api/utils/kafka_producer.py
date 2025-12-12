# api/utils/kafka_producer.py
import os
import json

BOOTSTRAP = os.getenv('KAFKA_BOOTSTRAP', 'kafka:9092')

# Try import, but fail gracefully if kafka-python not installed or server unreachable
try:
    from kafka import KafkaProducer
    producer = KafkaProducer(
        bootstrap_servers=BOOTSTRAP,
        value_serializer=lambda v: json.dumps(v).encode('utf-8'),
        request_timeout_ms=5000
    )
except Exception:
    producer = None

def publish(topic: str, payload: dict):
    """
    Publish a JSON payload to Kafka topic. If Kafka not configured, it's a no-op.
    """
    if not producer:
        # optional: log to file or stdout in dev
        print("Kafka not available - skipping publish:", topic, payload)
        return False
    try:
        producer.send(topic, payload)
        producer.flush()
        return True
    except Exception as e:
        print("Kafka publish error:", e)
        return False
