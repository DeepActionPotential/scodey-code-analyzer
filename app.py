from typing import List
import streamlit as st
from tkinter import Tk, filedialog
from streamlit.components.v1 import html
from autogen import ConversableAgent


from ui.introductory_page import IntroductoryPage
from ui.analysis_page import NavigationPanel, CodePreview, ResultsDisplay


from agents.code_overview_agents import CodeSummarizerAgent, CodeSmellDetectorAgent
from agents.code_structure_agents import DesignPatternDetectorAgent, DesignPatternRecommenderAgent, SOLIDPrinciplesManagerAgent
from agents.code_visualization_agents import MermaideDiagramAgent


from config import DefaultSettings
from utils.utils import load_config, load_css





# Configuration and Agent Initialization
llm_config = load_config(DefaultSettings().default_model_type)
agents = [
    CodeSummarizerAgent().make_agent(llm_config),
    CodeSmellDetectorAgent().make_agent(llm_config),
    DesignPatternDetectorAgent().make_agent(llm_config),
    DesignPatternRecommenderAgent().make_agent(llm_config),
    SOLIDPrinciplesManagerAgent().make_agent(llm_config),
    MermaideDiagramAgent().make_agent(llm_config)
]



class AnalysisManager:
    """Manages and provides access to analysis results."""
    
    def __init__(self, results):
        load_css("./ui/styles.css")
        self.results = results
    
    def get_file_data(self, file_path):
        return self.results.get(file_path, {})
    
    def list_files(self):
        return list(self.results.keys())



class CodeAnalysisApp:
    """Main application orchestrator."""


    def __init__(self, agents: List[ConversableAgent]) -> None:
        self.agents = agents
    
    def run(self):
        """Main application entry point."""
        st.set_page_config(
            layout="wide",
            initial_sidebar_state="expanded",
            page_icon="🔍"
        )
        
        if not self._check_analysis_state():
            IntroductoryPage(self.agents).render()
            return
        
        self._setup_interface()
        self._render_main_view()
        self._add_reset_button()

    def _check_analysis_state(self):
        """Validate analysis completion status."""
        if 'analysis_done' not in st.session_state:
            st.session_state.analysis_done = False
        return st.session_state.get('results') and st.session_state.analysis_done

    def _setup_interface(self):
        """Initialize application components."""
        load_css("./ui/styles.css")
        self.analysis = AnalysisManager(st.session_state.results)
        self.nav = NavigationPanel(self.analysis.list_files())

    def _render_main_view(self):
        """Display main two-column interface."""
        selected_file = self.nav.render()
        file_data = self.analysis.get_file_data(selected_file)
        
        col1, col2 = st.columns([0.5, 0.5])
        with col1:
            CodePreview(
                file_path=selected_file,
                language=file_data['language']
            ).render()
        
        with col2:
            ResultsDisplay(
                file_data['analysis_results']
            ).render()

    def _add_reset_button(self):
        """Add sidebar reset functionality."""
        st.sidebar.button(
            "New Analysis",
            on_click=self._reset_state
        )

    def _reset_state(self):
        """Clear analysis-related session state."""
        state_keys = ['results', 'analysis_done', 'selected_dir', 'prev_dir']
        for key in state_keys:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()


if __name__ == "__main__":
    CodeAnalysisApp(agents).run()