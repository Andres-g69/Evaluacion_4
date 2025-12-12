from kafka import KafkaProducer
import json, os

BOOTSTRAP = os.getenv('KAFKA_BOOTSTRAP', 'kafka:9092')
producer = KafkaProducer(bootstrap_servers=BOOTSTRAP, value_serializer=lambda v: json.dumps(v).encode('utf-8'))

def send_event(data):
    producer.send('calificaciones', data)
    producer.flush()

if __name__ == "__main__":
    send_event({'test': 'hello'})
