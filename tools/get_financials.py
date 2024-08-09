from langchain.tools import tool
from pydantic import BaseModel, Field
from enum import Enum
import yfinance as yf


# Define an enum for the type of financial statement
class FinancialType(str, Enum):
    income_stmt = "income_stmt"
    quarterly_income_stmt = "quarterly_income_stmt"
    balance_sheet = "balance_sheet"
    quarterly_balance_sheet = "quarterly_balance_sheet"
    cashflow = "cashflow"
    quarterly_cashflow = "quarterly_cashflow"


# Define the input schema
class FinancialsInput(BaseModel):
    ticker: str = Field(..., description="The ticker symbol of the stock to fetch financials for")
    financial_type: FinancialType = Field(..., description="The type of financial statement to fetch")


@tool(args_schema=FinancialsInput)
def get_financials(ticker: str, financial_type: FinancialType):
    """Fetch the specified financial statement for a given ticker symbol."""
    
    stock = yf.Ticker(ticker)
    
    # Fetch the appropriate financial statement based on the input
    if financial_type == FinancialType.income_stmt:
        return stock.income_stmt.to_dict()
    elif financial_type == FinancialType.quarterly_income_stmt:
        return stock.quarterly_income_stmt.to_dict()
    elif financial_type == FinancialType.balance_sheet:
        return stock.balance_sheet.to_dict()
    elif financial_type == FinancialType.quarterly_balance_sheet:
        return stock.quarterly_balance_sheet.to_dict()
    elif financial_type == FinancialType.cashflow:
        return stock.cashflow.to_dict()
    elif financial_type == FinancialType.quarterly_cashflow:
        return stock.quarterly_cashflow.to_dict()
    
    return {"error": "Invalid financial type selected."}
