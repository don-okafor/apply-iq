import os
import asyncio
from dotenv import load_dotenv
from app.core.mcp import MCPOrchestrator
from fastapi import FastAPI, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.api.routes import router as api_router

load_dotenv()
app = FastAPI()
app.include_router(api_router, prefix="/api")

"""oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_TOKEN = os.getenv("OAUTH_SECRET_KEY") 

def verify_token(token: str = Depends(oauth2_scheme)):
    if token != SECRET_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing token",
            headers={"WWW-Authenticate": "Bearer"},
        )

@app.get("/protected", dependencies=[Depends(verify_token)])
def protected_route():
    return {"message": "Token is valid, access granted."}

app.include_router(api_router, prefix="/api")"""


""" async def run_workflow():
  orchestrator = MCPOrchestrator()
  sequence = ["file_read", "job_search", "resume_tailoring", "job_application"]
    
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

  task = {
    "key": "user:123",
    "store_type": "mongo",
    "filepath": "C:/Users/Donald/Documents/MyDocs/resume/Resume-DonaldOkafor.pdf",
    'search_criteria': {
            'keywords': ['software', 'engineering manager'],
            'location': 'EMEA',
            'salary_range': {'min': 80000, 'max': 150000},
            'experience_range': {'min': 5, 'max': 25},
            'job_type': 'Remote',
            'category': 'Full-time',
            'recency': '2025-07-01'
        },
    "language_models": language_models,
    'smtp_config': smtp_config,
    "email_recipient": os.getenv('EMAIL_RECIPIENT'),
    # Optional agent chaining
    "next_agent": "logger",
    "next_task": {"message": "Data stored successfully."}
  }

  

  response = await orchestrator.run(sequence, task)
  print("Workflow result:", response)

asyncio.run(run_workflow()) """


