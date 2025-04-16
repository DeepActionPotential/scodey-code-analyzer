from dataclasses import dataclass
from pickle import DICT
from autogen import ConversableAgent, UserProxyAgent, AssistantAgent
from autogen.tools import tool


from typing import Dict, Any, List





# ----------------------------------------------------------------
# General Config
# ----------------------------------------------------------------


extension_to_language = {
        '.py': 'Python',
        '.js': 'JavaScript',
        '.java': 'Java',
        '.cpp': 'C++',
        '.cxx': 'C++',
        '.cc': 'C++',
        '.c': 'C',
        '.cs': 'C#',
        '.rb': 'Ruby',
        '.php': 'PHP',
        '.html': 'HTML',
        '.htm': 'HTML',
        '.css': 'CSS',
        '.ts': 'TypeScript',
        '.go': 'Go',
        '.rs': 'Rust',
        '.swift': 'Swift',
        '.kt': 'Kotlin',
        '.m': 'Objective-C',
        '.sh': 'Shell',
        '.pl': 'Perl',
        '.r': 'R',
        '.lua': 'Lua',
        '.scala': 'Scala',
        '.sql': 'SQL',
        '.dart': 'Dart',
        '.jl': 'Julia',
        '.json': 'JSON',
        '.xml': 'XML',
        '.yml': 'YAML',
        '.yaml': 'YAML',
    }



@dataclass
class DefaultSettings:
    default_model_type: str = "google"
    default_display_language: str = "python"





@dataclass
class BaseLLMConfig:
    model_name: str
    api_key: str
    api_type: str
    temperature: float
    max_tokens: int

    def get_llm_config(self):
        return {'config_list': [
            {'model': self.model_name,
             'api_key': self.api_key,
             'api_type': self.api_type}
        ]}


@dataclass
class GeminiLLMConfig(BaseLLMConfig):
    model_name: str = "gemini-2.0-flash"
    api_key: str = "api-key"
    api_type: str = "google"
    temperature: float = 0.1
    max_tokens: int = 1024



@dataclass
class OpenAILLMConfig(BaseLLMConfig):
    model_name: str = "chatgpt-4"
    api_key: str = "api-key"
    api_type: str = "openai"
    temperature: float = 0.1
    max_tokens: int = 1024




