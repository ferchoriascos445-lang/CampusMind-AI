"""
main.py — Project entry point. Launches the Streamlit app.
"""
import os
import subprocess
import sys
from pathlib import Path


def main() -> None:
    """Launch the CampusMind AI Streamlit application."""
    ui_path = Path(__file__).parent / "ui" / "streamlit_ui.py"

    port = int(os.environ.get("PORT", 8080))

    cmd = [
        sys.executable, "-m", "streamlit", "run",
        str(ui_path),
        "--server.port", str(port),
        "--server.address", "0.0.0.0",
        "--server.headless", "true",
        "--browser.gatherUsageStats", "false",
    ]

    print(f"Starting CampusMind AI on port {port}…")
    subprocess.run(cmd, check=True)


if __name__ == "__main__":
    main()
