import uuid
import requests
from config import DHAN_CLIENT_ID, DHAN_ACCESS_TOKEN, DHAN_BASE_URL
from security_lookup import find_security_details

def generate_correlation_id():
    """Generates a unique correlation ID for tracking orders."""
    return str(uuid.uuid4())

def place_order(security_id, transaction_type, quantity, price, instrument_type, expiry_date=None):
    """
    Places an order on the Dhan API.
    If price is non-zero, a LIMIT order is placed; if price is 0, a MARKET order is placed.
    Expiry date is required for options in "YYYY-MM-DD" format.
    """
    url = f"{DHAN_BASE_URL}/orders"
    headers = {
        "Authorization": f"Bearer {DHAN_ACCESS_TOKEN}",
        "ClientId": DHAN_CLIENT_ID,
        "Content-Type": "application/json"
    }

    correlationId = generate_correlation_id()

    # ✅ Determine order type
    order_type = "LIMIT" if float(price) > 0 else "MARKET"

    # ✅ Ensure valid exchangeSegment and productType
    if instrument_type == "OPTION":
        exchangeSegment = "NSE_FNO"
        productType = "MARGIN"  # Required for options
    else:
        exchangeSegment = "NSE_EQ"
        productType = "INTRADAY"

    # ✅ Ensure valid price and quantity formatting
    order_price = str(price) if order_type == "LIMIT" else "0"
    order_quantity = str(int(quantity))  # Ensure quantity is an integer

    # ✅ Prepare payload
    payload = {
        "dhanClientId": DHAN_CLIENT_ID,
        "correlationId": correlationId,
        "transactionType": transaction_type.upper(),  # BUY or SELL
        "exchangeSegment": exchangeSegment,
        "productType": productType,
        "orderType": order_type,
        "validity": "DAY",
        "securityId": security_id,
        "quantity": order_quantity,
        "disclosedQuantity": "0",
        "price": order_price,
        "triggerPrice": "0",
        "afterMarketOrder": False,
        "amoTime": "",
        "boProfitValue": 0,
        "boStopLossValue": 0
    }

    # ✅ Include expiryDate if it's an option order
    if instrument_type == "OPTION" and expiry_date:
        payload["expiryDate"] = expiry_date.split(" ")[0]  # Format YYYY-MM-DD

    print(f"📩 Payload Sent to Dhan API: {payload}")

    try:
        response = requests.post(url, json=payload, headers=headers)
        response_data = response.json()

        if response.status_code == 200 and "orderId" in response_data:
            print(f"✅ Trade Executed Successfully: {response_data}")
        else:
            print(f"❌ Trade Execution Failed: {response_data}")

        return response_data

    except Exception as e:
        print(f"❌ Error placing order: {e}")
        return None

def execute_trade(trade_details):
    """
    Executes the trade using extracted details.
    Looks up security details (security_id, lot_size, expiry_date) from DhanHQ API.
    Ensures correct quantity (1 lot), order type (LIMIT or MARKET), and expiry formatting.
    """
    formatted_symbol = trade_details.get("formatted_symbol")
    if not formatted_symbol:
        print("❌ Cannot execute trade: Missing formatted symbol!")
        return None

    sec_details = find_security_details(formatted_symbol)
    if not sec_details:
        print(f"⚠️ Security details not found for {formatted_symbol}")
        return None

    security_id = sec_details.get("security_id")
    lot_size = sec_details.get("lot_size")  # Use 1 lot
    expiry_date = sec_details.get("expiry_date") if trade_details.get("option_type", "").upper() in ["CE", "PE"] else None

    # ✅ Ensure quantity is correct (always 1 lot)
    total_quantity = lot_size

    price = trade_details.get("price")
    transaction_type = trade_details.get("transaction_type", "BUY").upper()

    # ✅ Determine instrument type
    instrument_type = "EQUITY"
    if trade_details.get("option_type", "").upper() in ["CE", "PE"]:
        instrument_type = "OPTION"

    if not security_id:
        print("❌ Cannot execute trade: Missing Security ID!")
        return None

    if price is None:
        print("❌ Cannot execute trade: Price not provided in message!")
        return None

    # ✅ Ensure expiryDate is formatted correctly
    formatted_expiry = expiry_date.split(" ")[0] if expiry_date else None

    # ✅ FIX: Define `order_type` before using it
    order_type = "LIMIT" if float(price) > 0 else "MARKET"

    print(f"🚀 Executing {order_type} Order: {transaction_type} {total_quantity} (1 lot) of {security_id} at ₹{price} as {instrument_type}")
    if instrument_type == "OPTION":
        print(f"   Expiry Date: {formatted_expiry}")

    return place_order(security_id, transaction_type, total_quantity, price, instrument_type, formatted_expiry)
