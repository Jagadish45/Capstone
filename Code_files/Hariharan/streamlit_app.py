import streamlit as st
import requests
from PIL import Image

# FastAPI Server URL
FASTAPI_URL = "http://127.0.0.1:8000"

# Custom UI Styles
st.set_page_config(page_title="LLM Query Service", page_icon="🤖", layout="wide")
st.markdown("""
    <style>
        .main-title {text-align: center; font-size: 2.5rem; color: #2C3E50;}
        .subheader {font-size: 1.5rem; color: #34495E;}
        .poll-container {text-align: center; margin-bottom: 20px;}
        .feedback-container {text-align: center; margin-top: 30px;}
        .query-box {background-color: #f8f9fa; padding: 15px; border-radius: 10px;}
        .file-upload-box {border: 2px dashed #4A90E2; padding: 20px; border-radius: 10px; text-align: center;}
        .comments-section {border-top: 2px solid #BDC3C7; padding-top: 20px; margin-top: 30px;}
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>🤖 LLM Query Service</h1>", unsafe_allow_html=True)

# Step Selection Poll
st.markdown("<h2 class='subheader poll-container'>📊 How would you like to proceed?</h2>", unsafe_allow_html=True)
choice = st.radio("", ["📄 Report", "📜 Step-by-step Guidance"], horizontal=True)

# Query Section
st.markdown("<h2 class='subheader'>🔍 Ask the LLM</h2>", unsafe_allow_html=True)
with st.container():
    user_query = st.text_area("Enter your query:", height=150)
    if st.button("Submit Query", use_container_width=True):
        if user_query:
            response = requests.post(f"{FASTAPI_URL}/query/", json={"user_query": user_query})
            if response.status_code == 200:
                st.success("Response:")
                st.write(response.json()["response"])
            else:
                st.error("Error: Could not retrieve response.")

# File Upload Section
st.markdown("<h2 class='subheader'>📂 Upload a Document</h2>", unsafe_allow_html=True)
with st.container():
    st.markdown("<div class='file-upload-box'>Drag and drop or select a file to upload</div>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("", type=["txt", "pdf", "csv", "docx"], label_visibility="collapsed")
    if uploaded_file and st.button("Upload", use_container_width=True):
        files = {"file": uploaded_file.getvalue()}
        response = requests.post(f"{FASTAPI_URL}/upload/", files=files)
        if response.status_code == 200:
            st.success("File uploaded successfully!")
        else:
            st.error("Error: File upload failed.")

# Feedback Section
st.markdown("<h2 class='subheader feedback-container'>👍 Did you find this helpful?</h2>", unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    if st.button("👍 Like", use_container_width=True):
        st.toast("Thank you for your feedback! 😊")
with col2:
    if st.button("👎 Dislike", use_container_width=True):
        st.toast("We'll work on improving this! 🙌")

# Past Comments Section
st.markdown("<h2 class='subheader comments-section'>💬 Past Comments</h2>", unsafe_allow_html=True)
past_comments = requests.get(f"{FASTAPI_URL}/comments/")
if past_comments.status_code == 200:
    comments = past_comments.json()
    for comment in comments:
        st.write(f"🗨 {comment}")
else:
    st.write("No past comments available.")
