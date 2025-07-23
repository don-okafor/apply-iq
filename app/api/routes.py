from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.core.mcp import MCPOrchestrator
from typing import Any
import os
from ..models.search_criteria import SearchCriteria

router = APIRouter()
#search_criteria = SearchCriteria()

"""class KVIn(BaseModel):
    key: str
    value: Any"""

class Request(BaseModel):
    file_path: str
    search_criteria: SearchCriteria

class KVOut(BaseModel):
    status: str
    key: str
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
    "preferred_model": "gemini"
    }

# SMTP configuration for email reports
smtp_config = {
    'server': os.getenv('SMTP_SERVER'),
    'port': int(os.getenv('SMTP_PORT', 587)),
    'username': os.getenv('SMTP_USERNAME'),
    'password': os.getenv('SMTP_PASSWORD')
    }


@router.post("/apply", response_model=KVOut)
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

    res = await orchestrator.run(sequence, task)
    if res.get("status") != "success":
        raise HTTPException(status_code=500, detail=res.get("message"))
    return res
