# Description: A tool to fetch all stock information for a given ticker symbol.
from langchain.tools import tool
from typing import Optional
from pydantic import BaseModel, Field
from enum import Enum

import yfinance as yf


# Define the input schema for the get_stock_information tool
class StockInfoInput(BaseModel):
    ticker: str = Field(..., description="The ticker symbol of the stock to fetch information for")


@tool(args_schema=StockInfoInput)
def get_stock_info(ticker: str) -> dict:
    """Fetch all stock information for a given ticker symbol."""
    
    stock = yf.Ticker(ticker)
    info = stock.info
    
    # Check if the info is retrieved properly
    if not info:
        return {"error": "Unable to fetch data. Please check the ticker symbol."}
    
    return info