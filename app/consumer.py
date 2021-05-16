import asyncio
import os
import time
from typing import Dict

import pika
from websocket import create_connection

import dotenv
dotenv.load_dotenv()

RMQ_USERNAME = os.getenv("RMQ_USERNAME")
RMQ_PWD = os.getenv("RMQ_PWD")
RMQ_HOST = os.getenv("RMQ_HOST")
RMQ_PORT = os.getenv("RMQ_PORT")

rmq_url = f"amqp://{RMQ_USERNAME}:{RMQ_PWD}@{RMQ_HOST}:{RMQ_PORT}/%2F"
# print(f"consuming at {rmq_url}")
parameters = pika.URLParameters(rmq_url)

uri = "ws://localhost:8000/listener/ws"


def on_message_callback(ch, method, properties, body):

    
    body_json = body.decode('utf8').replace("'", '"')

    for _ in range(5):
        try:
            publish_lossevent_ws = create_connection(uri)
            publish_lossevent_ws.send(body_json)
            publish_lossevent_ws.close()
            break
        except (BrokenPipeError, ConnectionResetError) as e:
            print(e)
            time.sleep(0.2)
        except ConnectionRefusedError:
            print("server went offline")
            break



async def process_event():


    rmq_connection = pika.BlockingConnection(parameters)
    channel = rmq_connection.channel()
    channel.basic_consume(queue='stream', auto_ack=True, on_message_callback=on_message_callback)
    channel.start_consuming()
        


if __name__ == "__main__":

    asyncio.get_event_loop().run_until_complete(process_event())