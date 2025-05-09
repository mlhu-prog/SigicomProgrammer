from logger import init_logger

from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox, QSplashScreen
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import * 
from PySide6.QtGui import * 
from PySide6.QtCore import Qt

import os

from basic_functions import set_error_handling

class NavigationApp(QWidget):
    def __init__(self):
        super().__init__()
        self.credential = None
        self.token = None

        self.output_dir = None

        self.logger = init_logger()
        self.logger.log("Starter Kalibreringsprogram - version 1.0", 2)
        self.logger.log("Se status i bunden af dette log-vindue (klar/arbejder)",1,1)
        self.logger.show()

        self.initial_settings()

        self.initUI()
        
        self.logger.log("Klar...",1,1)

    def initial_settings(self):
        from datetime import datetime

        self.drive = "O:"

        self.files_path = os.path.join("A000000", "A004371", "3_Pdoc", "Afrapportering")
        self.logo_path = os.path.join(self.files_path, "files", "Logo_no_background.png")
        self.ownership_path = os.path.join(self.files_path, "..", "Måleinstrumenter_og_kontorer.xlsx")

        self.logo_img = os.path.normpath(drive + os.sep + self.logo_path)
        
        self.ownership_path = os.path.normpath(self.drive + os.sep + self.ownership_path)

        self.today = datetime.today()
        self.filename = f"Kalibrering_{self.today.strftime('%Y_%m_%d')}.pdf"
        self.filename_expired = f"Kalibrering_{self.today.strftime('%Y_%m_%d')}_IKKE_OK.pdf"
        
    def initUI(self):

        self.setWindowTitle('Kalibrering')
        self.setGeometry(100, 100, 300, 250)

        layout = QVBoxLayout()

        # Add labels for project_atr and project_name
        layout.setSpacing(25)
        self.project_atr_label = QLabel('ATR:', self)
        self.project_atr_label.setFont(QFont('Arial', 10, QFont.Bold))
        self.project_atr_label.setAlignment(Qt.AlignCenter)
        self.project_atr_label.setText(f'Kalibrering')
        layout.addWidget(self.project_atr_label)

        self.buttons = {}

        self.buttons['login'] = QPushButton('Login', self)
        self.buttons['login'].clicked.connect(self.login_function)
        layout.addWidget(self.buttons['login'])

        self.buttons['collect_data'] = QPushButton('Outputsti og Hent status', self)
        self.buttons['collect_data'].setEnabled(False)
        self.buttons['collect_data'].clicked.connect(self.collect_data)
        layout.addWidget(self.buttons['collect_data'])

        img = QLabel()
        pixmap = QPixmap(self.logo_img)

        desired_width = 100  # change this to your desired width
        desired_height = 100  # change this to your desired height

        # Scale the pixmap
        scaled_pixmap = pixmap.scaled(desired_width, desired_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        img.setPixmap(scaled_pixmap)
        img.setAlignment(Qt.AlignCenter)
        #img.setPixmap(pixmap)
        layout.addWidget(img)

        self.setLayout(layout)

    def login_function(self):
        from scriptUI import loginWindow
        self.logger.log("Åbner login-vindue",2,2)
        self.login_window = loginWindow()
        res = self.login_window.exec()

        if res == QDialog.Accepted:
            self.credential, self.token = self.login_window.get_login()
            self.logger.log(f"Bruger er logget ind.",status=1)

        self.buttons['collect_data'].setEnabled(True)

    def collect_data(self):
        from scriptUI import output_entry_UI
        self.output_UI = output_entry_UI(self.credential, self.token)
        res = self.output_UI.exec()

        if res == QDialog.Accepted:
            print("OK")
            self.output_entry = self.output_UI.get_output_entry()

            self.pdf_output_expired = os.path.join(self.output_entry, self.filename_expired)
            self.pdf_output = os.path.join(self.output_entry, self.filename)

            self.logger.log("Output sti er indtastet", 1)
        else:
            self.logger.log("Afbrudt", 1, 1)


        if res == QDialog.Accepted:
            from inital_setting import gather_sensor_ids
            from fetch_sensor_info import fetch_sensor_info
            from load_ownership import load_ownership_data
            from combine_data import combine_data_with_ownership
            from report_generation import create_pdf

            self.sensor_ids, self.base_url, self.auth, self.calibration_period = gather_sensor_ids(self.credential, self.token)

            self.logger.log(f"Der er fundet {len(self.sensor_ids)} sensorer", 2, 1)

            self.logger.log("Henter sensor information fra API", 2)
            self.sensor_info = fetch_sensor_info(self.sensor_ids, self.base_url, self.auth, self.calibration_period)

            self.logger.log("Henter ejerskabsinformationer for alle sensorer", 2)
            self.ownership_dict = load_ownership_data(self.ownership_path)
        
            self.combined_data = combine_data_with_ownership(self.sensor_info, self.ownership_dict)

            self.logger.log("Sorterer sensorer efter kalibreringsstatus")
            self.sensor_expired = {key: data for key, data in self.combined_data.items() if data["Kalibreringsstatus"] == "IKKE OK"}

            self.logger.log(f"Der er {len(self.sensor_expired)} sensorer med kalibreringsstatus IKKE OK", 2, 1)
            self.logger.log("Opretter PDF", 2)
            create_pdf(self.sensor_expired, self.pdf_output_expired, self.calibration_period, self.logo_img)
            self.logger.log(f"PDF gemt i {self.pdf_output_expired}", 2)

            create_pdf(self.combined_data, self.pdf_output, self.calibration_period, self.logo_img)
            self.logger.log(f"PDF gemt i {self.pdf_output}", 2)

            self.logger.log("Åbner PDFer",2)
            os.startfile(self.pdf_output_expired)
            os.startfile(self.pdf_output)
            self.logger.log("Færdig",1, 1)


if __name__ == '__main__':
    import time
    import sys
    from basic_functions import set_error_handling

    set_error_handling()
    app = QApplication(sys.argv)
    
    drive = "O:"
    splash_file = os.path.join("A000000", "A004371", "3_Pdoc", "Python","Kalibrering","splash_screen.png")
    splash_file = os.path.normpath(drive + os.sep + splash_file)

    if not os.path.exists(splash_file):
        QMessageBox.critical(None, "O-drive", f"Vær sikker på du er koblet til O-drevet, før du kører det her program!")
        raise ConnectionError("Your PC is not connected to the O:-drive")  
    
    pixmap = QPixmap(splash_file)

    splash = QSplashScreen(pixmap)
    splash.show()

    time.sleep(2.5)

    app.processEvents()

    ex = NavigationApp()
    
    ex.show()

    splash.finish(ex)

    sys.exit(app.exec()) 
