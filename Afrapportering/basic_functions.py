
def update_row(row):
    return row+1

def save_json(data, file_path):
    import json
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def save_large_json(data, file_path):
    import orjson
    with open(file_path, 'wb') as file:
        file.write(orjson.dumps(data))

def load_json(file_path):
    import json
    import os
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)
    else:
        raise FileNotFoundError(f"No such file or directory '{file_path}'")
    
def load_large_json(file_path):
    import os
    import orjson
    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            return orjson.loads(file.read())
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
    import requests
    from requests.auth import HTTPBasicAuth

    username = "user"
    password = ":".join([credential, token]) 
    
    #API basale URL
    base_url = "https://cowidk.infralogin.com/api/v1"


    response = requests.get(url="/".join([base_url, "project", project_number]), auth=HTTPBasicAuth(username, password), headers={'accept': 'application/json'})
    
    if response.status_code == 200:
        data = response.json()
        atr = data["project_id"]
        name = data["name"]
        customer = data["customer_company"] if data["customer_company"] else ""

        return atr, name, customer

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
        if limit == 3:
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

def yes_no_cancel_operation(title, label):
    import sys
    from PySide6.QtCore import Qt
    from PySide6.QtWidgets import QApplication, QDialog, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox
    class YesNoCancelDialog(QDialog):
        def __init__(self, title, label):
            super().__init__()
            self.setWindowTitle(title)
            self.setFixedSize(260, 125)
            
            self.answer = None
            
            layout = QVBoxLayout()
            
            self.label = QLabel(label)
            self.label.setAlignment(Qt.AlignCenter)
            layout.addWidget(self.label)
            
            button_layout = QHBoxLayout()
            
            self.yes_button = QPushButton("Ja")
            self.yes_button.clicked.connect(self.on_yes)
            button_layout.addWidget(self.yes_button)
            
            self.no_button = QPushButton("Nej")
            self.no_button.clicked.connect(self.on_no)
            button_layout.addWidget(self.no_button)
            
            self.cancel_button = QPushButton("Afbryd")
            self.cancel_button.clicked.connect(self.on_cancel)
            button_layout.addWidget(self.cancel_button)
            
            layout.addLayout(button_layout)
            self.setLayout(layout)
        
        def on_yes(self):
            self.answer = "Yes"
            self.accept()
        
        def on_no(self):
            self.answer = "No"
            self.accept()
        
        def on_cancel(self):
            self.reject()
            sys.exit()  # Terminates the script immediately
    
    app = QApplication.instance() or QApplication(sys.argv)
    dialog = YesNoCancelDialog(title, label)
    dialog.exec()
    return dialog.answer

def weekday_danish(weekday_index):
    weekday = ["Mandag", "Tirsdag","Onsdag","Torsdag","Fredag","Lørdag","Søndag"]

    try:
        return weekday[weekday_index]
    except:
        return "Unknown"
    
def month_danish(month_number):
    month = ["januar", "februar","marts","april","maj","juni","juli","august","september","oktorber","november","december"]

    try:
        return month[month_number-1]
    except:
        return "Unknown"

def remove_all_files(folder_path):
    import os
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            if os.path.isfile(file_path):  # Ensure it's a file
                os.remove(file_path)


def remove_duplicate_entries(dict_list):
    seen = set()
    unique_list = []

    for entry in dict_list:
        # Create a tuple of (timestamp, datetime) for each entry
        identifier = (entry['timestamp'], entry['datetime'])

        # If the tuple is not already in the seen set, add the dictionary to unique_list
        if identifier not in seen:
            seen.add(identifier)
            unique_list.append(entry)

    return unique_list

def set_error_handling():
    from PySide6.QtWidgets import QMessageBox
    import getpass
    from tkinter import Tk
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

        subject=f"Fejl i Afrapportering_v3"
        body = f"User: {user}\n{tb_str}"

        send_error_email(subject, body, full_log, notify_email, smtp_server, smtp_port)

        #logger.error(f"User: {user}\n{tb_str}")
        #logger.exception(
        #    f"User: {user}\nProject ID: {project_id}",
        #    exc_info=(exc_type, exc_value, exc_traceback)
        #)
        
        
        QMessageBox.critical(None, None, f"Der skete en fejl. Der er blevet sendt en besked til {notify_email} med detaljerne.")
    
    sys.excepthook = excepthook
