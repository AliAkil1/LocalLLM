from openai import OpenAI
import streamlit as st
import json
import requests

class DeepSeekAPI:
    def __init__(self, api_key):
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com"
        )

    def make_api_call(self, messages):
        """Make API call with error handling"""
        try:
            st.write("Attempting to connect to DeepSeek API...")  # Debug statement
            response = self.client.chat.completions.create(
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

    def format_message_for_api(self, msg):
        """Format chat message for API consumption"""
        if "Source:" in msg["content"] and "Question:" in msg["content"]:
            parts = msg["content"].split("\n")
            question = parts[1].replace("Question: ", "").strip()
            return {"role": msg["role"], "content": question}
        return {"role": msg["role"], "content": msg["content"]} 