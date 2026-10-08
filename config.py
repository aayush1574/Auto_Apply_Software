"""
Configuration Module
Handles user settings and configuration loading.
"""

import json
import os
from pathlib import Path
from typing import Any, Dict

BASE_DIR = Path(__file__).resolve().parent
CONFIG_FILE = Path(os.environ.get("AUTO_APPLY_CONFIG", BASE_DIR / "config.json"))


def _default_config() -> Dict[str, Any]:
    return {
        "user_name": "Your Name",
        "email": "your.email@example.com",
        "phone": "+1234567890",
        "target_roles": ["Software Engineer", "Developer", "Data Scientist"],
        "preferred_locations": ["London", "Remote", "New York"],
        "experience_keywords": ["Python", "JavaScript", "Machine Learning"],
        "salary_range": "Competitive",
        "experience_years": 3,
        "visa_status": "Authorized to work",
        "visa_sponsorship": "No",
        "cv_path": "documents/CV.pdf",
        "cover_letter_path": "documents/Cover_Letter.pdf",
        "cover_letter_template": (
            "Dear Hiring Manager,\n\nI am writing to express my interest in the {role} "
            "position at {company}. With {experience_years} years of experience, "
            "my background in {experience_keywords} aligns with the role.\n\n"
            "Best regards,\n{name}"
        ),
        "application_style": "Quick",
        "tone": "Professional",
        "max_applications_per_day": 20,
        "screening_responses": {},
    }

def load_user_config() -> Dict[str, Any]:
    """Load user configuration from config.json or create default"""
    if CONFIG_FILE.exists():
        try:
            with CONFIG_FILE.open("r", encoding="utf-8") as file:
                loaded = json.load(file)
        except (OSError, json.JSONDecodeError) as exc:
            raise ValueError(f"Unable to read configuration at {CONFIG_FILE}: {exc}") from exc
        if not isinstance(loaded, dict):
            raise ValueError("Configuration must be a JSON object")
        return {**_default_config(), **loaded}

    config = _default_config()
    save_user_config(config)
    return config


def save_user_config(config: Dict[str, Any]) -> None:
    """Atomically save configuration as UTF-8 JSON."""
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    temporary = CONFIG_FILE.with_suffix(CONFIG_FILE.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8") as file:
        json.dump(config, file, indent=2, ensure_ascii=False)
        file.write("\n")
    temporary.replace(CONFIG_FILE)

def update_config(key: str, value: Any) -> None:
    """Update a specific configuration value"""
    config = load_user_config()
    config[key] = value
    
    save_user_config(config)
