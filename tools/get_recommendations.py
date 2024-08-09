from langchain.tools import tool
from pydantic import BaseModel, Field
from enum import Enum
import yfinance as yf

# Define an enum for the type of recommendation information
class RecommendationType(str, Enum):
    recommendations = "recommendations"
    recommendations_summary = "recommendations_summary"
    upgrades_downgrades = "upgrades_downgrades"

# Define the input schema
class RecommendationsInput(BaseModel):
    ticker: str = Field(..., description="The ticker symbol of the stock to fetch recommendations for")
    recommendation_type: RecommendationType = Field(..., description="The type of recommendation information to fetch")

@tool(args_schema=RecommendationsInput)
def get_recommendations(ticker: str, recommendation_type: RecommendationType):
    """Fetch the specified recommendation information for a given ticker symbol."""
    
    stock = yf.Ticker(ticker)
    
    # Fetch the appropriate recommendation information based on the input
    if recommendation_type == RecommendationType.recommendations:
        return stock.recommendations.to_dict()
    elif recommendation_type == RecommendationType.recommendations_summary:
        return stock.recommendations_summary.to_dict()
    elif recommendation_type == RecommendationType.upgrades_downgrades:
        return stock.upgrades_downgrades.to_dict()
    
    return {"error": "Invalid recommendation type selected."}
