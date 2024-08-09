from pydantic import BaseModel, Field
from langchain.tools import tool
import yfinance as yf


# Define the input schema
class OptionsInput(BaseModel):
    ticker: str = Field(..., description="The ticker symbol of the stock to fetch options expiration dates for")


@tool(args_schema=OptionsInput)
def get_options_expiration_dates(ticker: str):
    """Fetch the available options expiration dates for a given ticker symbol."""
    
    stock = yf.Ticker(ticker)
    options_dates = stock.options
    
    return {"options_expiration_dates": options_dates}
