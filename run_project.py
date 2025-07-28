# Run_project
import subprocess
import user_profile

def run_all():
    user_profile.setup_environment()
 

# Replace the filenames below with your actual script filenames in execution order
    scripts = [
        "scripts/load_data.py",
        "scripts/analyze_health_coverage.py",
        "scripts/visualize_results.py"
    ]

    for script in scripts:
        print(f"▶️ Running: {script}")
        subprocess.run(["python", script], check=True)

if __name__ == "__main__":
    run_all()
