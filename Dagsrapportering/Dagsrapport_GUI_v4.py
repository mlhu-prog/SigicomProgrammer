
from logger import init_logger

from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox, QSplashScreen
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import * 
from PySide6.QtGui import * 
from PySide6.QtCore import Qt

import os


class NavigationApp(QWidget):
    def __init__(self):
        super().__init__()
        self.cache_main_dir = None
        self.credential = None
        self.token = None

        self.atr = None
        self.name = None
        self.project_ID = None
        self.date_str = None
        self.output_dir = None

        self.drive = "O:"

        self.logger = init_logger()
        self.logger.log("Starter Dagsrapport UI - version 4.0", 2)
        self.logger.log("Se status i bunden af dette log-vindue (klar/arbejder)",1,1)
        self.logger.show()

        self.initUI()
        
        self.logger.log("Klar...",1,1)

    def initUI(self):

        drive = "O:"
        files_path = os.path.join("A000000", "A004371", "3_Pdoc", "Afrapportering")
        logo_path = os.path.join(files_path, "files", "Logo_no_background.png")

        logo_img = os.path.normpath(drive + os.sep + logo_path)

        self.transient_folder = os.path.normpath(drive + os.sep + os.path.join(files_path, "Transient Data"))

        self.setWindowTitle('Afrapportering')
        self.setGeometry(100, 100, 300, 250)

        layout = QVBoxLayout()

        # Add labels for project_atr and project_name
        layout.setSpacing(25)
        self.project_atr_label = QLabel('ATR:', self)
        self.project_atr_label.setFont(QFont('Arial', 10, QFont.Bold))
        self.project_atr_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.project_atr_label)

        self.project_name_label = QLabel('Projekt:', self)
        self.project_name_label.setFont(QFont('Arial', 10, QFont.Bold))
        self.project_name_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.project_name_label)

        self.date_label = QLabel('Dato:', self)
        self.date_label.setFont(QFont('Arial', 10, QFont.Bold))
        self.date_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.date_label)

        self.buttons = {}

        self.buttons['login'] = QPushButton('Login', self)
        self.buttons['login'].clicked.connect(self.login_function)
        layout.addWidget(self.buttons['login'])

        self.buttons['collect_data'] = QPushButton('Definer projekt', self)
        self.buttons['collect_data'].setEnabled(False)
        self.buttons['collect_data'].clicked.connect(self.collect_data)
        layout.addWidget(self.buttons['collect_data'])

        self.buttons['gather_data'] = QPushButton('Hent data og generer rapport', self)
        self.buttons['gather_data'].setEnabled(False)
        self.buttons['gather_data'].clicked.connect(self.gather_data)
        layout.addWidget(self.buttons['gather_data'])

        img = QLabel()
        pixmap = QPixmap(logo_img)

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
        from scriptUI import input_UI
        self.input_UI = input_UI(self.credential, self.token, self.project_ID, self.date_str, self.output_dir)
        res = self.input_UI.exec()

        if res == QDialog.Accepted:
            self.atr, self.name, self.project_ID, self.date_str, self.output_dir = self.input_UI.get_data()
            self.logger.log("Input-data er indtastet", 1, 1)
        else:
            self.logger.log("Input-vindue er afbrudt", 1, 1)

        if self.atr is not None:
            self.project_atr_label.setText(f'ATR: {self.atr}')
            self.project_name_label.setText(f'Projekt: {self.name}')
            self.date_label.setText(f'Dato: {self.date_str}')

            self.buttons['gather_data'].setEnabled(True)
        
    def gather_data(self):   
        from scriptUI import resultWindow_UI
        from datetime import datetime
        from Dagsrapport_main import Dagsrapport
        self.logger.log(f"Henter data!", 2) 
        self.date = datetime.strptime(self.date_str, '%Y-%m-%d').date()
    
        self.date = datetime.combine(self.date, datetime.now().time())

        instance = Dagsrapport(self.project_ID, self.date, self.output_dir, self.credential, self.token)

        self.out_file_pdf, self.cache_main_dir, self.cache_date, self.active_final_df = instance.gather_outputs()

        if self.out_file_pdf == None:
            self.buttons['gather_data'].setEnabled(False)
            return
        
        self.result_UI = resultWindow_UI(self.active_final_df, self.cache_main_dir, self.cache_date, self.project_ID, self.output_dir, self.date, self.credential, self.token)
        res = self.result_UI.exec()
        self.result_UI.raise_()

        while res != QDialog.Accepted:
            self.out_file_pdf, self.active_final_df = self.result_UI.get_latest_results()
            self.result_UI.close()
            self.result_UI = resultWindow_UI(self.active_final_df, self.cache_main_dir, self.cache_date, self.project_ID, self.output_dir, self.date, self.credential, self.token)

            self.result_UI.raise_()

            res = self.result_UI.exec()
        
        self.logger.log("Åbner {}".format(os.path.basename(self.out_file_pdf)))
        os.startfile(self.out_file_pdf)

        QMessageBox.information(None, "Rapport", f"PDF-filen er dannet.")

        self.logger.log(f"Rapport er dannet og gemt!", 2, 1)



if __name__ == '__main__':
    import time
    import sys
    from basic_functions import set_error_handling

    #set_error_handling()
    app = QApplication(sys.argv)
    
    drive = "O:"
    splash_file = os.path.join("A000000", "A004371", "3_Pdoc", "Dagsrapportering","files","splash_screen.png")
    splash_file = os.path.normpath(drive + os.sep + splash_file)

    if not os.path.exists(splash_file):
        QMessageBox.critical(None, "O-drive", f"Vær sikker på du er koblet til O-drevet, før du kører det her program!")
        raise ConnectionError("Your PC is not connected to the O:-drive")  
    
    pixmap = QPixmap(splash_file)

    splash = QSplashScreen(pixmap)
    splash.show()

    time.sleep(2.5)

    app.processEvents()

    #set_error_handling()
    ex = NavigationApp()
    #ex.set_error_handling_pyqt5()
    ex.show()

    splash.finish(ex)

    sys.exit(app.exec()) 


