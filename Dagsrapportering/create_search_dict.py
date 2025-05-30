# Create search dict to gather data from devices
import time
import pandas as pd
from datetime import timedelta
import os
import requests
from requests.auth import HTTPBasicAuth
from PySide6.QtWidgets import QMessageBox

#Project imports
from logger import get_logger
from basic_functions import load_json, search_json, save_json

def wait_for_status_ok(get_fn, logger, max_wait=100, retry_delay=5):
    wait = 0
    while True:
        response = get_fn()
        if response.status_code == 200:
            return response
        wait += retry_delay
        if wait > max_wait:
            return None
        logger.log(f"Venter: {wait} sekunder")
        time.sleep(retry_delay)

def abort_old_searches(sensor_id, search_dicts, token, username, password):
    url_base = f"https://cowidk.infralogin.com/api/v1/sensor/{sensor_id}/search/"
    headers = {"accept": "application/json", "Content-Type": "application/json", "Authorization": f"Bearer {token}"}
    for sd in search_dicts:
        if "id" in sd:
            url = url_base + f"{sd['id']}/"
            requests.delete(url, auth=HTTPBasicAuth(username, password), headers=headers, json={"action": "abort"})

def find_newest_entry(original_dict, new_response):
    # Extract IDs from the original search_dict
    original_ids = set(search_json(original_dict, "id"))
    
    # Extract IDs from the new response
    new_ids = set(search_json(new_response, "id"))
    
    # Find the extra ID(s)
    extra_ids = new_ids - original_ids
    
    if not extra_ids:
        return None  # No extra entries
    
    # Find the entry in the new response that corresponds to the extra ID
    extra_entries = [entry for entry in new_response if entry['id'] in extra_ids]
    
    return extra_entries[0] if extra_entries else None

def create_search_dict(
        project_id, username, password, sensor_dict, 
        cache_main_dir, cache_date, date_to=None, date_from=None
    ):
    """
    Creates search dicts for sensors in project, caching by project and date.
    """

    logger = get_logger()
    _, token = password.split(":")
    base_url = "https://cowidk.infralogin.com/api/v1"
    data_search_dict = {
        "datetime_from": date_from,
        "datetime_to": date_to,
        "data_types": {"transient": True, "interval": True}
    }

    cache_file = os.path.join(cache_main_dir, "API", cache_date, f"{project_id}_search.json")

    if os.path.exists(cache_file):
        return load_json(cache_file)

    searches_dict = {}

    for adresse, sensor_info in sensor_dict.items():
        cache_file_adresse = os.path.join(cache_main_dir, adresse, cache_date, "JSON")

        # Date logic
        info_from = pd.to_datetime(sensor_info['date_from'])
        user_from = pd.to_datetime(date_from) if date_from else info_from

        compare_date = info_from.replace(hour=0, minute=0, second=0, microsecond=0)
        if info_from.weekday() < 5:
            if compare_date > user_from:
                continue
        else:
            if compare_date - timedelta(hours=48) > user_from:
                continue

        sensor_id = str(sensor_info['sensor_id'])
        sensor_url = f"{base_url}/sensor/{sensor_id}/search/"
        auth = HTTPBasicAuth(username, password)

        # Start search
        requests.post(sensor_url, headers={"Content-Type": "application/json"}, auth=auth, json=data_search_dict)
        get_search = lambda: requests.get(url=sensor_url, auth=auth, headers={'accept': 'application/json'})
        response = wait_for_status_ok(get_search, logger)
        if not response:
            QMessageBox.critical(None, "Fejl", f"Der kan ikke laves ID for {adresse}. \n Prøv igen, ellers kontakt Mikkel Houe, MLHU")
            raise LookupError(f"Can't create search dict for {adresse}, {sensor_id}")

        search_dict = response.json()

        # If there are multiple or incomplete searches, abort them and try again once
        try_delete = 0
        while (isinstance(search_dict, list) and (len(search_dict) > 1 or "datetime_to" not in search_dict[0] or "datetime_from" not in search_dict[0])):
            if try_delete < 2:
                old_search_dict = search_dict
                abort_old_searches(sensor_id, search_dict, token, username, password)
                requests.post(sensor_url, headers={"Content-Type": "application/json"}, auth=auth, json=data_search_dict)
                response = wait_for_status_ok(get_search, logger)
                if not response:
                    QMessageBox.critical(None, "Fejl", f"Der kan ikke laves ID for {adresse}. \n Prøv igen, ellers kontakt Mikkel Houe, MLHU")
                    raise LookupError(f"Can't create search dict for {adresse}, {sensor_id}")
                search_dict = response.json()
                try_delete += 1
            else:
                search_dict = find_newest_entry(old_search_dict, search_dict)

        # save and aggregate
        save_json(search_dict, os.path.join(cache_file_adresse, "search_dict.json"))
        if isinstance(search_dict, list) and len(search_dict) > 0:
            search_dict[0]["sensor_id"] = sensor_id
            searches_dict[adresse] = search_dict[0]
        else:
            search_dict["sensor_id"] = sensor_id
            searches_dict[adresse] = search_dict

    save_json(searches_dict, cache_file)
    return searches_dict


def remake_search_dict(
        project_id, username, password, sensor_info, 
        cache_main_dir, cache_date, adresse, 
        date_to=None, date_from=None):
    """
    Re-creates the search dict for a specific sensor and adresse, aborts old searches, and returns the data_url.
    Args:
        project_id, username, password, sensor_info, cache_main_dir, cache_date, adresse, date_to, date_from
    Returns:
        str: The full data_url for the sensor's search results.
    """
    logger = get_logger()
    _, token = password.split(":")
    base_url = "https://cowidk.infralogin.com/api/v1"

    # Set up dates
    if not date_from:
        date_from = sensor_info['date_from']
    if not date_to:
        date_to = sensor_info['date_to']

    compare_date = pd.to_datetime(sensor_info['date_from']).replace(hour=0, minute=0, second=0, microsecond=0)
    input_date_from = pd.to_datetime(date_from) if date_from else compare_date

    # If date check fails, return empty dict
    if compare_date > input_date_from:
        return {}

    data_search_dict = {
        "datetime_from": date_from,
        "datetime_to": date_to,
        "data_types": { "transient": True, "interval": True }
    }

    sensor_id = str(sensor_info['sensor_id'])
    sensor_url = f"{base_url}/sensor/{sensor_id}/search/"
    cache_file = os.path.join(cache_main_dir, "API", cache_date, f"{project_id}_search.json")
    cache_file_adresse = os.path.join(cache_main_dir, adresse, cache_date, "JSON")
    # Create dirs if necessary
    os.makedirs(cache_file_adresse, exist_ok=True)

    searches_dict = load_json(cache_file)
    # Remove old searches for this adresse
    search_dict_adresse_path = os.path.join(cache_file_adresse, "search_dict.json")
    if os.path.exists(search_dict_adresse_path):
        search_dict_adresse = load_json(search_dict_adresse_path)
        search_ids = search_json(search_dict_adresse, "id")
        abort_old_searches(sensor_id, [{"id": sid} for sid in search_ids], token, username, password)

    # Create new search
    auth = HTTPBasicAuth(username, password)
    requests.post(sensor_url, headers={"Content-Type": "application/json"}, auth=auth, json=data_search_dict)
    get_search = lambda: requests.get(url=sensor_url, auth=auth, headers={'accept': 'application/json'})
    response = wait_for_status_ok(get_search, logger)

    if not response:
        QMessageBox.critical(None, "Fejl", f"Der kan ikke laves ID for {adresse}. \n Prøv igen, ellers kontakt Mikkel Houe, MLHU")
        raise LookupError(f"Can't create search dict for {adresse}, {sensor_id}")

    search_dict = response.json()

    try_delete = 0
    while (isinstance(search_dict, list) and (len(search_dict) > 1 or "datetime_to" not in search_dict[0] or "datetime_from" not in search_dict[0])):
        if try_delete < 2:
            old_search_dict = search_dict
            abort_old_searches(sensor_id, search_dict, token, username, password)
            requests.post(sensor_url, headers={"Content-Type": "application/json"}, auth=auth, json=data_search_dict)
            response = wait_for_status_ok(get_search, logger)
            if not response:
                QMessageBox.critical(None, "Fejl", f"Der kan ikke laves ID for {adresse}. \n Prøv igen, ellers kontakt Mikkel Houe, MLHU")
                raise LookupError(f"Can't create search dict for {adresse}, {sensor_id}")
            search_dict = response.json()
            try_delete += 1
        else:
            search_dict = find_newest_entry(old_search_dict, search_dict)

    save_json(search_dict, search_dict_adresse_path)

    # Register in overall searches_dict as in your logic
    if isinstance(search_dict, list) and len(search_dict) > 0:
        search_dict[0]["sensor_id"] = sensor_id
        searches_dict[adresse] = search_dict[0]
    else:  # fallback if not a list (usually shouldn't happen)
        search_dict["sensor_id"] = sensor_id
        searches_dict[adresse] = search_dict

    save_json(searches_dict, cache_file)
    # Return data_url
    return "https://cowidk.infralogin.com" + searches_dict[adresse]["data_url"]

    