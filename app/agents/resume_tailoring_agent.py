import os
import json
import logging
import time
from pathlib import Path
from unidecode import unidecode
from datetime import datetime, date
from typing import Any, Dict, List
from ..models.key_value import KeyValue
from ..tools.job_search import JobBoardSearchTool
from ..tools.stores.mongo_store import MongoStore
from ..tools.utilities.type_converter import TypeConverter
from ..tools.utilities.document_parser import parse_document
from ..tools.resume_tailoring import ResumeFineTunerTool, CoverLetterGeneratorTool
from ..config import get_settings

class ResumeTailoringAgent:

    def __init__(self, base: Any = None):
        self.base = base
        self.cfg = get_settings()
        self.type_converter = TypeConverter()


    def tailor_resume_to_jobs(self, resume: str, jobs: List[Dict[str, Any]], 
                              language_models: Dict[str, Any]):
        """Tailor Resume to a list of jobs."""
        #profile = self.profile_aggregator.get_aggregated_profile()
        #profile = resume
        self.resume_tailor = ResumeFineTunerTool(language_models)
        self.cover_letter = CoverLetterGeneratorTool(language_models)
        applications = []
        pending_applications = {"batch_id": datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]}

        for job in jobs:
            logging.info(f"\nProcessing job: {job['title']} at {job['company']}")
            
            # Tailor resume for the job
            logging.info("Tailoring resume...")
            tailored_resume = self.resume_tailor.tailor_resume(resume, job)

            #application_id = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
            application_id = datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]
            #data = self.utility.get_dict_from_json(tailored_resume)
            resume_data = self.resume_tailor.create_update_prompt(tailored_resume)
           


            #Change this to write the tailored resume to mongo. 
            # Then create an agent to read tailored resume and write to file location
            max_len = 20
            long_file_name = self.type_converter.remove_spaces_and_special_characters(job['company'] + "-" + job['title'])
            file_name = long_file_name[:max_len] if len(long_file_name) > max_len else long_file_name
            file_path = self.cfg.file_write_root_path + self.cfg.file_write_tailored_resume + file_name + ".pdf"
            #self.utility.write_dict_to_pdf(data, file_path)
            self.type_converter.write_string_to_pdf_file(resume_data, file_path)
            logging.info("Tailored Resume:")
            logging.info(json.dumps(tailored_resume, indent=2))
            time.sleep(10)

            # Generate cover letter
            logging.info("Generating cover letter...")
            cover_letter = self.cover_letter.generate_cover_letter(resume, job)
            file_path =  self.cfg.file_write_root_path + self.cfg.file_write_cover_letter  + file_name + ".pdf"
            cover_letter_data = unidecode(cover_letter)
            self.type_converter.write_string_to_pdf_file(cover_letter_data, file_path)
            logging.info("Cover Letter:")
            logging.info(cover_letter)

            applications.append({"id": application_id, 
                                     "job": job, 
                                     "resume": tailored_resume, 
                                     "cover_letter": cover_letter_data,
                                     "status": "pending"})
            time.sleep(10)

        pending_applications["applications"] = applications
        return pending_applications

        
    def run(self, task: Dict[str, Any]) -> Dict[str, Any]:
        resume = task.get("resume")
        jobs = task.get("jobs")
        language_models = task.get("language_models")

        if not resume:
           return {"ResumeTailoringAgentError": {"status": "error", "message": "No resume found: Upload your most recent resume"}}

        try:
           pending_applications = self.tailor_resume_to_jobs(resume, jobs, language_models)
           return {"pending_applications": pending_applications}
        except Exception as e:
            return {"ResumeTailoringAgentError": {"status": "error", "message": str(e)}}