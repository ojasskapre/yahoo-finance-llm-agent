# Yahoo Finance Agent

This application leverages OpenAI's language models, the Yahoo Finance Python library, and LangChain's agents and tools to provide users with real-time financial data and insights. Whether you're interested in stock prices, company financials, or the latest news, this assistant is here to help.

## Features

- **Stock Information**: Get detailed information about any stock, including historical data and recent news.
- **Financial Statements**: Access income statements, balance sheets, and cash flow statements, both annual and quarterly.
- **Options Data**: Explore available options expiration dates and detailed options chains.
- **Holders and Recommendations**: View information about major holders, insider transactions, and analyst recommendations.
- **Interactive Chat Interface**: Engage with the assistant through a user-friendly chat interface built with Streamlit.
- **LangChain Integration**: Utilizes LangChain's agents and tools for efficient task management and interaction with various data sources.
- **Conversation Buffer Memory**: Maintains the context of the conversation by passing chat message history to the model, ensuring more coherent and context-aware responses over the course of the interaction.
- **Powered by OpenAI**: Leverages OpenAI's language model to generate responses and provide insights based on user queries.
- **Langsmith**: Integrated with Langsmith to easily debug, analyze and visualize the agent's conversation flow and model outputs.

## Installation

1. Clone the Repository

```bash
git clone git@github.com:ojasskapre/yahoo-finance-llm-agent.git
cd yahoo-finance-llm-agent
```

2. Install Dependencies

```bash
pip install -r requirements.txt
```

3. Copy the `.env.sample` file to `.env` and add the OpenAI API key. To enable tracing using Langsmith, add Langchain API Key and Project name as well.

```bash
OPENAI_API_KEY=<YOUR_OPENAI_KEY_HERE>
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT="https://api.smith.langchain.com"
LANGCHAIN_API_KEY="<YOUR_LANGCHAIN_API_KEY>"
LANGCHAIN_PROJECT="<YOUR_PROJECT_NAME_HERE>"
```

4. To start the Streamlit app, run the following command:

```bash
streamlit run app.py
```

## Resources

- [Streamlit Agent Tools UI with Langchain](https://python.langchain.com/v0.2/docs/integrations/callbacks/streamlit/)
- [Streamlit Chat Message History UI with Langchain](https://python.langchain.com/v0.2/docs/integrations/memory/streamlit_chat_message_history/)
- [Streamlit Agent UI examples GitHub repository](https://github.com/langchain-ai/streamlit-agent)
- [Functions, Tools and Agents in Langchain](https://learn.deeplearning.ai/courses/functions-tools-agents-langchain)
