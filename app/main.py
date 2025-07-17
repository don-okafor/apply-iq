from .core.mcp import MCPOrchestrator
import asyncio
import os

async def run_workflow():
  orchestrator = MCPOrchestrator()
  sequence = ["file_read", "job_search", "kv_store"]
    
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
        "preferred_model": "deepseek"
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
    # Optional agent chaining
    "next_agent": "logger",
    "next_task": {"message": "Data stored successfully."}
  }

  

  response = await orchestrator.run(sequence, task)
  print("Workflow result:", response)

asyncio.run(run_workflow())
