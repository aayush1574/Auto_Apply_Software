"""
LinkedIn Job Search Module
Handles job searching and filtering on LinkedIn.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import Dict, List
import time

class LinkedInJobSearch:
    def __init__(self, config: Dict):
        self.config = config
        self.driver = None
        
    def _init_driver(self):
        """Initialize Chrome driver with options"""
        if not self.driver:
            options = webdriver.ChromeOptions()
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            self.driver = webdriver.Chrome(options=options)
    
    def search_jobs(self, role: str, location: str) -> List[Dict]:
        """Search for Easy Apply jobs"""
        self._init_driver()
        
        # Build LinkedIn job search URL
        base_url = "https://www.linkedin.com/jobs/search/"
        params = f"?keywords={role}&location={location}&f_AL=true"  # f_AL=true for Easy Apply
        
        self.driver.get(base_url + params)
        time.sleep(3)
        
        jobs = []
        try:
            # Find job cards
            job_cards = self.driver.find_elements(By.CSS_SELECTOR, "[data-job-id]")
            
            for card in job_cards[:20]:  # Limit to first 20 results
                try:
                    job_id = card.get_attribute("data-job-id")
                    title = card.find_element(By.CSS_SELECTOR, "h3 a").text
                    company = card.find_element(By.CSS_SELECTOR, "h4 a").text
                    location_elem = card.find_element(By.CSS_SELECTOR, "[data-test-job-location]")
                    job_location = location_elem.text if location_elem else location
                    
                    # Check if Easy Apply is available
                    easy_apply = len(card.find_elements(By.XPATH, ".//span[contains(text(), 'Easy Apply')]")) > 0
                    
                    if easy_apply:
                        jobs.append({
                            "id": job_id,
                            "title": title,
                            "company": company,
                            "location": job_location,
                            "url": f"https://www.linkedin.com/jobs/view/{job_id}",
                            "easy_apply": True
                        })
                except Exception as e:
                    continue
                    
        except Exception as e:
            print(f"Error searching jobs: {e}")
        
        return jobs
    
    def close(self):
        """Close the browser driver"""
        if self.driver:
            self.driver.quit()
            self.driver = None