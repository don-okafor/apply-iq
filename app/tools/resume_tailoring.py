from typing import Dict, Any
import google.generativeai as genai
from docx import Document
import json
import time
from pathlib import Path
from ..config import get_settings
from datetime import datetime, date
from .utilities.llm_client import run_completion
from ..tools.utilities.document_parser import parse_document

class ResumeFineTunerTool:
    def __init__(self, language_models: Dict[str, Any] = None):
        self.cfg = get_settings()
        self.preferred_model = language_models["preferred_model"]
        self.language_model = language_models[self.preferred_model]
        self.model = self.language_model["model"]

    def tailor_resume(self, resume: str, job_description: Dict[str, Any]) -> Dict[str, Any]:
        """Tailor resume for a specific job description."""
        # Prepare the prompt for the LLM
       
        prompt = self._create_prompt(resume, job_description)
        # Call the LLM to get tailored content
        tailored_content = run_completion(self.preferred_model, prompt, None, model=self.model)

        # Parse the response and update the resume
        #tailored_content = response.text
        print("Tailored Content: ", tailored_content)

        #return self._update_resume(resume, tailored_content)
        return tailored_content
    
    def _create_prompt(self, resume: str, job_description: Dict[str, Any]) -> str:
        """Create a prompt for the LLM."""

        tailor_prompt_file_path = str((Path(__file__).parent.parent.parent / self.cfg.prompts_root_path / self.cfg.rt_prompt_filename).resolve())
        tailor_prompt = parse_document(tailor_prompt_file_path)

        try:
            prompt = tailor_prompt.format(
                job_description = job_description,
                resume = resume,
            )
            return prompt
        except Exception as e:
            print(f"Error during resume parsing: {e}")
            return None
         
    
    def create_update_prompt(self, tailored_content: str) -> str:
        """create prompt for formatting tailored resume"""
        tailor_prompt_file_path = str((Path(__file__).parent.parent.parent / self.cfg.prompts_root_path / self.cfg.rt_upd_prompt_filename).resolve())
        tailor_prompt = parse_document(tailor_prompt_file_path)

        try:
            prompt = tailor_prompt.format(
                tailored_content = tailored_content,
            )
            return prompt
        except Exception as e:
            print(f"Error during resume parsing: {e}")
            return None

    def _update_resume(self, tailored_content: str) -> str:
        """Update the resume with tailored content."""
        # Parse the LLM response and update the resume structure
        # This is a simplified version - in production, you'd want more robust parsing

         # Prepare the prompt for the LLM
        prompt = self.create_update_prompt(tailored_content)
        
        # Call the LLM to get tailored content
        tailored_resume = run_completion(self.preferred_model, prompt, None, model=self.model)
        
    
        print("Tailored Content: ", tailored_resume)
        #return self._update_resume(resume, tailored_content)
        return tailored_resume
    

class CoverLetterGeneratorTool:
    def __init__(self, language_models: Dict[str, Any] = None):
        self.cfg = get_settings()
        self.preferred_model = language_models["preferred_model"]
        self.language_model = language_models[self.preferred_model]
        self.model = self.language_model["model"]

    def generate_cover_letter(self, resume: Dict[str, Any], job_description: Dict[str, Any]) -> str:
        """Generate a tailored cover letter."""

        prompt = self._create_prompt(resume, job_description)
        
        cover_letter = run_completion(self.preferred_model, prompt, None, model=self.model)
        return cover_letter

    def _create_prompt(self, resume: Dict[str, Any], job_description: Dict[str, Any]) -> str:
        """Create a prompt for the LLM."""

        cover_prompt_file_path = str((Path(__file__).parent.parent.parent / self.cfg.prompts_root_path / self.cfg.cl_prompt_filename).resolve())
        cover_letter_prompt = parse_document(cover_prompt_file_path)

        try:
            prompt = cover_letter_prompt.format(
                job_description = job_description,
                resume = resume,
            )
            return prompt
        except Exception as e:
            print(f"Error during resume parsing: {e}")
            return None