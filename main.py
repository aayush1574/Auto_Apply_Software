#!/usr/bin/env python3
"""
LinkedIn Easy Apply Job Search Assistant
Command-line entry point for search and confirmed-application tracking.
"""

from job_agent import JobApplicationAgent
from config import load_user_config

def main():
    """Main execution function"""
    print("🚀 LinkedIn Job Search Assistant")
    print("=" * 50)
    
    # Load user configuration
    config = load_user_config()
    
    # Initialize the agent
    agent = JobApplicationAgent(config)
    
    # Start interactive mode
    agent.run_interactive()

if __name__ == "__main__":
    main()
