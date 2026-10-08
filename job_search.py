"""Serverless-compatible LinkedIn public job search."""

from typing import Dict, List
from urllib.parse import urlencode

import requests
from bs4 import BeautifulSoup

PUBLIC_SEARCH_URL = "https://www.linkedin.com/jobs/search/"
GUEST_SEARCH_URL = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"
DEFAULT_HEADERS = {
    "Accept": "text/html,application/xhtml+xml",
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0 Safari/537.36"
    ),
}


def build_linkedin_search_url(role: str, location: str) -> str:
    """Build a user-facing LinkedIn Easy Apply search URL."""
    params = urlencode({"keywords": role, "location": location, "f_AL": "true"})
    return f"{PUBLIC_SEARCH_URL}?{params}"

class LinkedInJobSearch:
    def __init__(self, config: Dict, session=None):
        self.config = config
        self.session = session or requests.Session()
        self.last_error = None
    
    def search_jobs(self, role: str, location: str) -> List[Dict]:
        """Return up to 20 public Easy Apply listings without a browser driver."""
        self.last_error = None
        try:
            response = self.session.get(
                GUEST_SEARCH_URL,
                params={
                    "keywords": role,
                    "location": location,
                    "f_AL": "true",
                    "start": 0,
                },
                headers=DEFAULT_HEADERS,
                timeout=12,
            )
            response.raise_for_status()
            response.encoding = "utf-8"
        except requests.RequestException as exc:
            self.last_error = f"LinkedIn did not return public results: {exc}"
            return []

        soup = BeautifulSoup(response.text, "html.parser")
        jobs = []
        seen_ids = set()
        for card in soup.select("div.base-search-card"):
            entity_urn = card.get("data-entity-urn", "")
            job_id = entity_urn.rsplit(":", 1)[-1]
            title = card.select_one(".base-search-card__title")
            company = card.select_one(".base-search-card__subtitle")
            job_location = card.select_one(".job-search-card__location")
            link = card.select_one("a.base-card__full-link")
            if not job_id.isdigit() or job_id in seen_ids or not all((title, company, link)):
                continue

            seen_ids.add(job_id)
            jobs.append({
                "id": job_id,
                "title": title.get_text(" ", strip=True),
                "company": company.get_text(" ", strip=True),
                "location": (
                    job_location.get_text(" ", strip=True) if job_location else location
                ),
                "url": f"https://www.linkedin.com/jobs/view/{job_id}",
                "easy_apply": True,
            })
            if len(jobs) == 20:
                break

        return jobs
    
    def close(self):
        """Close the reusable HTTP session."""
        self.session.close()
