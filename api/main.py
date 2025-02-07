from fastapi import FastAPI
import asyncio
from core.telegram_listener import main as start_telegram_bot

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Telegram Trading Bot is Running"}

@app.get("/start-bot")
async def start_bot():
    asyncio.create_task(start_telegram_bot())
    return {"message": "Bot Started Successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
