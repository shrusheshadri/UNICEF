# user_profile.py
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
