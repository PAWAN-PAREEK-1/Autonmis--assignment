import random
import asyncio  

async def generate_stock_price():
    stock_data = [
        {"stock": "AAPL"},
        {"stock": "GOOG"},
        {"stock": "AMZN"},
        {"stock": "EURO"},
    ]
    
    while True:
        stock = random.choice(stock_data)
        stock["price"] = round(random.uniform(100, 2000), 2) 
        yield stock
        await asyncio.sleep(1) 
