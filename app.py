import os
import openai
import streamlit as st

from dotenv import load_dotenv, find_dotenv
from tools import get_historical_data, get_stock_info, get_stock_actions, get_shares_count, get_financials, get_holders_info, get_recommendations, get_options_expiration_dates, get_option_chain, get_stock_news
from utils import run_agent, create_chain, tool_registry
from langchain.agents import AgentExecutor
from langchain_community.callbacks.streamlit import (
    StreamlitCallbackHandler,
)

_ = load_dotenv(find_dotenv()) # read local .env file
openai.api_key = os.environ['OPENAI_API_KEY']

def register_tools():
    if not hasattr(tool_registry, "_is_registered"):
        tool_registry.register_tool("get_stock_info", get_stock_info)
        tool_registry.register_tool("get_historical_data", get_historical_data)
        tool_registry.register_tool("get_stock_actions", get_stock_actions)
        tool_registry.register_tool("get_shares_count", get_shares_count)
        tool_registry.register_tool("get_financials", get_financials)
        tool_registry.register_tool("get_holders_info", get_holders_info)
        tool_registry.register_tool("get_recommendations", get_recommendations)
        tool_registry.register_tool("get_options_expiration_dates", get_options_expiration_dates)
        tool_registry.register_tool("get_option_chain", get_option_chain)
        tool_registry.register_tool("get_stock_news", get_stock_news)
        
        # Mark as registered
        tool_registry._is_registered = True

# Register the tools if not already registered
register_tools()

# Load the tools from the registry
tools = tool_registry.get_tools()

# Create the agent chain
agent_chain = create_chain(tools)

# Create the agent executor
agent_executor = AgentExecutor(agent=agent_chain, tools=tools, verbose=True)

if prompt := st.chat_input():
    st.chat_message("user").write(prompt)
    with st.chat_message("assistant"):
        st_callback = StreamlitCallbackHandler(st.container())
        response = agent_executor.invoke(
            {"input": prompt}, {"callbacks": [st_callback]}
        )
        st.write(response["output"])