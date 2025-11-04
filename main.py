#!/usr/bin/env python3
"""
LinkedIn Easy Apply Job Application Automation Agent
Main entry point for the intelligent job application system.
"""

from job_agent import JobApplicationAgent
from config import load_user_config

def main():
    """Main execution function"""
    print("🚀 LinkedIn Easy Apply Automation Agent")
    print("=" * 50)
    
    # Load user configuration
    config = load_user_config()
    
    # Initialize the agent
    agent = JobApplicationAgent(config)
    
    # Start interactive mode
    agent.run_interactive()

if __name__ == "__main__":
    main()