from langchain.schema.agent import AgentFinish
from utils.tool_registry import tool_registry

def run_agent(agent_chain, user_input):
    intermediate_steps = []
    while True:
        result = agent_chain.invoke({
            "input": user_input, 
            "intermediate_steps": intermediate_steps
        })
        if isinstance(result, AgentFinish):
            return result
        
        # Get the appropriate tool from the registry
        tool_function = tool_registry.get_tool(result.tool)
        if tool_function is None:
            raise ValueError(f"No tool found for: {result.tool}")

        # Run the tool and capture the observation
        observation = tool_function.run(result.tool_input)
        intermediate_steps.append((result, observation))
