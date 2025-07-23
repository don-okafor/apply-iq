from pydantic import BaseModel
from dataclasses import dataclass
from typing import Any, List, Dict

@dataclass
class SearchCriteria(BaseModel):
    keywords: List[str]
    location: str
    salary_range: Dict[str, Any]
    experience_range: Dict[str, Any]
    job_type: str
    category: str
    recency: str
