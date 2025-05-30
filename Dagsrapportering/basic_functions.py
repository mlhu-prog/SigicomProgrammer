
def save_json(data, file_path):
    import json
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def load_json(file_path):
    import os
    import json
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)
    return {}
    
def search_json(json_object, search_keyword):
    description_values = []

    if isinstance(json_object, dict):
        for key, value in json_object.items():
            if key == search_keyword:
                description_values.append(value)
            elif isinstance(value, (dict, list)):
                description_values.extend(search_json(value, search_keyword))
    elif isinstance(json_object, list):
        for item in json_object:
            description_values.extend(search_json(item, search_keyword))
    
    return description_values

def project_ID_to_ATR(project_number, credential, token):
    from requests.auth import HTTPBasicAuth
    import requests

    username = "user"
    password = ":".join([credential, token]) 
    
    #API basale URL
    base_url = "https://cowidk.infralogin.com/api/v1"


    response = requests.get(url="/".join([base_url, "project", project_number]), auth=HTTPBasicAuth(username, password), headers={'accept': 'application/json'})

    if response.status_code == 200:
        data = response.json()
        atr = data["project_id"]
        name = data["name"]

        return atr, name

def set_error_handling():
    from PySide6.QtWidgets import QMessageBox
    import getpass
    import traceback
    from logger import get_logger
    from email.message import EmailMessage
    import smtplib
    import sys

    notify_email = "mlhu@cowi.com"

    def send_error_email(subject, body, log_content, notify_email, smtp_server, smtp_port):
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = notify_email
        msg['To'] = notify_email

        # Email body (traceback, user info, etc.)
        msg.set_content(body)

        # Add the log file as attachment
        msg.add_attachment(
            log_content,
            filename='application_log.txt',
            subtype='plain'
        )

        # Send it (no login assumed here, adapt if auth is needed)
        with smtplib.SMTP(smtp_server, smtp_port) as s:
            s.send_message(msg)

    def excepthook(exc_type, exc_value, exc_traceback):
        
        tb_str = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))

        log_window = get_logger()
        log_window.log("Fejl! Forbereder mail til {} med detaljerne".format(notify_email),2,1)
        
        if log_window:
            full_log = log_window.get_log_messages()
        else:
            full_log = "No log messages collected"

        user = getpass.getuser()
        smtp_server = "smtp.cowi.com"
        smtp_port = 25

        subject=f"Fejl i Dagsrapport_4.0"
        body = f"User: {user}\n{tb_str}"

        send_error_email(subject, body, full_log, notify_email, smtp_server, smtp_port)

        #logger.error(f"User: {user}\n{tb_str}")
        #logger.exception(
        #    f"User: {user}\nProject ID: {project_id}",
        #    exc_info=(exc_type, exc_value, exc_traceback)
        #)
        
        
        QMessageBox.critical(None, None, f"Der skete en fejl. Der er blevet sendt en besked til {notify_email} med detaljerne.")
    
    sys.excepthook = excepthook

def safe_float_conversion(value):
    try:
        return float(value)
    except ValueError:
        return value  # Return the original value if it can't be converted

def calculate_weighted_vibration(mms, hz, limit):
    if limit == 3:
        if hz <= 10:
            a = 0
            b = limit
        elif 50 >= hz > 10:
            a = 0.125
            b = 1.75
        else:
            a = 0.04
            b = 6
    elif limit == 5:
        if hz <= 10:
            a = 0
            b = limit
        elif 50 >= hz > 10:
            a = 0.25
            b = 2.5
        else:
            a = 0.1
            b = 10
    
    percent = mms/(a*hz+b) * 100

    return percent

def calculate_vibration_data(frequency, limit, vibration=None, percentage = None):
    import numpy as np
    try:
        frequency = float(frequency)
    except TypeError:
        frequency = 0
    
    frequency = min(frequency, 100)
    
    if percentage == None:
        try:
            vibration = float(vibration)
        except TypeError:
            vibration = 0

        if limit == 3:
            if frequency <= 10:
                per = vibration / limit
            elif 10 < frequency <= 50:
                per = vibration / (1.75 + frequency * 0.125)
            else:
                per = vibration / (6 + frequency * 0.04)
        elif limit == 5:
            if frequency <= 10:
                per = vibration / limit
            elif 10 < frequency <= 50:
                per = vibration / (2.5 + frequency * 0.25)
            else:
                per = vibration / (10 + frequency * 0.1)
        return np.round(per*100, 1)
    else:
        percentage = percentage / 100
        if limit == 3 or limit == 'OFF':
            if frequency <= 10:
                per = percentage * limit
            elif 10 < frequency <= 50:
                per = percentage * (1.75 + frequency * 0.125)
            else:
                per = percentage * (6 + frequency * 0.04)
        elif limit == 5:
            if frequency <= 10:
                per = percentage * limit
            elif 10 < frequency <= 50:
                per = percentage * (2.5 + frequency * 0.25)
            else:
                per = percentage * (10 + frequency * 0.1)
        return np.round(per, 2)

def month_number_to_name(month_number):
    month_names_danish = {
        1: 'januar',
        2: 'februar',
        3: 'marts',
        4: 'april',
        5: 'maj',
        6: 'juni',
        7: 'juli',
        8: 'august',
        9: 'september',
        10: 'oktober',
        11: 'november',
        12: 'december'
    }

    return month_names_danish.get(month_number, "Ukendt måned")  # "Ukendt måned" means "Unknown month" in Danish

def remove_suffix(address):
    return address.split("_")[0]
