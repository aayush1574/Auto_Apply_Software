#!/usr/bin/env python3
"""
Web Frontend Launcher
Simple script to start the web interface
"""

import webbrowser
import time
from threading import Timer
from app import app

def open_browser():
    """Open browser after a short delay"""
    webbrowser.open('http://localhost:5000')

if __name__ == '__main__':
    print("🚀 Starting LinkedIn Job Agent Web Interface...")
    print("📱 Opening browser at http://localhost:5000")
    
    # Open browser after 1.5 seconds
    Timer(1.5, open_browser).start()
    
    # Start Flask app
    app.run(debug=False, port=5000, host='127.0.0.1')