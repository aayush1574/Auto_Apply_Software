"""
Application Handler Module
Handles Easy Apply form filling and submission.
"""

from typing import Dict

class ApplicationHandler:
    def __init__(self, config: Dict):
        self.config = config
        
    def apply_to_job(self, job: Dict) -> bool:
        """Return False until a real, verifiable submission flow is implemented.

        The previous implementation simulated work and returned True, causing the
        application log to claim applications had been submitted when they had not.
        """
        print(
            f"Not submitted: {job.get('title', 'job')} at "
            f"{job.get('company', 'unknown company')}. Open the job URL to apply manually."
        )
        return False
    
    def generate_cover_letter(self, job: Dict) -> str:
        """Generate context-aware cover letter"""
        template = self.config.get("cover_letter_template", "")
        
        values = {
            "company": job.get("company", "the company"),
            "role": job.get("title", "the role"),
            "name": self.config.get("user_name", ""),
            "experience_years": self.config.get("experience_years", ""),
            "experience_keywords": ", ".join(self.config.get("experience_keywords", [])),
        }
        try:
            return template.format_map(values)
        except (KeyError, ValueError) as exc:
            raise ValueError(f"Invalid cover-letter template: {exc}") from exc
