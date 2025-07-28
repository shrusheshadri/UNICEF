# user_profile.py
# Requirements for user to set up
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import base64

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
