from telethon import TelegramClient, events

# Your credentials
API_ID = 21898440  # Replace with your TELEGRAM_API_ID
API_HASH = "92ebf0c4fe09835fa0c41b323d79efb2"  # Replace with your TELEGRAM_API_HASH
SESSION_NAME = "session_local"  # The session file name

# Initialize Telegram Client
client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

@client.on(events.NewMessage())  # Listen for all messages
async def handler(event):
    print(f"📩 Received: {event.message.text}")  # Print the message received

async def main():
    await client.start()
    print("✅ Telegram listener started! Waiting for messages...")
    await client.run_until_disconnected()  # Keep running indefinitely

# Run the client
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
