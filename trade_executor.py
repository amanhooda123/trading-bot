from kiteconnect import KiteConnect
from config import ZERODHA_API_KEY, ZERODHA_ACCESS_TOKEN

kite = KiteConnect(api_key=ZERODHA_API_KEY)
kite.set_access_token(ZERODHA_ACCESS_TOKEN)

# Track if a trade is active
active_trade = None

def execute_trade(trade_details):
    global active_trade
    
    if active_trade:
        print("⚠️ Already in a trade. Waiting for exit before placing a new order.")
        return

    try:
        order_id = kite.place_order(
            variety="regular",
            exchange="NSE",
            tradingsymbol=trade_details["stock"],
            transaction_type=trade_details["action"],
            quantity=1,
            order_type="LIMIT",
            product="CNC",
            price=trade_details["price"]
        )
        print(f"✅ Order Placed: {order_id}")

        # Store active trade details
        active_trade = {
            "stock": trade_details["stock"],
            "order_id": order_id
        }
    except Exception as e:
        print(f"❌ Error Placing Order: {e}")

def exit_trade():
    global active_trade
    
    if not active_trade:
        print("⚠️ No active trade to exit.")
        return

    try:
        exit_order_id = kite.place_order(
            variety="regular",
            exchange="NSE",
            tradingsymbol=active_trade["stock"],
            transaction_type="SELL",
            quantity=1,
            order_type="MARKET",
            product="CNC"
        )
        print(f"✅ Trade Exited: {exit_order_id}")
        active_trade = None  # Clear active trade after exit

    except Exception as e:
        print(f"❌ Error Exiting Trade: {e}")
