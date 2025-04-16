# CodeReader

A powerful code analysis tool that leverages AI agents to provide comprehensive insights into your codebase. CodeReader analyzes code structure, design patterns, code quality, and generates visual diagrams to help you understand and improve your code.

## Features

- **Code Analysis**
  - Design pattern detection and recommendations
  - Code quality assessment
  - SOLID principles evaluation
  - Code smell detection

- **Visualizations**
  - Mermaid diagrams for code structure
  - Interactive code previews
  - File dependency visualization

- **User Interface**
  - Streamlit-based web interface
  - Directory selection and analysis
  - Detailed analysis results display
  - Code preview with syntax highlighting

## Project Structure

```
code-reader/
├── ui/                   # Streamlit UI components
│   ├── __init__.py      # Module initialization
│   ├── introductory_page.py # Initial directory selection UI
│   └── analysis_page.py  # Analysis results display
│
├── agents/               # AI agents for code analysis
│   ├── __init__.py      # Module initialization
│   ├── code_overview_agents.py # Code summarization and smell detection
│   ├── code_structure_agents.py # Design pattern and SOLID analysis
│   ├── code_visualization_agents.py # Code visualization with Mermaid
│   ├── directory_agents.py # Directory analysis
│   └── manager_agent.py   # Agent orchestration
│
├── scripts/              # Utility scripts
│   ├── __init__.py      # Module initialization
│   └── utils.py         # Helper functions and utilities
│
├── config.py            # Configuration settings
├── requirements.txt     # Project dependencies
├── app.py              # Main application entry point
└── run.py              # Application runner
```
