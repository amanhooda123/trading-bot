from fastapi import FastAPI
from contextlib import asynccontextmanager
import asyncio
from telegram_listener import start_telegram_bot
from config import ZERODHA_ACCESS_TOKEN

print("Starting FastAPI application...")

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Lifespan started...")
    print(f"Using Zerodha Access Token: {ZERODHA_ACCESS_TOKEN}")  # Debugging
    asyncio.create_task(start_telegram_bot())
    yield
    print("Lifespan ended...")

app = FastAPI(lifespan=lifespan)

@app.get("/")
def home():
    return {"message": "Trading bot is running with Zerodha API integration!"}
