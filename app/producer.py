import os
import json

import pika

import dotenv
dotenv.load_dotenv()

RMQ_USERNAME = os.getenv("RMQ_USERNAME")
RMQ_PWD = os.getenv("RMQ_PWD")
RMQ_HOST = os.getenv("RMQ_HOST")
RMQ_PORT = os.getenv("RMQ_PORT")

rmq_url = f"amqp://{RMQ_USERNAME}:{RMQ_PWD}@{RMQ_HOST}:{RMQ_PORT}/%2F"
# print(f"publishing at {rmq_url}")

parameters = pika.URLParameters(rmq_url)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.queue_declare(queue='stream')


def send_lossevent_into_rmq(lossevent_info):

    body = json.dumps(lossevent_info)
    channel.basic_publish(exchange='', routing_key='stream', body=body)