from langchain.tools import tool
from pydantic import BaseModel, Field
import yfinance as yf


# Define the input schema
class OptionChainInput(BaseModel):
    ticker: str = Field(..., description="The ticker symbol of the stock to fetch the options chain for")
    expiration_date: str = Field(..., description="The expiration date for the options chain (format: 'YYYY-MM-DD')")


@tool(args_schema=OptionChainInput)
def get_option_chain(ticker: str, expiration_date: str):
    """Fetch the options chain for a given ticker symbol and expiration date."""
    
    stock = yf.Ticker(ticker)
    
    # Check if the expiration date is valid
    if expiration_date not in stock.options:
        return {"error": f"No options available for the date {expiration_date}. Please choose a valid expiration date."}
    
    # If the date is valid, fetch the option chain
    try:
        option_chain = stock.option_chain(expiration_date)
        calls_dict = option_chain.calls.to_dict(orient='index')
        puts_dict = option_chain.puts.to_dict(orient='index')
        
        return {
            "calls": calls_dict,
            "puts": puts_dict
        }
    
    except Exception as e:
        return {"error": f"An error occurred while fetching the options chain: {str(e)}"}
