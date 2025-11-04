# LinkedIn Easy Apply Automation Agent

An intelligent job application automation system that searches, prioritizes, and applies to LinkedIn Easy Apply jobs efficiently and professionally.

## Features

- 🔍 **Smart Job Search**: Filter jobs by role, location, and keywords
- 🤖 **Auto-Fill Forms**: Complete Easy Apply forms automatically
- 📝 **STAR Responses**: Answer screening questions professionally
- 📎 **Document Upload**: Attach CV and cover letters automatically
- 📊 **Application Tracking**: Log all applications in CSV format
- 📈 **Weekly Reports**: Track response rates and follow-ups

## Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
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
- `apply [number]` - Apply to found jobs (default: 5)
- `status` - View weekly application summary
- `quit` - Exit the program

## Example Workflow

```
> search sustainability jobs in London
Found 15 Easy Apply jobs for 'sustainability jobs' in 'London'

> apply 10
✅ Applied: Sustainability Analyst at GreenTech Ltd
✅ Applied: Environmental Consultant at EcoSolutions
...
Applied to 8 jobs, 2 failed

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

- No passwords or sensitive data are stored
- All data remains local on your machine
- Applications logged in `Applications.csv`

## Ethics & Compliance

- Maintains accuracy and professionalism
- Does not misrepresent experience
- Respects LinkedIn's terms of service
- Provides human-quality responses