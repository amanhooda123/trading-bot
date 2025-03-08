from telethon.sync import TelegramClient
from config import TELEGRAM_API_ID, TELEGRAM_API_HASH

client = TelegramClient("session_local", TELEGRAM_API_ID, TELEGRAM_API_HASH)

async def fetch_all_dialogs():
    """Print all dialogs, including groups, private chats, and channels."""
    await client.start()
    print("\n✅ Telegram client started using session_local! Fetching ALL dialogs...\n")

    total_dialogs = 0

    async for dialog in client.iter_dialogs():
        dialog_type = (
            "Group" if dialog.is_group else 
            "Channel" if dialog.is_channel else 
            "Private Chat"
        )

        print(f"📌 {dialog_type}: {dialog.title} | ID: {dialog.entity.id}")
        total_dialogs += 1

    print(f"\n✅ Total dialogs found: {total_dialogs}")

    if total_dialogs == 0:
        print("❌ No groups/channels found! Try rejoining them.")

    await client.disconnect()

# ✅ Run the script
with client:
    client.loop.run_until_complete(fetch_all_dialogs())
