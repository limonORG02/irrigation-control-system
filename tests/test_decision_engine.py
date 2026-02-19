import importlib
import sqlite3

import pytest


@pytest.fixture()
def temp_db(tmp_path, monkeypatch):
    """Prepare temporary DB path via environment variable for isolated tests."""
    db_path = tmp_path / "decision_engine_test.db"
    monkeypatch.setenv("IRRIGATION_DB_PATH", str(db_path))

    import config
    import database.db as db_module
    import database.models as models

    importlib.reload(config)
    importlib.reload(db_module)
    importlib.reload(models)
    models.init_db()

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("INSERT INTO zones (id, name, area, plant_type) VALUES (1, 'Zone 1', 100, 'lawn')")
    cur.execute(
        "INSERT INTO norms (plant_type, min_moisture, max_moisture) VALUES ('lawn', 20, 30)"
    )
    conn.commit()
    conn.close()

    yield db_path


@pytest.mark.parametrize(
    ("moisture", "expected_status"),
    [
        ([25], "Норма"),
        ([10], "Требуется полив"),
        ([35], "Переувлажнение"),
        ([], "Ошибка данных"),
    ],
)
def test_moisture_scenarios(temp_db, moisture, expected_status):
    """Check moisture analysis outcomes for normal and edge scenarios."""
    from analysis.decision_engine import analyze_zone

    result = analyze_zone(1, "lawn", moisture, (20, 30), gas_values=[])

    assert result["moisture_status"] == expected_status


def test_gas_alert_blocks_irrigation(temp_db):
    """Gas alert should always block irrigation regardless of moisture deficit."""
    from analysis.decision_engine import analyze_zone

    result = analyze_zone(1, "lawn", [10], (20, 30), gas_values=[950])

    assert result["gas_status"] == "Высокая вероятность запаха газа"
    assert result["irrigation_allowed"] is False
    assert result["irrigation_reason"] == "Полив отключён из-за газовой тревоги"


def test_combined_status_with_warning_gas(temp_db):
    """Combined status should include gas warning suffix for warning gas levels."""
    from analysis.decision_engine import analyze_zone

    result = analyze_zone(1, "lawn", [25], (20, 30), gas_values=[650])

    assert result["status"] == "Норма + Проверить газ"
    assert result["gas_status"] == "Есть вероятность запаха газа"
