"""
Multi-Site Job Application Agent
Handles job search and application across LinkedIn, Naukri, and Monster
"""

from typing import Dict, List
from job_search import LinkedInJobSearch
from job_sites.naukri import NaukriJobSearch
from job_sites.monster import MonsterJobSearch
from application_handler import ApplicationHandler
from logger import ApplicationLogger

class MultiSiteJobAgent:
    def __init__(self, config: Dict):
        self.config = config
        self.linkedin = LinkedInJobSearch(config)
        self.naukri = NaukriJobSearch(config)
        self.monster = MonsterJobSearch(config)
        self.app_handler = ApplicationHandler(config)
        self.logger = ApplicationLogger()
        
    def search_all_sites(self, role: str, location: str, sites: List[str] = None) -> Dict:
        """Search jobs across multiple sites"""
        if sites is None:
            sites = ["linkedin", "naukri", "monster"]
        
        all_jobs = {}
        
        if "linkedin" in sites:
            linkedin_jobs = self.linkedin.search_jobs(role, location)
            all_jobs["linkedin"] = linkedin_jobs
            
        if "naukri" in sites:
            naukri_jobs = self.naukri.search_jobs(role, location)
            all_jobs["naukri"] = naukri_jobs
            
        if "monster" in sites:
            monster_jobs = self.monster.search_jobs(role, location)
            all_jobs["monster"] = monster_jobs
        
        return all_jobs
    
    def apply_to_jobs_by_site(self, jobs_by_site: Dict, max_per_site: int = 5) -> Dict:
        """Apply to jobs from multiple sites"""
        results = {"total_applied": 0, "total_failed": 0, "by_site": {}}
        
        for site, jobs in jobs_by_site.items():
            site_applied = 0
            site_failed = 0
            
            for job in jobs[:max_per_site]:
                try:
                    success = False
                    
                    if site == "linkedin":
                        success = self.app_handler.apply_to_job(job)
                    elif site == "naukri":
                        success = self.naukri.apply_to_job(job)
                    elif site == "monster":
                        success = self.monster.apply_to_job(job)
                    
                    if success:
                        self.logger.log_application(job, "Applied", f"{site.title()} Apply")
                        site_applied += 1
                        print(f"✅ {site.title()}: {job['title']} at {job['company']}")
                    else:
                        site_failed += 1
                        print(f"❌ {site.title()}: {job['title']} at {job['company']}")
                        
                except Exception as e:
                    site_failed += 1
                    print(f"❌ {site.title()}: Error applying to {job['title']}: {str(e)}")
            
            results["by_site"][site] = {"applied": site_applied, "failed": site_failed}
            results["total_applied"] += site_applied
            results["total_failed"] += site_failed
        
        return results
    
    def close_all(self):
        """Close all browser instances"""
        self.linkedin.close()
        self.naukri.close()
        self.monster.close()