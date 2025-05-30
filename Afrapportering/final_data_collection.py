

def final_project_data_collection(cache_main_dir, collected_data, gather_data=True):
    import os
    from basic_functions import load_json, save_json
    from datetime import datetime

    trans_dict_path = os.path.join(cache_main_dir, "Results","trans_dict.json")
    info_dict_path = os.path.join(cache_main_dir, "API","project_sensor_dict_final.json")

    # Sample input dictionary
    data = load_json(info_dict_path)

    # Initialize variables to hold min and max dates
    min_date_from = None
    max_date_to = None

    # Iterate over the entries in the dictionary
    for adresse, details in data.items():
        # Parse date_from and date_to into datetime objects
        date_from = datetime.strptime(details["date_from"], "%Y-%m-%d %H:%M")
        date_to = datetime.strptime(details["date_to"], "%Y-%m-%d %H:%M")

        # Update min_date_from
        if min_date_from is None or date_from < min_date_from:
            min_date_from = date_from

        # Update max_date_to
        if max_date_to is None or date_to > max_date_to:
            max_date_to = date_to


    # Create collected_data dictionary to store the results
    collected_data["date_from"] =  min_date_from.strftime("%d.%m.%Y") if min_date_from else None
    collected_data["date_to"] = max_date_to.strftime("%d.%m.%Y") if max_date_to else None

    save_json(collected_data, os.path.join("O:\\A000000\\A004371\\3_Pdoc\\Afrapportering\\files\\saved_projects\\{}.json".format(collected_data["project_ID"])))

    return collected_data

#cache_main_dir = "O:\\A000000\\A004371\\3_Pdoc\\Afrapportering\\A223276-087 - Hadsundvej Syd, Gistrup"
#collected_data = load_json("JSON\\collected_data_hadsund.json")

#final_project_data_collection(cache_main_dir, collected_data)