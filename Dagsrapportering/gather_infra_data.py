import time
import os
import pandas as pd
import requests
from requests.auth import HTTPBasicAuth
from PySide6.QtWidgets import QMessageBox

#Project imports
from logger import get_logger
from basic_functions import load_json, search_json, save_json
from create_search_dict import remake_search_dict

LABELS = ['V', 'L', 'T', 'rV', 'rL', 'rT']

def extract_values(entry_list, labels):
    # Filter out entries where 'regoff' is True
    filtered_entries = [entry for entry in entry_list if not entry['regoff'] and not entry['regon']]

    # Create a mapping of label to entry
    label_to_entry = {entry['label']: entry for entry in filtered_entries}
    
    # Initialize the result dictionary
    result = {label: {'value': '0', 'frequency': '0'} for label in labels}
    
    # Populate the result dictionary with values and frequencies from the entries
    for label in labels:
        if label in label_to_entry:
            entry = label_to_entry[label]
            try:
                result[label]['value'] = entry['value']
            except KeyError:
                result[label]['value'] = entry['max']
            # Set frequency to zero if it is None
            try:
                result[label]['frequency'] = entry['frequency'] if entry['frequency'] is not None else '0'
            except KeyError:
                result[label]['frequency'] = 0
    
    return result

def get_sensor_data_url(search_entry):
    return "https://cowidk.infralogin.com" + search_entry["data_url"]

def wait_for_api_data(data_url, username, password, logger, sensor_id, adresse, remade_attempts=0):
    """Attempt to GET data from API endpoint, with exponential backoff and up to N retries."""
    wait_limits = [30, 45, 60, 90]
    wait = 0
    wait_limit = wait_limits[remade_attempts]
    while wait <= wait_limit:
        if wait != 0 and remade_attempts != 0:
            logger.log(f"Venter: {wait}/{wait_limit} sekunder")
        response = requests.get(url=data_url, auth=HTTPBasicAuth(username, password), headers={'accept': 'application/json'})
        if response.status_code == 200:
            return response
        time.sleep(5)
        wait += 5
    return None

def check_measurement_limit(raw_json, labels):
    try:
        weighting = search_json(raw_json,"frequency_weighting")[0]
        if weighting == 'Z3':
            limit = 3    
        elif weighting == 'Z2': 
            limit = 5
        elif weighting == 'Z1':
            limit = 20
        elif weighting == 'OFF':
            limit = "OFF"
        else:
            limit = 3
    except IndexError:
        limit = 3
    return limit

def process_raw_sensor_data(intervals, sensor_id, labels):
    data = {}
    for timestamp in intervals:
        time_step = timestamp["datetime"]
        timeseries_dict = timestamp[sensor_id]["intervals"]
        res = extract_values(timeseries_dict, labels)
        data[time_step] = {
            'V': float(res["V"]["value"]),
            'L': float(res["L"]["value"]),
            'T': float(res["T"]["value"]),
            'rV': float(res["rV"]["value"]),
            'rL': float(res["rL"]["value"]),
            'rT': float(res["rT"]["value"]),
            'Vfreq': float(res["V"]["frequency"]),
            'Lfreq': float(res["L"]["frequency"]),
            'Tfreq': float(res["T"]["frequency"]),
            'rVfreq': float(res["rV"]["frequency"]),
            'rLfreq': float(res["rL"]["frequency"]),
            'rTfreq': float(res["rT"]["frequency"]),
        }
    return data

def clean_up_searches(search_ids, sensor_id, token, username, password):
    """Delete all old searches for completeness."""
    for search_id in search_ids:
        search_delete_url = f"https://cowidk.infralogin.com/api/v1/sensor/{sensor_id}/search/{search_id}/"
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {token}"
        }
        requests.delete(url=search_delete_url, auth=HTTPBasicAuth(username, password), headers=headers)

def gather_INFRA_data(searches_dict, sensor_dict, username, password, cache_main_dir, cache_date):
    """Main sensor data gathering function. Pulls data from API and stores locally as needed."""
    logger = get_logger()
    logger.log("Henter data for alle aktive målepunkter")
    _, token = password.split(":")
    cache_file_sens = os.path.join(cache_main_dir, "API", cache_date, "project_sensor_dict_final.json")

    # Try to load sensors from cache if they exist:
    if os.path.exists(cache_file_sens):
        sensor_dict = load_json(cache_file_sens)

    data_dict = {}
    trans_dict = {}
    n_adresser = len(searches_dict)
    logger.log(f"Der er {n_adresser} aktive målepunkter som behandles", 2)

    for i, adresse in enumerate(searches_dict):
        logger.log(f"Behandler {adresse}: {i+1}/{n_adresser}")
        data_dict[adresse] = {}
        trans_dict[adresse] = {}

        # Set up directories
        cache_dir_json = os.path.join(cache_main_dir, adresse, cache_date, "JSON")
        cache_dir_ascii = os.path.join(cache_main_dir, adresse, cache_date, "Ascii")
        os.makedirs(cache_dir_json, exist_ok=True)
        os.makedirs(cache_dir_ascii, exist_ok=True)

        files_expected = [
            os.path.join(cache_dir_json, "data.json"),
            os.path.join(cache_dir_json, "data_API.json"),
            os.path.join(cache_dir_ascii, "data.dat"),
            os.path.join(cache_dir_ascii, "data_flagged.dat"),
        ]
        file_data_json_transient = os.path.join(cache_dir_json, "data_Transienter.json")

        has_cached = all(os.path.exists(f) for f in files_expected) and "Ziele" in sensor_dict.get(adresse, {})
        if has_cached:
            data_dict[adresse] = load_json(files_expected[0])
            trans_dict[adresse] = load_json(file_data_json_transient)
            continue

        # If not cached, pull from API:
        search_entry = searches_dict[adresse]
        sensor_id = search_entry["sensor_id"]
        search_ids = search_entry["id"]
        data_url = get_sensor_data_url(search_entry)

        response_data = wait_for_api_data(data_url, username, password, logger, sensor_id, adresse)

        # If couldn't get data, attempt to remake search dict, up to 4 times.
        retries = 4
        remade = 1
        while response_data is None or response_data.status_code != 200:
            if remade >= retries:
                QMessageBox.critical(None, "Fejl", f"Der kan ikke laves ID for {adresse}. \n Prøv igen, ellers kontakt Mikkel Houe, MLHU")
                raise LookupError(f"Cant create search dict for {adresse}, sensor {sensor_id}")
            logger.log(f"Forsøger at lave nyt ID. {remade}/{retries}", 2)
            project_id_file = os.path.join(cache_main_dir, "API", cache_date, "project.json")
            dict_temp = load_json(project_id_file)
            project_id = str(search_json(dict_temp, "project_id")[0])
            date_to = search_json(search_entry, "datetime_to")[0]
            date_from = search_json(search_entry, "datetime_from")[0]

            data_url = remake_search_dict(
                project_id, username, password, sensor_dict[adresse],
                cache_main_dir, cache_date, adresse,
                date_to=date_to, date_from=date_from
            )
            response_data = wait_for_api_data(data_url, username, password, logger, sensor_id, adresse, remade)
            remade += 1

        raw_json = response_data.json()
        save_json(raw_json, files_expected[1])

        # Determine 'Ziele'
        sensor_dict[adresse]["Ziele"] = check_measurement_limit(raw_json, LABELS)
        trans_dict[adresse]["Transienter"] = raw_json.get("transients", [])

        # Extract and save interval data
        intervals = raw_json.get("intervals", [])
        data_dict[adresse] = process_raw_sensor_data(intervals, sensor_id, LABELS)

        save_json(data_dict[adresse], files_expected[0])
        if trans_dict[adresse]["Transienter"]:
            save_json(trans_dict[adresse], file_data_json_transient)

        # Save ASCII files:
        df_temp = pd.DataFrame.from_dict(data_dict[adresse], orient="index")
        df_temp.to_csv(files_expected[2], sep="\t")
        df_temp.assign(Flag=0).to_csv(files_expected[3], sep="\t")

        # Clean up previous searches from API:
        clean_up_searches(search_ids, sensor_id, token, username, password)

    # End - cache sensor_dict
    save_json(sensor_dict, cache_file_sens)

    return data_dict, trans_dict, sensor_dict
