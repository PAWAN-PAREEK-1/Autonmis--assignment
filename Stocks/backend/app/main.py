
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from fastapi import FastAPI, WebSocket

from fastapi.middleware.cors import CORSMiddleware
import asyncio
from stock_price_generator import generate_stock_price  
from system_stats import get_system_stats 



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ConnectionManager:
    def __init__(self):
        self.stock_connections: list[WebSocket] = []
        self.stats_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket, endpoint: str):
        await websocket.accept()
        if endpoint == "stocks":
            self.stock_connections.append(websocket)
        elif endpoint == "stats":
            self.stats_connections.append(websocket)

    def disconnect(self, websocket: WebSocket, endpoint: str):
        if endpoint == "stocks":
            self.stock_connections.remove(websocket)
        elif endpoint == "stats":
            self.stats_connections.remove(websocket)

    async def broadcast(self, message: dict, endpoint: str):
        if endpoint == "stocks":
            connections = self.stock_connections
        elif endpoint == "stats":
            connections = self.stats_connections
        else:
            connections = []

        for connection in connections:
            try:
                await connection.send_json(message)
            except:
                self.disconnect(connection, endpoint)

manager = ConnectionManager()


@app.websocket("/ws/stocks")
async def stock_price(websocket: WebSocket):
    print("Stock WebSocket connected")
    await manager.connect(websocket, "stocks")
    try:
        async for price in generate_stock_price(): 
            await manager.broadcast(price, "stocks")
    except Exception as e:
        print(f"Error in stock WebSocket: {e}")
    finally:
        print("Stock WebSocket disconnected")
        manager.disconnect(websocket, "stocks")




@app.websocket("/ws/stats")
async def system_stats(websocket: WebSocket):
    print("System Stats WebSocket connected")
    await manager.connect(websocket, "stats")
    try:
        while True:
            await asyncio.sleep(1)
            stats = get_system_stats()  
    
            await manager.broadcast(stats, "stats")
    except Exception as e:
        print(f"Error in stats WebSocket: {e}")
    finally:
       
        manager.disconnect(websocket, "stats")
