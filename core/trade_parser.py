import openai
from config.config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

async def extract_trade_details(message_text):
    """ Extract trade details from a Telegram message using OpenAI API. """
    prompt = f"""
    Extract the trade details from the following message:
    "{message_text}"
    
    Return in JSON format:
    {{
        "trade_type": "BUY/SELL",
        "symbol": "Stock/Option",
        "strike_price": "Number",
        "option_type": "CALL/PUT",
        "entry_price": "Number",
        "stop_loss": "Number",
        "target_price": "Number"
    }}
    """

    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[{"role": "system", "content": prompt}]
    )

    trade_details = response["choices"][0]["message"]["content"]
    return eval(trade_details)  # Convert OpenAI response into dictionary
