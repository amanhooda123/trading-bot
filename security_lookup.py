import pandas as pd
from config import SECURITY_CSV_FILE

def find_security_details(formatted_symbol):
    """
    Finds security details for a given formatted symbol from the CSV.
    Expected CSV columns:
      - SEM_TRADING_SYMBOL: e.g., "BANKNIFTY-Feb2025-55000-CE"
      - SEM_SMST_SECURITY_ID: The corresponding security ID
      - SEM_LOT_UNITS: The lot size for the instrument
      - SEM_EXPIRY_DATE: The expiry date (for options), e.g., "2025-02-27 14:30:00"
    Returns a dictionary with keys "security_id", "lot_size", and "expiry_date" if found; otherwise, None.
    """
    try:
        dtype_spec = {
            "SEM_TRADING_SYMBOL": str,
            "SEM_SMST_SECURITY_ID": str,
            "SEM_LOT_UNITS": int,
            "SEM_EXPIRY_DATE": str
        }
        df = pd.read_csv(
            SECURITY_CSV_FILE,
            dtype=dtype_spec,
            usecols=["SEM_TRADING_SYMBOL", "SEM_SMST_SECURITY_ID", "SEM_LOT_UNITS", "SEM_EXPIRY_DATE"],
            low_memory=False
        )

        # Normalize the trading symbol for consistency
        df["SEM_TRADING_SYMBOL"] = df["SEM_TRADING_SYMBOL"].str.replace(" ", "").str.upper()
        formatted_symbol = formatted_symbol.replace(" ", "").upper()

        match = df[df["SEM_TRADING_SYMBOL"] == formatted_symbol]

        if not match.empty:
            security_id = match.iloc[0]["SEM_SMST_SECURITY_ID"]
            lot_size = int(match.iloc[0]["SEM_LOT_UNITS"])
            expiry_date = match.iloc[0]["SEM_EXPIRY_DATE"]
            print(f"✅ Found security details for {formatted_symbol}: security_id = {security_id}, lot_size = {lot_size}, expiry_date = {expiry_date}")
            return {"security_id": security_id, "lot_size": lot_size, "expiry_date": expiry_date}

        print(f"⚠️ Security details not found for symbol {formatted_symbol}")
        return None

    except Exception as e:
        print(f"❌ Error fetching security details: {e}")
        return None
