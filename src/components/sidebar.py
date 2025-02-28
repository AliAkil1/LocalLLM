import streamlit as st
import time

def render_sidebar():
    """Render the sidebar with API key management and controls"""
    with st.sidebar:
        st.image("https://img.icons8.com/clouds/200/000000/chat.png", width=100)
        st.title("Ali's Chatbot")
        st.markdown("---")
        
        # API Key Management
        st.markdown("### API Key Configuration")
        env_api_key = st.session_state.get('env_api_key')
        
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
        
        if st.session_state.get('chat_history', []):
            st.markdown("---")
            chat_history_text = "\n\n".join([
                f"{msg['role'].upper()}: {msg['content']}" 
                for msg in st.session_state.chat_history
            ])
            st.download_button(
                label="Download Chat History",
                data=chat_history_text,
                file_name=f"chat_history_{int(time.time())}.txt",
                mime="text/plain"
            ) 