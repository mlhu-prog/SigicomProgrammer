## Endelig tabel af målepunkter

import os
import pandas as pd
from datetime import datetime

#Project imports
from logger import get_logger
from basic_functions import safe_float_conversion

def build_active_rows(cache_main_dir, cache_date, data_dict, info_dict):
    """
    Build result rows for active sensors.
    """
    logger = get_logger()
    result_rows = []
    n_adresser = len(data_dict)

    subfolders = [f.name for f in os.scandir(os.path.join(cache_main_dir,"Results")) if f.is_dir()]
    date_folders = []

    for folder in subfolders:
        try:
            date = datetime.strptime(folder, "%Y-&m-%d")
            date_folders.append((date, folder))
        except ValueError:
            continue
    
    previous_results = False

    if date_folders:
        latest_folder = max(date_folders, key=lambda x: x[0])[0]
        newest_result_file = os.path.join(cache_main_dir, "Results", latest_folder, "final_tabel.dat")
        df_latest = pd.read_csv(newest_result_file, sep="\t")
        previous_results = True


    for i, adresse in enumerate(data_dict):
        logger.log(f"Behandler {adresse}: {i+1}/{n_adresser}")
        dict_temp = info_dict.get(adresse, {})
        limit = 3 if dict_temp.get("Ziele", 3) == "OFF" else dict_temp.get("Ziele", 3)
        max_vib_per = max_vib_mms = "-"  # Defaults if no data found
        day_vib_mms = day_vib_per = tidspunkt_max = freq_max = "-"
        cache_path = os.path.join(cache_main_dir, adresse)
        # Defensive: skip if sensor directory doesn't exist
        if not os.path.exists(cache_path):
            continue


        date_path = os.path.join(cache_path, cache_date, "Ascii", "data_resultat.dat")
        if not os.path.isfile(date_path):
            continue

        try:
            df = pd.read_csv(date_path, sep="\t", index_col=0)
        except Exception:
            continue

        if df.iloc[0]["Tidspunkt"] == "Ingen data":
            continue  # ignore dates with "no data"

        vib_per = df.iloc[0]["Maks vib. [%]"]
        vib_mms = df.iloc[0]["Maks vib. [mm/s]"]
        tidspunkt = df.iloc[0]["Tidspunkt"]
        vib_freq = df.iloc[0]["Tilsvarende frekvens [Hz]"]

        if previous_results:
            if adresse in list(df_latest["Adresse"]):
                max_vib_per = df_latest.loc[df_latest["Adresse"] == adresse, "Maks vib. [%]"].values[0]
                max_vib_mms = df_latest.loc[df_latest["Adresse"] == adresse, "Maks vib. [mm/s]"].values[0]
                tidspunkt_max = df_latest.loc[df_latest["Adresse"] == adresse, "Tidspunkt max vib."].values[0]
                freq_max = df_latest.loc[df_latest["Adresse"] == adresse, "Tilsvarende frekvens"].values[0]

        # For current date's data:
        day_vib_mms = round(safe_float_conversion(vib_mms), 1) if vib_mms != "-" else "-"
        day_vib_per = round(safe_float_conversion(vib_per), 1) if vib_per != "-" else "-"

        if vib_per != "-" and (max_vib_per == "-" or safe_float_conversion(vib_per) > safe_float_conversion(max_vib_per)):
            max_vib_per = round(safe_float_conversion(vib_per), 1)
            max_vib_mms = round(safe_float_conversion(vib_mms), 1)
            tidspunkt_max = tidspunkt
            freq_max = vib_freq
        elif vib_mms != "-" and (max_vib_mms == "-" or safe_float_conversion(vib_mms) > safe_float_conversion(max_vib_mms)):
            max_vib_mms = round(safe_float_conversion(vib_mms), 1)
            max_vib_per = "-"
            tidspunkt_max = tidspunkt
            freq_max = "-"

        row = {
            "Adresse": adresse,
            "Postnummer": dict_temp.get("postcode", "-"),
            "Grænse værdi": limit,
            "Logger": dict_temp.get("logger", "-"),
            "Sensor": dict_temp.get("sensor_id", "-"),
            "Dato, opsat": dict_temp.get("date_from", "-").split(' ')[0] if dict_temp.get("date_from") else "-",
            "Maks vib. [mm/s]": max_vib_mms,
            "Maks vib. [%]": max_vib_per,
            "Vib. [mm/s]": day_vib_mms,
            "Vib. [%]": day_vib_per,
            "Tidspunkt max vib.": tidspunkt_max,
            "Tilsvarende frekvens": freq_max
        }
        result_rows.append(row)

    return result_rows

def build_inactive_rows(cache_main_dir, cache_date, inactive_sensor_dict):
    """
    Build result rows for inactive sensors.
    """
    logger = get_logger()
    result_rows = []
    n_adresser = len(inactive_sensor_dict)
    for i, adresse in enumerate(inactive_sensor_dict):
        logger.log(f"Behandler {adresse}: {i+1}/{n_adresser}")
        dict_temp = inactive_sensor_dict[adresse]
        date_down = dict_temp["date_to"].split(" ")[0]
        main_dir = os.path.join(cache_main_dir, adresse)
        if not os.path.isdir(main_dir):
            continue

        # Find the newest result folder
        date_folders = []
        for f in os.listdir(main_dir):
            try:
                test_date = datetime.strptime(f, '%Y-%m-%d')
                date_folders.append((test_date, f))
            except Exception:
                continue
        if not date_folders:
            continue
        latest_folder = max(date_folders, key=lambda x: x[0])[1]
        result_file = os.path.join(cache_main_dir, "Results", latest_folder, "final_table.dat")
        if not os.path.isfile(result_file):
            continue
        try:
            df = pd.read_csv(result_file, sep="\t")
            df = df[df["Adresse"] == adresse]
        except Exception:
            continue
        if df.empty:
            continue
        row = {
            "Adresse": adresse,
            "Postnummer": df.iloc[0].get("Postnummer", "-"),
            "Grænse værdi": df.iloc[0].get("Grænse værdi", "-"),
            "Logger": df.iloc[0].get("Logger", "-"),
            "Sensor": df.iloc[0].get("Sensor", "-"),
            "Dato, opsat": df.iloc[0].get("Dato, opsat", "-"),
            "Dato, nedtaget": date_down,
            "Maks vib. [mm/s]": df.iloc[0].get("Maks vib. [mm/s]", "-"),
            "Maks vib. [%]": df.iloc[0].get("Maks vib. [%]", "-"),
            "Tidspunkt max vib.": df.iloc[0].get("Tidspunkt max vib.", "-"),
            "Tilsvarende frekvens": df.iloc[0].get("Tilsvarende frekvens", "-")
        }
        result_rows.append(row)
    return result_rows

def table_creater(cache_main_dir, cache_date, data_dict, info_dict, inactive_sensor_dict):
    """
    Create a table for active and inactive sensors.
    """
    logger = get_logger()
    result_dir = os.path.join(cache_main_dir, "Results", cache_date)
    os.makedirs(result_dir, exist_ok=True)
    result_file = os.path.join(result_dir, "final_table.dat")

    logger.log("Danner endelig tabel for aktive og inaktive målepunkter", 2)

    # Active sensors
    active_rows = build_active_rows(cache_main_dir, cache_date, data_dict, info_dict)
    active_final_df = pd.DataFrame(active_rows)
    # Apply safe_float_conversion, except for specific columns
    not_include_columns = ["Grænse værdi", "Sensor"]
    for col in active_final_df.columns:
        if col not in not_include_columns:
            active_final_df[col] = active_final_df[col].apply(safe_float_conversion)
    active_final_df.to_csv(result_file, sep="\t", index=False)

    # Inactive sensors
    inactive_final_df = pd.DataFrame(columns=["Adresse" ,"Postnummer", "Grænse værdi", "Logger", "Sensor", "Dato, opsat", "Dato, nedtaget",
                                    "Maks vib. [mm/s]", "Maks vib. [%]","Tidspunkt max vib.", 
                                    "Tilsvarende frekvens"])
    inactive_rows = build_inactive_rows(cache_main_dir, cache_date, inactive_sensor_dict)
    if inactive_rows:
        inactive_final_df = pd.DataFrame(inactive_rows)
        
    for col in inactive_final_df.columns:
        if col not in not_include_columns:
            inactive_final_df[col] = inactive_final_df[col].apply(safe_float_conversion)


    active_final_df = active_final_df.sort_values(by=['Postnummer', 'Adresse'])
    inactive_final_df = inactive_final_df.sort_values(by=['Postnummer', 'Adresse'])


    return active_final_df, inactive_final_df




