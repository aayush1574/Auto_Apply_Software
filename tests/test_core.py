import csv
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock

import app as web_app
from application_handler import ApplicationHandler
from job_search import LinkedInJobSearch, build_linkedin_search_url
from logger import ApplicationLogger


class ApplicationHandlerTests(unittest.TestCase):
    def test_placeholder_never_claims_submission(self):
        handler = ApplicationHandler({})
        self.assertFalse(handler.apply_to_job({"title": "Engineer", "company": "Example"}))

    def test_cover_letter_formats_all_supported_fields(self):
        handler = ApplicationHandler({
            "user_name": "A. User",
            "experience_years": 4,
            "experience_keywords": ["Python", "APIs"],
            "cover_letter_template": "{name}: {role} at {company}; {experience_years}; {experience_keywords}",
        })
        result = handler.generate_cover_letter({"title": "Engineer", "company": "Example"})
        self.assertEqual(result, "A. User: Engineer at Example; 4; Python, APIs")


class JobSearchTests(unittest.TestCase):
    def test_search_url_encodes_user_input(self):
        url = build_linkedin_search_url("C++ engineer", "New York")
        self.assertIn("keywords=C%2B%2B+engineer", url)
        self.assertIn("location=New+York", url)

    def test_parses_public_job_cards(self):
        response = Mock()
        response.text = """
        <div class="base-search-card" data-entity-urn="urn:li:jobPosting:12345">
          <a class="base-card__full-link" href="https://example.test/job"></a>
          <h3 class="base-search-card__title"> AI Engineer </h3>
          <h4 class="base-search-card__subtitle"> Example Inc </h4>
          <span class="job-search-card__location"> Remote </span>
        </div>
        """
        response.raise_for_status.return_value = None
        session = Mock()
        session.get.return_value = response
        search = LinkedInJobSearch({}, session=session)

        jobs = search.search_jobs("AI Engineer", "Remote")

        self.assertEqual(jobs[0]["id"], "12345")
        self.assertEqual(jobs[0]["title"], "AI Engineer")
        self.assertEqual(jobs[0]["company"], "Example Inc")
        session.get.assert_called_once()


class LoggerTests(unittest.TestCase):
    def test_log_and_weekly_summary(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "applications.csv"
            logger = ApplicationLogger(path)
            logger.log_application({"title": "Engineer", "company": "Example"})
            self.assertEqual(logger.get_weekly_summary()["total"], 1)
            with path.open(encoding="utf-8") as file:
                self.assertEqual(len(list(csv.DictReader(file))), 1)


class WebTests(unittest.TestCase):
    def setUp(self):
        web_app.app.config.update(TESTING=True)
        self.client = web_app.app.test_client()

    def test_dashboard_renders(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Job Search Assistant", response.data)

    def test_applications_page_renders(self):
        response = self.client.get("/applications")
        self.assertEqual(response.status_code, 200)

    def test_search_validates_required_fields(self):
        response = self.client.post("/search", data={})
        self.assertEqual(response.status_code, 400)

    def test_automatic_apply_is_explicitly_disabled(self):
        web_app.current_jobs = {"linkedin": [{"url": "https://example.test/job"}]}
        response = self.client.post("/apply", data={"count": "1"})
        self.assertEqual(response.status_code, 501)
        self.assertFalse(response.get_json()["success"])

    def test_record_rejects_non_linkedin_urls(self):
        response = self.client.post("/applications/record", data={
            "url": "https://example.test/jobs/view/123",
            "title": "Engineer",
            "company": "Example",
        })
        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()
