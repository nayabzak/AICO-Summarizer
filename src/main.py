# src/main.py
import uvicorn
import logging
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, HttpUrl
from src.config import API_HOST, API_PORT, LOG_LEVEL
from src.agent_setup import summarize_webpage, get_llm
from src.utils import is_valid_url
from langchain.chains import LLMChain 
from langchain.prompts import PromptTemplate

# Initialize logging
logging.basicConfig(level=LOG_LEVEL.upper())
logger = logging.getLogger(__name__)

# FastAPI app
tmp_app = FastAPI(title="AICO Summarizer")

# Request and Response models
class SummarizeRequest(BaseModel):
    url: HttpUrl

class SummarizeResponse(BaseModel):
    summary: str
    main_topic: str

# Health check endpoint
@tmp_app.get("/health")
def health_check():
    return {"status": "ok"}

# Summarize endpoint
@tmp_app.post("/summarize", response_model=SummarizeResponse)
def summarize_endpoint(request: SummarizeRequest):
    url = str(request.url)
    if not is_valid_url(url):
        raise HTTPException(status_code=400, detail="Invalid URL format.")
    try:
        # Fetch and summarize webpage
        summary = summarize_webpage(url)

        # Extract main topic using LLMChain
        llm = get_llm()
        # Define a prompt template for extracting the main topic
        prompt = PromptTemplate.from_template(
            "What is the main topic of the following summary? Summary: {summary_text}"
        )
        # Create an LLMChain
        chain = LLMChain(llm=llm, prompt=prompt)

        # Invoke the chain
        # The result structure might vary slightly based on LangChain version.
        # For newer versions, result is a dict. For older, .run() might return a string directly.
        main_topic_result = chain.invoke({"summary_text": summary})

        # Extract the text from the result. Adjust 'text' key if necessary.
        main_topic = main_topic_result.get('text', 'Could not determine main topic').strip()

        return SummarizeResponse(summary=summary, main_topic=main_topic)
    except Exception as e:
        logger.error(f"Error processing URL {url}: {e}")
        # Consider logging the full traceback here for better debugging:
        # import traceback
        # logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Failed to process the URL: {e}")


# Global exception handler
@tmp_app.exception_handler(Exception)
def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error: {exc}")
    return JSONResponse(status_code=500, content={"detail": "Internal server error."})

# Shutdown event to clean up Selenium driver
@tmp_app.on_event("shutdown")
def shutdown_event():
    logger.info("Shutting down: closing webdriver.")
    try:
        from src.agent_setup import get_webdriver
        driver = get_webdriver()
        driver.quit()
    except Exception as ex:
        logger.warning(f"Error shutting down webdriver: {ex}")

if __name__ == "__main__":
    uvicorn.run("src.main:tmp_app", host=API_HOST, port=API_PORT, log_level=LOG_LEVEL)