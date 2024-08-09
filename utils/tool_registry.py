class ToolRegistry:
    def __init__(self):
        self._registry = {}

    def register_tool(self, name: str, func):
        """Registers a tool function with a given name."""
        if name in self._registry:
            raise ValueError(f"Tool with name '{name}' is already registered.")
        self._registry[name] = func

    def get_tool(self, name: str):
        """Retrieves a tool function by name."""
        return self._registry.get(name, None)

    def get_tools(self):
        """get all registered tools function."""
        return list(self._registry.values())

    def list_tools_name(self):
        """Lists all registered tools."""
        return list(self._registry.keys())

# Instantiate a global tool registry
tool_registry = ToolRegistry()
