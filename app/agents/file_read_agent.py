from pathlib import Path
import PyPDF2
from docx import Document
import os
from typing import Any, Dict
from ..tools.utilities.document_parser import parse_document

class FileReadAgent:
    def __init__(self, base: Any = None):
        self.base = base

    def run(self, task: Dict[str, Any]) -> Dict[str, Any]:
        filepath = task.get("filepath")
        
        if not filepath or not os.path.isfile(filepath):
            return {"FileReadAgentError": {"status": "error", "message": "Invalid or missing filepath"}}

        try:
           return {"resume": parse_document(filepath)}
        except Exception as e:
            return {"FileReadAgentError":{"status": "error", "message": str(e)}}
    