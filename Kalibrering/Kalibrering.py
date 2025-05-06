import os
from requests.auth import HTTPBasicAuth
import tkinter as tk
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.platypus import BaseDocTemplate, Table, TableStyle, Paragraph, Spacer, Frame, PageTemplate
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import tempfile
import json
import requests

drive = "O:"
files_path = os.path.join("A000000", "A004371", "3_Pdoc", "Afrapportering", "files")
logo_path = os.path.join(files_path,"Logo_no_background.png")

files_path = os.path.join("A000000", "A004371", "3_Pdoc")
ownership_path = os.path.join(files_path, "Måleinstrumenter_og_Kontorer.xlsx")

page_width, page_height = A4  # Page dimensions

logo_img = os.path.normpath(drive + os.sep + logo_path)
ownership_path = os.path.normpath(drive + os.sep + ownership_path)

logo_width = 4 * cm  # Width of the logo
logo_height = 1.5 * cm  # Height of the logo

def save_json(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def load_json(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)
    return {}

def load_ownership_data(file_path):
    import pandas as pd
    df = pd.read_excel(file_path, sheet_name="Sheet1")  # Change "Sheet1" if necessary
    ownership_dict = df.set_index("ID")["Ejer"].to_dict()  # Assuming Excel columns are "ID" and "Owner"
    return ownership_dict

def fetch_sensor_info(sensor_ids, base_url, auth, years):
    import requests, time
    from datetime import datetime, timedelta
    today = datetime.today()
    sensor_info = {}


    dir_name = f"{today.day}_{today.month}_{today.year}"
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
        
    filename = f"sensor_info.json"

    file_out = os.path.join(dir_name, filename)


    for idx, sensor_id in enumerate(sensor_ids):
        print(f"{idx+1}:{len(sensor_ids)}")
        url = f"{base_url}/{sensor_id}"
        response = requests.get(url=url, auth=auth, headers={'accept': 'application/json'})
        
        # Retry logic
        wait_time = 0
        while response.status_code != 200:
            print(f"Waiting time: {wait_time + 5}")
            time.sleep(5)
            wait_time += 5
            response = requests.get(url=url, auth=auth, headers={'accept': 'application/json'})
        
        data_temp = response.json()
        
        last_time_read = data_temp.get("timestamp_last_read",1)
        last_time_read = datetime.fromtimestamp(last_time_read).strftime("%Y-%m-%d %H:%M")
        
        cali_date_str = data_temp.get("calibration_date", "ukendt")

        if cali_date_str == None:
            cali_date_str = "ukendt"
        
        try:
            cali_date = datetime.strptime(cali_date_str, "%Y-%m-%d")

            cali_status = "OK" if today - cali_date < timedelta(days=365*years) else "IKKE OK"
        except:
            cali_status = "Ukendt"

        sensor_info[sensor_id] = {"Type": data_temp.get("type", "ukendt"), "Status": data_temp.get("state","ukendt"), "Sidste data hentet": last_time_read, 
                                "Kalibreringsdato": cali_date_str, "Kalibreringsstatus": cali_status}
    
    save_json(sensor_info, file_out)
    
    return sensor_info, dir_name

def combine_data_with_ownership(sensor_info, ownership_dict):

    for sensor_id, date in sensor_info.items():
        owner = ownership_dict.get(int(sensor_id), "Ukendt")
        sensor_info[sensor_id]["Ejer"] = owner

    return sensor_info

def create_pdf(sensor_data, pdf_output, years):
    from tkinter import messagebox
    from datetime import datetime
    styles = getSampleStyleSheet()

    bold_text = styles["Normal"].clone('bold_text_style')
    bold_text.fontName = "Times-Bold"
    bold_text.fontSize = 12
    
    with tempfile.TemporaryDirectory() as tmpdirname:
        
        def add_logo(canvas, doc):
            if doc.page == 1:
                # Save the state of the canvas
                canvas.saveState()

                # Calculate X and Y position for the logo
                x_position = page_width - pdf.rightMargin - logo_width  # Align to the right margin
                y_position = page_height - pdf.topMargin - logo_height  # Align to the top margin

                # Draw the logo
                canvas.drawImage(logo_img, x_position, y_position, width=logo_width, height=logo_height, mask='auto')

                # Restore the state of the canvas
                canvas.restoreState()

        temp_file_path = os.path.join(tmpdirname, "temp_file.pdf")
        pdf = BaseDocTemplate(temp_file_path, pagesize=A4)

        # Define a Frame for the PageTemplate
        frame = Frame(pdf.leftMargin, pdf.bottomMargin, pdf.width, pdf.height - 2 * cm, id='normal')

        # Add the PageTemplate to the document
        pdf.addPageTemplates([PageTemplate(id='header_template', frames=frame, onPage=add_logo)])

        # Prepare table data
        table_data = [
            ['Type', 'ID', 'Sidste Kalibreringsdato', 'Kalibreringsstatus', 'Status', 'Sidste data hentet d.', 'Ejer']
        ]

        elements = []
        elements.append(Paragraph(f"Dato: {datetime.today().strftime('%Y-%m-%d')}. Kalibreringsstatus er baseret på en periode på {years} år.", bold_text))
        elements.append(Spacer(0,6))

        
        sorted_data = sorted(
            sensor_data.items(),
            key=lambda x: (
                x[1]["Ejer"],
                x[1]["Type"],
                datetime.strptime(x[1]["Kalibreringsdato"], "%Y-%m-%d") 
                if x[1]["Kalibreringsdato"] != "ukendt" else datetime.min  # Set "unknown" to a default date
            )
        )

        # Add data rows from the combined_data dictionary
        for key, data in sorted_data:
            row = [
                data["Type"],
                key,
                data['Kalibreringsdato'],  # Kalibreringsdato
                data['Kalibreringsstatus'],  # Kalibreringsstatus
                data['Status'],  # Status
                data['Sidste data hentet'],
                data['Ejer']  # Ejer
            ]
            table_data.append(row)

        # Create the table
        table = Table(table_data)

        # Set style for the table
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Header row background color
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # Header row text color
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center align all cells
            ('FONTNAME', (0, 0), (-1, 0), 'Times-Bold'),  # Bold header
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Padding for header
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),  # Data rows background color
            ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Gridlines
        ])

        # Apply the style
        table.setStyle(style)


        c = canvas.Canvas(temp_file_path, pagesize=A4)

        # Add the image to the top-right corner (adjust the coordinates as needed)

        # Coordinates for the top-right corner (adjust accordingly)
        c.drawImage(logo_img, page_width - 0.99 * cm - logo_width, page_height - 2.5 * cm, width=logo_width, height=logo_height, mask='auto')

        # Build the document with the table
        elements.append(table)
        pdf.build(elements)
        
        # Ensure the destination directory exists
        if os.name == 'nt':
            pdf_output = f'\\\\?\\{os.path.abspath(pdf_output)}'
        
        os.makedirs(os.path.dirname(pdf_output), exist_ok=True)
        
        # Use os.rename to move the temporary PDF to the final path and rename it
        try:
            if os.path.exists(pdf_output):
                os.remove(pdf_output)

            os.rename(temp_file_path, pdf_output)
        except PermissionError:
            messagebox.showerror("Fejl", f"{pdf_output} er allerede åben. Luk filen og prøv igen.")
            raise PermissionError("Filen kan ikke laves, da den allerede er åben. Luk filen og prøv igen.")
        
def initial_login_window():
    from PIL import Image, ImageTk
    drive = "O:"
    # Determine the path to save credentials based on the operating system
    def get_credentials_file_path():
        home_dir = os.path.expanduser("~")
        if os.name == 'nt':  # Windows
            app_data_dir = os.getenv('APPDATA', home_dir)
            credentials_dir = os.path.join(app_data_dir, 'Sigicom Dagsrapportering')
        else:  # Unix-like systems
            credentials_dir = os.path.join(home_dir, '.Sigicom Dagsrapportering')

        # Create the directory if it doesn't exist
        os.makedirs(credentials_dir, exist_ok=True)
        
        return os.path.join(credentials_dir, 'credentials.txt')

    # Function to save credentials
    def save_credentials(credentials, token):
        with open(credentials_file, 'w') as file:
            file.write(f"{credentials}\n{token}")

    # Validate crecentials and proceed if correct
    def validate_and_proceed():
        
        from tkinter import messagebox
        global credentials, token
        # Get credentials and token from the entries
        credentials = credentials_entry.get()
        token = password_entry.get()

        # Basic validation
        if not credentials or not token:
            messagebox.showerror("Error", "Please enter both credentials and token.")
            return

        # Handle Update Credentials checkbox
        if update_credentials_var.get():
            if os.path.exists(credentials_file):

                os.remove(credentials_file)

                save_credentials(credentials, token)

        # Save credentials to file if checkbox is selected
        if save_credentials_var.get():
            save_credentials(credentials, token)

        # Close the login window
        login_window.quit()
        login_window.destroy()

        return credentials, token

    # Function to load saved credentials from file
    def load_saved_credentials():
        if os.path.exists(credentials_file):
            with open(credentials_file, 'r') as file:
                lines = file.readlines()
                if len(lines) >= 2:
                    return lines[0].strip(), lines[1].strip()
        return None, None

    # Path to save/load credentials
    credentials_file = get_credentials_file_path()
    # Initial login window
    login_window = tk.Tk()
    login_window.title("Login")
    login_window.geometry("250x340")


    # Load saved credentials if available
    saved_credentials, saved_token = load_saved_credentials()

    # Credentials label and entry
    credentials_label = tk.Label(login_window, text="Credentials:")
    credentials_label.pack(pady=5)
    credentials_entry = tk.Entry(login_window, show="*", justify= "center")
    credentials_entry.pack(pady=5)
    if saved_credentials:
        credentials_entry.insert(0, saved_credentials)

    # Password label and entry
    password_label = tk.Label(login_window, text="Token:")
    password_label.pack(pady=5)
    password_entry = tk.Entry(login_window, show="*", justify= "center")
    password_entry.pack(pady=5)
    if saved_token:
        password_entry.insert(0, saved_token)

    # Checkbox to save credentials
    save_credentials_var = tk.BooleanVar()
    save_credentials_checkbox = tk.Checkbutton(login_window, text="Gem credentials", variable=save_credentials_var)
    save_credentials_checkbox.pack(pady=5)

    # Checkbox to update credentials
    update_credentials_var = tk.BooleanVar()
    update_credentials_checkbox = tk.Checkbutton(login_window, text="Opdater credentials", variable=update_credentials_var)
    update_credentials_checkbox.pack(pady=5)

    # Login button
    login_button = tk.Button(login_window, text="Login", command=validate_and_proceed)
    login_button.pack(pady=20)

    # Hyperlink label
    def open_hyperlink(event):
        import webbrowser
        webbrowser.open("https://cowidk.infralogin.com/api/v1/user/0/token")  # Replace with your desired URL

    hyperlink = tk.Label(login_window, text="Hent Credential og Token her", fg="blue", cursor="hand2")
    hyperlink.pack(pady=10)
    hyperlink.bind("<Button-1>", open_hyperlink)

    # Load and resize the logo image
    rest_of_path = os.path.join("A000000", "A004371", "3_Pdoc", "Afrapportering", "files", "Logo_no_background.png")
    image_logo = os.path.normpath(drive + os.sep + rest_of_path)

    logo_original = Image.open(image_logo)
    logo_resized = logo_original.resize((76, 28), Image.Resampling.LANCZOS)
    logo_image = ImageTk.PhotoImage(logo_resized)

    # Create a frame for the logo at the bottom right
    logo_frame = tk.Frame(login_window)
    logo_frame.pack(side=tk.BOTTOM, anchor=tk.SE, padx=5, pady=5)

    # Add the logo to the frame
    logo_label = tk.Label(logo_frame, image=logo_image)
    logo_label.pack()

    # Start the login window
    login_window.mainloop()

    return credentials, token


credentials, token = initial_login_window()

username = "user"
password = ":".join([credentials, token]) 
base_url = "https://cowidk.infralogin.com/api/v1/sensor"
auth = HTTPBasicAuth(username, password)


# Laver request til Sigicom API server
response = requests.get(url=base_url, auth=auth, headers={'accept': 'application/json'})
data = response.json()
data = [sensor for sensor in data if sensor["type"] == "C22" or sensor["type"] == "V12"]
sensor_ids = [entry["serial"] for entry in data]

years = 2

sensor_info, dir_name = fetch_sensor_info(sensor_ids, base_url, auth, years)

ownership_dict = load_ownership_data(ownership_path)

combined_data = combine_data_with_ownership(sensor_info, ownership_dict)

sensor_expired = {key: data for key, data in combined_data.items() if data["Kalibreringsstatus"] == "IKKE OK"}

#pd.DataFrame.from_dict(combined_data, orient='index').to_excel("sensor_list.xlsx")

pdf_output_expired = os.path.join("..\\Kalibreringsstatus", dir_name, "Kalibreringsstatus_IKKE_OK.pdf")
pdf_output_all = os.path.join("..\\Kalibreringsstatus", dir_name, "Kalibreringsstatus.pdf")

create_pdf(sensor_expired, pdf_output_expired, years)
create_pdf(combined_data, pdf_output_all, years)



os.startfile(pdf_output_expired)
os.startfile(pdf_output_all)


print("DONE!")