**AICO Summarizer**

A simple FastAPI service that fetches a webpage with Selenium, summarizes its content using a LangChain refine chain with a HuggingFace Flan-T5 model, and returns both a concise summary and the main topic.

**What It Does**

Fetches the raw HTML of any URL via a headless Chrome browser (Selenium + webdriver-manager).

Extracts visible text from the page using BeautifulSoup.

Summarizes the text with a LangChain refine summarization chain powered by the free google/flan-t5-large model.

Returns a JSON response containing:

summary: high-quality, concise summary

main_topic: the key topic extracted from the summary

**Getting Started**

1. Clone & Install

git clone https://github.com/nayabzak/AICO-Summarizer.git
cd aico_summarizer
python -m venv venv

# Windows: .\\venv\\Scripts\\activate

# Unix: source venv/bin/activate

pip install -r requirements.txt
pip install selenium webdriver-manager beautifulsoup4 langchain-huggingface

**2**. Create .env****

In the project root, add a .env file:

HUGGINGFACE_MODEL=google/flan-t5-large
HUGGINGFACE_TOKEN=
API_HOST=0.0.0.0
API_PORT=8000
CONV_MEMORY_K=3
SUMMARY_CHAIN_TYPE=refine
LOG_LEVEL=info

**3. Run the Service**

uvicorn src.main:app --reload

Visit Swagger UI at http://127.0.0.1:8000/docs

Health check: GET /health

Summarize a page: POST /summarize with JSON { "url": "https://example.com" }

**4. Quick Test Script
**
python quick_test.py

That’s it—your summarization API is ready! Feel free to tweak memory window (CONV_MEMORY_K) or chain type (SUMMARY_CHAIN_TYPE) in .env to suit your needs.
