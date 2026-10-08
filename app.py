"""
Flask Web Frontend for LinkedIn Job Application Agent
"""

import atexit

from flask import Flask, render_template, request, jsonify, redirect, url_for
from pathlib import Path
from werkzeug.utils import secure_filename
from multi_site_agent import MultiSiteJobAgent
from config import BASE_DIR, load_user_config, save_user_config
from logger import ApplicationLogger, BASE_DIR as LOGGER_BASE_DIR

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = str(BASE_DIR / 'documents')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}
Path(app.config['UPLOAD_FOLDER']).mkdir(parents=True, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
multi_agent = None
current_jobs = {}
selected_sites = ["linkedin"]


def close_browser() -> None:
    """Release Selenium processes when the local server exits."""
    if multi_agent is not None:
        multi_agent.close_all()


atexit.register(close_browser)

@app.route('/')
def index():
    """Main dashboard"""
    config = load_user_config()
    logger = ApplicationLogger()
    stats = logger.get_weekly_summary()
    return render_template('index.html', config=config, stats=stats)

@app.route('/search', methods=['POST'])
def search_jobs():
    """Search for jobs across multiple sites"""
    global multi_agent, current_jobs, selected_sites
    
    role = request.form.get('role', '').strip()
    location = request.form.get('location', '').strip()
    sites = request.form.getlist('sites') or selected_sites

    if not role or not location:
        return jsonify({'success': False, 'message': 'Role and location are required.'}), 400
    
    if not multi_agent:
        config = load_user_config()
        multi_agent = MultiSiteJobAgent(config)
    
    try:
        current_jobs = multi_agent.search_all_sites(role, location, sites)
    except ValueError as exc:
        return jsonify({'success': False, 'message': str(exc)}), 400
    except Exception as exc:
        app.logger.exception("Job search failed")
        return jsonify({'success': False, 'message': f'Job search failed: {exc}'}), 502
    
    total_jobs = sum(len(jobs) for jobs in current_jobs.values())
    
    return jsonify({
        'success': True,
        'total_count': total_jobs,
        'by_site': {site: len(jobs) for site, jobs in current_jobs.items()},
        'jobs': current_jobs
    })

@app.route('/apply', methods=['POST'])
def apply_jobs():
    """Apply to jobs across multiple sites"""
    global multi_agent, current_jobs
    
    try:
        count_per_site = int(request.form.get('count', 5))
    except (TypeError, ValueError):
        return jsonify({'success': False, 'message': 'Count must be a number.'}), 400

    if not 1 <= count_per_site <= 20:
        return jsonify({'success': False, 'message': 'Count must be between 1 and 20.'}), 400
    
    if not current_jobs:
        return jsonify({'success': False, 'message': 'No jobs found. Search first.'})
    
    return jsonify({
        'success': False,
        'message': (
            'Automatic submission is disabled because the repository does not yet '
            'contain a verifiable form-submission implementation. Open a job link and '
            'apply manually; only confirmed applications should be logged.'
        )
    }), 501


@app.route('/applications/record', methods=['POST'])
def record_application():
    """Record an application only after the user confirms manual submission."""
    job_url = request.form.get('url', '').strip()
    job = next(
        (job for jobs in current_jobs.values() for job in jobs if job.get('url') == job_url),
        None,
    )
    if not job:
        return jsonify({'success': False, 'message': 'Choose a job from the current search.'}), 400
    ApplicationLogger().log_application(job, 'Applied', 'Manual confirmation')
    return jsonify({'success': True, 'message': 'Application recorded.'})

@app.route('/config', methods=['GET', 'POST'])
def config_page():
    """Configuration page"""
    if request.method == 'POST':
        # Update configuration
        config = load_user_config()
        for key, value in request.form.items():
            if key in config:
                if key in {'experience_years', 'max_applications_per_day'}:
                    try:
                        config[key] = max(0, int(value))
                    except ValueError:
                        continue
                else:
                    config[key] = value.strip()

        save_user_config(config)
        
        return redirect(url_for('index'))
    
    config = load_user_config()
    return render_template('config.html', config=config)

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file uploads"""
    if 'file' not in request.files:
        return jsonify({'success': False, 'message': 'No file selected'})
    
    file = request.files['file']
    file_type = request.form.get('type', 'cv')
    
    if file.filename == '':
        return jsonify({'success': False, 'message': 'No file selected'})
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = Path(app.config['UPLOAD_FOLDER']) / filename
        file.save(filepath)
        
        # Update config with new file path
        config = load_user_config()
        if file_type == 'cv':
            config['cv_path'] = str(filepath.relative_to(BASE_DIR))
        else:
            config['cover_letter_path'] = str(filepath.relative_to(BASE_DIR))

        save_user_config(config)
        
        return jsonify({'success': True, 'filename': filename})
    
    return jsonify({'success': False, 'message': 'Invalid file type. Use PDF, DOC, or DOCX'})

@app.route('/applications')
def applications():
    """View applications log"""
    logger = ApplicationLogger()
    apps = []
    
    csv_path = LOGGER_BASE_DIR / 'Applications.csv'
    if csv_path.exists():
        import csv
        with csv_path.open('r', encoding='utf-8', newline='') as f:
            reader = csv.DictReader(f)
            apps = list(reader)
    
    return render_template('applications.html', applications=apps)

if __name__ == '__main__':
    app.run(debug=False, port=5000)
