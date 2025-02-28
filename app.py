# Import necessary libraries
import streamlit as st
import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv, find_dotenv
from openai import OpenAI
import time
import PyPDF2
import io
import json

# Page configuration
st.set_page_config(
    page_title="Ali's Chatbot",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    /* Modern color palette */
    :root {
        --primary-color: #1a1a2e;
        --secondary-color: #0f3460;
        --accent-color: #1565C0;
        --background-color: #f8f9fa;
        --text-color: #1a1a2e;
        --border-color: #e0e0e0;
        --success-color: #0288D1;
        --error-color: #d32f2f;
        --shadow-color: rgba(26, 26, 46, 0.1);
    }

    /* Main container styling */
    .main {
        background-color: var(--background-color);
        color: var(--text-color);
        font-family: 'Inter', sans-serif;
        background-image: 
            radial-gradient(circle at 20% 20%, rgba(15, 52, 96, 0.05) 0%, transparent 50%),
            radial-gradient(circle at 80% 80%, rgba(21, 101, 192, 0.05) 0%, transparent 50%);
    }

    /* Button styling */
    .stButton>button {
        background: linear-gradient(135deg, #1565C0 0%, #0D47A1 100%);
        color: white;
        border-radius: 8px;
        border: none;
        padding: 12px 24px;
        width: 100%;
        font-weight: 600;
        letter-spacing: 0.5px;
        transition: all 0.2s ease;
        box-shadow: 0 4px 6px var(--shadow-color);
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px var(--shadow-color);
        background: linear-gradient(135deg, #1976D2 0%, #1565C0 100%);
    }

    /* Chat message styling */
    .chat-message {
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        position: relative;
        transition: all 0.3s ease;
    }

    .chat-message.user {
        background-color: white;
        border: 1px solid var(--border-color);
        margin-left: 2rem;
        box-shadow: 0 2px 4px var(--shadow-color);
    }

    .chat-message.user::before {
        content: '';
        position: absolute;
        left: -8px;
        top: 50%;
        transform: translateY(-50%) rotate(45deg);
        width: 16px;
        height: 16px;
        background: white;
        border-left: 1px solid var(--border-color);
        border-bottom: 1px solid var(--border-color);
    }

    .chat-message.assistant {
        background: linear-gradient(135deg, #1565C0 0%, #0D47A1 100%);
        color: white;
        margin-right: 2rem;
        box-shadow: 0 2px 4px var(--shadow-color);
    }

    .chat-message.assistant::before {
        content: '';
        position: absolute;
        right: -8px;
        top: 50%;
        transform: translateY(-50%) rotate(45deg);
        width: 16px;
        height: 16px;
        background: #1565C0;
    }

    /* Input area styling */
    .source-input {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        padding: 1.5rem;
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        box-shadow: 0 -4px 20px var(--shadow-color);
        border-top: 1px solid var(--border-color);
    }

    /* Text input styling */
    .stTextInput>div>div>input {
        border-radius: 8px;
        border: 2px solid var(--border-color);
        padding: 12px 16px;
        transition: all 0.3s ease;
        background: white;
    }

    .stTextInput>div>div>input:focus {
        border-color: var(--accent-color);
        box-shadow: 0 0 0 3px rgba(21, 101, 192, 0.1);
    }

    /* Chat container */
    .chat-container {
        margin-bottom: 180px;
        padding: 20px;
        max-width: 900px;
        margin-left: auto;
        margin-right: auto;
    }

    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, var(--primary-color) 0%, var(--secondary-color) 100%);
    }

    .css-1d391kg .sidebar-content {
        color: white;
    }

    /* File uploader styling */
    .stFileUploader {
        border-radius: 8px;
        border: 2px dashed var(--accent-color);
        padding: 16px;
        transition: all 0.3s ease;
        background: rgba(21, 101, 192, 0.05);
    }

    .stFileUploader:hover {
        background: rgba(21, 101, 192, 0.1);
        border-color: var(--accent-color);
    }

    /* Success/warning message styling */
    .stSuccess {
        border-radius: 8px;
        border-left: 4px solid var(--success-color);
        background: rgba(2, 136, 209, 0.1);
    }

    .stWarning {
        border-radius: 8px;
        border-left: 4px solid var(--error-color);
        background: rgba(211, 47, 47, 0.1);
    }

    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }

    ::-webkit-scrollbar-track {
        background: var(--background-color);
    }

    ::-webkit-scrollbar-thumb {
        background: var(--accent-color);
        border-radius: 4px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: var(--secondary-color);
    }

    /* Title styling */
    h1, h2, h3 {
        color: var(--primary-color);
        font-weight: 700;
        letter-spacing: -0.5px;
    }

    /* Image styling */
    img {
        border-radius: 12px;
        transition: transform 0.3s ease;
        filter: drop-shadow(0 4px 6px var(--shadow-color));
    }

    img:hover {
        transform: scale(1.05);
    }

    /* Loading spinner */
    .stSpinner > div {
        border-color: var(--accent-color) transparent transparent transparent;
    }

    /* Download button */
    .stDownloadButton>button {
        background: linear-gradient(135deg, #1565C0 0%, #0D47A1 100%);
    }

    .stDownloadButton>button:hover {
        background: linear-gradient(135deg, #1976D2 0%, #1565C0 100%);
    }

    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .chat-message {
        animation: fadeIn 0.3s ease-out;
    }

    /* API key input */
    .api-key-input {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px var(--shadow-color);
        border: 1px solid var(--border-color);
    }
    </style>
    """, unsafe_allow_html=True)

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

# Try to get API key from environment
env_api_key = os.getenv("DEEPSEEK_API_KEY")

# Sidebar with controls and API key input
with st.sidebar:
    st.image("https://img.icons8.com/clouds/200/000000/chat.png", width=100)
    st.title("Ali's Chatbot")
    st.markdown("---")
    
    # API Key Management
    st.markdown("### API Key Configuration")
    if not env_api_key or env_api_key == "your_api_key_here":
        st.warning("No API key found in environment.")
        st.markdown("""
        To use this app, you need a DeepSeek API key. You can:
        1. Get your API key from [DeepSeek Platform](https://platform.deepseek.com/api_keys)
        2. Enter it below
        """)
        api_key_input = st.text_input(
            "Enter your DeepSeek API key:",
            type="password",
            key="api_key_input",
            help="Your API key will be stored only for this session"
        )
        if api_key_input:
            st.session_state.api_key = api_key_input
            st.success("API key set successfully!")
    else:
        st.success("API key loaded from environment!")
        st.session_state.api_key = env_api_key
    
    st.markdown("---")
    if st.button("Clear Chat History", key="clear_chat"):
        st.session_state.chat_history = []
        st.session_state.content_cache = {}
        st.rerun()
    
    if st.session_state.chat_history:
        st.markdown("---")
        chat_history_text = "\n\n".join([f"{msg['role'].upper()}: {msg['content']}" for msg in st.session_state.chat_history])
        st.download_button(
            label="Download Chat History",
            data=chat_history_text,
            file_name=f"chat_history_{int(time.time())}.txt",
            mime="text/plain"
        )

# Check for API key before proceeding
if not st.session_state.api_key:
    st.warning("Please provide a DeepSeek API key in the sidebar to use the app.")
    st.stop()

# Initialize OpenAI client with DeepSeek configuration
client = OpenAI(
    api_key=st.session_state.api_key,
    base_url="https://api.deepseek.com"
)

def truncate_text(text, max_length=8000):
    """Truncate text to a maximum length while keeping whole sentences"""
    if len(text) <= max_length:
        return text
    
    # Find the last sentence boundary before max_length
    truncated = text[:max_length]
    last_period = truncated.rfind('.')
    if last_period != -1:
        return text[:last_period + 1]
    return truncated

def extract_text_from_pdf(pdf_file):
    """Extract text from uploaded PDF file"""
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return truncate_text(text)
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

def scrape_website(url):
    """Scrape and clean web content"""
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
            
        # Get text and clean it
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        return truncate_text(text)
    except Exception as e:
        return str(e)

def format_message_for_api(msg):
    """Format chat message for API consumption"""
    if "Source:" in msg["content"] and "Question:" in msg["content"]:
        parts = msg["content"].split("\n")
        question = parts[1].replace("Question: ", "").strip()
        return {"role": msg["role"], "content": question}
    return {"role": msg["role"], "content": msg["content"]}

def make_api_call(messages):
    """Make API call with error handling"""
    try:
        st.write("Attempting to connect to DeepSeek API...")  # Debug statement
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            temperature=0.7,
            max_tokens=2000
        )
        if not response or not response.choices:
            st.error("Received empty response from API")
            return None
            
        return response.choices[0].message.content
    except requests.exceptions.ConnectionError as ce:
        st.error("Connection error: Unable to reach the DeepSeek API.")
        st.error(f"Details: {str(ce)}")
    except Exception as e:
        st.error(f"API Error: {str(e)}")
        if hasattr(e, 'response') and hasattr(e.response, 'text'):
            try:
                error_details = json.loads(e.response.text)
                st.error(f"API Error Details: {json.dumps(error_details, indent=2)}")
            except json.JSONDecodeError:
                st.error(f"Raw API Error Response: {e.response.text}")
        return None

# Main chat container
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
chat_container = st.container()

# Display chat history in main container
with chat_container:
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
st.markdown('</div>', unsafe_allow_html=True)

# Input area at the bottom
with st.container():
    st.markdown("<div class='source-input'>", unsafe_allow_html=True)
    col1, col2 = st.columns([2, 1])
    
    with col1:
        url = st.text_input("Enter website URL (optional):", key="url_input", placeholder="https://example.com")
    
    with col2:
        uploaded_file = st.file_uploader("Upload PDF (optional)", type="pdf", label_visibility="collapsed")
    
    question = st.text_input("Enter your question:", key="question_input", placeholder="Ask me anything...")
    
    if st.button("Get Answer", key="submit"):
        if not question:
            st.warning("Please enter a question.")
            st.stop()
            
        # Add user's question to chat history
        if url or uploaded_file:
            source_type = "URL" if url else "PDF"
            source_id = url if url else uploaded_file.name
            user_message = {
                "role": "user",
                "content": f"Source: {source_type} - {source_id}\nQuestion: {question}"
            }
        else:
            user_message = {
                "role": "user",
                "content": question
            }
        st.session_state.chat_history.append(user_message)
        
        with st.chat_message("user"):
            st.markdown(user_message["content"])

        with st.spinner("Generating response..."):
            content = None
            # Get content from URL or PDF if provided
            if url or uploaded_file:
                source_id = url if url else uploaded_file.name
                if source_id not in st.session_state.content_cache:
                    if url:
                        content = scrape_website(url)
                    else:
                        content = extract_text_from_pdf(uploaded_file)
                        
                    if isinstance(content, str) and not content.startswith("Error"):
                        st.session_state.content_cache[source_id] = content
                    else:
                        st.error(f"Failed to process content: {content}")
                        st.session_state.chat_history.pop()
                        st.stop()
                
                content = st.session_state.content_cache.get(source_id)
                if not content:
                    st.error("Failed to retrieve content.")
                    st.session_state.chat_history.pop()
                    st.stop()
            
            # Prepare messages for the API
            messages = [
                {"role": "system", "content": "You are a helpful AI assistant. If content is provided, base your answers on that content. Otherwise, provide helpful and informative responses based on your general knowledge."}
            ]
            
            # Add formatted chat history for context
            for msg in st.session_state.chat_history[:-1]:
                messages.append(format_message_for_api(msg))
            
            # Add the current question with context if available
            if content:
                messages.append({
                    "role": "user",
                    "content": f"Based on this content: {content}\n\nPlease answer: {question}"
                })
            else:
                messages.append({
                    "role": "user",
                    "content": question
                })
            
            # Make API call with error handling
            response_content = make_api_call(messages)
            
            if response_content:
                # Add assistant's response to chat history
                assistant_message = {
                    "role": "assistant",
                    "content": response_content
                }
                st.session_state.chat_history.append(assistant_message)
                
                # Display the response
                with st.chat_message("assistant"):
                    st.markdown(assistant_message["content"])
            else:
                st.session_state.chat_history.pop()
    
    st.markdown("</div>", unsafe_allow_html=True)
