# src/config.py
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Hugging Face settings
HUGGINGFACE_MODEL = os.getenv("HUGGINGFACE_MODEL", "google/flan-t5-large")
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")

# Playwright/Selenium settings
# PLAYWRIGHT_BROWSERS_PATH unused when using Selenium

# FastAPI settings
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))

# Agent settings
CONV_MEMORY_K = int(os.getenv("CONV_MEMORY_K", "3"))
SUMMARY_CHAIN_TYPE = os.getenv("SUMMARY_CHAIN_TYPE", "refine")

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "info")
