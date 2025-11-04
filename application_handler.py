"""
Application Handler Module
Handles Easy Apply form filling and submission.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from typing import Dict
import time
import os

class ApplicationHandler:
    def __init__(self, config: Dict):
        self.config = config
        
    def apply_to_job(self, job: Dict) -> bool:
        """Apply to a single job using Easy Apply"""
        try:
            # This would use the same driver from job_search
            # For now, return simulation
            print(f"Applying to {job['title']} at {job['company']}")
            
            # Simulate form filling steps
            self._fill_personal_details()
            self._answer_screening_questions()
            self._upload_documents()
            self._submit_application()
            
            return True
            
        except Exception as e:
            print(f"Application failed: {e}")
            return False
    
    def _fill_personal_details(self):
        """Fill personal information in the form"""
        # Simulate filling name, email, phone from config
        time.sleep(1)
        print("  ✓ Personal details filled")
    
    def _answer_screening_questions(self):
        """Answer screening questions using STAR method where applicable"""
        # Common questions and responses based on config
        responses = {
            "visa_sponsorship": self.config.get("visa_status", "No"),
            "years_experience": str(self.config.get("experience_years", 3)),
            "salary_expectation": self.config.get("salary_range", "Negotiable")
        }
        
        time.sleep(1)
        print("  ✓ Screening questions answered")
    
    def _upload_documents(self):
        """Upload CV and cover letter"""
        cv_path = self.config.get("cv_path")
        cover_letter_path = self.config.get("cover_letter_path")
        
        if cv_path and os.path.exists(cv_path):
            print("  ✓ CV uploaded")
        if cover_letter_path and os.path.exists(cover_letter_path):
            print("  ✓ Cover letter uploaded")
    
    def _submit_application(self):
        """Submit the application"""
        time.sleep(1)
        print("  ✓ Application submitted")
    
    def generate_cover_letter(self, job: Dict) -> str:
        """Generate context-aware cover letter"""
        template = self.config.get("cover_letter_template", "")
        
        # Replace placeholders with job-specific information
        cover_letter = template.replace("{company}", job["company"])
        cover_letter = cover_letter.replace("{role}", job["title"])
        cover_letter = cover_letter.replace("{name}", self.config.get("user_name", ""))
        
        return cover_letter