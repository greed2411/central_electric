import argparse
import asyncio
import datetime
import json
from typing import Dict

import websockets

async def initiate_failure(args: Dict):

    lapse = 1
    device_id = args.id

    try:

        uri = f"ws://localhost:8000/device/ws/{device_id}"
        async with websockets.connect(uri) as websocket:

            while True:

                payload = {
                    "timestamp": str(datetime.datetime.now()),
                    "lapse": lapse,
                }

                payload = json.dumps(payload)
                
                # TODO: if websockets.exceptions.ConnectionClosedError: code = 1006,
                # persist locally. then continue 
                await websocket.send(payload)
                print(f"-> payload_sent :: {payload}")

                recv_payload = await websocket.recv()
                recv_payload = json.loads(recv_payload)

                await asyncio.sleep(1)
                lapse += 1
    
    except websockets.exceptions.ConnectionClosedError as e:
        print(e, "websocket unexpectedly closed!")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='process to notify node failure every second')
    parser.add_argument('id', type=int, help='an integer for the device_id')
    args = parser.parse_args()

    asyncio.get_event_loop().run_until_complete(initiate_failure(args))