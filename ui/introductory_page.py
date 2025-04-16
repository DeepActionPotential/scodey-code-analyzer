import os
import streamlit as st
from tkinter import Tk, filedialog
import time

from utils.utils import analyze_directory_with_agents, load_css







class IntroductoryPage:
    """Handles directory selection and initial analysis."""
    
    def __init__(self, agents):
        self.agents = agents
        self._init_session_state()

    def _init_session_state(self):
        required_state = {
            'analysis_done': False,
            'selected_dir': None,
            'prev_dir': None,
            'results': None
        }
        for key, val in required_state.items():
            if key not in st.session_state:
                st.session_state[key] = val

    @staticmethod
    def _select_directory():
        """Open system directory picker."""
        root = Tk()
        root.withdraw()
        root.wm_attributes('-topmost', 1)
        directory = filedialog.askdirectory(parent=root)
        root.destroy()
        return directory

    def _process_directory(self):
        """Handle directory selection and analysis."""
        directory = self._select_directory()
        
        if not directory:
            st.warning("No directory selected")
            return
            
        if not os.path.isdir(directory):
            st.error("Invalid directory")
            return

        st.session_state.selected_dir = directory
        self._analyze_directory(directory)

    
    def _progress_bar_callback_func(
        self, 
        current_idx: int, 
        file_path: str, 
        progress_value: int
    ) -> None:
        """
        Callback function for `analyze_directory_with_agents`.
        Updates the progress bar and status text with the current file being processed.
        """
        if current_idx == 0:
            self.status_text.markdown("🔍 Analyzing code structure...")
        



        progress_value = progress_value if progress_value < 100 else 100
        self.progress_bar.progress(current_idx * progress_value)
        self.status_text.markdown(f"Processing {file_path}")




        
        

    def _analyze_directory(self, directory):
        """Run analysis on selected directory with progress bar."""
        self.progress_bar = st.progress(0)
        self.status_text = st.empty()

        try:

            st.session_state.results = analyze_directory_with_agents(
                directory, self.agents, verbose=True, callback_func = self._progress_bar_callback_func
            )

            st.session_state.analysis_done = True
            st.rerun()

        except Exception as e:
            self.status_text.empty()
            st.error(f"Analysis failed: {str(e)}")
            st.session_state.analysis_done = False
            st.session_state.selected_dir = None

    def render(self):
        """Main entry point for introductory page."""
        self._handle_state()
        
        if not st.session_state.analysis_done:
            self._render_selector()

    def _render_selector(self):
        """Render file selection interface."""
        load_css("./ui/styles.css")
        if st.button("Select Directory", key="start_button"):
            self._process_directory()

    def _handle_state(self):
        """Manage session state transitions."""
        if st.session_state.selected_dir != st.session_state.prev_dir:
            st.session_state.analysis_done = False
            st.session_state.prev_dir = st.session_state.selected_dir