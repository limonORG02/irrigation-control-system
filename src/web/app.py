import sys
from pathlib import Path

from flask import Flask, render_template

SRC_DIR = Path(__file__).resolve().parents[1]
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from database.models import init_db
from services.zone_service import get_zone_summaries

app = Flask(__name__)


@app.route("/")
def index():
    init_db()
    zones = get_zone_summaries()
    return render_template("index.html", zones=zones)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
