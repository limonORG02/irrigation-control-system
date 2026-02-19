import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = os.getenv("IRRIGATION_DB_PATH", str(BASE_DIR / "data" / "irrigation.db"))
