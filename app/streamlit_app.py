import streamlit as st
from sidebar import display_sidebar
from chat_interface import display_chat_interface

# Configure the page and hamburger menu
st.set_page_config(
    page_title="Document Analyzer Support Tool",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/yourusername/document-analyzer',
        'Report a bug': "https://github.com/yourusername/document-analyzer/issues",
        'About': "# Document Analyzer Support Tool\n\nThis tool helps you analyze documents using AI. Upload documents and ask questions about them."
    }
)

st.title("MetricStream Support Bot")

#Inittialize session state
if "messages" not in st.session_state:
    st.session_state["messages"] = []

if "session_id" not in st.session_state:
    st.session_state["session_id"] = None

#Display sidebar
display_sidebar()

#Display chat interface
display_chat_interface()