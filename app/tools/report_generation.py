from datetime import datetime, date
from typing import Dict, Any, List
class DailyReportGeneratorTool:
    def __init__(self):
        self.template = """
        Daily Job Application Report
        Date: {date}
        
        Applications Summary:
        {summary}
        
        Detailed Applications:
        {details}
        """

    def generate_report(self, applications: List[Dict[str, Any]]) -> str:
        """Generate a daily report of applications."""
        summary = self._generate_summary(applications)
        details = self._generate_details(applications)
        
        return self.template.format(
            date=datetime.now().strftime('%Y-%m-%d'),
            summary=summary,
            details=details
        )

    def _generate_summary(self, applications: List[Dict[str, Any]]) -> str:
        """Generate a summary of applications."""
        status_counts = {}
        for app in applications:
            status = app['status']
            status_counts[status] = status_counts.get(status, 0) + 1
        
        summary = "Total Applications: {}\n".format(len(applications))
        for status, count in status_counts.items():
            summary += f"{status}: {count}\n"
        return summary

    def _generate_details(self, applications: List[Dict[str, Any]]) -> str:
        """Generate detailed information about each application."""
        details = ""
        for app in applications:
            details += f"""
            Application ID: {app['application_id']}
            Job Title: {app['job'].get('title', 'N/A')}
            Company: {app['job'].get('company', 'N/A')}
            Status: {app['status']}
            Application Date: {app['application_date']}
            Last Updated: {app.get('last_updated', 'N/A')}
            """
        return details