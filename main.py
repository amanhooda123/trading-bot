from fastapi import FastAPI
import uvicorn
import asyncio
from telegram_listener import start_telegram_listener

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Option Trading Bot is running!"}

@app.get("/status")
def check_status():
    return {"status": "Running"}

async def run_services():
    """Runs Telegram listener alongside FastAPI."""
    telegram_task = asyncio.create_task(start_telegram_listener())  # Start Telegram Listener
    await telegram_task  # Ensure it doesn't stop prematurely

if __name__ == "__main__":
    asyncio.run(run_services())  # Run Telegram listener properly
    uvicorn.run(app, host="0.0.0.0", port=8000)
