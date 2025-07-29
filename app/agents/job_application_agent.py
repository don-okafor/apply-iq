import json
import logging
from typing import Any, Dict, List
from ..tools.report_generation import DailyReportGeneratorTool
from ..tools.utilities.email_sender import EmailSenderTool


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class JobApplicationAgent:

    def __init__(self, base: Any = None):
        self.base = base
        self.report = DailyReportGeneratorTool()
       



    def apply_to_jobs(self, email_recipient: str, applications: List[Dict[str, Any]], 
                      smtp_config: Dict[str, Any]):
        """Apply to a list of jobs."""
        logging.info("Applying for the jobs:")
        #profile = self.profile_aggregator.get_aggregated_profile()
        #profile = resume
        
        send_email = EmailSenderTool(smtp_config["server"],smtp_config["port"],
                                     smtp_config["username"],smtp_config["password"],)
        
        reports = self.report.generate_report(applications)
        logging.info("Creating reports: ")
        logging.info(json.dumps(reports, indent=2))
        send_email.send_report(email_recipient, reports)
        logging.info("Email Sent.")
        return reports

    

    def run(self, task: Dict[str, Any]) -> Dict[str, Any]:
        pending_applications = task.get("pending_applications")
        email_recipient = task.get("email_recipient")
        smtp_config = task.get("smtp_config")

        if not pending_applications:
            return {"status": "error", "message": "JobSearchAgentError: No pending applications"}
        
        applications = pending_applications["applications"]
        
        try:
            reports = self.apply_to_jobs(email_recipient, applications, smtp_config)
            return {"status": "success", "reports": reports}
        except Exception as e:
            return {"status": "error", "message": "JobSearchAgentError: " + str(e)}