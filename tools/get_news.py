from langchain.tools import tool
from pydantic import BaseModel, Field
import yfinance as yf

# Define the input schema
class NewsInput(BaseModel):
    ticker: str = Field(..., description="The ticker symbol of the stock to fetch the latest news for")

@tool(args_schema=NewsInput)
def get_stock_news(ticker: str):
    """Fetch the latest news articles for a given ticker symbol."""
    
    stock = yf.Ticker(ticker)
    news = stock.news
    
    return news
