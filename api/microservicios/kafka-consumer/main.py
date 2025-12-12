from confluent_kafka import Consumer, KafkaError
import json
from config import KAFKA_BOOTSTRAP, KAFKA_TOPIC, GROUP_ID

conf = {
    'bootstrap.servers': KAFKA_BOOTSTRAP,
    'group.id': GROUP_ID,
    'auto.offset.reset': 'earliest'
}

def handle_message(msg):
    try:
        payload = json.loads(msg.value().decode('utf-8'))
    except:
        payload = msg.value().decode('utf-8')
    print("Evento recibido:", payload)

def run_consumer():
    c = Consumer(conf)
    c.subscribe([KAFKA_TOPIC])
    try:
        while True:
            msg = c.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    print("Error:", msg.error())
                    continue
            handle_message(msg)
    except KeyboardInterrupt:
        pass
    finally:
        c.close()

if __name__ == "__main__":
    run_consumer()
