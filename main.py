from fastapi import FastAPI
from contextlib import asynccontextmanager
import asyncio
from telegram_listener import start_telegram_bot

print("Starting FastAPI application...")  # Debug print

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Lifespan started...")  # Debug print
    asyncio.create_task(start_telegram_bot())
    yield  # Control will pass to the application here
    print("Lifespan ended...")  # Debug print

app = FastAPI(lifespan=lifespan)

@app.get("/")
def home():
    print("Handling root endpoint request...")  # Debug print
    return {"message": "Trading bot is running!"}
