# Summarize Content from YouTube or Website using LangChain + Groq

import os
import streamlit as st
import validators
from dotenv import load_dotenv

from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import YoutubeLoader, UnstructuredURLLoader

# ===============================
# 1. Load environment variables
# ===============================
load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY", "")

# ====================================
# 2. Optionally enable LangSmith tracing
# ====================================
try:
    from langsmith import traceable
    tracing_enabled = True
    os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGSMITH_API_KEY", "")
    os.environ["LANGSMITH_PROJECT"] = os.getenv("LANGSMITH_PROJECT", "yt_url_summary")
    os.environ["LANGSMITH_RUN_NAME"] = os.getenv("LANGSMITH_RUN_NAME", "yt_or_web_summary")
    os.environ["LANGSMITH_TRACING"] = "true"
except ImportError:
    tracing_enabled = False

# =============================
# 3. Setup Streamlit UI Layout
# =============================
st.set_page_config(page_title="LangChain: Summarize Text From YT or Website")
st.title("LangChain: Summarize Text From YouTube or Website")
st.subheader("Summarize Any URL Content")

# Sidebar input for API key and LangSmith toggle
with st.sidebar:
    groq_api_key = os.getenv("GROQ_API_KEY") or st.text_input("GROQ API Key", type="password")
    use_langsmith = st.checkbox("Enable LangSmith Tracing", value=tracing_enabled)

# ======================
# 4. Handle Input Fields
# ======================
generic_url = st.text_input("Enter a YouTube or Website URL")

# Validate and initialize LLM
if groq_api_key:
    llm = ChatGroq(model="llama3-70b-8192", groq_api_key=groq_api_key)
else:
    st.warning("Please enter a valid GROQ API Key to continue")
    st.stop()

# ================================
# 5. Define summarization prompt
# ================================
prompt_template = """
Provide a concise and informative summary of the following content in under 300 words:
Content: {text}
"""
prompt = PromptTemplate(template=prompt_template, input_variables=["text"])

# ============================================
# 6. Load content and perform summarization
# ============================================
def load_content(url: str):
    """Dynamically load content from YouTube or website."""
    try:
        if "youtube.com" in url or "youtu.be" in url:
            return YoutubeLoader.from_youtube_url(url, add_video_info=True).load()
        else:
            return UnstructuredURLLoader(
                urls=[url],
                ssl_verify=False,
                headers={
                    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_1) Chrome/116.0.0.0"
                },
            ).load()
    except Exception as e:
        st.error(f"❌ Error loading content from URL: {url}")
        st.exception(e)
        return []

def run_summary_chain(llm, docs, prompt, enable_trace=False):
    """Runs the summarization chain with optional LangSmith tracing."""
    chain = load_summarize_chain(llm, chain_type="stuff", prompt=prompt)
    if enable_trace:
        st.warning("wrap_chain is not available in your langsmith installation. Tracing is enabled, but wrapping is skipped.")
    return chain.run(docs)

# ===================================
# 7. Trigger summarization workflow
# ===================================
if st.button("Summarize the Content"):
    if not generic_url.strip():
        st.error("Please provide a URL to summarize")
    elif not validators.url(generic_url):
        st.error("Please enter a valid URL (YouTube or Website)")
    else:
        try:
            with st.spinner("Loading and summarizing content..."):
                documents = load_content(generic_url)
                if documents:
                    summary = run_summary_chain(llm, documents, prompt, enable_trace=use_langsmith)
                    st.success("Summary:")
                    st.write(summary)
                else:
                    st.warning("No documents were returned for summarization.")
        except Exception as e:
            st.error("An error occurred during summarization.")
            st.exception(e)
