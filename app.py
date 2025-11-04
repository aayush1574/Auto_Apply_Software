"""
Flask Web Frontend for LinkedIn Job Application Agent
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for
import json
import os
from werkzeug.utils import secure_filename
from job_agent import JobApplicationAgent
from multi_site_agent import MultiSiteJobAgent
from config import load_user_config, update_config
from logger import ApplicationLogger

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'documents'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
agent = None
multi_agent = None
current_jobs = {}
selected_sites = ["linkedin", "naukri", "monster"]

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
    
    role = request.form.get('role')
    location = request.form.get('location')
    sites = request.form.getlist('sites') or selected_sites
    
    if not multi_agent:
        config = load_user_config()
        multi_agent = MultiSiteJobAgent(config)
    
    current_jobs = multi_agent.search_all_sites(role, location, sites)
    
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
    
    count_per_site = int(request.form.get('count', 5))
    
    if not current_jobs:
        return jsonify({'success': False, 'message': 'No jobs found. Search first.'})
    
    results = multi_agent.apply_to_jobs_by_site(current_jobs, count_per_site)
    
    return jsonify({
        'success': True,
        'total_applied': results['total_applied'],
        'total_failed': results['total_failed'],
        'by_site': results['by_site']
    })

@app.route('/config', methods=['GET', 'POST'])
def config_page():
    """Configuration page"""
    if request.method == 'POST':
        # Update configuration
        config = load_user_config()
        for key, value in request.form.items():
            if key in config:
                config[key] = value
        
        with open('config.json', 'w') as f:
            json.dump(config, f, indent=2)
        
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
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Update config with new file path
        config = load_user_config()
        if file_type == 'cv':
            config['cv_path'] = filepath
        else:
            config['cover_letter_path'] = filepath
        
        with open('config.json', 'w') as f:
            json.dump(config, f, indent=2)
        
        return jsonify({'success': True, 'filename': filename, 'path': filepath})
    
    return jsonify({'success': False, 'message': 'Invalid file type. Use PDF, DOC, or DOCX'})

@app.route('/applications')
def applications():
    """View applications log"""
    logger = ApplicationLogger()
    apps = []
    
    if os.path.exists('Applications.csv'):
        import csv
        with open('Applications.csv', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            apps = list(reader)
    
    return render_template('applications.html', applications=apps)

if __name__ == '__main__':
    app.run(debug=True, port=5000)