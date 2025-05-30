
def analyse_data(cache_main_dir, reorder=False):
    from basic_functions import search_json
    from basic_functions import load_json
    from basic_functions import save_json
    from basic_functions import calculate_vibration_data
    import os
    from logger import get_logger   
    from numpy import round
    
    logger = get_logger()
    logger.log("Starter analyse af data")

    sensor_dict_file = os.path.join(cache_main_dir, "API", "project_sensor_dict_final.json")
    final_analysis_file_json = os.path.join(cache_main_dir, "Results","max_data.json")

    note_txt_path = os.path.join(cache_main_dir, "Results","max_data_note.txt")
    text_lines = []

    duplicate_MPs = False

    sensor_dict = load_json(sensor_dict_file)

    final_data_dict = {}

    for adresse in sensor_dict.keys():

        sensor_dict_temp = sensor_dict[adresse]
    
        sensor_id = search_json(sensor_dict_temp, "sensor_id")[0]
    
        data_file = os.path.join(cache_main_dir,f"{adresse}","JSON", "data_API.json")

        data_temp = load_json(data_file)

        
        max_vibration = 0

        base_key = adresse.split("_")[0]
        if base_key in final_data_dict.keys():
            duplicate_MPs = True

            max_percentage = final_data_dict[base_key]["percentage"]

            max_data = {"vibration": final_data_dict[base_key]["vibration"], 
                        "percentage": final_data_dict[base_key]["percentage"], 
                        "frequency": final_data_dict[base_key]["frequency"], 
                        "label": final_data_dict[base_key]["label"],
                        "frequency": final_data_dict[base_key]["time"]}
            
            transient = final_data_dict[base_key]["transient"]

            temp_data = {"frequency": final_data_dict[base_key]["frequency"], 
                         "label": final_data_dict[base_key]["label"]}

            text_lines.append(f"Målepunkt '{base_key}' er sammensat med målepunkt '{adresse}' i max_data.json \n")
        else:
            max_percentage = 0

            max_data = {"vibration": None, 
                        "percentage": None, 
                        "frequency": None, 
                        "label": None,
                        "time": None}
            
            transient = False

            temp_data = {"frequency": None, "label": None}  # Temp storage for this section’s data

        for interval in data_temp["intervals"]:
            time_stamp = interval["datetime"]
            for entry in interval[str(sensor_id)]["intervals"]:
                if "19" not in entry['meta_id'] and "18B" not in entry['meta_id']:
                    continue
                if entry["label"] in ["rV", "rT", "rL"]:
                    imidiate_limit  = 3 if entry.get('meta_id')[-2:] == 'Z3' else 5

                    # Convert max value to a float for comparison
                    percentage_value = float(entry.get("max", entry.get("value", 0)))

                    # Convert recorced value to value corresponding to the selected limit of the measring point
                    if imidiate_limit != sensor_dict_temp["limit"]:
                        vibration_unweighed = calculate_vibration_data(float(entry.get("frequency",0)), imidiate_limit, vibration=None, percentage=percentage_value)

                        percentage_value = calculate_vibration_data(float(entry.get("frequency",0)), sensor_dict_temp["limit"], vibration=vibration_unweighed, percentage=None)
                    
                    # If any percentage is above 100, mark transient as True and skip this section
                    if percentage_value > 100:
                        transient = True
                        break
                    # Update if this percentage value is higher than the current max in this section
                    if percentage_value > max_percentage:
                        max_percentage = percentage_value
                        frequency = float(entry.get("frequency",0))

                        temp_data = {
                            "percentage": percentage_value,
                            "frequency": frequency,
                            "label": entry["label"],
                            "time": time_stamp
                        }

                elif entry["label"] in ["V", "T", "L"]:

                    vibration_unweighed = float(entry.get("unweighted", entry.get("value", entry.get("max", 0))))

                    frequency = float(entry.get("frequency",0)) if "frequency" in entry.keys() and entry["frequency"] != None else 0


                    percentage_value = calculate_vibration_data(frequency, sensor_dict_temp["limit"], vibration=vibration_unweighed, percentage=None)
                    
                    if percentage_value > 100:
                        transient = True
                        break

                    if percentage_value > max_percentage:
                        max_percentage = percentage_value
                        max_vibration = sensor_dict_temp["limit"] * percentage_value / 100   
                        
                        temp_data = {
                            "vibration": round(max_vibration, 2),
                            "percentage": percentage_value,
                            "frequency": frequency,
                            "label": entry["label"],
                            "time": time_stamp
                        }



        # Only update global max_data if transient is False and a new max is found in this section

        max_data.update(temp_data)
        if sensor_dict_temp['logger'] != "V12":
            max_data["vibration"] = calculate_vibration_data(max_data["frequency"], sensor_dict_temp["limit"], vibration=None, percentage=max_data["percentage"])

        max_data["transient"] = transient
        

        final_data_dict[base_key] = max_data

    if duplicate_MPs:
        with open(note_txt_path, 'w') as file:
            for line in text_lines:
                file.write(line)

    save_json(final_data_dict, final_analysis_file_json)
    if reorder:
        logger.log("Rækkefølgen af målepunkter er bekræftet.")

    
#cache_main_dir = "O:\\A000000\\A004371\\3_Pdoc\\Afrapportering\\A223276-125 - Chr. Kongsbaks Vej m.fl., Frederikshavn"
#analyse_data(cache_main_dir)

2+2


