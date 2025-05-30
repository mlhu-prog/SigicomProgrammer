


def gather_infra_data(credential, token, info):
    import os
    import shutil
    from requests.auth import HTTPBasicAuth
    import requests
    import time
    import re
    import pandas as pd
    from PySide6.QtWidgets import QMessageBox
    import tkinter as tk
    from tkinter import ttk
    from datetime import datetime, timedelta
    from basic_functions import load_json
    from basic_functions import save_json
    from basic_functions import save_large_json
    from basic_functions import search_json
    from basic_functions import update_row
    from basic_functions import yes_no_cancel_operation

    from logger import get_logger
    
    logger = get_logger()

    def split_date_range(date_from, date_to):
        intervals = []
        start_date = datetime.strptime(date_from, "%Y-%m-%d %H:%M")
        end_date = datetime.strptime(date_to, "%Y-%m-%d %H:%M")
        while start_date < end_date:
            interval_end = start_date + timedelta(days=60)
            if interval_end > end_date:
                interval_end = end_date
            intervals.append((start_date.strftime("%Y-%m-%d %H:%M"), interval_end.strftime("%Y-%m-%d %H:%M")))
            start_date = interval_end + timedelta(minutes=2)
        return intervals

    def create_dirs(project_id, credential, token, output_folder):

        atr, name = project_ID_to_ATR(project_id, credential, token)

        # Main cache folder. 
        main_cache_folder = "O:\\A000000\\A004371\\3_Pdoc\\Afrapportering"

        if atr != None and name != None:
            cache_folder_project = f"{atr} - {name}"

            cache_main_dir = os.path.join(main_cache_folder, cache_folder_project)

            os.makedirs(os.path.join(cache_main_dir, "API"), exist_ok=True)
            os.makedirs(os.path.join(cache_main_dir, "Results"), exist_ok=True)
            os.makedirs(os.path.join(cache_main_dir, "Rapport"), exist_ok=True)
            os.makedirs(os.path.join(cache_main_dir, "Rapport", "Tekst"), exist_ok=True)
            os.makedirs(os.path.join(cache_main_dir, "Rapport", "Figurer","Oversigtsfoto"), exist_ok=True)          
    
            os.makedirs(os.path.join(output_folder, "INFRA"), exist_ok=True)

            return cache_main_dir
        else:
            QMessageBox.critical(None,"Forkert projekt ID", "Projekt ID eksisterer ikke i INFRA. Prøv igen")
            return None

    def create_appendix_dirs(output_folder, trans_dict):
        not_existing = False

        base_folder  = os.path.join(output_folder, "INFRA")
        for adresse in trans_dict.keys():
            split_adresse = adresse.split("_")

            base_key = split_adresse[0]

            basesub_key = split_adresse[1] if len(split_adresse) > 1 else ""       

            if basesub_key:
                dir_path = os.path.join(base_folder, base_key, f"_{basesub_key}")
            else:
                dir_path = os.path.join(base_folder, base_key)

            if not os.path.exists(dir_path):
                not_existing = True
            
            os.makedirs(dir_path, exist_ok=True)
        
        if not not_existing:
            logger.log(f"{base_folder} \n Herunder er lavet mappestruktur til bilag \n Husk at hente bilag fra InfraNet.", 2, status=1)
        
    def check_available_data(cache_main_dir, project_id, credential, token, output_folder):
        missing_data = False

        project_sensor_file = os.path.join(cache_main_dir,"API","project_sensor_dict_final.json")
        if os.path.exists(project_sensor_file):
            sensor_dict = load_json(project_sensor_file)
            for adresse in sensor_dict.keys():
                result_file_1 = os.path.join(cache_main_dir, f"{adresse}","JSON", "data.json")
                result_file_2 = os.path.join(cache_main_dir, f"{adresse}","JSON", "data_API.json")
                result_file_3 = os.path.join(cache_main_dir, f"{adresse}","Ascii", "data.dat")
                search_file_1 = os.path.join(cache_main_dir, f"{adresse}","JSON", "search_dict.json")
                
                if not all(os.path.exists(result_file) for result_file in [result_file_1, result_file_2, result_file_3, search_file_1]):
                    missing_data = True
        else:
            missing_data = True


        if not missing_data:
            answer = yes_no_cancel_operation("Data", "Data eksisterer allerede for projektet. \n Vil du slette dette og hente på ny?")
            if answer == "Yes":
                answer = yes_no_cancel_operation("Data", "Er du sikker på at du vil slette alt data for projektet? \n Dette kan ikke fortrydes")
                if answer == "Yes":
                    logger.log("Sletter alt eksisterende data!", 2, status=2)
                    shutil.rmtree(cache_main_dir)
                    cache_main_dir = create_dirs(project_id, credential, token, output_folder)
                    return cache_main_dir, answer
                else:
                    return cache_main_dir, answer
            elif answer == "No":
                answer = yes_no_cancel_operation("Data", "Vil du køre 'Hent Data' alligevel?.\n Data som allerede eksisterer\n vil ikke blive overskrevet.")
                return cache_main_dir, answer
        else:
            return cache_main_dir, "Yes"

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

    def project_ID_to_ATR(project_number, username, password):
        
        #API basale URL
        base_url = "https://cowidk.infralogin.com/api/v1"


        response = requests.get(url="/".join([base_url, "project", project_number]), auth=HTTPBasicAuth(username, password), headers={'accept': 'application/json'})
        
        if response.status_code == 200:
            data = response.json()
            atr = data["project_id"]
            name = data["name"]
        else:
            logger.log(f"Project ID er ikke tilgængelig")
            return None, None
        
        return atr, name

    def extract_values(entry_list, labels, Logger):
        # Filter out entries where 'regoff' is True
        filtered_entries = [entry for entry in entry_list if not entry['regoff'] and not entry['regon']]

        # Create a mapping of label to entry
        label_to_entry = {entry['label']: entry for entry in filtered_entries}
        
        # Initialize the result dictionary
        result = {label: {'value': '0', 'frequency': '0'} for label in labels}

        entry_id = 'value' if Logger != "V12" else 'unweighted'
        entry_try = 'max' if Logger != "V12" else 'value'
        
        # Populate the result dictionary with values and frequencies from the entries
        for label in labels:
            if label in label_to_entry:
                entry = label_to_entry[label]
                try:
                    result[label]['value'] = entry[entry_id]
                except KeyError:
                    result[label]['value'] = entry[entry_try]
                # Set frequency to zero if it is None
                try:
                    result[label]['frequency'] = entry['frequency'] if entry['frequency'] is not None else '0'
                except KeyError:
                    result[label]['frequency'] = 0
        
        return result

    def get_sensorlist_in_project(project_number, username, password, cache_main_dir):

        project_sensor_file = os.path.join(cache_main_dir,"API","project_sensor.json")
        if os.path.exists(project_sensor_file):
            sensor_dict = load_json(project_sensor_file)
        else:
            ### Laver directiories
            # Henter ATR og navn for givne project-ID 

            base_url = "https://cowidk.infralogin.com/api/v1"

            project_url = "/".join([base_url, "project", project_number, "measure_point/"])

            # Laver request til Sigicom API server
            response = requests.get(url=project_url, auth=HTTPBasicAuth(username, password), headers={'accept': 'application/json'})
        
            cache_file_raw = os.path.join(cache_main_dir,"API","project.json")

            if response.status_code == 200:
                data = response.json()
                save_json(data, cache_file_raw)

                names = search_json(data, "name") #Navn på målepunkt

                # Finder relevante informationer i data hentet fra server
                Loggers = search_json(data,"sensor_type") #Sensor type
                lats = search_json(data, "lat") #Koordinat
                longs = search_json(data, "lng") #Koordinat
                #adresses = get_addresses_by_coordinates(lats, longs)
                sensor_ids = search_json(data, "sensor_serial") #Sensor ID
                measuring_points = search_json(data, "id") #Bruger til senere at hente data
                date_tos = search_json(data, "datetime_to") #Angiver hvornår målepunktet er afsluttet (I infra)
                date_froms = search_json(data, "datetime_from") #Angiver hvornår målepunktet er oprettet (I infra)
                #Samler det hele
                sensor_dict = dict(zip(names, [{'measuring_point': measuring_point, 'logger': Logger, 'sensor_id': sensor_id, 'date_to': date_to, 'date_from': date_from} 
                                            for measuring_point, Logger, sensor_id, date_to, date_from in zip(measuring_points, Loggers, sensor_ids, date_tos, date_froms)]))
            else:
                logger.log(f'Error: {response.status_code}')

            # Samlet cache dir for den angivne dato og projekt-id. 
            for adresse in sensor_dict.keys():
                cache_dir = os.path.join(cache_main_dir, f"{adresse}")
                if not os.path.exists(cache_dir):
                    os.makedirs(os.path.join(cache_dir,"JSON"), exist_ok=True)
                    os.makedirs(os.path.join(cache_dir,"Ascii"), exist_ok=True)
            
            save_json(sensor_dict, project_sensor_file)
            
        return sensor_dict

    def UI_measuringpoint_information(sensor_dict, cache_main_dir):
        new_dates = {}  # Dictionary to store updated dates
        project_sensor_file_final = os.path.join(cache_main_dir,"API","project_sensor_dict_final.json")
        project_sensor_file = os.path.join(cache_main_dir,"API","project_sensor.json")

        # Date format validator
        def validate_date(date_text):
            pattern = r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}$"
            return re.match(pattern, date_text) is not None

        def collect_dates_and_limits():
            """ Collects all dates from entries and validates format """

            for adresse_key, entries in okVar.items():
                if entries.get() == 0:
                    QMessageBox.critical(None, "Fejl: Manglende check", f"{adresse_key} mangler at blive sammenlignet med målelog")
                    return

            for adresse_key, entries in date_entries.items():
                date_from = entries['date_from'].get()
                date_to = entries['date_to'].get()

                # Validate date format
                if not validate_date(date_from) or not validate_date(date_to):
                    QMessageBox.critical(None,"Fejl: Dato-format", f"Fejl: {adresse_key}. \n Ved angivelse af dato, skal det være i følgende format 'yyyy-mm-dd HH:MM'")
                    return

                # Store in new_dates dictionary
                sensor_dict[adresse_key]['date_from'] = date_from
                sensor_dict[adresse_key]['date_to'] = date_to
                sensor_dict[adresse_key]['limit'] = limit_vars[adresse_key].get()
            
            save_json(sensor_dict, project_sensor_file_final)
            save_json(sensor_dict, project_sensor_file)

            root_MPInfoGUI.quit()
            root_MPInfoGUI.destroy()

        root_MPInfoGUI = tk.Tk()
        root_MPInfoGUI.title("Målepunkts information")
        root_MPInfoGUI.geometry("800x365")
        notebook = ttk.Notebook(root_MPInfoGUI)
        notebook.pack(pady=5, expand=True)

        # Dictionary to hold date entries for each address
        date_entries = {}
        
        okVar = {}
        limit_vars = {}

        # Generate a tab for each address
        for adresse_key, info in sensor_dict.items():

            okVar[adresse_key] = tk.IntVar()
            limit_vars[adresse_key] = tk.IntVar(value=3) if not "limit" in sensor_dict[adresse_key] else tk.IntVar(value=sensor_dict[adresse_key]["limit"])

            row = 0
            frame = ttk.Frame(notebook, width=800)
            frame.pack(fill="both", expand=True)
            notebook.add(frame, text=adresse_key)
            date_entries[adresse_key] = {}

            # Display Logger and Sensor ID
            ttk.Label(frame, text=f"{adresse_key}").grid(row=row, column=0,columnspan=2, padx=5, pady=5, sticky="w")
            row = update_row(row)
            ttk.Label(frame, text="Logger:").grid(row=row, column=0, padx=5, pady=5, sticky="w")
            ttk.Label(frame, text=info['logger']).grid(row=row, column=1, padx=5, pady=5, sticky="w")
            row = update_row(row)

            ttk.Label(frame, text="Serienr.:").grid(row=row, column=0, padx=5, pady=5, sticky="w")
            ttk.Label(frame, text=info['sensor_id']).grid(row=row, column=1, padx=5, pady=5, sticky="w")
            row = update_row(row)

            # Entry for date_from
            ttk.Label(frame, text="Dato opsat:").grid(row=row, column=0, padx=5, pady=5, sticky="w")
            date_from_entry = ttk.Entry(frame)
            date_from_entry.insert(0, info['date_from'])
            date_from_entry.grid(row=row, column=1, padx=5, pady=5, sticky="w")
            date_entries[adresse_key]['date_from'] = date_from_entry
            row = update_row(row)

            # Entry for date_to
            ttk.Label(frame, text="Dato nedtaget:").grid(row=row, column=0, padx=5, pady=5, sticky="w")
            date_to_entry = ttk.Entry(frame)
            date_to_entry.insert(0, info['date_to'])
            date_to_entry.grid(row=row, column=1, padx=5, pady=5, sticky="w")
            date_entries[adresse_key]['date_to'] = date_to_entry
            row = update_row(row)

            # Radiobuttons for limit selection
            ttk.Label(frame, text="Grænseværdi:").grid(row=row, column=0, padx=5, pady=5, sticky="w")
            ttk.Radiobutton(frame, text="Zeile 3", variable=limit_vars[adresse_key], value=3).grid(row=row, column=1, padx=5, pady=5, sticky="w")
            row = update_row(row)
            ttk.Radiobutton(frame, text="Zeile 2", variable=limit_vars[adresse_key], value=5).grid(row=row, column=1, padx=5, pady=5, sticky="w")
            row = update_row(row)
            ttk.Radiobutton(frame, text="Zeile 1", variable=limit_vars[adresse_key], value=20).grid(row=row, column=1, padx=5, pady=5, sticky="w")
            row = update_row(row)

            checkbutton = ttk.Checkbutton(frame, text = "OK", variable=okVar[adresse_key], onvalue = 1, offvalue=0)
            checkbutton.grid(row=row, column=0, padx=5, pady=5, sticky='w')

        # Button to collect all dates
        collect_button = ttk.Button(root_MPInfoGUI, text="Fortsæt", command=collect_dates_and_limits)
        collect_button.pack(pady=10)

        root_MPInfoGUI.mainloop()
        return sensor_dict

    def create_search_dict(project_id, username, password, sensor_dict, cache_main_dir, date_to = None, date_from = None):  
        _, token = password.split(":")

        base_url = "https://cowidk.infralogin.com/api/v1"
        
        cache_file = os.path.join(cache_main_dir, "API", f"{project_id}_search.json")

        logger.log("Danner ID's til at søge efter data for hvert målepunkt",2)

        if os.path.exists(cache_file):
            searches_dict = load_json(cache_file)           
        else:
            searches_dict = {}
            for adresse in sensor_dict.keys():
                cache_file_path = os.path.join(cache_main_dir, f"{adresse}","JSON")
                cache_file_adresse = os.path.join(cache_file_path, "search_dict.json")
                
                sensor_info = sensor_dict[adresse]
                sensor_id = str(sensor_info['sensor_id'])
                
                os.makedirs(cache_file_path, exist_ok=True)

                if not date_from:   
                    date_from_adresse = sensor_info['date_from']

                if not date_to:
                    date_to_adresse = sensor_info['date_to']
                    # Angiver data-input for at senere at hente måledata

                if sensor_info["logger"] == "V12":
                    sensor_url = "/".join([base_url, "sensor", sensor_id, "search/"])
    
                    response_check = requests.get(url=sensor_url, auth=HTTPBasicAuth(username, password), headers={'accept': 'application/json'})
                    
                    while response_check.status_code != 200:
                        time.sleep(5)
                        response_check = requests.get(url=sensor_url, auth=HTTPBasicAuth(username, password), headers={'accept': 'application/json'})


                    if len(response_check.json())>0:
                        search_ids = search_json(response_check.json(), "id")
                        for search_id in search_ids:
                            delete_search_id(project_id, sensor_id, adresse, search_id, token, username, password, cache_main_dir, first_creation=True)


                    intervals = split_date_range(date_from_adresse, date_to_adresse)
                    for interval in intervals:
                        data_search_dict = {
                            "datetime_from": interval[0],
                            "datetime_to": interval[1],
                            "data_types": {
                                "transient": True,
                                "interval": True
                            }
                        }
                        response = requests.post(sensor_url, headers = {"Content-Type": "application/json"}, auth=HTTPBasicAuth(username, password), json=data_search_dict)
                        response = requests.get(url=sensor_url, auth=HTTPBasicAuth(username, password), headers={'accept': 'application/json'})
                        check = response.status_code
                        wait = 0
                        while check != 200:
                            logger.log(f"{wait} sekunder")
                            response = requests.get(url=sensor_url, auth=HTTPBasicAuth(username, password), headers={'accept': 'application/json'})
                            time.sleep(5)
                            check = response.status_code
                            if check == 200:
                                break
                            wait += 5
                    
                    search_dict = response.json()

                    try:
                        search_dict[0]["sensor_id"] = sensor_id
                    except KeyError:
                        search_dict["sensor_id"] = sensor_id
                    
                    searches_dict[adresse] = search_dict

                    save_json(search_dict, cache_file_adresse)
                else:
                    sensor_url = "/".join([base_url, "sensor", sensor_id, "search/"])
    
                    response_check = requests.get(url=sensor_url, auth=HTTPBasicAuth(username, password), headers={'accept': 'application/json'})
                    
                    while response_check.status_code != 200:
                        time.sleep(5)
                        response_check = requests.get(url=sensor_url, auth=HTTPBasicAuth(username, password), headers={'accept': 'application/json'})


                    if len(response_check.json())>0:
                        search_ids = search_json(response_check.json(), "id")
                        for search_id in search_ids:
                            delete_search_id(project_id, sensor_id, adresse, search_id, token, username, password, cache_main_dir, first_creation=True)
                    data_search_dict = {
                        "datetime_from": date_from_adresse,
                        "datetime_to": date_to_adresse,
                        "data_types": {
                            "transient": True,
                            "interval": True
                        }
                    }

                    sensor_id = str(sensor_info['sensor_id'])
                    sensor_url = "/".join([base_url, "sensor", sensor_id, "search/"])
                    
                    response = requests.post(sensor_url, headers = {"Content-Type": "application/json"}, auth=HTTPBasicAuth(username, password), json=data_search_dict)
                    response = requests.get(url=sensor_url, auth=HTTPBasicAuth(username, password), headers={'accept': 'application/json'})

                    # Ser om data er hentet
                    check = response.status_code

                    wait = 0

                    while check != 200:
                        logger.log(f"Venter: {wait} sekunder")
                        response = requests.get(url=sensor_url, auth=HTTPBasicAuth(username, password), headers={'accept': 'application/json'})

                        time.sleep(5)

                        check = response.status_code

                        if check == 200:
                            break

                        wait += 5
                    
                    try_delete = 0

                    search_dict = response.json()

                    while len(search_dict) > 1 or "datetime_to" not  in search_dict[0] or "datetime_from" not in search_dict[0]:
                        if try_delete < 2:
                            old_search_dict = search_dict
                            search_ids = search_json(search_dict, "id")
                            for search_id in search_ids:
                                    
                                    search_delete_url = f"https://cowidk.infralogin.com/api/v1/sensor/{sensor_id}/search/{search_id}/"
                                    
                                    headers = {
                                        "accept": "application/json",
                                        "Content-Type": "application/json",
                                        "Authorization": f"Bearer {token}"
                                    }

                                    data = {"action": "abort"}
                                    
                                    response = requests.delete(url=search_delete_url, auth=HTTPBasicAuth(username, password), headers=headers, json=data)
                                    
                            
                            response = requests.post(sensor_url, headers = {"Content-Type": "application/json"}, auth=HTTPBasicAuth(username, password), json=data_search_dict)
                            response = requests.get(url=sensor_url, auth=HTTPBasicAuth(username, password), headers={'accept': 'application/json'})

                            # Ser om data er hentet
                            check = response.status_code

                            wait = 0

                            while check != 200:
                                logger.log(f"Venter: {wait} sekunder")
                                response = requests.get(url=sensor_url, auth=HTTPBasicAuth(username, password), headers={'accept': 'application/json'})

                                time.sleep(5)

                                check = response.status_code

                                if check == 200:
                                    break

                                wait += 5
                            
                            search_dict = response.json()

                            try_delete += 1
                        else:

                            search_dict = find_newest_entry(old_search_dict, search_dict)

                            break

                    try:
                        search_dict[0]["sensor_id"] = sensor_id
                        searches_dict[adresse] = search_dict[0]
                    except KeyError:
                        search_dict["sensor_id"] = sensor_id
                        searches_dict[adresse] = search_dict

                    save_json(search_dict, cache_file_adresse)
                
                
                
            
            save_json(searches_dict, cache_file)



        return searches_dict

    def remake_search_dict(project_id, username, password, sensor_dict, search_ids, existing_ids, cache_main_dir, adresse, date_to = None, date_from = None):  
        _, token = password.split(":")

        base_url = "https://cowidk.infralogin.com/api/v1"
        cache_file = os.path.join(cache_main_dir,"API",f"{project_id}_search.json")
        
        cache_file_adresse = os.path.join(cache_main_dir, f"{adresse}","JSON")
        
        searches_dict = load_json(cache_file)

        sensor_info = sensor_dict
        
        sensor_id = str(sensor_info['sensor_id'])
        sensor_url = "/".join([base_url, "sensor", sensor_id, "search/"])

        if not date_from:   
            date_from = sensor_info['date_from']

        if not date_to:
            date_to = sensor_info['date_to']

        # Convert date_from and date_to to datetime objects
        #date_from_dt = datetime.datetime.strptime(date_from, '%Y-%m-%d %H:%M:%S')
        #date_to_dt = datetime.datetime.strptime(date_to, '%Y-%m-%d %H:%M:%S')
        
        
        # Angiver data-input for at senere at hente måledata
        data_search_dict = {
            "datetime_from": date_from,
            "datetime_to": date_to,
            "data_types": {
                "transient": True,
                "interval": True
            }
        }

        response = requests.post(sensor_url, headers = {"Content-Type": "application/json"}, auth=HTTPBasicAuth(username, password), json=data_search_dict)
        response = requests.get(url=sensor_url, auth=HTTPBasicAuth(username, password), headers={'accept': 'application/json'})

        search_dict_adresse = load_json(os.path.join(cache_file_adresse, "search_dict.json"))

        # Ser om data er hentet
        check = response.status_code

        while check != 200:
            if wait > 100:
                QMessageBox.critical(None,"Fejl",f"Der kan ikke laves ID for {adresse}. \n Prøv igen, ellers kontakt Mikkel Houe, MLHU")
                raise LookupError(f"Cant create search dict for {adresse}, {sensor_id}")
            logger.log(f"Venter: {wait} sekunder")
            response = requests.get(url=sensor_url, auth=HTTPBasicAuth(username, password), headers={'accept': 'application/json'})

            time.sleep(5)

            check = response.status_code

            if check == 200:
                break

            wait += 5
        
        if len(response.json()) > len(existing_ids):
            logger.log("Fejl i hentning af data for målepunkt. Laver nyt ID",2)
            delete_ids = search_json(response.json(), "id")

            for delete_id in delete_ids:
                
                search_delete_url = f"https://cowidk.infralogin.com/api/v1/sensor/{sensor_id}/search/{delete_id}/"
                
                headers = {
                    "accept": "application/json",
                    "Authorization": f"Bearer {token}"
                }
                
                response = requests.delete(url=search_delete_url, auth=HTTPBasicAuth(username, password), headers=headers)
            
            search_dict_adresse




        #search_ids = search_json(search_dict_adresse, "id")
        else:
            for search_id in search_ids:
                
                search_delete_url = f"https://cowidk.infralogin.com/api/v1/sensor/{sensor_id}/search/{search_id}/"
                
                headers = {
                    "accept": "application/json",
                    "Authorization": f"Bearer {token}"
                }
                
                response = requests.delete(url=search_delete_url, auth=HTTPBasicAuth(username, password), headers=headers)
            

        search_dict = response.json()

        try:
            search_dict[0]["sensor_id"] = sensor_id
        except KeyError:
            search_dict["sensor_id"] = sensor_id
        
        searches_dict[adresse] = search_dict

        save_json(search_dict, search_dict_adresse)
        
        new_entry = [entry for entry in search_dict if entry['id'] not in existing_ids]


        return "".join(["https://cowidk.infralogin.com", new_entry["data_url"]])

    def delete_search_id(project_id, sensor_id, adresse, search_id, token, username, password, cache_main_dir, first_creation = False):
        search_dict_file = os.path.join(cache_main_dir, "API", f"{project_id}_search.json")
        search_dict_adresse_file = os.path.join(cache_main_dir, f"{adresse}", "JSON", f"search_dict.json")

        search_delete_url = f"https://cowidk.infralogin.com/api/v1/sensor/{sensor_id}/search/{search_id}/"

        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "Authorization": f"Token {token}"
        }

        data = {"action": "delete"}

        response = requests.delete(search_delete_url, auth=HTTPBasicAuth(username, password), headers=headers, json=data)
        if all(os.path.exists(file) for file in [search_dict_file, search_dict_adresse_file]):
            search_dict = load_json(search_dict_file)
            search_dict_adresse = load_json(search_dict_adresse_file)
        
        if not first_creation and len(search_dict_adresse)>1:
            search_dict = load_json(search_dict_file)
            search_dict_adresse = load_json(search_dict_adresse_file)
            search_dict[adresse] = [entry for entry in search_dict[adresse] if entry["id"] != search_id]
            search_dict_adresse = [entry for entry in search_dict_adresse if entry["id"] != search_id]
        else:
            search_dict = {}
            search_dict[adresse] = {}
            search_dict_adresse = {}
    

            save_json(search_dict, search_dict_file)
            save_json(search_dict_adresse, search_dict_adresse_file)

    def create_single_search_dict(project_id, sensor_id, username, adresse, password, cache_main_dir, date_to, date_from, create_url = False):
        search_dict_file = os.path.join(cache_main_dir, "API", f"{project_id}_search.json")
        search_dict_adresse_file = os.path.join(cache_main_dir, f"{adresse}", "JSON", f"search_dict.json")

        search_dict = load_json(search_dict_file)
        
        base_url = "https://cowidk.infralogin.com/api/v1"
        sensor_url = "/".join([base_url, "sensor", sensor_id, "search/"])
        data_search_dict = {
            "datetime_from": date_from,
            "datetime_to": date_to,
            "data_types": {
                "transient": True,
                "interval": True
            }
        }
        response_check = requests.get(url=sensor_url, auth=HTTPBasicAuth(username, password), headers={'accept': 'application/json'})
        while response_check.status_code != 200:
            time.sleep(5)
            response_check = requests.get(url=sensor_url, auth=HTTPBasicAuth(username, password), headers={'accept': 'application/json'})

        data_check_ids = search_json(response_check.json(),"id")

        sensor_url = "/".join([base_url, "sensor", sensor_id, "search/"])
        response = requests.post(sensor_url, headers = {"Content-Type": "application/json"}, auth=HTTPBasicAuth(username, password), json=data_search_dict)
        response = requests.get(url=sensor_url, auth=HTTPBasicAuth(username, password), headers={'accept': 'application/json'})
        
        while response.status_code != 200:
            time.sleep(5)
            response = requests.get(url=sensor_url, auth=HTTPBasicAuth(username, password), headers={'accept': 'application/json'})
            
        
        data = response.json()

        try:
            data[0]["sensor_id"] = sensor_id
        except KeyError:
            data["sensor_id"] = sensor_id

        search_dict[adresse] = data
        search_dict_adresse = data

        save_json(search_dict, search_dict_file)
        save_json(search_dict_adresse, search_dict_adresse_file)

        if create_url:
            new_url = [entry['data_url'] for entry in search_dict_adresse if entry["id"] not in data_check_ids][0]
            return "".join(["https://cowidk.infralogin.com", new_url])

    def check_INFRA_and_dirData(project_id, username, password, cache_main_dir):
        
        search_dict_file = os.path.join(cache_main_dir, "API", f"{project_id}_search.json")
        search_dict = load_json(search_dict_file)

        sensor_dict_file = os.path.join(cache_main_dir, "API", "project_sensor.json")
        sensor_dict = load_json(sensor_dict_file)

        base_url = "https://cowidk.infralogin.com/api/v1"

        for adresse in search_dict.keys():
            
            sensor_id = search_json(search_dict[adresse], "sensor_id")[0]

            sensor_url = "/".join([base_url, "sensor", sensor_id, "search/"])

            response_check = requests.get(url=sensor_url, auth=HTTPBasicAuth(username, password), headers={'accept': 'application/json'})

            while response_check.status_code != 200:
                time.sleep(5)

                response_check = requests.get(url=sensor_url, auth=HTTPBasicAuth(username, password), headers={'accept': 'application/json'})

            if len(response_check.json()) > len(search_dict[adresse]):
                search_ids = search_json(response_check.json(),"id")

                for search_id in search_ids:
                    delete_search_id(project_id, sensor_id, adresse, search_id, token, username, password, cache_main_dir)
                
                if sensor_dict[adresse]["logger"] == "V12":
                    intervals = split_date_range(sensor_dict[adresse]['date_from'], sensor_dict[adresse]['date_to'])
                    for interval in intervals:
                        date_from = interval[0]
                        date_to = interval[1]
                        create_single_search_dict(project_id, sensor_id, username, adresse, password, cache_main_dir, date_to, date_from)
                else:
                    create_single_search_dict(project_id, sensor_id, username, adresse, password, cache_main_dir, sensor_dict['date_to'], sensor_dict['date_from'])

        return load_json(search_dict_file)

    def gather_INFRA_data(searches_dict, sensor_dict, username, password, cache_main_dir):  
        logger.log("Henter data for alle målepunkter",2)
        _, token = password.split(":")

        labels = ['V', 'L', 'T', 'rV', 'rL', 'rT']

        base_url = "https://cowidk.infralogin.com/api/v1"

        cache_file_sens = os.path.join(cache_main_dir,"API","project_sensor_dict_final.json")
        transient_file = os.path.join(cache_main_dir,"Results","trans_dict.json")

        if os.path.exists(cache_file_sens) and os.path.exists(transient_file):
            trans_dict = load_json(transient_file)
            sensor_dict = load_json(cache_file_sens)
            return trans_dict, sensor_dict

        data_dict = {}
        trans_dict = {}
        n_adresser = len(searches_dict)
        logger.log(f"Der er {n_adresser} målepunkter som behandles")
        for i, adresse in enumerate(searches_dict.keys()):
            
            logger.log(f"Behandler {adresse}: {i+1}/{n_adresser}")

            cache_dir_adresse_json = os.path.join(cache_main_dir, f"{adresse}","JSON")
            cache_dir_adresse_asci = os.path.join(cache_main_dir, f"{adresse}","Ascii")
            
            file_data_json = os.path.join(cache_dir_adresse_json,f"data.json")
            file_data_json_API = os.path.join(cache_dir_adresse_json,f"data_API.json")
            file_data_asci = os.path.join(cache_dir_adresse_asci,f"data.dat")
            #file_data_asci_flagged = os.path.join(cache_dir_adresse_asci,f"data_flagged.dat")

            file_all = [file_data_json, file_data_json_API, file_data_asci]

            file_data_json_transient = os.path.join(cache_dir_adresse_json,f"data_Transienter.json")

            if all(os.path.exists(file) for file in file_all):
                data_dict[adresse] = load_json(file_data_json)  # Create a dictionary for each adresse
                trans_dict[adresse] = load_json(file_data_json_transient)
                #sensor_dict[adresse] = load_json(file_data_json_sensor_final)

            else:
                data_dict[adresse] = {}  # Create a dictionary for each adresse
                trans_dict[adresse] = {}

                Logger = sensor_dict[adresse]["logger"]

                temp_search_dict = searches_dict[adresse]
                sensor_id = search_json(temp_search_dict, 'sensor_id')[0]

                #Tjek
                sensor_url = "/".join([base_url, "sensor", sensor_id, "search/"])
                response_check = requests.get(url=sensor_url, auth=HTTPBasicAuth(username, password), headers={'accept': 'application/json'})

                if Logger == "V12":

                    logger.log(f"{adresse} er en V12 og behandles ud fra {len(temp_search_dict)} intervaller")

                    search_ids = search_json(temp_search_dict,"id")
                    try:
                        sensor_id = search_json(temp_search_dict,"sensor_id")[0]
                    except:
                        sensor_id = search_json(temp_search_dict,"sensor_id")

                    raw_json = {}
                    for idx, temp_dict in enumerate(temp_search_dict):

                        date_to = search_json(temp_dict, "datetime_to")[0]
                        date_from = search_json(temp_dict, "datetime_from")[0]

                        logger.log(f"\t{idx+1}/{len(temp_search_dict)} - {date_from} - {date_to}")

                        file_data_json_API_temp = os.path.join(cache_dir_adresse_json,f"data_API_{idx+1}.json")

                        data_url = temp_dict["data_url"]
                        search_id = search_ids[idx]

                        data_url = "".join(["https://cowidk.infralogin.com", data_url])

                        response_data = requests.get(url=data_url, auth=HTTPBasicAuth(username, password), headers={'accept': 'application/json'})

                        check = response_data.status_code

                        wait = 0

                        new_id = 0
                        
                        while check != 200:
                            if new_id == 0:
                                wait_limit = 10
                            elif new_id == 1:
                                wait_limit = 25
                            else:
                                wait_limit = 45

                            logger.log(f"{wait}/{wait_limit} sekunder")

                            time.sleep(5)

                            wait += 5

                            if wait > wait_limit:
                                if new_id > 3:
                                    QMessageBox.critical(None,"Fejl",f"Der kan ikke laves ID for {adresse}. \n Prøv igen, ellers kontakt Mikkel Houe, MLHU")
                                    raise LookupError(f"Cant create search dict for {adresse}, sensor {sensor_id}")
                                
                                logger.log(f"Forsøger at lave nyt ID. {new_id+1}/4",2)

                                project_id_file = os.path.join(cache_main_dir,"API","project.json")
                                dict_temp = load_json(project_id_file)
                                project_id = str(search_json(dict_temp,"project_id")[0])

                                delete_search_id(project_id, sensor_id, adresse, search_id, token, username, password, cache_main_dir)
                                data_url = create_single_search_dict(project_id, sensor_id, username, adresse, password, cache_main_dir, 
                                                                     date_to, date_from, create_url = True)

                                #data_url = remake_search_dict(project_id, username, password, sensor_dict[adresse], [search_id], search_ids, 
                                #                              cache_main_dir, adresse, date_to = date_to, date_from = date_from)

                                wait = 0

                                new_id += 1

                            response_data = requests.get(url=data_url, auth=HTTPBasicAuth(username, password), headers={'accept': 'application/json'})

                            check = response_data.status_code

                            if check == 200:
                                break
                        
                        if raw_json:
                            raw_json["intervals"] += response_data.json()["intervals"]
                            raw_json["transients"] += response_data.json()["transients"]
                        else:
                            raw_json = response_data.json()

                        save_large_json(response_data.json(), file_data_json_API_temp)

                    # Add transients if they exist
                    trans_dict[adresse]["Transienter"] = raw_json['transients']
                    
                    save_large_json(raw_json, file_data_json_API)
                    
                    if trans_dict[adresse]["Transienter"]:
                        save_json(trans_dict[adresse], file_data_json_transient)
                
                    
                    intervals = raw_json["intervals"]
                    for timestamp in intervals:
                        time_step = timestamp["datetime"]
                        timeseries_dict = timestamp[sensor_id]["intervals"]

                        res = extract_values(timeseries_dict, labels, "V12")

                        data_dict[adresse][time_step] = {
                            'V': float(res["V"]["value"]),
                            'L': float(res["L"]["value"]),
                            'T': float(res["T"]["value"]),
                            'Vfreq': float(res["V"]["frequency"]),
                            'Lfreq': float(res["L"]["frequency"]),
                            'Tfreq': float(res["T"]["frequency"]),
                        }

                    data_dict[adresse] = dict(sorted(data_dict[adresse].items(), key=lambda x: x[0]))

                    save_json(data_dict[adresse], file_data_json)

                    df_temp = pd.DataFrame.from_dict(data_dict[adresse],orient="index")
                    df_temp.to_csv(file_data_asci,sep="\t")

                    for search_id in search_ids:
                        
                        search_delete_url = f"https://cowidk.infralogin.com/api/v1/sensor/{sensor_id}/search/{search_id}/"
                        
                        headers = {
                            "accept": "application/json",
                            "Authorization": f"Bearer {token}"
                        }
                        
                        response = requests.delete(url=search_delete_url, auth=HTTPBasicAuth(username, password), headers=headers)

                        

                else:

                    sensor_id = searches_dict[adresse]["sensor_id"]
                    search_ids = search_json(searches_dict[adresse],"id")
                    search_id = search_ids[0]

                    data_url = "".join(["https://cowidk.infralogin.com", searches_dict[adresse]["data_url"]])
                    
                    response_data = requests.get(url=data_url, auth=HTTPBasicAuth(username, password), headers={'accept': 'application/json'})

                    check = response_data.status_code

                    wait = 0
                    
                    new_id = 0

                    while check != 200:

                        if new_id == 0:
                            wait_limit = 10
                        elif new_id == 1:
                            wait_limit = 25
                        else:
                            wait_limit = 45

                        logger.log(f"{wait}/{wait_limit} sekunder")

                        time.sleep(5)

                        wait += 5

                        if wait > wait_limit:
                            if new_id > 3:
                                QMessageBox.critical(None,"Fejl",f"Der kan ikke laves ID for {adresse}. \n Prøv igen, ellers kontakt Mikkel Houe, MLHU")
                                raise LookupError(f"Cant create search dict for {adresse}, sensor {sensor_id}")
                            
                            logger.log(f"Forsøger at lave nyt ID. {new_id+1}/4",2)

                            project_id_file = os.path.join(cache_main_dir,"API","project.json")
                            dict_temp = load_json(project_id_file)
                            project_id = str(search_json(dict_temp,"project_id")[0])

                            date_to = search_json(searches_dict[adresse], "datetime_to")[0]
                            date_from = search_json(searches_dict[adresse], "datetime_from")[0]

                            #data_url = remake_search_dict(project_id, username, password, sensor_dict[adresse], [search_ids], 
                            #                               cache_main_dir, adresse, date_to = date_to, date_from = date_from)

                            delete_search_id(project_id, sensor_id, adresse, search_id, token, username, password, cache_main_dir)
                            data_url = create_single_search_dict(project_id, sensor_id, username, adresse, password, cache_main_dir, date_to, date_from, create_url = True)

                            wait = 0

                            new_id += 1

                        response_data = requests.get(url=data_url, auth=HTTPBasicAuth(username, password), headers={'accept': 'application/json'})

                        check = response_data.status_code

                        if check == 200:
                            break

                    raw_json = response_data.json()
                    save_json(raw_json, file_data_json_API)
                    
                    trans_dict[adresse]["Transienter"] = raw_json["transients"]
                    
                    intervals = response_data.json()["intervals"]
                    for timestamp in intervals:
                        time_step = timestamp["datetime"]
                        timeseries_dict = timestamp[sensor_id]["intervals"]

                        res = extract_values(timeseries_dict, labels, "C22")

                        data_dict[adresse][time_step] = {
                            'V': float(res["V"]["value"]),
                            'L': float(res["L"]["value"]),
                            'T': float(res["T"]["value"]),
                            'rV': float(res["rV"]["value"]),
                            'rL': float(res["rL"]["value"]),
                            'rT': float(res["rT"]["value"]),
                            'Vfreq': float(res["V"]["frequency"]),
                            'Lfreq': float(res["L"]["frequency"]),
                            'Tfreq': float(res["T"]["frequency"]),
                        }

                    save_json(data_dict[adresse], file_data_json)
                    
                    if trans_dict[adresse]["Transienter"]:
                        save_json(trans_dict[adresse], file_data_json_transient)

                    df_temp = pd.DataFrame.from_dict(data_dict[adresse],orient="index")
                    df_temp.to_csv(file_data_asci,sep="\t")

                    for search_id in search_ids:
                        
                        search_delete_url = f"https://cowidk.infralogin.com/api/v1/sensor/{sensor_id}/search/{search_id}/"
                        
                        headers = {
                            "accept": "application/json",
                            "Authorization": f"Bearer {token}"
                        }
                        
                        response = requests.delete(url=search_delete_url, auth=HTTPBasicAuth(username, password), headers=headers)

        save_json(trans_dict, transient_file)
        
        return trans_dict, sensor_dict

    def gather_waveform_data(username, password, trans_dict, info_dict, cache_main_dir):
        _, token = password.split(":")
        
        trans_dict_with_transients = {adresse: value for adresse, value in trans_dict.items() if trans_dict[adresse] != {}}

        logger.log("Henter transient data for alle målepunkter, hvor der har været transienter",2)
        logger.log(f"Der er {len(trans_dict_with_transients)} målepunkter som behandles")

        for i, adresse in enumerate(trans_dict_with_transients.keys()):
            
            logger.log(f"Henter for {adresse}: {i+1}/{len(trans_dict_with_transients)}")
            

            waveform_path = os.path.join(cache_main_dir, f"{adresse}", "Ascii", "data_waveform")

            os.makedirs(waveform_path, exist_ok=True)

            sensor_id = str(info_dict[adresse]["sensor_id"])
            
            transienter = trans_dict[adresse]["Transienter"]

            trans = search_json(transienter, sensor_id)
            n_trans = len(trans)
            logger.log(f"{adresse} har {n_trans} transienter")
            for i_trans, temp in enumerate(trans):

                urls = search_json(temp, "transient_url")
                timestamp = str(search_json(temp, "timestamp")[0])
                
                waveform_adresse_path = os.path.join(waveform_path, timestamp)

                os.makedirs(waveform_adresse_path, exist_ok=True)

                labels = search_json(temp, "label")
                
                for i, (url, label) in enumerate(zip(urls, labels)):
                    waveform_file = os.path.join(waveform_adresse_path, f"{label}_waveform.dat")
                    if os.path.exists(waveform_file):
                        continue
                    logger.log(f"Henter transient nr. {i_trans+1}/{n_trans} for {adresse}: Retning {label} ({i+1}/3)")
                    transient_url = "".join(["https://cowidk.infralogin.com", url])
            
                    response_data = requests.get(url=transient_url, auth=HTTPBasicAuth(username, password), headers={'accept': 'application/json'})

                    while response_data.status_code != 200:
                        time.sleep(5)

                        response_data = requests.get(url=transient_url, auth=HTTPBasicAuth(username, password), headers={'accept': 'application/json'})

                        if response_data.status_code == 200:
                            break
                    
                    waveform_meta_data = response_data.json()

                    if 'data' in waveform_meta_data.keys():
                        time_values = [(float(k), v) for k, v in waveform_meta_data["data"].items()]
                    elif 'samples_data' in waveform_meta_data.keys():
                        waveform_meta_data['samples_data'] = waveform_meta_data['samples_data'][1:]
                        waveform_meta_data['samples_data'] = waveform_meta_data['samples_data'][:-1] 
                        pattern = re.compile(r'\[([^\]]+)\]')
                        matches = pattern.findall(waveform_meta_data['samples_data'])
                        time_values = []
                        for match in matches:
                            values = [v.strip().strip('"') for v in match.split(',')]

                            values = [float(v) for v in values]
                            time_values.append(values)

                    df = pd.DataFrame(time_values, columns=["time", "value"])

                    df.to_csv(waveform_file, sep="\t", index=False)

    username = "user"
    password = ":".join([credential, token]) 

    project_id = info["project_ID"]

    cache_main_dir = create_dirs(project_id, username, password, info["output_folder"])

    cache_main_dir, answer = check_available_data(cache_main_dir, project_id, username, password, info["output_folder"])
    if answer == "No":
        return cache_main_dir

    sensor_dict = get_sensorlist_in_project(project_id, username, password, cache_main_dir)

    sensor_dict = UI_measuringpoint_information(sensor_dict, cache_main_dir)

    searches_dict = create_search_dict(project_id, username, password, sensor_dict, cache_main_dir)   

    searches_dict = check_INFRA_and_dirData(project_id, username, password, cache_main_dir)

    trans_dict, info_dict = gather_INFRA_data(searches_dict, sensor_dict, username, password, cache_main_dir)

    gather_waveform_data(username, password, trans_dict, info_dict, cache_main_dir)

    create_appendix_dirs(info["output_folder"], trans_dict)

    return cache_main_dir


#credential = "42882"
#token = "141635c7532e819727546481365f4c9448006bd23fbd69d98968f1b7dc07062a"
#project_id = "108790"
#gather_infra_data(credential, token, project_id)