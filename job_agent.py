"""
Core Job Application Agent
Handles job search, filtering, application, and logging.
"""

import csv
import os
from datetime import datetime
from typing import Dict, List
from job_search import LinkedInJobSearch
from application_handler import ApplicationHandler
from logger import ApplicationLogger

class JobApplicationAgent:
    def __init__(self, config: Dict):
        self.config = config
        self.job_search = LinkedInJobSearch(config)
        self.app_handler = ApplicationHandler(config)
        self.logger = ApplicationLogger()
        
    def run_interactive(self):
        """Interactive mode for user commands"""
        print(f"Agent initialized for {self.config['user_name']}")
        print("Commands: 'search [role] in [location]', 'apply [count]', 'status', 'quit'")
        
        while True:
            try:
                command = input("\n> ").strip().lower()
                
                if command == 'quit':
                    break
                elif command.startswith('search'):
                    self._handle_search_command(command)
                elif command.startswith('apply'):
                    self._handle_apply_command(command)
                elif command == 'status':
                    self._show_status()
                else:
                    print("Unknown command. Try 'search [role] in [location]' or 'apply [count]'")
                    
            except KeyboardInterrupt:
                print("\nExiting...")
                break
    
    def _handle_search_command(self, command: str):
        """Parse and execute search command"""
        # Extract role and location from command
        parts = command.replace('search ', '').split(' in ')
        if len(parts) == 2:
            role, location = parts[0].strip(), parts[1].strip()
            jobs = self.job_search.search_jobs(role, location)
            print(f"Found {len(jobs)} Easy Apply jobs for '{role}' in '{location}'")
            self.current_jobs = jobs
        else:
            print("Format: search [role] in [location]")
    
    def _handle_apply_command(self, command: str):
        """Parse and execute apply command"""
        try:
            count = int(command.split()[1]) if len(command.split()) > 1 else 5
            if hasattr(self, 'current_jobs'):
                results = self.apply_to_jobs(self.current_jobs[:count])
                print(f"Applied to {results['successful']} jobs, {results['failed']} failed")
            else:
                print("Search for jobs first")
        except (ValueError, IndexError):
            print("Format: apply [number]")
    
    def apply_to_jobs(self, jobs: List[Dict]) -> Dict:
        """Apply to a list of jobs"""
        successful = 0
        failed = 0
        
        for job in jobs:
            try:
                success = self.app_handler.apply_to_job(job)
                if success:
                    self.logger.log_application(job, "Applied", "Easy Apply")
                    successful += 1
                    print(f"✅ Applied: {job['title']} at {job['company']}")
                else:
                    failed += 1
                    print(f"❌ Failed: {job['title']} at {job['company']}")
            except Exception as e:
                failed += 1
                print(f"❌ Error applying to {job['title']}: {str(e)}")
        
        return {"successful": successful, "failed": failed}
    
    def _show_status(self):
        """Show application statistics"""
        stats = self.logger.get_weekly_summary()
        print(f"📊 Weekly Summary:")
        print(f"   Total Applications: {stats['total']}")
        print(f"   Response Rate: {stats['response_rate']}%")
        print(f"   Follow-ups Needed: {stats['follow_ups']}")