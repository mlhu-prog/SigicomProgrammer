def fetch_sensor_info(sensor_ids, base_url, auth, years):
    import requests, time
    from datetime import datetime, timedelta
    import os
    from basic_functions import save_json
    from logger import get_logger

    logger = get_logger()

    today = datetime.today()
    sensor_info = {}

    for idx, sensor_id in enumerate(sensor_ids):
        logger.log(f"Henter data for sensor {sensor_id}: {idx+1}/{len(sensor_ids)}", 1)

        url = f"{base_url}/{sensor_id}"
        response = requests.get(url=url, auth=auth, headers={'accept': 'application/json'})
        
        # Retry logic
        wait_time = 0
        while response.status_code != 200:
            logger.log(f"Venter på API svar: {wait_time + 5} sekunder")
            time.sleep(5)
            wait_time += 5
            response = requests.get(url=url, auth=auth, headers={'accept': 'application/json'})
            if wait_time > 60:
                logger.log(f"API svarer ikke. Kontakt MLHU", 2, 1)
                raise ConnectionError("API is not responding. Please contact MLHU.")

        data_temp = response.json()
        
        last_time_read = data_temp.get("timestamp_last_read",1)
        last_time_read = datetime.fromtimestamp(last_time_read).strftime("%Y-%m-%d %H:%M")
        
        cali_date_str = data_temp.get("calibration_date", "ukendt")

        if cali_date_str == None:
            cali_date_str = "ukendt"
        
        try:
            cali_date = datetime.strptime(cali_date_str, "%Y-%m-%d")

            cali_status = "OK" if today - cali_date < timedelta(days=365*years) else "IKKE OK"
        except:
            cali_status = "Ukendt"

        sensor_info[sensor_id] = {"Type": data_temp.get("type", "ukendt"), "Status": data_temp.get("state","ukendt"), "Sidste data hentet": last_time_read, 
                                "Kalibreringsdato": cali_date_str, "Kalibreringsstatus": cali_status}
    
    logger.log(f"Sensor information hentet", 2)

    return sensor_info
