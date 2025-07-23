import os
import json
import logging
from pathlib import Path
from datetime import datetime, date
from typing import Any, Dict, List
from ..config import get_settings
from ..models.key_value import KeyValue
from ..tools.job_search import JobBoardSearchTool
from ..tools.stores.mongo_store import MongoStore
from ..tools.utilities.type_converter import TypeConverter
from ..tools.utilities.document_parser import parse_document

class JobSearchAgent:

    def __init__(self, base: Any = None):
        self.base = base
        self.cfg = get_settings()
        self.type_convereter = TypeConverter()
       
    
    
    def search_jobs(self, search_criteria: Dict[str, Any], 
                    resume_text: str, language_models: Dict[str, Any]) -> str: #List[Dict[str, Any]]:
        """Search for jobs based on criteria."""
        logging.info("Searching for jobs with criteria:")
        logging.info(json.dumps(search_criteria, indent=2))
        
        #Instantiate JobBoardSearchClass
        job_search = JobBoardSearchTool(search_criteria, language_models)

        # Get aggregated profile
        # Elicit the job search based off of the resume and provided criteria. 
        # Leverage models that can take a resume and get jobs that match to a certain degree. 
        # Then fine tune the resume to match the jobs
       
        #temporary implementation so as not to access llm
        #jobs_text = self.utility.read_file("sample_job_response1.txt")

        # Initial Mongo Store for job save
        mongo_db = "apply_ql_db"
        job_list = MongoStore(mongo_db , "job_board")
        #job_search_prompts = MongoStore(mongo_db, "job_search_prompts")

        #Get file path
        instruction_file_path = str((Path(__file__).parent.parent.parent / self.cfg.prompts_root_path / self.cfg.js_instruction_filename).resolve()) 
        prompt_file_path = str((Path(__file__).parent.parent.parent / self.cfg.prompts_root_path / self.cfg.js_prompt_filename).resolve()) 

        
        instruction = parse_document(instruction_file_path)
        prompt = parse_document(prompt_file_path)
        
    
        prompts = {
            "instruction": instruction,
            "prompt": prompt
        }

        # Search for jobs
        jobs_text = job_search.llm_job_search(resume_text, prompts)
        #jobs_text = parse_document(root_path + "\sample_job_response1.txt")
        
        key = datetime.now().strftime("%Y%m%d %H%M%S.%f")[:-3]
        kv = KeyValue(key=key, value=jobs_text)
        #job_list.save(kv)

        jobs = self.type_convereter.get_dict_from_json(jobs_text)
        
        logging.info(f"Found {len(jobs)} jobs")
        for job in jobs:
            logging.info(f"Job: {job['title']} at {job['company']}")
            logging.info(f"Location: {job['location']}")
            logging.info(f"Description: {job['description']}")
            logging.info(f"URL: {job['url']}")
            logging.info("---")

        
        return jobs
    
    def run(self, task: Dict[str, Any]) -> Dict[str, Any]:
        resume = task.get("resume")
        search_criteria = task.get("search_criteria")
        language_models = task.get("language_models")

        if not resume:
            return {"JobSearchAgentError": {"status": "error", "message": "Upload your most recent resume"}} 

        try:
            jobs = self.search_jobs(search_criteria, resume, language_models)
            return {"jobs": jobs}
        except Exception as e:
            return {"JobSearchAgentError": {"status": "error", "message": str(e)}}