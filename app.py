import streamlit as st
import requests
import os
from dotenv import load_dotenv
from io import BytesIO

# Load API Key
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Streamlit Config
st.set_page_config(page_title="Future Mind AI", page_icon="🤖", layout="wide")

# Sidebar
st.sidebar.image("assets/logo.png", width=120)
st.sidebar.title("Future Mind AI")
st.sidebar.markdown("**Your AI-powered lecture assistant!**")

# Tabs for multiple features
tab1, tab2 = st.tabs(["Chat with AI", "Upload & Summarize Notes"])

with tab1:
    st.header("AI Chat Assistant")
    user_input = st.text_area("Ask your question here:")
    
    if st.button("Generate Answer"):
        if user_input:
            headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
            payload = {
                "model": "llama3-8b-8192",
                "messages": [{"role": "user", "content": user_input}]
            }
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers=headers, json=payload
            )
            if response.status_code == 200:
                result = response.json()
                st.success(result["choices"][0]["message"]["content"])
            else:
                st.error("Error connecting to Groq API")
        else:
            st.warning("Please enter a question!")

with tab2:
    st.header("Upload Lecture Notes")
    uploaded_file = st.file_uploader("Upload your text or Word file:", type=["txt", "docx"])
    
    if uploaded_file:
        file_content = uploaded_file.read().decode("utf-8", errors="ignore")
        st.text_area("Preview", file_content, height=200)
        
        if st.button("Generate Summary"):
            headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
            payload = {
                "model": "llama3-8b-8192",
                "messages": [{"role": "user", "content": f"Summarize this:\n{file_content}"}]
            }
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers=headers, json=payload
            )
            if response.status_code == 200:
                result = response.json()
                summary = result["choices"][0]["message"]["content"]
                st.success("Summary Generated!")
                st.text_area("Summary", summary, height=200)
                
                # Download button
                st.download_button("Download Summary", summary, file_name="Lecture_Summary.txt")
            else:
                st.error("Error connecting to Groq API")
