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
from langchain.schema import ChatMessage
from langchain.memory import ConversationBufferMemory

_ = load_dotenv(find_dotenv()) # read local .env file
openai.api_key = os.environ['OPENAI_API_KEY']

st.set_page_config(layout="wide")


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

# Sidebar for selecting the OpenAI model
st.sidebar.markdown("### Select OpenAI Model")
model_options = ["gpt-4o", "gpt-4o-mini", "gpt-3.5-turbo-0125"]
selected_model = st.sidebar.selectbox("Choose a model:", model_options, index=model_options.index("gpt-3.5-turbo-0125"))

# Create the agent chain
agent_chain = create_chain(tools, model=selected_model)

# Create the memory for storing conversation history
memory = ConversationBufferMemory(return_messages=True,memory_key="chat_history")

# Create the agent executor
agent_executor = AgentExecutor(agent=agent_chain, tools=tools, verbose=True, memory=memory)

st.title("Yahoo Finance Agent")

st.markdown("""
Welcome to the Finance Insights Assistant! This application leverages OpenAI, Langchain Agents and the Yahoo Finance Python library to provide you with up-to-date financial data and insights. Whether you're interested in stock prices, company financials, or the latest news, this assistant is here to help.

##### Features:
- **Stock Information**: Get detailed information about any stock, including historical data and recent news.
- **Financial Statements**: Access income statements, balance sheets, and cash flow statements, both annual and quarterly.
- **Options Data**: Explore available options expiration dates and detailed options chains.
- **Holders and Recommendations**: View information about major holders, insider transactions, and analyst recommendations.
""")

# Sidebar for Sample Questions
st.sidebar.markdown("### Sample Questions")
sample_questions = {
    "Stock Information": [
        "Give me information about Microsoft"
        "What is the current price of Apple?",
        "Give me the historical data for Tesla over the last month.",
        "What are the latest news articles for Microsoft?"
    ],
    "Financial Statements": [
        "Show me the latest income statement for Google.",
        "What is the quarterly cash flow for Amazon?",
        "Can you provide the annual balance sheet for Facebook?",
        "Please provide the quarterly balance sheet for Amazon."
    ],
    "Splits and Dividends": [
        "Give me dividends and splits for Goldman Sachs",
        "Give me splits for apple",
        "Give me dividends for cocacola"
    ],
    "Shares Count": [
        "Tell me the number of Microsoft shares outstanding since January 1, 2022.",
        "How many shares did Microsoft have outstanding between January 1, 2022, and December 31, 2022?",
        "What is the most recent number of Microsoft shares outstanding?",
    ],
    "Options Data": [
        "What are the available options expiration dates for Apple?",
        "Show me the options chain for Tesla expiring on 2024-01-19."
    ],
    "Holders and Recommendations": [
        "Who are the major holders of Netflix?",
        "Which mutual funds hold the most shares in Amazon?",
        "What are the recent analyst recommendations for Tesla?",
        "Show me the recent insider transactions for Microsoft.",
        "What are the sustainability scores for Google?",
        "Can you provide a summary of the latest recommendations for Tesla?"
    ]
}

# Display Sample Questions in the Sidebar with Expanders
for category, questions in sample_questions.items():
    with st.sidebar:
        with st.expander(f"{category}"):
            for question in questions:
                st.markdown(f"- {question}")

# TODO: Accept OpenAI API key as input in sidebar

if "messages" not in st.session_state:
    st.session_state["messages"] = [ChatMessage(role="assistant", content="How can I help you?")]

# Display the chat messages already in the session state
for msg in st.session_state.messages:
    st.chat_message(msg.role).write(msg.content)

if prompt := st.chat_input():
    # add the user message to the session state
    st.session_state.messages.append(ChatMessage(role="user", content=prompt))
    
    # display the user message in the chat
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        # Uncomment the following lines to enable Streamlit callbacks and display agent execution
        
        # st_callback = StreamlitCallbackHandler(st.container())
        # response = agent_executor.invoke(
        #     {"input": prompt}, {"callbacks": [st_callback]}
        # )
        try: 
            response = agent_executor.invoke(
                {"input": prompt}
            )
            st.write(response["output"])
            st.session_state.messages.append(ChatMessage(role="assistant", content=response["output"]))
        except Exception as e:
            st.write(f"An error occurred: {e}")
            st.session_state.messages.append(ChatMessage(role="assistant", content="An error occurred. Please try again."))