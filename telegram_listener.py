from telethon import TelegramClient, events
from trade_parser import parse_trade_signal
from trade_executor import execute_trade, exit_trade
from config import TELEGRAM_API_ID, TELEGRAM_API_HASH, TELEGRAM_PHONE_NUMBER, TELEGRAM_GROUP_ID

client = TelegramClient("session_render", TELEGRAM_API_ID, TELEGRAM_API_HASH)

@client.on(events.NewMessage(chats=TELEGRAM_GROUP_ID))
async def handle_message(event):
    """Handle new messages from the Telegram group."""
    message_text = event.message.message.strip()
    print(f"📩 New message received: {message_text}")
    
    # If the message contains an "Exit" command, exit the active trade immediately
    exit_keywords = ["exit", "book profit", "close trade", "stop trade"]
    if any(exit_word in message_text.lower() for exit_word in exit_keywords):
        print("⚠️ Exit signal detected! Exiting the trade immediately.")
        exit_trade()
        return  # Stop processing further

    try:
        trade_details = await parse_trade_signal(message_text)  # Extract trade details
        if trade_details:
            print(f"✅ Extracted trade details: {trade_details}")
            execute_trade(trade_details)  # Execute trade
        else:
            print("ℹ️ No valid trade signal detected. Ignoring the message.")

    except Exception as e:
        print(f"❌ Error handling message: {e}")

async def start_telegram_bot():
    """Start the Telegram bot."""
    await client.start(TELEGRAM_PHONE_NUMBER)
    print("✅ Telegram bot started successfully!")
    await client.run_until_disconnected()
