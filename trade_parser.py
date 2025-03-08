import openai
import json
from config import OPENAI_API_KEY
from security_lookup import find_security_details

openai.api_key = OPENAI_API_KEY

# Mapping for month conversion to match CSV format
MONTH_MAP = {
    "JAN": "Jan", "FEB": "Feb", "MAR": "Mar", "APR": "Apr",
    "MAY": "May", "JUN": "Jun", "JUL": "Jul", "AUG": "Aug",
    "SEP": "Sep", "OCT": "Oct", "NOV": "Nov", "DEC": "Dec"
}

def parse_trade_signal(message):
    """
    Uses AI to extract structured trade details from the message.
    Expected keys:
      - symbol (e.g., "BANKNIFTY")
      - expiry_month (e.g., "FEB")
      - strike_price (e.g., 55000)
      - option_type (e.g., "CE" or "PE")
      - price (buy price, e.g., 3.0)
      - stop_loss (e.g., 2.0)
      - target (e.g., 5.0)
    Constructs a formatted symbol (e.g., "BANKNIFTY-Feb2025-55000-CE") and looks up security details.
    """
    try:
        prompt = f"""
        Extract structured trade details from the following message:
        "{message}"
        
        Return ONLY a valid JSON object with these keys:
        - symbol (e.g., "BANKNIFTY")
        - expiry_month (e.g., "FEB")
        - strike_price (e.g., 55000)
        - option_type (e.g., "CE" or "PE")
        - price (buy price, e.g., 3.0)
        - stop_loss (e.g., 2.0)
        - target (e.g., 5.0)
        
        Output must be valid JSON without any extra text.
        """

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "system", "content": prompt}]
        )

        trade_data = response["choices"][0]["message"]["content"].strip()
        trade_data = trade_data.replace("```json", "").replace("```", "").strip()
        print(f"📊 AI Raw Response (Cleaned): {trade_data}")

        trade_details = json.loads(trade_data)

        # Normalize and convert types
        trade_details["symbol"] = trade_details.get("symbol", "").replace(" ", "").upper()
        trade_details["expiry_month"] = trade_details.get("expiry_month", "").upper()
        trade_details["strike_price"] = int(trade_details.get("strike_price", 0))
        trade_details["option_type"] = trade_details.get("option_type", "").upper()
        trade_details["price"] = float(trade_details.get("price", 0))
        trade_details["stop_loss"] = float(trade_details.get("stop_loss", 0))
        trade_details["target"] = float(trade_details.get("target", 0))

        # Format symbol for CSV lookup (assume expiry year is 2025)
        month_formatted = MONTH_MAP.get(trade_details["expiry_month"], trade_details["expiry_month"])
        formatted_symbol = f"{trade_details['symbol']}-{month_formatted}2025-{trade_details['strike_price']}-{trade_details['option_type']}"
        trade_details["formatted_symbol"] = formatted_symbol

        print(f"✅ AI Extracted and Formatted Symbol: {formatted_symbol}")

        # Lookup security details using the formatted symbol
        sec_details = find_security_details(formatted_symbol)
        if sec_details:
            trade_details["security_id"] = sec_details["security_id"]
            trade_details["lot_size"] = sec_details["lot_size"]
            trade_details["expiry_date"] = sec_details["expiry_date"]
            return trade_details
        else:
            print(f"⚠️ Security details not found for {formatted_symbol}")
            return None

    except json.JSONDecodeError as je:
        print(f"❌ AI Error: Invalid JSON format in response! {je}")
        return None
    except Exception as e:
        print(f"❌ AI Error extracting trade details: {e}")
        return None
