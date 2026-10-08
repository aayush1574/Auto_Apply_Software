import csv
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

import app as web_app
from application_handler import ApplicationHandler
from job_search import LinkedInJobSearch
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
        search = LinkedInJobSearch({})
        search.driver = Mock()
        search.driver.find_elements.return_value = []
        with patch("job_search.time.sleep"):
            self.assertEqual(search.search_jobs("C++ engineer", "New York"), [])
        url = search.driver.get.call_args.args[0]
        self.assertIn("keywords=C%2B%2B+engineer", url)
        self.assertIn("location=New+York", url)


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


if __name__ == "__main__":
    unittest.main()
