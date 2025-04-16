from typing import Dict, Any
from autogen import AssistantAgent

from services.utils import get_directory_tree

class DirectoryManagerAgent:
    """
    An assistant agent designed to inspect and analyze project directory structures.

    Your job is to:
    1. Fetch and present the directory tree of a given path.
    2. Identify the structure of codebases.
    3. Suggest which folders might contain main modules, tests, configs, documentation, etc.
    4. Help other agents decide what to analyze next based on the file layout.

    at the end of your response, show used python tools from my enviroment "functions"
    """

    name: str = 'DirectoryManagerAgent'
    system_message: str = """
    
    An assistant agent designed to inspect and analyze project directory structures.

    Your job is to:
    1. Fetch and present the directory tree of a given path.
    2. Identify the structure of codebases.
    3. Suggest which folders might contain main modules, tests, configs, documentation, etc.
    4. Help other agents decide what to analyze next based on the file layout.

    
    """
    human_input_mode: str = "NEVER"


    def to_dict(self) -> Dict[str, Any]:
        """Convert agent configuration to a dictionary"""
        return {
            "name": self.name,
            "system_message": self.system_message,
            "human_input_mode": self.human_input_mode,
        }


    def _store_function_tools(self) -> None:
        """Set the list of function tools for the agent"""
        self.tools =  [
        {
            "type": "function",
            "function": {
                "name": "get_directory_tree",
                "description": "Get directory tree structure starting from specified path, excluding certain folders",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "Directory path to start from (e.g., '.' for current directory)"
                        },
                        "indent": {
                            "type": "string",
                            "description": "Indentation string for formatting",
                            "default": ""
                        },
                        "exclude_folder": {
                            "type": "string",
                            "description": "Folder name to exclude from the tree",
                            "default": "__pycache__"
                        }
                    },
                    "required": ["path"]
                }
            }
        }
        ]

    
    def _add_agents_tools_to_config(self, llm_config:Dict[str, Any]) -> None:
        """Add the tools to the llm_config"""
        llm_config["tools"] = self.tools
        return llm_config

    def make_agent(self, llm_config: Dict[str, Any]) -> AssistantAgent:
        """Create an instance of the agent with the given configuration"""
        self._store_function_tools()
        self.llm_config = self._add_agents_tools_to_config(llm_config)

        return AssistantAgent(
            **self.to_dict(), 
            llm_config=self.llm_config,
            code_execution_config={"work_dir": ".", 'use_docker': False},
            function_map={
            "get_directory_tree": get_directory_tree
        }
        )