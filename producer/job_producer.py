import json
import time

from kafka import KafkaProducer

from producer.data_generator import generate_job


producer = KafkaProducer(

    bootstrap_servers="localhost:9092",

    value_serializer=lambda value:
        json.dumps(value).encode("utf-8")

)


print("Kafka producer started")


while True:

    job = generate_job()

    producer.send(
        "job_events",
        job
    )


    print(
        f"Sent: {job}"
    )


    time.sleep(0.05)