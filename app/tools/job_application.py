from typing import Dict, Any
from datetime import datetime
class JobApplicationTool:
    def __init__(self):
        self.applications = []

    def apply(self, job: Dict[str, Any], resume: Dict[str, Any], cover_letter: str) -> Dict[str, Any]:
        """Apply to a job with the given resume and cover letter."""
        application = {
            'job': job,
            'resume': resume,
            'cover_letter': cover_letter,
            'status': 'applied',
            'application_date': datetime.now().isoformat(),
            'application_id': self._generate_application_id()
        }
        self.applications.append(application)
        return application