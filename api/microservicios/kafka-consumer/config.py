from os import environ
KAFKA_BOOTSTRAP = environ.get('KAFKA_BOOTSTRAP', 'kafka:9092')
KAFKA_TOPIC = environ.get('KAFKA_TOPIC', 'nuam-events')
GROUP_ID = environ.get('KAFKA_GROUP', 'nuam-group')
