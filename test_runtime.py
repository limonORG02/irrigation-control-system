import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
from services.sensor_service import list_sensors, add_sensor, remove_sensor, add_measurement
from services.gas_service import record_gas_event, list_unacknowledged, acknowledge

print('Zones:', __import__('services.zone_service').services.zone_service.get_zones() if False else 'skipped')
# We'll operate on zone 1
zid = 1
print('Listing sensors before:', list_sensors(zid))
new_id = add_sensor(zid, 'moisture')
print('Added sensor id=', new_id)
print('Listing sensors after:', list_sensors(zid))
add_measurement(new_id, 15.5)
print('Added measurement 15.5 for sensor', new_id)
# Gas event
eid = record_gas_event(zid, 99.9)
print('Recorded gas event id=', eid)
print('Unacknowledged events:', list_unacknowledged())
acknowledge(eid)
print('Unacknowledged after ack:', list_unacknowledged())
# cleanup
remove_sensor(new_id)
print('Removed sensor', new_id)
print('Final sensors:', list_sensors(zid))
