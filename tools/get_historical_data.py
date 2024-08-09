from langchain.tools import tool
from typing import Optional
from pydantic import BaseModel, Field
from enum import Enum
import yfinance as yf

# Define the Enum for valid periods
class PeriodEnum(str, Enum):
    one_day = '1d'
    five_days = '5d'
    one_month = '1mo'
    three_months = '3mo'
    six_months = '6mo'
    one_year = '1y'
    two_years = '2y'
    five_years = '5y'
    ten_years = '10y'
    year_to_date = 'ytd'
    max_period = 'max'

# Define the input schema with optional and enum fields
class HistoricalDataInput(BaseModel):
    ticker: str = Field(..., description="The ticker symbol of the stock to fetch historical data for")
    period: Optional[PeriodEnum] = Field(PeriodEnum.one_month, description="The period for which to fetch historical data")

@tool(args_schema=HistoricalDataInput)
def get_historical_data(ticker: str, period: str = "1mo") -> dict:
    """Fetch historical market data for a given ticker symbol and period."""
    
    stock = yf.Ticker(ticker)
    history = stock.history(period=period)
    
    # Convert the DataFrame to a dictionary for easy serialization
    history_dict = history.to_dict(orient='index')
    
    return history_dict