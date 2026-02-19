from services.sensor_service import GAS_CRITICAL_THRESHOLD_PPM, GAS_WARNING_THRESHOLD_PPM
from utils.logger import log

GAS_ALERT_STATUSES = {
    "Высокая вероятность запаха газа",
    "Есть вероятность запаха газа",
}


def _analyze_moisture(zone_id, moisture_values, norms):
    """Analyze average moisture relative to norms."""
    if not moisture_values:
        log(f"Нет данных от датчиков влажности зоны {zone_id}", "ERROR")
        return "Ошибка данных"

    avg = sum(moisture_values) / len(moisture_values)
    min_m, max_m = norms

    if avg < min_m:
        return "Требуется полив"
    if avg > max_m:
        return "Переувлажнение"
    return "Норма"


def _analyze_gas(gas_values):
    """Analyze gas peak level and map it to a risk status."""
    if not gas_values:
        return "Нет газовых датчиков"

    peak = max(gas_values)
    if peak >= GAS_CRITICAL_THRESHOLD_PPM:
        return "Высокая вероятность запаха газа"
    if peak >= GAS_WARNING_THRESHOLD_PPM:
        return "Есть вероятность запаха газа"
    return "Газовая норма"


def _build_irrigation_decision(moisture_status, gas_status):
    """Return whether irrigation can be started, with gas alert priority."""
    if gas_status in GAS_ALERT_STATUSES:
        log("Полив отключён из-за газовой тревоги", "WARNING")
        return False, "Полив отключён из-за газовой тревоги"

    if moisture_status == "Требуется полив":
        return True, "Полив разрешён"

    if moisture_status == "Ошибка данных":
        return False, "Полив отключён из-за ошибки данных"

    return False, "Полив не требуется"


def analyze_zone(zone_id, plant_type, moisture_values, norms, gas_values=None):
    """Analyze zone state by moisture and gas and return combined decision payload."""
    moisture_status = _analyze_moisture(zone_id, moisture_values, norms)
    gas_status = _analyze_gas(gas_values or [])

    if gas_status in GAS_ALERT_STATUSES:
        log(
            f"Зона {zone_id} ({plant_type}): {gas_status}. Требуется проверка территории.",
            "WARNING",
        )

    if moisture_status == "Ошибка данных":
        final_status = moisture_status
    elif gas_status == "Высокая вероятность запаха газа":
        final_status = f"{moisture_status} + Газовая тревога"
    elif gas_status == "Есть вероятность запаха газа":
        final_status = f"{moisture_status} + Проверить газ"
    else:
        final_status = moisture_status

    irrigation_allowed, irrigation_reason = _build_irrigation_decision(
        moisture_status,
        gas_status,
    )

    return {
        "moisture_status": moisture_status,
        "gas_status": gas_status,
        "status": final_status,
        "irrigation_allowed": irrigation_allowed,
        "irrigation_reason": irrigation_reason,
    }
