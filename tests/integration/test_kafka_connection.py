import pytest
import time
from confluent_kafka import Producer, Consumer, KafkaError

def test_kafka_produce_consume(kafka_bootstrap_servers):
    topic = "test-connection-topic"
    conf = {"bootstrap.servers": kafka_bootstrap_servers}
    
    # Producer
    producer = Producer(conf)
    def delivery_report(err, msg):
        if err is not None:
            pytest.fail(f"Message delivery failed: {err}")
    
    producer.produce(topic, b"test-message", callback=delivery_report)
    producer.flush()

    # Consumer
    conf["group.id"] = "test-group"
    conf["auto.offset.reset"] = "earliest"
    consumer = Consumer(conf)
    consumer.subscribe([topic])

    message_received = False
    for _ in range(10):
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                pytest.fail(f"Consumer error: {msg.error()}")
        
        if msg.value() == b"test-message":
            message_received = True
            break
        time.sleep(1)

    consumer.close()
    assert message_received, "Failed to consume the test message from Kafka"
