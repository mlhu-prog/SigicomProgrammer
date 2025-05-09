import json
import os

def save_json(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def load_json(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)
    return {}

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

        subject=f"Fejl i Kalibrering_v1"
        body = f"User: {user}\n{tb_str}"

        send_error_email(subject, body, full_log, notify_email, smtp_server, smtp_port)

        #logger.error(f"User: {user}\n{tb_str}")
        #logger.exception(
        #    f"User: {user}\nProject ID: {project_id}",
        #    exc_info=(exc_type, exc_value, exc_traceback)
        #)
        
        
        QMessageBox.critical(None, None, f"Der skete en fejl. Der er blevet sendt en besked til {notify_email} med detaljerne.")
    
    sys.excepthook = excepthook