# LinkedIn Job Search Assistant

A local assistant that finds LinkedIn Easy Apply listings and tracks applications that you confirm submitting. It deliberately keeps a human in the loop: the current code does **not** fill or submit LinkedIn forms.

## Features

- 🔍 **Smart Job Search**: Filter jobs by role, location, and keywords
- 🔗 **Review Links**: Open each result on LinkedIn to review and apply
- 📝 **Cover Letter Templates**: Prepare job-specific drafts
- 📎 **Local Documents**: Store a résumé for your own workflow
- 📊 **Application Tracking**: Log all applications in CSV format
- 📈 **Weekly Reports**: Track response rates and follow-ups

## Quick Start

1. **Install Dependencies**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   python -m pip install -r requirements.txt
   ```

2. **Run Web Interface**
   ```bash
   python run_web.py
   ```
   Opens automatically at http://localhost:5000

3. **Or Run Command Line**
   ```bash
   python main.py
   ```

4. **Configure Settings**
   - Use web interface or edit `config.json`
   - Add documents to `documents/` folder

## Usage Commands

- `search [role] in [location]` - Find Easy Apply jobs
- `apply [number]` - Reports that manual review is required; it never claims a submission
- `status` - View weekly application summary
- `quit` - Exit the program

## Example Workflow

```
> search sustainability jobs in London
Found 15 Easy Apply jobs for 'sustainability jobs' in 'London'

Open a result on LinkedIn, submit it there, then use the web interface's
"I applied — record it" button.

> status
📊 Weekly Summary:
   Total Applications: 25
   Response Rate: 12.0%
   Follow-ups Needed: 3
```

## Configuration

Edit `config.json` to customize:
- Personal information
- Job preferences and keywords
- Salary expectations
- Work authorization status
- Application style and tone
- Screening question responses

## Data Privacy

- LinkedIn passwords are neither requested nor stored
- All data remains local on your machine
- Applications logged in `Applications.csv`

## Ethics & Compliance

- Maintains accuracy and professionalism
- Does not misrepresent experience
- Requires the user to review and submit every application
- Provides human-quality responses

## Current limitations

- LinkedIn can change its page markup or require sign-in, which may prevent results from loading.
- Naukri and Monster were previously shown in the UI but had no implementation; they are disabled until real provider modules exist.
- Automatic form submission is intentionally disabled. The old placeholder returned success without submitting anything, so it was unsafe to use for application tracking.

## Tests

```bash
python -m unittest discover -s tests -v
```
