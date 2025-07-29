from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.core.mcp import MCPOrchestrator
from typing import Any, Dict,List
from dotenv import load_dotenv
import os
import json
import logging
from ..models.search_criteria import SearchCriteria

load_dotenv()
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

router = APIRouter()
#search_criteria = SearchCriteria()

"""class KVIn(BaseModel):
    key: str
    value: Any"""

class Request(BaseModel):
    file_path: str
    search_criteria: Dict[str, Any]

class Response(BaseModel):
    reports: str
    #key: str
# Language models
language_models = {
    'gemini': {
        "api_key": os.getenv('GEMINI_API_KEY'),
        "model": os.getenv('GEMINI_VERSION')
        },
    'openai': {
        "api_key": os.getenv('OPENAI_API_KEY'),
        "model": os.getenv('OPENAI_VERSION')
        },
    'grok': {
        "api_key": os.getenv('GROK_API_KEY'),
        "model": os.getenv('GROK_VERSION')
        },
    'deepseek': {
        "api_key": os.getenv('DEEPSEEK_API_KEY'),
        "model": os.getenv('DEEPSEEK_VERSION')
        },
    "preferred_model": "openai"
    }

# SMTP configuration for email reports
smtp_config = {
    'server': os.getenv('SMTP_SERVER'),
    'port': int(os.getenv('SMTP_PORT', 587)),
    'username': os.getenv('SMTP_USERNAME'),
    'password': os.getenv('SMTP_PASSWORD')
    }

print("about to hit dummy breakpoint") 
@router.post("/apply", response_model=Response)
async def post_kv(request: Request):
    orchestrator = MCPOrchestrator()
    sequence = ["file_read", "job_search", "resume_tailoring", "job_application"]

    task = {
    "key": "user:123",
    "store_type": "mongo",
    "filepath": request.file_path,
    'search_criteria': request.search_criteria,
    "language_models": language_models,
    'smtp_config': smtp_config,
    "email_recipient": os.getenv('EMAIL_RECIPIENT'),
    }
    
    language_model = language_models["openai"]
    logging.info("API Key: ")
    logging.info(language_model["api_key"])

    logging.info("API Version: ")
    logging.info(language_model["model"])

    res = await orchestrator.run(sequence, task)
    if res.get("status") != "success":
        raise HTTPException(status_code=500, detail=res.get("message"))
    return res
