from langchain.tools import tool
from pydantic import BaseModel, Field
from enum import Enum
import yfinance as yf

# Define an enum for the type of holders' information
class HolderType(str, Enum):
    major_holders = "major_holders"
    institutional_holders = "institutional_holders"
    mutualfund_holders = "mutualfund_holders"
    insider_transactions = "insider_transactions"
    insider_purchases = "insider_purchases"
    insider_roster_holders = "insider_roster_holders"
    sustainability = "sustainability"

# Define the input schema
class HoldersInput(BaseModel):
    ticker: str = Field(..., description="The ticker symbol of the stock to fetch holders' information for")
    holder_type: HolderType = Field(..., description="The type of holders' information to fetch")

@tool(args_schema=HoldersInput)
def get_holders_info(ticker: str, holder_type: HolderType):
    """Fetch the specified holders' information or sustainability metrics for a given ticker symbol."""
    
    stock = yf.Ticker(ticker)
    
    # Fetch the appropriate holders' information based on the input
    if holder_type == HolderType.major_holders:
        return stock.major_holders.to_dict()
    elif holder_type == HolderType.institutional_holders:
        return stock.institutional_holders.to_dict()
    elif holder_type == HolderType.mutualfund_holders:
        return stock.mutualfund_holders.to_dict()
    elif holder_type == HolderType.insider_transactions:
        return stock.insider_transactions.to_dict()
    elif holder_type == HolderType.insider_purchases:
        return stock.insider_purchases.to_dict()
    elif holder_type == HolderType.insider_roster_holders:
        return stock.insider_roster_holders.to_dict()
    elif holder_type == HolderType.sustainability:
        return stock.sustainability.to_dict()
    
    return {"error": "Invalid holder type selected."}
