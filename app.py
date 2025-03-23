from fastapi import FastAPI, WebSocket
import asyncio
import random

app = FastAPI()

# WebSocket endpoint for stock prices
@app.websocket("/ws/stocks")
async def stock_websocket(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            stock_price = round(random.uniform(100, 500), 2)  # Generate a random stock price
            await websocket.send_json({"stock": "XYZ", "price": stock_price})
            await asyncio.sleep(2)  # Send updates every 2 seconds
    except Exception as e:
        print(f"WebSocket Error: {e}")
    finally:
        await websocket.close()
