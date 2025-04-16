from autogen import ConversableAgent

import os
from typing import List, Dict, Optional, Callable
import time
import streamlit as st

from config import DefaultSettings, GeminiLLMConfig, OpenAILLMConfig, extension_to_language



def load_css(file_path):
    """Load and inject CSS styles from file."""
    try:
        with open(file_path, "r") as f:
            css = f.read()
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Failed to load CSS: {str(e)}")


    
def load_config(
    model_type: str) -> dict:
    """
    Load the configuration for a given model type.

    Args:
    - model_type (str): The type of model to load the config for. Supported options are 'google' and 'openai'.

    Returns:
    - dict: A dictionary containing the configuration for the specified model type.
    """
    if model_type == 'google':
        return GeminiLLMConfig().get_llm_config()
    elif model_type == 'openai':
        return OpenAILLMConfig().get_llm_config()
    else:
        raise ValueError(f"Unsupported model type: {model_type}")






def get_directory_tree(
    path: str, 
    indent: str = "", 
    exclude_folder: str = "__pycache__"
) -> str:
    """
    Returns a tree-like string representation of the directory at 'path', skipping excluded folders.
    """
    result = ""
    for item in os.listdir(path):
        if item == exclude_folder:
            continue
        full_path = os.path.join(path, item)
        if os.path.isdir(full_path):
            result += f"{indent}📁 {item}/\n"
            result += get_directory_tree(full_path, indent + "    ", exclude_folder)
        else:
            result += f"{indent}📄 {item}\n"
    return result




def detect_language_by_extension(file_path: str) -> str:
    """
    Detect the language of a file by its extension.

    Args:
        file_path (str): The path to the file to detect.

    Returns:
        str: The detected language.
    """
    _, ext = os.path.splitext(file_path.lower())
    return extension_to_language.get(ext, 'Unknown')





def get_supported_code_files(directory_path: str) -> List[str]:
    """
    Scans a directory for files with supported programming language extensions.

    Args:
        directory_path (str): Path to the directory to scan

    Returns:
        List[str]: List of absolute paths to supported code files
    """
    code_files = []
    for root, _, files in os.walk(directory_path):
        for file in files:
            _, ext = os.path.splitext(file)
            if ext in extension_to_language:
                full_path = os.path.join(root, file)
                code_files.append(full_path)
    return code_files

def analyze_code_with_agents(
    source_code: str, 
    analysis_agents: List[ConversableAgent]
) -> Dict[str, str]:
    """
    Analyzes source code using multiple code analysis agents.

    Args:
        source_code (str): The code to analyze
        analysis_agents (List[ConversableAgent]): List of agents to perform analysis

    Returns:
        Dict[str, str]: A dictionary mapping each agent's name to its analysis result
    """
    results = {}
    for agent in analysis_agents:
        agent_response = agent.generate_reply(messages=[{'role': 'user', 'content': source_code}])
        results[agent.name] = agent_response['content']
    return results

def analyze_code_file(
    file_path: str,
    analysis_agents: List[ConversableAgent]
) -> Optional[Dict[str, str]]:
    """
    Analyzes a single code file using multiple analysis agents.

    Args:
        file_path (str): Path to the code file to analyze
        analysis_agents (List[ConversableAgent]): List of agents to perform analysis

    Returns:
        Optional[Dict[str, str]]: Analysis results if successful, None if an error occurred
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            code = file.read()
            
        analysis_results = analyze_code_with_agents(code, analysis_agents)
        return analysis_results
        
    except UnicodeDecodeError:
        print(f"Skipping binary file {file_path}")
        return None
    except PermissionError:
        print(f"Permission denied for file {file_path}")
        return None
    except Exception as e:
        print(f"Error processing file {file_path}: {str(e)}")
        return None

def analyze_directory_with_agents(
    directory_path: str, 
    analysis_agents: List[ConversableAgent],
    time_between_analysis: int = 10,
    verbose: bool = False,
    callback_func: Callable[[int], None] = None
) -> Dict[str, Dict[str, str]]:
    """
    Analyzes all code files in a directory using multiple analysis agents.

    Args:
        directory_path (str): Path to the directory to analyze
        analysis_agents (List[ConversableAgent]): List of agents to perform analysis
        verbose (bool): Whether to print verbose output (default: False)

    Returns:
        Dict[str, Dict[str, str]]: A nested dictionary where:
            - Outer keys are file paths
            - Inner keys are agent names
            - Values are agent analysis results
    """
    if verbose:
        print(f"Started Analyzing using these agents {[agent.name for agent in analysis_agents]} [+]")

    analysis_results = {}
    
    # Get all supported code files in the directory
    code_files = get_supported_code_files(directory_path)

    # Progress Value
    progress_value = int( 100 / (len(code_files) + 1))
    
    # Process each code file
    for idx, file_path in enumerate(code_files):
        if callback_func:
            callback_func(idx, file_path, progress_value)
            
        try:
            agents_names = [agent.name for agent in analysis_agents]
            file_language = detect_language_by_extension(file_path)
            file_analysis = analyze_code_file(file_path, analysis_agents)
            
            if file_analysis is not None:
                analysis_results[file_path] = {
                    "language": file_language,
                    "analysis_results": file_analysis
                }
                
                if verbose:
                    print(f"Analyzed {file_path} Successfully using agents {agents_names} [+]")

        except Exception as e:
            print(f"Error processing file {file_path}: {str(e)}")
            continue
        


        time.sleep(time_between_analysis)
    
    if verbose:
        print(f"Analyzed {len(code_files)} files in {directory_path}")
    
    return analysis_results