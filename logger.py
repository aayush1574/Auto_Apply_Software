"""
Application Logger Module
Handles CSV logging and reporting of job applications.
"""

import csv
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict

from config import DATA_DIR

APPLICATIONS_FILE = DATA_DIR / "Applications.csv"

class ApplicationLogger:
    def __init__(self, csv_file: str | os.PathLike | None = None):
        self.csv_file = Path(csv_file) if csv_file is not None else APPLICATIONS_FILE
        self._ensure_csv_exists()
    
    def _ensure_csv_exists(self):
        """Create CSV file with headers if it doesn't exist"""
        if not self.csv_file.exists():
            self.csv_file.parent.mkdir(parents=True, exist_ok=True)
            with self.csv_file.open('w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([
                    "Date", "Job Title", "Company", "Location", 
                    "Method", "Status", "Follow-up", "Notes", "URL"
                ])
    
    def log_application(self, job: Dict, status: str = "Applied", method: str = "Easy Apply"):
        """Log a job application to CSV"""
        with self.csv_file.open('a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M"),
                job.get("title", ""),
                job.get("company", ""),
                job.get("location", ""),
                method,
                status,
                "Pending",  # Follow-up status
                "",  # Notes
                job.get("url", "")
            ])
    
    def get_weekly_summary(self) -> Dict:
        """Generate weekly application summary"""
        if not self.csv_file.exists():
            return {"total": 0, "response_rate": 0, "follow_ups": 0}
        
        week_ago = datetime.now() - timedelta(days=7)
        total_apps = 0
        responses = 0
        follow_ups = 0
        
        with self.csv_file.open('r', encoding='utf-8', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    app_date = datetime.strptime(row["Date"], "%Y-%m-%d %H:%M")
                    if app_date >= week_ago:
                        total_apps += 1
                        if row["Status"] in ["Interview", "Response", "Offer"]:
                            responses += 1
                        if row["Follow-up"] == "Pending":
                            follow_ups += 1
                except (KeyError, ValueError):
                    continue
        
        response_rate = (responses / total_apps * 100) if total_apps > 0 else 0
        
        return {
            "total": total_apps,
            "response_rate": round(response_rate, 1),
            "follow_ups": follow_ups
        }
    
    def update_application_status(self, company: str, job_title: str, new_status: str):
        """Update the status of an existing application"""
        # Read all rows
        rows = []
        with self.csv_file.open('r', encoding='utf-8', newline='') as file:
            reader = csv.DictReader(file)
            rows = list(reader)
        
        # Update matching row
        for row in rows:
            if row["Company"] == company and row["Job Title"] == job_title:
                row["Status"] = new_status
                row["Follow-up"] = "Completed" if new_status != "Applied" else "Pending"
                break
        
        # Write back to file
        if not rows:
            return

        with self.csv_file.open('w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)
