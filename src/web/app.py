import os
import sys
from pathlib import Path

from flask import Flask, render_template

SRC_DIR = Path(__file__).resolve().parents[1]
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from database.models import init_db
from services.zone_service import get_gas_history, get_zone_summaries

app = Flask(__name__)


@app.context_processor
def inject_global_gas_alert():
    """Provide gas alert flag for rendering the warning panel on every page."""
    zones = get_zone_summaries()
    gas_alert = any(
        zone["gas_status"]
        in {"Есть вероятность запаха газа", "Высокая вероятность запаха газа"}
        for zone in zones
    )
    return {"global_gas_alert": gas_alert}


@app.route("/")
def index():
    """Render the zones summary table."""
    init_db()
    zones = get_zone_summaries()
    return render_template("index.html", zones=zones)


@app.route("/gas/<int:zone_id>")
def gas_history(zone_id):
    """Render historical gas measurements chart for the selected zone."""
    init_db()
    history = get_gas_history(zone_id)
    return render_template("gas_history.html", history=history)


if __name__ == "__main__":
    debug_mode = os.getenv("IRRIGATION_DEBUG", "1").lower() in {"1", "true", "yes"}
    app.run(host="0.0.0.0", port=5000, debug=debug_mode)
