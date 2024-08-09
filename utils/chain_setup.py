from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.tools.render import format_tool_to_openai_function
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from langchain.prompts import MessagesPlaceholder
from langchain.schema.runnable import RunnablePassthrough
from langchain.agents.format_scratchpad import format_to_openai_functions

def create_chain(tools, model="gpt-3.5-turbo-0125"):
    functions = [format_tool_to_openai_function(f) for f in tools]
    
    # TODO: use better model with larger context window
    model = ChatOpenAI(model=model, temperature=0).bind(functions=functions)

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a highly knowledgeable financial assistant. You provide accurate and detailed financial data, analysis, and recommendations. Use the appropriate tools to fetch real-time data when needed."),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "User is asking: {input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
        # ("system", "Based on the available information and tools, generate a concise and accurate response. If additional data is needed, use the corresponding tool."),
    ])

    chain = prompt | model | OpenAIFunctionsAgentOutputParser()

    agent_chain = RunnablePassthrough.assign(
        agent_scratchpad=lambda x: format_to_openai_functions(x["intermediate_steps"])
    ) | chain

    return agent_chain
