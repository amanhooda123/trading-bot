from kiteconnect import KiteConnect
from config import ZERODHA_API_KEY, ZERODHA_ACCESS_TOKEN

kite = KiteConnect(api_key=ZERODHA_API_KEY)
kite.set_access_token(ZERODHA_ACCESS_TOKEN)

def execute_trade(trade_details):
    """Execute a trade on Zerodha."""
    try:
        order = kite.place_order(
            variety=kite.VARIETY_REGULAR,
            exchange="NSE",
            tradingsymbol=trade_details["symbol"],
            transaction_type=kite.TRANSACTION_TYPE_BUY if trade_details["trade_type"] == "BUY" else kite.TRANSACTION_TYPE_SELL,
            quantity=1,  # Adjust quantity as needed
            order_type=kite.ORDER_TYPE_LIMIT,
            product=kite.PRODUCT_MIS,
            price=float(trade_details["entry_price"]),
            trigger_price=float(trade_details["stop_loss"]),
            validity=kite.VALIDITY_DAY
        )
        print(f"Trade executed: {order}")
    except Exception as e:
        print(f"Trade execution failed: {str(e)}")
