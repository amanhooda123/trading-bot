from fastapi import FastAPI
import asyncio
from telegram_listener import start_telegram_bot  # Import from the correct file

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Trading bot is running!"}

@app.on_event("startup")
async def start_bot():
    asyncio.create_task(start_telegram_bot())
