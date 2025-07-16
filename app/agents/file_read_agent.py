from pathlib import Path
import PyPDF2
from docx import Document
import os
from typing import Any, Dict
from ..tools.utilities.document_parser import DocumentParserFactory

class FileReadAgent:
    def __init__(self, base: Any = None):
        self.base = base

    def run(self, task: Dict[str, Any]) -> Dict[str, Any]:
        filepath = task.get("filepath")
        
        if not filepath or not os.path.isfile(filepath):
            return {"status": "error", "message": "Invalid or missing filepath"}

        try:
           parser = DocumentParserFactory.get_parser(filepath)
           if not parser:
               raise ValueError(f"No parser available for: {filepath}")
           return parser.parse(filepath)
        except Exception as e:
            return {"status": "error", "message": str(e)}
    