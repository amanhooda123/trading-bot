import requests
from kiteconnect import KiteConnect
from config.config import ZERODHA_API_KEY, ZERODHA_ACCESS_TOKEN

# Telegram Bot Details (Replace with your actual bot token and chat ID)
TELEGRAM_BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
TELEGRAM_CHAT_ID = "YOUR_TELEGRAM_CHAT_ID"  # Your Telegram user ID or group ID

kite = KiteConnect(api_key=ZERODHA_API_KEY)
kite.set_access_token(ZERODHA_ACCESS_TOKEN)

def send_telegram_alert(message):
    """Send a message to Telegram."""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    requests.post(url, json=payload)

def execute_trade(trade_details):
    """Place an order on Zerodha based on extracted trade details."""
    try:
        order = kite.place_order(
            variety=kite.VARIETY_REGULAR,
            exchange="NSE",
            tradingsymbol=trade_details["symbol"],
            transaction_type=kite.TRANSACTION_TYPE_BUY if trade_details["trade_type"] == "BUY" else kite.TRANSACTION_TYPE_SELL,
            quantity=1,
            order_type=kite.ORDER_TYPE_LIMIT,
            product=kite.PRODUCT_MIS,
            price=float(trade_details["entry_price"]),
            trigger_price=float(trade_details["stop_loss"]),
            validity=kite.VALIDITY_DAY
        )

        # Create alert message
        trade_message = f"""
        ✅ Trade Executed:
        🔹 **{trade_details['trade_type']} {trade_details['symbol']}**
        📌 **Entry Price:** {trade_details['entry_price']}
        🛑 **Stop Loss:** {trade_details['stop_loss']}
        🎯 **Target Price:** {trade_details['target_price']}
        """
        send_telegram_alert(trade_message)  # Send alert

        print(f"Trade Executed: {order}")
    
    except Exception as e:
        error_message = f"❌ Trade Execution Failed: {str(e)}"
        send_telegram_alert(error_message)  # Send alert for failure
        print(error_message)
