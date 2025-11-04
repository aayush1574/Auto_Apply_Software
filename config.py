"""
Configuration Module
Handles user settings and configuration loading.
"""

import json
import os
from typing import Dict

def load_user_config() -> Dict:
    """Load user configuration from config.json or create default"""
    config_file = "config.json"
    
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            return json.load(f)
    else:
        # Create default configuration
        default_config = {
            "user_name": "Your Name",
            "email": "your.email@example.com",
            "phone": "+1234567890",
            "linkedin_username": "",
            "linkedin_password": "",
            
            # Job preferences
            "target_roles": ["Software Engineer", "Developer", "Data Scientist"],
            "preferred_locations": ["London", "Remote", "New York"],
            "experience_keywords": ["Python", "JavaScript", "Machine Learning"],
            "salary_range": "Competitive",
            "experience_years": 3,
            
            # Work authorization
            "visa_status": "Authorized to work",
            "visa_sponsorship": "No",
            
            # Documents
            "cv_path": "documents/CV.pdf",
            "cover_letter_path": "documents/Cover_Letter.pdf",
            "cover_letter_template": """Dear Hiring Manager,

I am writing to express my interest in the {role} position at {company}. With {experience_years} years of experience in software development, I am excited about the opportunity to contribute to your team.

My background in {experience_keywords} aligns well with your requirements, and I am particularly drawn to {company}'s innovative approach to technology.

I look forward to discussing how my skills can benefit your organization.

Best regards,
{name}""",
            
            # Application settings
            "application_style": "Quick",  # Quick or Detailed
            "tone": "Professional",  # Professional/Warm/Technical/Creative
            "max_applications_per_day": 20,
            
            # Screening question responses
            "screening_responses": {
                "years_experience": "3+ years",
                "willing_to_relocate": "Yes",
                "salary_expectation": "Market rate",
                "notice_period": "2 weeks",
                "remote_work": "Yes"
            }
        }
        
        # Save default config
        with open(config_file, 'w') as f:
            json.dump(default_config, f, indent=2)
        
        print(f"Created default config.json - please update with your details")
        return default_config

def update_config(key: str, value: str):
    """Update a specific configuration value"""
    config = load_user_config()
    config[key] = value
    
    with open("config.json", 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"Updated {key} to {value}")