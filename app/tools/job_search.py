from typing import Dict, List, Any
import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime, date
import time
from urllib.parse import quote_plus
from google import genai
from google.genai import types
from pathlib import Path


class JobBoardSearchTool:
    def __init__(self, search_criteria: Dict[str, Any] = None,
                 language_models: Dict[str, Any] = None):
        
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.preferred_model = language_models["preferred_model"]
        self.language_model = language_models[self.preferred_model]
        self.api_key = self.language_model['api_key']
        self.model = self.language_model['model']
        self.search_criteria = search_criteria

    def search(self, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Search for jobs across multiple job boards."""
        results = []
        for board, search_func in self.job_boards.items():
            try:
                board_results = search_func(query)
                results.extend(board_results)
                time.sleep(1)  # Be nice to the servers
            except Exception as e:
                print(f"Error searching {board}: {str(e)}")
        return results
    

    def llm_job_search(self, resume: str, search_prompt: str) -> str:
        from .utilities.llm_client import run_completion
        try:
            full_user_prompt = self.get_search_prompt(resume, search_prompt["prompt"])
            print(full_user_prompt)
            system_instruction=search_prompt["instruction"]
            openai_response_format = {"type": "json_object"}
            response = run_completion(self.preferred_model, full_user_prompt, system_instruction, model=self.model)
          
            # Assuming the response directly contains the JSON string
            print(response)
            return response
        except Exception as e:
            print(f"Error during resume parsing: {e}")
            return None
    
    def get_search_prompt(self, resume: str, search_prompt: str):
        #prompt_template = self.read_file(job_search_prompt_path)
        
        search_criteria = self.search_criteria

        recency = search_criteria["recency"]
        today = date.today().strftime("%Y-%m-%d")
        location = search_criteria["location"]
        job_type = search_criteria["job_type"]
        category = search_criteria["category"]
        resume_text = resume

        try:
            prompt = search_prompt.format(
                recency = recency,
                today = today,
                location = location,
                job_type = job_type,
                category = category,
                resume_text = resume_text
            )
            return prompt
        except Exception as e:
            print(f"Error during resume parsing: {e}")
            return None