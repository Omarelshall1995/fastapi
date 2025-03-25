from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import asyncio
import random
import os

app = FastAPI()

SECRET_KEY = os.getenv("SECRET_KEY", "default_secret")

# WebSocket endpoint with authentication
@app.websocket("/ws/stocks")
async def stock_websocket(websocket: WebSocket):
    query_params = websocket.query_params
    token = query_params.get("token")

    if token != SECRET_KEY:
        await websocket.close(code=1008)  # 1008: Policy Violation
        return

    await websocket.accept()
    try:
        while True:
            stock_price = round(random.uniform(100, 500), 2)  # Generate a random stock price
            await websocket.send_json({"stock": "XYZ", "price": stock_price})
            await asyncio.sleep(2)  # Send updates every 2 seconds
    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        print(f"WebSocket Error: {e}")
    finally:
        await websocket.close()
