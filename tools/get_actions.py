from langchain.tools import tool
from typing import Optional
from pydantic import BaseModel, Field
from enum import Enum
import yfinance as yf


# Define an enum for the type of action to fetch
class ActionType(str, Enum):
    actions = "actions"
    dividends = "dividends"
    splits = "splits"


# Define the input schema
class ActionInput(BaseModel):
    ticker: str = Field(..., description="The ticker symbol of the stock to fetch actions for")
    action_type: ActionType = Field(..., description="The type of action to fetch (actions, dividends, or splits)")

# TODO: check if action_type `actions` is used correctly
@tool(args_schema=ActionInput)
def get_stock_actions(ticker: str, action_type: ActionType):
    """Fetch stock actions such as dividends, splits, or both for a given ticker symbol."""
    
    stock = yf.Ticker(ticker)
    
    if action_type == ActionType.actions:
        return stock.actions.to_dict()
    elif action_type == ActionType.dividends:
        return stock.dividends.to_dict()
    elif action_type == ActionType.splits:
        return stock.splits.to_dict()
    
    return {"error": "Invalid action type selected."}
