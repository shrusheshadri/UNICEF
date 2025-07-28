# user_profile.py
# Requirements for user to set up
pandas>=1.3.0
matplotlib>=3.4.0
seaborn>=0.11.0
numpy>=1.21.0
openpyxl>=3.0.0
jupyterlab>=3.0.0  # Optional, for notebooks if used

import os
import platform
import sys

def setup_environment():
    print("🔧 Setting up user environment...")
    print(f"Operating System: {platform.system()}")
    print(f"Python Version: {platform.python_version()}")
    project_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_dir)
    print(f"Working Directory Set To: {project_dir}")

if __name__ == "__main__":
    setup_environment()
