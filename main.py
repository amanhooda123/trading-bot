from fastapi import FastAPI
from contextlib import asynccontextmanager
import asyncio
from telegram_listener import start_telegram_bot

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start Telegram bot when FastAPI starts
    asyncio.create_task(start_telegram_bot())
    yield  # Control will pass to the application here
    # Add any cleanup code if necessary (e.g., shutting down resources)

app = FastAPI(lifespan=lifespan)

@app.get("/")
def home():
    return {"message": "Trading bot is running!"}
