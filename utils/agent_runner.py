# This function is not needed. Same functionality is provided by the AgentExecutor from langchain.agents


from langchain.schema.agent import AgentFinish
from utils.tool_registry import tool_registry

def run_agent(agent_chain, user_input):
    intermediate_steps = []  # List to store intermediate steps and outputs of each tool
    tools_ran = []  # List to keep track of all tools that were run

    while True:
        try:
            result = agent_chain.invoke({
                "input": user_input, 
                "intermediate_steps": intermediate_steps
            })
        except Exception as e:
            return {
                "error": e,
                "tools_ran": tools_ran
            }
            

        if isinstance(result, AgentFinish):
            return {
                "final_result": result,
                "tools_ran": tools_ran
            }
        
        # Get the appropriate tool from the registry
        tool_function = tool_registry.get_tool(result.tool)
        if tool_function is None:
            raise ValueError(f"No tool found for: {result.tool}")

        # Run the tool and capture the observation
        observation = tool_function.run(result.tool_input)
        intermediate_steps.append((result, observation))

        # Track the tool and its params that was run
        tools_ran.append({"tool_name": result.tool, "tool_params": result.tool_input})
