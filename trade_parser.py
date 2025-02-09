import openai
import re
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def parse_trade_signal(message):
    """
    Uses OpenAI's NLP model to parse and extract trade signals from Telegram messages.
    """
    prompt = """
    You are an AI trade execution assistant that processes trade signals from a Telegram trading group. Your task is to extract **ONLY option trading signals** and execute them based on clear rules. Ignore irrelevant messages.

    ### **Rules for Execution:**
    1. **Trade Only Options (CALL or PUT)**
       - Ignore trades related to stocks, futures, or any other instrument.
       - Execute trades only for options in **NIFTY, BANKNIFTY, or STOCK OPTIONS**.

    2. **Buy Only One Trade at a Time**
       - If there is an **active trade**, ignore all new trades until the current trade is exited.
       - Once exited, allow new trades.

    3. **Extract Key Trade Details:**
       - **BUY or SELL** (If the signal says "Buy XYZ CALL/PUT" or "Short XYZ CALL/PUT").
       - **Strike Price** (E.g., "Buy BANKNIFTY 44500CE at 120").
       - **Entry Price** (Extract the entry price from the message).
       - **Target Price** (If mentioned, extract the target price).
       - **Stop Loss (SL)** (If mentioned, extract the stop loss).

    4. **Exit Immediately on Exit Signals:**
       - If a message contains **"Exit", "Book Profits", "Close trade", "Stop trade"**, exit the current position immediately.

    5. **Example Messages to Process:**
       - ✅ "Buy BANKNIFTY 44500CE at 120, SL 100, Target 150"
       - ✅ "Short NIFTY 18800PE at 85, SL 70, Target 110"
       - ✅ "Exit BANKNIFTY 44500CE, Book Profits"
       - ❌ "Buy Reliance 2500 at 2400" (Ignored, not an option trade)
       - ❌ "Gold trading signal - Buy at 1950" (Ignored, not an option trade)

    6. **Trade Execution:**
       - **Entry:** Immediately place an order for **1 lot** at the specified price.
       - **Exit:** If an exit message is detected, immediately close the position.
       - **Ignore Other Messages:** Do not process irrelevant messages.

    **Message to Process:**
    {message}

    **Extracted Trade Details:**
    """

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt.format(message=message),
        max_tokens=100
    )

    trade_details = response["choices"][0]["text"].strip()

    if "BUY" in trade_details or "SELL" in trade_details:
        return trade_details
    elif "EXIT" in trade_details:
        return {"exit": True}
    else:
        return None
