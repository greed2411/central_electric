import argparse
import asyncio
import json
from typing import Dict

import websockets

async def show_live_interest(args: Dict):

    user_id = args.id

    try:

        uri = f"ws://localhost:8000/user/ws/{user_id}"
        async with websockets.connect(uri) as websocket:

            while True:

                recv_payload = await websocket.recv()
                recv_payload = json.loads(recv_payload)
                yield recv_payload
    
    except websockets.exceptions.ConnectionClosedError as e:
        print(e, "websocket unexpectedly closed!")


async def main(args):

    async for payload in show_live_interest(args):
        payload_str = f"For device: {payload['device_id']}, accrued interest is ₹ {payload['accrued_interest']:.4}, as of {payload['timestamp']}"
        print(payload_str, end='\r')


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='process to check live interest accumulation for users')
    parser.add_argument('id', type=int, help='an integer for the user_id')
    args = parser.parse_args()

    asyncio.get_event_loop().run_until_complete(main(args))