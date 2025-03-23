import asyncio
import websockets

async def connect():
    uri = "ws://0.0.0.0/ws/stocks"
    async with websockets.connect(uri) as websocket:
        while True:
            message = await websocket.recv()
            print(f"Received: {message}")

# Run the client
asyncio.run(connect())
