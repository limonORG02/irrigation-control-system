from datetime import datetime

def log(message, level="INFO"):
    print(f"[{datetime.now()}] [{level}] {message}")
