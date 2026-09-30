import os
import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 1. Load Environment Variables
load_dotenv()

# 2. Page Configuration
st.set_page_config(
    page_title="LegalEase AI - Document & Complaint Generator",
    page_icon="⚖️",
    layout="wide"
)

# 3. Model Setup
@st.cache_resource
def load_llm():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        st.error("⚠️ API Key not found. Please set OPENAI_API_KEY in your .env file.")
        st.stop()
    return ChatOpenAI(model="gpt-4o-mini", temperature=0.2)

llm = load_llm()

# 4. Prompt Templates
SUMMARIZE_PROMPT = ChatPromptTemplate.from_template(
    """You are LegalEase AI, an expert legal educational assistant. 
Translate and explain the following legal text or contract into simple, plain English. 
Highlight key obligations, liabilities, renewal terms, and potential risk areas for the user.

Legal Text:
{user_input}
"""
)

COMPLAINT_PROMPT = ChatPromptTemplate.from_template(
    """You are LegalEase AI, a consumer advocacy assistant.
Draft a formal, professional consumer complaint letter based on the details provided below.
Include appropriate placeholders like [Your Name], [Company Name], and [Date] where required.

Issue Details:
{user_input}
"""
)

RIGHTS_PROMPT = ChatPromptTemplate.from_template(
    """You are LegalEase AI.
Based on the following dispute scenario, outline the legal and consumer rights relevant to the user, 
and suggest actionable next steps or government grievance mechanisms/portals to reach out to.

Scenario:
{user_input}
"""
)

# 5. Core Processing Function
def process_legal_request(prompt_template, text):
    chain = prompt_template | llm | StrOutputParser()
    return chain.invoke({"user_input": text})

# 6. Streamlit User Interface
def main():
    st.title("⚖️ LegalEase AI Generator")
    st.caption("Simplify legal documents, analyze consumer rights, and draft formal complaint letters.")

    # Sidebar Navigation
    st.sidebar.header("Navigation")
    task = st.sidebar.radio(
        "Choose an AI Tool:",
        [
            "📄 Document Simplifier",
            "✉️ Complaint Generator",
            "🛡️️ Consumer Rights Analyzer"
        ]
    )

    st.sidebar.markdown("---")
    st.sidebar.info(
        "**Disclaimer:** LegalEase AI provides educational information and automated drafts. "
        "It does not constitute official legal advice."
    )

    # Main Tool Views
    if task == "📄 Document Simplifier":
        st.subheader("Document Simplifier & Risk Analyzer")
        input_text = st.text_area(
            "Paste contract clauses, legal documents, or terms of service here:",
            height=200,
            placeholder="Paste text here..."
        )
        if st.button("Simplify & Analyze", type="primary"):
            if not input_text.strip():
                st.warning("Please enter some legal text to analyze.")
            else:
                with st.spinner("Analyzing document and detecting potential risks..."):
                    result = process_legal_request(SUMMARIZE_PROMPT, input_text)
                    st.success("Analysis Complete!")
                    st.markdown("### Simplified Analysis")
                    st.markdown(result)

    elif task == "✉️ Complaint Generator":
        st.subheader("Consumer Complaint Generator")
        input_text = st.text_area(
            "Describe the product, service, or grievance issue in detail:",
            height=200,
            placeholder="E.g., I bought an electronic item online on Sept 10. It arrived damaged, and customer support refused a refund..."
        )
        if st.button("Generate Complaint Draft", type="primary"):
            if not input_text.strip():
                st.warning("Please describe your issue first.")
            else:
                with st.spinner("Drafting your formal complaint letter..."):
                    result = process_legal_request(COMPLAINT_PROMPT, input_text)
                    st.success("Draft Generated!")
                    st.markdown("### Draft Letter")
                    st.code(result, language="markdown")

    elif task == "🛡️ Consumer Rights Analyzer":
        st.subheader("Consumer Rights & Next Steps")
        input_text = st.text_area(
            "Describe the issue or dispute you are facing:",
            height=200,
            placeholder="Describe your legal query or dispute..."
        )
        if st.button("Analyze Rights & Options", type="primary"):
            if not input_text.strip():
                st.warning("Please provide details regarding your situation.")
            else:
                with st.spinner("Evaluating applicable rights and grievance options..."):
                    result = process_legal_request(RIGHTS_PROMPT, input_text)
                    st.success("Guidance Ready!")
                    st.markdown("### Rights & Actionable Steps")
                    st.markdown(result)

if __name__ == "__main__":
    main()