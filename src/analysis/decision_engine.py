from utils.logger import log

def analyze_zone(zone_id, plant_type, moisture_values, norms):
    if not moisture_values:
        log(f"Нет данных от датчиков зоны {zone_id}", "ERROR")
        return "Ошибка данных"

    avg = sum(moisture_values) / len(moisture_values)
    min_m, max_m = norms

    if avg < min_m:
        return "Требуется полив"
    elif avg > max_m:
        return "Переувлажнение"
    else:
        return "Норма"
