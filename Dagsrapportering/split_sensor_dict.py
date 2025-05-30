#Splitting sensor dict into active and inactive MP's. 
def split_sensor_dict(sensor_dict, date_to):
    import pandas as pd

        # Tjekker om målepunktet er "aktivt" baseret på datoerne hentet fra Infra
    for key, value in sensor_dict.items():
        if pd.to_datetime(value['date_from']).weekday() < 5:
            date_to_active = pd.to_datetime(value['date_to'])
            date_from_active = pd.to_datetime(value['date_from']).replace(hour=12, minute=0, second=0, microsecond=0)
            value["active"] = date_from_active < date_to < date_to_active.replace(hour=date_to.hour, minute=date_to.minute, second=1)
        else:
            date_to_active = pd.to_datetime(value['date_to'])
            date_from_active = pd.to_datetime(value['date_from']).replace(hour=12, minute=0, second=0, microsecond=0)
            value["active"] = date_from_active < date_to < date_to_active.replace(hour=date_to.hour, minute=date_to.minute, second=1)
    active_sensors = {}
    inactive_sensors = {}
    
    for key, value in sensor_dict.items():
        if value.get("active") == True:
            active_sensors[key] = value
        else:
            inactive_sensors[key] = value
    
    return active_sensors, inactive_sensors