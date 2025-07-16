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
        
        """self.job_boards = {
            'linkedin': self._search_linkedin,
            'indeed': self._search_indeed,
            # Add more job boards as needed
        }"""
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.language_model = language_models['gemini']
        self.client = genai.Client(api_key = self.language_model['api_key'])
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
        try:
            full_user_prompt = self.get_search_prompt(resume, search_prompt["prompt"])
            print(full_user_prompt)

            response = self.client.models.generate_content(
                model=self.model,
                config=types.GenerateContentConfig(
                    #system_instruction={"parts": [{"text": "You are a highly skilled job search assistant capable of performing real-time web searches."}]},
                    #contents={"parts": [{"text": full_user_prompt}]}
                    #system_instruction="You are a highly skilled job search assistant capable of performing real-time web searches."
                    system_instruction=search_prompt["instruction"]
                    ),
                contents=full_user_prompt
            )
            
            # Assuming the response directly contains the JSON string
            print(response.text)
            return response.text
        except Exception as e:
            print(f"Error during resume parsing: {e}")
            return None
    
    def get_search_prompt(self, resume: str, search_prompt: str):
        #prompt_template = self.read_file(job_search_prompt_path)
        
        """recency = "2025-06-10"
        today = date.today().strftime("%Y-%m-%d")
        location = "EMEA"
        job_type = "Remote"
        category = "Full-time"
        resume_text = resume"""

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