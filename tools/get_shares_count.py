from langchain.tools import tool
from pydantic import BaseModel, Field
from enum import Enum
import yfinance as yf


# Define the input schema for the tool
class SharesCountInput(BaseModel):
    ticker: str = Field(..., description="The ticker symbol of the stock to fetch share count for")
    start: str = Field(..., description="The start date for the date range (YYYY-MM-DD)")
    end: str = Field(None, description="The end date for the date range (YYYY-MM-DD). Defaults to None.")


@tool(args_schema=SharesCountInput)
def get_shares_count(ticker: str, start: str, end: str = None):
    """Fetch the number of shares outstanding over a specified date range."""
    
    stock = yf.Ticker(ticker)
    shares_count = stock.get_shares_full(start=start, end=end)
    
    # Convert the DataFrame to a dictionary for easy serialization
    shares_count_dict = shares_count.to_dict()
    
    return shares_count_dict
