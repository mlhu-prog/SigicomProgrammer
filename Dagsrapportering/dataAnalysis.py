## Analyse af data

import os
import gc
import pandas as pd

#Project imports
from logger import get_logger
from basic_functions import calculate_vibration_data


def get_corresponding_values(row):
    import pandas as pd
    import numpy as np

    if row['max_r_column'] == 'rV':
        try:
            return pd.Series([row['rVfreq']], index=['Hz'])
        except:
            return pd.Series([row['Vfreq']], index=['Hz'])
    elif row['max_r_column'] == 'rL':
        try:
            return pd.Series([row['rLfreq']], index=['Hz'])
        except:
            return pd.Series([row['Lfreq']], index=['Hz'])
    elif row['max_r_column'] == 'rT':
        try:
            return pd.Series([row['rTfreq']], index=['Hz'])
        except:
            return pd.Series([row['Tfreq']], index=['Hz'])
    
    elif row['max_r_column'] == 'V':
        return pd.Series([row['Vfreq']], index=['Hz'])
    elif row['max_r_column'] == 'L':
        return pd.Series([row['Lfreq']], index=['Hz'])
    elif row['max_r_column'] == 'T':
        return pd.Series([row['Tfreq']], index=['Hz'])
    else:
        return pd.Series(np.nan, index='Hz')

def dataAnalysis(cache_main_dir, cache_date, data_dict, info_dict):
    logger = get_logger()

    logger.log("Analyserer data fra aktive målepunkter", 2, 2)
    # Find maksimal vibrationsniveau for den pågældende dag for hver sensor.
    n_adresser = len(data_dict)

    for i, adresse in enumerate(data_dict.keys()):
        
        logger.log(f"Behandler {adresse}: {i+1}/{n_adresser}")

        result_dict = {}
        log = info_dict[adresse]["logger"]
        limit_value = info_dict[adresse]["Ziele"]
        result_file = os.path.join(cache_main_dir, f'{adresse}',cache_date,'Ascii',f'data_flagged.dat') 
        result_end_file = result_file.replace('flagged.dat','resultat.dat')

        df_temp = pd.read_csv(result_file, sep="\t",index_col=0)

        if df_temp.empty:
            result_dict[adresse] = {"Tidspunkt": "Ingen data",
                                    "Maks vib. [mm/s]": "-",
                                    "Maks vib. [%]": "-",
                                    "Tilsvarende frekvens [Hz]": "-"}
        else:

            df_temp = df_temp[~df_temp["Flag"].isin([1, 2])]

            if log != "V12":
                if limit_value == "OFF":
                    df_temp["max_vib"] = df_temp[["V","L","T"]].max(axis=1)
                    df_temp['max_r_column'] = df_temp[['V', 'L', 'T']].idxmax(axis=1)

                    df_temp["Hz"] = df_temp.apply(get_corresponding_values,axis=1)

                    max_row = df_temp.loc[df_temp["max_vib"].idxmax()]

                    highest_value = calculate_vibration_data(max_row["Hz"], 3, vibration=max_row["max_vib"])
                else:
                    df_temp["max_vib_per"] = df_temp[["rV","rL","rT"]].max(axis=1)
                    df_temp['max_r_column'] = df_temp[['rV', 'rL', 'rT']].idxmax(axis=1)

                    df_temp["Hz"] = df_temp.apply(get_corresponding_values,axis=1)

                    max_row = df_temp.loc[df_temp["max_vib_per"].idxmax()]

                    highest_value = max_row['max_vib_per']

                time_for_max = max_row.name
                corresponding_m_s = calculate_vibration_data(max_row["Hz"], limit_value, vibration=None, percentage=highest_value)
                corresponding_hz = max_row['Hz']
            else:
                df_temp["max_vib"] = df_temp[["V","L","T"]].max(axis=1)
                df_temp['max_r_column'] = df_temp[['V', 'L', 'T']].idxmax(axis=1)

                df_temp["Hz"] = df_temp.apply(get_corresponding_values,axis=1)

                max_row = df_temp.loc[df_temp["max_vib"].idxmax()]

                if limit_value == "OFF":
                    percent = 3 / max_row["max_vib"] * 100
                    corresponding_m_s = calculate_vibration_data(max_row["Hz"], 3, vibration=None, percentage=percent)
                else:
                    percent = int(limit_value) / max_row["max_vib"] * 100
                    corresponding_m_s = calculate_vibration_data(max_row["Hz"], int(limit_value), vibration=None, percentage=percent)

                time_for_max = max_row.name
                corresponding_hz = max_row['Hz']
                highest_value = "-"

            result_dict[adresse] = {"Tidspunkt": time_for_max,
                                    "Maks vib. [mm/s]": corresponding_m_s,
                                    "Maks vib. [%]": highest_value,
                                    "Tilsvarende frekvens [Hz]": corresponding_hz}


        # Eksporter resultaterne (maks vib. [mm/s], maks vib. [%]) i en seperat ascii fil. 
        # Navngiv ascii-filen datoen og projekt-ID.  
        
        df_temp = pd.DataFrame.from_dict(result_dict,orient="index")
        df_temp.to_csv(result_end_file, sep="\t")

        del df_temp
        gc.collect()
        