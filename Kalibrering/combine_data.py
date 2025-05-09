def combine_data_with_ownership(sensor_info, ownership_dict):

    for sensor_id, date in sensor_info.items():
        owner = ownership_dict.get(int(sensor_id), "Ukendt")
        sensor_info[sensor_id]["Ejer"] = owner

    return sensor_info