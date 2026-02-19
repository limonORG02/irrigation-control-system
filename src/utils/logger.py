from datetime import datetime
from pathlib import Path

from config import BASE_DIR

LOG_DIR = BASE_DIR / "logs"
LOG_FILE = LOG_DIR / "app.log"


def log(message, level="INFO"):
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    record = f"[{datetime.now()}] [{level}] {message}"
    print(record)
    with LOG_FILE.open("a", encoding="utf-8") as file:
        file.write(record + "\n")
