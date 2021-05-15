import asyncio
import os
import json
from typing import Dict

import pika
from websocket import create_connection

# import dotenv
# dotenv.load_dotenv()

RMQ_USERNAME = os.getenv("RMQ_USERNAME")
RMQ_PWD = os.getenv("RMQ_PWD")
RMQ_HOST = os.getenv("RMQ_HOST")
RMQ_PORT = os.getenv("RMQ_PORT")

rmq_url = f"amqp://{RMQ_USERNAME}:{RMQ_PWD}@{RMQ_HOST}:{RMQ_PORT}/%2F"
print(f"consuming at {rmq_url}")
parameters = pika.URLParameters(rmq_url)

import time
print("consumer sleeping and waiting for rmq")
time.sleep(10)

uri = "ws://localhost:8000/listener/ws"
publish_lossevent_ws = create_connection(uri)


def on_message_callback(ch, method, properties, body):

    payload = json.loads(body)
    # SQL logic to find & update interest on device.
    # return the user_id, device_id & accrued interest
    publish_lossevent_ws.send(payload)
    print(f"-> payload_sent :: {payload}")


async def process_event(args: Dict):

    try:

        rmq_connection = pika.BlockingConnection(parameters)
        channel = rmq_connection.channel()
        channel.basic_consume(queue='stream', auto_ack=True, on_message_callback=on_message_callback)
        channel.start_consuming()
        
    except Exception as e:
        print(e)


if __name__ == "__main__":

    asyncio.get_event_loop().run_until_complete(process_event())