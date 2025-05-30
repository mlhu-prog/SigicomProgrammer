#Gather a list of sensors (MP's) in given project, and split it into active and inactive list
def get_sensorlist_in_project(project_number, username, password, atr, name,
                              date_to, date_range, cache_date, cache_main_dir
                              ):
    import pandas as pd
    from datetime import datetime
    import os
    import time
    import requests
    from requests.auth import HTTPBasicAuth

    #Project imports
    from logger import get_logger
    from basic_functions import load_json, search_json, save_json
    from address_locater import get_addresses_by_coordinates
    from split_sensor_dict import split_sensor_dict

    logger = get_logger()
    logger.log(f"{atr} - {name}")
    logger.log(f"Data periode: {date_range}")

    base_url = "https://cowidk.infralogin.com/api/v1"
    project_url = "/".join([base_url, "project", project_number, "measure_point/"])
    cache_file_sens = os.path.join(cache_main_dir,"API",cache_date,"project_sensor_dict.json")

    #Try to load existing sensor dictionary from cache   
    if os.path.exists(cache_file_sens):
        sensor_dict = load_json(cache_file_sens)
    else:
        logger.log("Henter data fra INFRA Server")
        # Fetch sensor data from API and handle errors
        response = requests.get(url=project_url, auth=HTTPBasicAuth(username, password), headers={'accept': 'application/json'})

        wait_time = 0
        while response.status_code != 200:
            logger.log(f"Venter: {wait_time+5}")
            time.sleep(5)
            response = requests.get(url=project_url, auth=HTTPBasicAuth(username, password), headers={'accept': 'application/json'})
            wait_time += 5

        #Save raw API response to cache
        data = response.json()
        cache_file_raw = os.path.join(cache_main_dir, "API", cache_date, "project.json")
        save_json(data, cache_file_raw)  

        #Try to find previous sensor address info, if any
        subfolders = [f.name for f in os.scandir(os.path.join(cache_main_dir,"API")) if f.is_dir()]
        date_folders = []
        for folder in subfolders:
            try:
                date = datetime.strptime(folder, '%Y-%m-%d')
                date_folders.append((date, folder))
            except ValueError:
                continue   
        newest_sensor_dict = None 
        if date_folders:
            latest_folder = max(date_folders, key=lambda x: x[0])[1]
            newest_sensor_dict_file = os.path.join(cache_main_dir, "API", latest_folder, "project_sensor_dict_final.json")
            if os.path.exists(newest_sensor_dict_file):
                newest_sensor_dict = load_json(newest_sensor_dict_file)


        #Extract sensor data from API response
        names = search_json(data, "name") #Name of measueringpoints
        loggers = search_json(data,"sensor_type") #Sensor type
        lats = search_json(data, "lat") #Coordinate Latitude
        longs = search_json(data, "lng") #Coordinate Longitude
        sensor_ids = search_json(data, "sensor_serial") #Sensor ID
        measuring_points = search_json(data, "id") #Uses for later gathering of data
        date_tos = search_json(data, "datetime_to") #Info about the date_to from Infra
        date_froms = search_json(data, "datetime_from") #Info about the date_from from Infra

        #Resolve addresses, using both previous cache and fresh lookups as needed
        adresses = []
        if newest_sensor_dict:
            for name, lat, long in zip(names, lats, longs):
                if name in newest_sensor_dict.keys():
                    adresses.append(newest_sensor_dict[name]["postcode"])
                else:
                    lookup = get_addresses_by_coordinates(lat, long, name)
                    adresses.append(lookup[0] if lookup else None)
        else:
            adresses = get_addresses_by_coordinates(lats, longs, names)

        #If any address is missing, raise error
        if None in adresses:
            indicies = [i for i in range(len(adresses)) if adresses[i] == None]
            logger.log("Der er ikke angivet en placering i INFRA for [{}]. Angiv en placering og prøv igen.".format(names[indicies]),2,2)
            raise KeyError("Der er ikke sat en placering i INFRA for [{}]. Angiv en placering og prøv igen.".format(names[indicies]))
        

        #Building sensor dict
        sensor_dict = dict(
            zip(
                names,
                [
                    {
                        'measuring_point': measuring_point,
                        'logger': logger_name,
                        'sensor_id': sensor_id,
                        'date_to': date_to_value,
                        'date_from': date_from_value,
                        'postcode': postnummer
                    }
                    for measuring_point, logger_name, sensor_id, date_to_value, date_from_value, postnummer in zip(
                        measuring_points, loggers, sensor_ids, date_tos, date_froms, adresses
                    )
                ]
            )
        )

        #Saving sensor dict to cache for future runs
        save_json(sensor_dict, cache_file_sens)
        logger.log("Tilgængelig data fra INFRA Server er nu hentet")


    # Divide into active and inactive sensor dict
    active_sensor_dict, inactive_sensor_dict = split_sensor_dict(sensor_dict, date_to)

    # Ensure cache output folders exist for each active sensor
    for adresse in active_sensor_dict.keys():
        cache_dir = os.path.join(cache_main_dir, f"{adresse}", cache_date)
        os.makedirs(cache_dir, exist_ok=True)
        os.makedirs(os.path.join(cache_dir,"JSON"), exist_ok=True)
        os.makedirs(os.path.join(cache_dir,"Ascii"), exist_ok=True)
    

    # Removes "inactive" sensors, that is not yet installed (compared to the specified date minus 1 day)
    for value in inactive_sensor_dict.values():
        value['date_from'] = datetime.strptime(value['date_from'], '%Y-%m-%d %H:%M')

    # Removes MP's where 'date_from' is higher them 'date_to'
    keys_to_drop = [key for key, value in inactive_sensor_dict.items() if value['date_from'].replace(hour=23, minute=59) > date_to.replace(hour=0, minute=0)]

    for key in keys_to_drop:
        del inactive_sensor_dict[key]
        del sensor_dict[key]

    # Converts date_from in inactive sensor dict back to datestrings
    for value in inactive_sensor_dict.values():
        value['date_from'] = value['date_from'].strftime('%Y-%m-%d %H:%M')

    return sensor_dict, active_sensor_dict, inactive_sensor_dict, cache_main_dir, cache_date