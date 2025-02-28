import streamlit as st
import os
from dotenv import load_dotenv, find_dotenv
from src.components.sidebar import render_sidebar
from src.components.chat_interface import display_chat_history, render_input_area
from src.services.api_service import DeepSeekAPI

# Page configuration
st.set_page_config(
    page_title="Ali's Chatbot",
    page_icon="🤖",
    layout="wide"
)

# Load CSS
css_path = os.path.join(os.path.dirname(__file__), 'styles', 'main.css')
with open(css_path) as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'content_cache' not in st.session_state:
    st.session_state.content_cache = {}
if 'api_key' not in st.session_state:
    st.session_state.api_key = None

# Load environment variables
dotenv_path = find_dotenv()
load_dotenv(dotenv_path, override=True)
st.session_state.env_api_key = os.getenv("DEEPSEEK_API_KEY")

# Render sidebar
render_sidebar()

# Check for API key before proceeding
if not st.session_state.api_key:
    st.warning("Please provide a DeepSeek API key in the sidebar to use the app.")
    st.stop()

# Initialize API service
api_service = DeepSeekAPI(st.session_state.api_key)

# Display chat interface
display_chat_history()
render_input_area(api_service) 