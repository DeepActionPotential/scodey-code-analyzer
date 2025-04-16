


from autogen import ConversableAgent, UserProxyAgent, AssistantAgent
from typing import Dict, Any


class CodeSummarizerAgent:
    name: str = 'CodeSummarizerAgent'
    system_message: str = """
    
        You are an expert software engineer and technical writer.

    Your job is to analyze the code provided to you and produce:
    1. A high-level summary of what the code is doing.
    2. An explanation of any major classes, functions, and logic flow.
    3. The purpose of the code (what task it's solving).
    4. Any helpful notes about the code structure or style, if relevant.

    Your goal is to make the code understandable to a junior developer or a non-expert.
    Keep the explanation concise, clear, and helpful.

    
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
    
    def make_agent(self, llm_config:Dict[str, Any]) -> ConversableAgent:
        return ConversableAgent(**self.to_dict(), llm_config=llm_config)




class CodeSmellDetectorAgent:
    name: str = 'CodeSmellDetectorAgent'
    system_message: str = """
You are an expert software engineer and code quality reviewer.

Your task is to detect code smells in the provided source code.
You should:
1. Identify common code smells such as:
   - Long methods/functions
   - God objects (classes doing too much)
   - Deep nesting
   - Duplicate code
   - Poor naming conventions
   - Too many parameters
   - Magic numbers or hardcoded values
   - Violations of the Single Responsibility Principle
2. Explain why each code smell is problematic.
3. Suggest specific refactoring strategies to improve the code quality.
4. Optionally, evaluate how severe the smell is (low, medium, high impact).

Present your findings clearly and helpfully as if you're mentoring a junior developer.
Do not rewrite the code unless asked to. Focus on code critique and reasoning.
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




class ComplexityAnalyzerAgent:
    name: str = "ComplexityAnalyzerAgent"
    system_message: str = """
    You are an expert software performance engineer and static code analyzer.

    Your job is to analyze the complexity of the given code file. Focus on:
    1. Cyclomatic complexity of each function.
    2. Deeply nested conditionals or loops.
    3. Long functions or classes that might be doing too much.
    4. Recommendations for breaking down complex parts.

    Provide a complexity score or risk level for each main function and class.
    Your output should be formatted and readable for engineers reviewing the code quality.
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

    def make_agent(self, llm_config: Dict[str, Any]) -> ConversableAgent :
        return ConversableAgent(**self.to_dict(), llm_config=llm_config)