from typing import Any, Dict, List
from ..tools.report_generation import DailyReportGeneratorTool
from ..tools.utilities.email_sender import EmailSenderTool
class JobApplicationAgent:

    def __init__(self, base: Any = None):
        self.base = base
        self.report = DailyReportGeneratorTool()
       



    def apply_to_jobs(self, email_recipient: str, applications: List[Dict[str, Any]], 
                      smtp_config: Dict[str, Any]):
        """Apply to a list of jobs."""
        #profile = self.profile_aggregator.get_aggregated_profile()
        #profile = resume
        
        send_email = EmailSenderTool(smtp_config["server"],smtp_config["port"],
                                     smtp_config["username"],smtp_config["password"],)
        reports = self.report.generate_report(applications)
        send_email.send_report(email_recipient, reports)

    

    def run(self, task: Dict[str, Any]) -> Dict[str, Any]:
        pending_applications = task.get("pending_applications")
        applications = pending_applications["applications"]
        email_recipient = task.get("email_recipient")
        smtp_config = task.get("smtp_config")

        if not pending_applications:
            return {"JobSearchAgentError": {"status": "error", "message": "No pending applications"}} 

        try:
            apply = self.apply_to_jobs(email_recipient, applications, smtp_config)
            return {"applications": apply}
        except Exception as e:
            return {"JobSearchAgentError": {"status": "error", "message": str(e)}}