import asyncio
import websockets
import os

SECRET_KEY = os.getenv("SECRET_KEY", "default_secret")

async def connect():
    uri = f"ws://0.0.0.0/ws/stocks?token={SECRET_KEY}"
    async with websockets.connect(uri) as websocket:
        while True:
            message = await websocket.recv()
            print(f"Received: {message}")

# Run the client
asyncio.run(connect())
