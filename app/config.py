# config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    mongo_uri: str
    mongo_db: str = "apply_ql_db"
    mongo_collection: str = "resume_store"
    file_write_root_path: str = "C:/Users/Donald/Documents/MyDocs/resume/"
    file_write_tailored_resume: str = "tailored_resumes/"
    file_write_cover_letter: str = "tailored_cover_letters/"
    prompts_root_path: str = "prompts_and_instructions/"
    js_instruction_filename: str = prompts_root_path + "job_search_instruction.txt"
    js_prompt_filename: str = prompts_root_path + "job_search_prompt.txt"
    rt_prompt_filename: str = "resume_tailoring_prompt.md"
    rt_upd_prompt_filename: str = "resume_tailoring_update_prompt.txt"
    cl_prompt_filename: str = "cover_letter_prompt.md"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

@lru_cache()
def get_settings():
    return Settings()
