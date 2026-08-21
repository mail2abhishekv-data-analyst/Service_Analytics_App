import os
import subprocess
import time
import webbrowser
from pathlib import Path


def main():

    # ========================================================
    # FIND PROJECT ROOT
    # ========================================================

    current_folder = Path(__file__).resolve().parent

    project_dir = None

    for folder in [current_folder] + list(current_folder.parents):

        if (
            (folder / ".venv" / "Scripts" / "python.exe").exists()
            and (folder / "main.py").exists()
        ):
            project_dir = folder
            break

    if project_dir is None:

        print()
        print("=" * 60)
        print("ERROR: Project folder could not be found.")
        print("Make sure the .venv and main.py are in the project folder.")
        print("=" * 60)
        print()

        input("Press ENTER to close...")
        return

    # ========================================================
    # PYTHON FROM PROJECT VIRTUAL ENVIRONMENT
    # ========================================================

    python_exe = project_dir / ".venv" / "Scripts" / "python.exe"

    main_file = project_dir / "main.py"

    # ========================================================
    # START STREAMLIT
    # ========================================================

    process = subprocess.Popen(
        [
            str(python_exe),
            "-m",
            "streamlit",
            "run",
            str(main_file),
            "--server.headless=true",
            "--browser.gatherUsageStats=false",
        ],
        cwd=str(project_dir)
    )

    # ========================================================
    # OPEN BROWSER
    # ========================================================

    time.sleep(3)

    webbrowser.open(
        "http://localhost:8501"
    )

    # ========================================================
    # KEEP STREAMLIT RUNNING
    # ========================================================

    process.wait()


if __name__ == "__main__":
    main()