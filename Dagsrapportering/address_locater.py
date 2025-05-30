def get_address_by_location(lat, lon, name):
    import pandas as pd
    import os

    from logger import get_logger

    logger = get_logger()
    drive = "O:"
    rest_of_path = os.path.join("A000000", "A004371", "3_Pdoc", "Dagsrapportering", "files","Postnumre_DK.csv")
    postnr_file = os.path.normpath(drive + os.sep + rest_of_path)

    df_postnr = pd.read_csv(postnr_file, sep=";", header=None, names=["Post nr.", "By"])

    import time
    time.sleep(0.5) # Avoid hitting rate limits
    
    import ssl, certifi
    ssl_context = ssl.create_default_context(cafile=certifi.where())

    # Initialize geolocator with the SSL context
    from geopy.geocoders import Nominatim
    geolocator = Nominatim(user_agent="Dagsrapportering_API", ssl_context=ssl_context)
    
    try:
        location = geolocator.reverse(f"{lat}, {lon}")

        postnr = location.raw["address"]["postcode"]

        by = df_postnr.loc[df_postnr['Post nr.'] == int(postnr), 'By'].values[0]

        result_address = postnr + " " + by

        return result_address
    except:
        from manualPostcode_UI import manualPostcode_UI
        from PySide6.QtWidgets import QDialog
        logger.log(f"Kunne ikke finde postnummer for {name}",2)
        logger.log(f"Angiv manuelt postnummer for {name}",2)        
        manualUI = manualPostcode_UI(name)
        res = manualUI.exec()

        if res == QDialog.Accepted:
            return manualUI.get_postcode()

def get_addresses_by_coordinates(lat_list, lon_list, names_list):
    result_addresses = []
    for lat, lon, name in zip(lat_list, lon_list, names_list):
        address = get_address_by_location(lat, lon, name)
        result_addresses.append(address)
    return result_addresses