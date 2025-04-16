

from autogen import ConversableAgent
from typing import Dict, Any

class MermaideDiagramAgent:
    name: str = "MermaideDiagramAgent"
    system_message: str = """
    You are an expert software architect.

    Your task is to read a given code file and generate a visual architecture diagram using Mermaid.js syntax.
    Focus on:
    1. High-level modules and packages.
    2. Class and function relationships (inheritance, calls).
    3. Imports and module-level structure.
    
    Output should be concise, visual, and suitable for developers to understand overall code architecture quickly.
    Only output the Mermaid.js code block, nothing else.
    """
    code_execution_config: bool = False
    human_input_mode: str = "NEVER"

    def to_dict(self):
        return {
            "name": self.name,
            "system_message": self.system_message,
            "code_execution_config": self.code_execution_config,
            "human_input_mode": self.human_input_mode
        }

    def make_agent(self, llm_config: Dict[str, Any]) -> ConversableAgent:
        return ConversableAgent(**self.to_dict(), llm_config=llm_config)