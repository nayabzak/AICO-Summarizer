# src/agent_setup.py
import os
from langchain.memory import ConversationBufferWindowMemory
from langchain.chains.summarize import load_summarize_chain
from langchain_huggingface import HuggingFacePipeline
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from transformers import pipeline
from bs4 import BeautifulSoup
from langchain.docstore.document import Document
from src.config import CONV_MEMORY_K, SUMMARY_CHAIN_TYPE
from langchain.tools import Tool
from langchain.agents import initialize_agent, AgentType

# Singleton resources for LLM and summarization chain
_llm = None
_summarize_chain = None
_memory = None
_agent = None


def get_llm():
    """
    Initialize and return a singleton HuggingFacePipeline LLM.
    """
    global _llm
    if _llm is None:
        hf_model = os.getenv("HUGGINGFACE_MODEL", "google/flan-t5-large")
        hf_pipe = pipeline(
            "text2text-generation",
            model=hf_model,
            tokenizer=hf_model,
            device_map="auto",
            max_length=512,
            temperature=0.7,
        )
        _llm = HuggingFacePipeline(pipeline=hf_pipe)
    return _llm


def get_summarize_chain():
    """
    Initialize and return a singleton summarization chain.
    """
    global _summarize_chain
    if _summarize_chain is None:
        _summarize_chain = load_summarize_chain(
            get_llm(),
            chain_type=SUMMARY_CHAIN_TYPE,
            verbose=True
        )
    return _summarize_chain


def browse_webpage_text(url: str) -> str:
    """
    Ephemeral Selenium WebDriver: navigate to URL and return visible text.
    """
    # Setup ChromeDriver using webdriver-manager
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    try:
        driver.get(url)
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        return soup.get_text(separator="")
    finally:
        driver.quit()


def summarize_webpage(url: str) -> str:
    """
    Browse and summarize a webpage using the refine summarization chain.
    """
    text = browse_webpage_text(url)
    docs = [Document(page_content=text)]
    return get_summarize_chain().run(docs)


def create_agent():
    """
    Create and return a LangChain agent with browsing and summarization tools and session memory.
    """
    global _agent, _memory
    if _agent is None:
        # Initialize memory
        _memory = ConversationBufferWindowMemory(
            k=CONV_MEMORY_K,
            return_messages=True
        )
        # Define tools
        browse_tool = Tool(
            name="BrowseWebPage",
            func=browse_webpage_text,
            description="Fetch the full text content of a webpage."
        )
        summarize_tool = Tool(
            name="SummarizeWebPage",
            func=summarize_webpage,
            description="Summarize the content of a webpage using the refine chain."
        )
        # Initialize agent
        _agent = initialize_agent(
            tools=[browse_tool, summarize_tool],
            llm=get_llm(),
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            memory=_memory,
            verbose=True
        )
    return _agent, _memory