import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

async def extract_trade_details(message_text):
    """Extract trade details from a message using OpenAI."""
    prompt = f"""
    Extract the trade details from this message:
    "{message_text}"
    
    Return in JSON format:
    {{
        "trade_type": "BUY/SELL",
        "symbol": "Stock/Option",
        "entry_price": "Number",
        "stop_loss": "Number",
        "target_price": "Number"
    }}
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": prompt}]
    )
    return eval(response["choices"][0]["message"]["content"])
