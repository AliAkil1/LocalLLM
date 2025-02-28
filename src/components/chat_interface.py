import streamlit as st
from src.utils.content_processor import scrape_website, extract_text_from_pdf

def display_chat_history():
    """Display the chat history in the main container"""
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    chat_container = st.container()

    with chat_container:
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    st.markdown('</div>', unsafe_allow_html=True)

def render_input_area(api_service):
    """Render the input area for URL, PDF, and questions"""
    with st.container():
        st.markdown("<div class='source-input'>", unsafe_allow_html=True)
        col1, col2 = st.columns([2, 1])
        
        with col1:
            url = st.text_input("Enter website URL (optional):", key="url_input", placeholder="https://example.com")
        
        with col2:
            uploaded_file = st.file_uploader("Upload PDF (optional)", type="pdf", label_visibility="collapsed")
        
        question = st.text_input("Enter your question:", key="question_input", placeholder="Ask me anything...")
        
        if st.button("Get Answer", key="submit"):
            process_user_input(question, url, uploaded_file, api_service)
        
        st.markdown("</div>", unsafe_allow_html=True)

def process_user_input(question, url, uploaded_file, api_service):
    """Process user input and generate response"""
    if not question:
        st.warning("Please enter a question.")
        return
        
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
                    return
            
            content = st.session_state.content_cache.get(source_id)
            if not content:
                st.error("Failed to retrieve content.")
                st.session_state.chat_history.pop()
                return
        
        # Prepare messages for the API
        messages = [
            {"role": "system", "content": "You are a helpful AI assistant. If content is provided, base your answers on that content. Otherwise, provide helpful and informative responses based on your general knowledge."}
        ]
        
        # Add formatted chat history for context
        for msg in st.session_state.chat_history[:-1]:
            messages.append(api_service.format_message_for_api(msg))
        
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
        response_content = api_service.make_api_call(messages)
        
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