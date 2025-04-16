import os
import streamlit as st

from utils.utils import load_css




class NavigationPanel:
    """Renders the sidebar file navigation."""
    
    def __init__(self, files):
        self.files = files
    
    def render(self):
        load_css("./ui/styles.css")
        with st.sidebar:
            st.title("Code Analyis")

            selected = st.selectbox(
                "Select File",
                self.files,
                format_func=os.path.basename
            )

        return selected


class CodePreview:
    """Displays file contents with syntax highlighting."""
    
    def __init__(self, file_path, language):
        load_css("./ui/styles.css")
        self.file_path = file_path
        self.language = language.lower()
    
    def render(self):
        st.header("Code Preview")
        try:
            with open(self.file_path, 'r') as f:
                st.code(f.read(), language=self.language)
        except FileNotFoundError:
            st.error("File not found")


class ResultsDisplay:
    """Presents analysis results in expandable sections."""
    
    def __init__(self, results):
        load_css("./ui/styles.css")
        self.results = results
    
    def render(self):
        st.header("Analysis")
        for agent, findings in self.results.items():
            with st.expander(f"{agent}", expanded=False):
                st.write(findings)