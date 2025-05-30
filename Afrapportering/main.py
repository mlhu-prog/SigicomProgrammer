
import os

from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import * 
from PySide6.QtGui import * 
from PySide6.QtCore import Qt

from scriptUI import *
from logger import init_logger


class NavigationApp(QWidget):
    def __init__(self):
        super().__init__()
        self.cache_main_dir = None
        self.credential = None
        self.token = None
        self.collected_data = None
        self.old_id = None

        self.drive = "O:"

        self.MP_order = None

        self.logger = init_logger()
        self.logger.show()
        self.logger.log("Starter Afrapportering UI - Version 3.0", 2, status=1)
        

        self.initUI()

        self.logger.log("Programmet er opstartet og klar", 1, status=1)
        self.logger.log("Se i bunden af dette vindue for status", 1, status=1)

    def initUI(self):

        drive = "O:"
        files_path = os.path.join("A000000", "A004371", "3_Pdoc", "Afrapportering")
        logo_path = os.path.join(files_path, "files", "Logo_no_background.png")

        logo_img = os.path.normpath(drive + os.sep + logo_path)

        self.transient_folder = os.path.normpath(drive + os.sep + os.path.join(files_path, "Transient Data"))

        self.setWindowTitle('Afrapportering')
        self.setGeometry(100, 100, 300, 450)

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

        self.buttons = {}

        self.buttons['login'] = QPushButton('Login', self)
        self.buttons['login'].clicked.connect(self.login_function)
        layout.addWidget(self.buttons['login'])


        self.buttons['collect_data'] = QPushButton('Definer projekt', self)
        self.buttons['collect_data'].setEnabled(False)
        self.buttons['collect_data'].clicked.connect(lambda: self.button_wrapper(self.collect_data))
        layout.addWidget(self.buttons['collect_data'])

        self.buttons['gather_data'] = QPushButton('Hent Data', self)
        self.buttons['gather_data'].setEnabled(False)
        self.buttons['gather_data'].clicked.connect(self.gather_data)
        layout.addWidget(self.buttons['gather_data'])

        self.buttons['reorder_points'] = QPushButton('Rækkefølge af målepunkter', self)
        self.buttons['reorder_points'].setEnabled(False)
        self.buttons['reorder_points'].clicked.connect(self.reorder_points)
        layout.addWidget(self.buttons['reorder_points'])

        self.buttons['transient_gui'] = QPushButton('Analyser Transienter og generer resultat tekst', self)
        self.buttons['transient_gui'].setEnabled(False)
        self.buttons['transient_gui'].clicked.connect(self.transient_gui)
        layout.addWidget(self.buttons['transient_gui'])

        self.buttons['project_info'] = QPushButton('Indledning', self)
        self.buttons['project_info'].setEnabled(False)
        self.buttons['project_info'].clicked.connect(self.project_info)
        layout.addWidget(self.buttons['project_info'])

        self.buttons['work_info'] = QPushButton('Anlægsarbejde', self)
        self.buttons['work_info'].setEnabled(False)
        self.buttons['work_info'].clicked.connect(self.work_info)
        layout.addWidget(self.buttons['work_info'])

        self.buttons['image_selector'] = QPushButton('Oversigtsfoto', self)
        self.buttons['image_selector'].setEnabled(False)
        self.buttons['image_selector'].clicked.connect(self.image_selector)
        layout.addWidget(self.buttons['image_selector'])

        self.buttons['measurement_condition'] = QPushButton('Målekonditoner (Valgfrit)', self)
        self.buttons['measurement_condition'].setEnabled(False)
        self.buttons['measurement_condition'].clicked.connect(self.measurement_condition)
        layout.addWidget(self.buttons['measurement_condition'])

        self.buttons['limit_construction_damage'] = QPushButton('Grænseværdi for bygningsskader (Valgfrit)', self)
        self.buttons['limit_construction_damage'].setEnabled(False)
        self.buttons['limit_construction_damage'].clicked.connect(self.limit_construction_damage_main)
        layout.addWidget(self.buttons['limit_construction_damage'])

        self.buttons['initial_mp_result_text'] = QPushButton('Indledende resultat tekst (Valgfrit)', self)
        self.buttons['initial_mp_result_text'].setEnabled(False)
        self.buttons['initial_mp_result_text'].clicked.connect(self.initial_mp_result_text_main)
        layout.addWidget(self.buttons['initial_mp_result_text'])

        self.buttons['edit_mp_text_gui'] = QPushButton('Resultat tekst for målepunkter (Valgfrit)', self)
        self.buttons['edit_mp_text_gui'].setEnabled(False)
        self.buttons['edit_mp_text_gui'].clicked.connect(self.edit_mp_text_gui)
        layout.addWidget(self.buttons['edit_mp_text_gui'])

        self.buttons['create_conclusion'] = QPushButton('Konklusion', self)
        self.buttons['create_conclusion'].setEnabled(False)
        self.buttons['create_conclusion'].clicked.connect(self.create_conclusion)
        layout.addWidget(self.buttons['create_conclusion'])

        self.buttons['generate_report'] = QPushButton('Generer Rapport', self)
        self.buttons['generate_report'].setEnabled(False)
        self.buttons['generate_report'].clicked.connect(self.generate_report)
        layout.addWidget(self.buttons['generate_report'])

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

    def button_wrapper(self, func):
        func()
        self.after_button_pressed()

    def after_button_pressed(self):
        from final_data_collection import final_project_data_collection
        if self.collected_data: 
            if not self.old_id:
                self.old_id = self.collected_data["project_ID"]
            elif self.collected_data["project_ID"] != self.old_id:
                self.old_id = self.collected_data["project_ID"]
                for key in self.buttons.keys():
                    if key == 'gather_data' or key == 'collect_data' or key == 'login':
                        self.buttons[key].setEnabled(True)
                    else:
                        self.buttons[key].setEnabled(False) 

            if os.path.exists(self.cache_main_dir):
                check_file_1 = os.path.join(self.cache_main_dir, "Rapport", "Tekst", "Indledning.md")
                check_file_2 = os.path.join(self.cache_main_dir, "Rapport", "Tekst", "Anlægsarbejde.md")
                check_file_3 = os.path.join(self.cache_main_dir, "Rapport", "Tekst", "Konklusion_1.md")
                check_file_4 = os.path.join(self.cache_main_dir, "Results", "trans_dict_final.json")
                
                images_dir = os.path.join(self.cache_main_dir,"Rapport","Figurer","Oversigtsfoto")

                if all(os.path.exists(file) for file in [check_file_1, check_file_2, check_file_3, check_file_4]) and os.listdir(images_dir):
                    QMessageBox.information(self, "Projekt information", "Projektet er oprettet før.")

                    self.logger.log("Projektet er oprettet før.")

                    self.collected_data = final_project_data_collection(self.cache_main_dir, self.collected_data, False)
                    self.buttons['project_info'].setEnabled(True)
                    self.buttons['work_info'].setEnabled(True)
                    self.buttons['image_selector'].setEnabled(True)
                    self.buttons['reorder_points'].setEnabled(True)
                    self.buttons['transient_gui'].setEnabled(True)
                    self.buttons['initial_mp_result_text'].setEnabled(True)
                    self.buttons['measurement_condition'].setEnabled(True)
                    self.buttons['limit_construction_damage'].setEnabled(True)
                    self.buttons['edit_mp_text_gui'].setEnabled(True)
                    self.buttons['create_conclusion'].setEnabled(True)
                    self.buttons['generate_report'].setEnabled(True)

    def login_function(self):
        self.logger.log(f"Starter login vindue", 2, status=2)
        self.login_window = loginWindow()
        res = self.login_window.exec()

        if res == QDialog.Accepted:
            self.credential, self.token = self.login_window.get_login()
            self.logger.log(f"Bruger er logget ind", status=1)
         
            self.buttons['collect_data'].setEnabled(True)

    def collect_data(self):
        self.logger.log(f"Kører UI til at indtaste projekt information", 2, status=2)

        self.input_UI = input_UI(self.credential, self.token, self.collected_data)
        res = self.input_UI.exec()
        
        if res == QDialog.Accepted:
            self.collected_data = self.input_UI.get_data()

            self.cache_main_dir = os.path.join("A000000", "A004371", "3_Pdoc", "Afrapportering", f"{self.collected_data['project_atr']} - {self.collected_data['project_name']}")
            self.cache_main_dir = os.path.normpath(self.drive + os.sep + self.cache_main_dir)
            
            self.project_atr_label.setText(f"ATR: {self.collected_data.get('project_atr', '')}")
            self.project_name_label.setText(f"Projekt: {self.collected_data.get('project_name', '')}")

            self.buttons['gather_data'].setEnabled(True)

            self.logger.log(f"Projekt information er indtastet", status=1)
        else:
            self.logger.log("UI er annulleret", 2, 1)

    def gather_data(self):
        from final_data_collection import final_project_data_collection
        from gather_infra_data import gather_infra_data
        from analyse_data import analyse_data
        self.logger.log(f"Henter data!", 2, status=2)

        self.cache_main_dir = gather_infra_data(self.credential, self.token, self.collected_data)
        self.collected_data = final_project_data_collection(self.cache_main_dir, self.collected_data)
        analyse_data(self.cache_main_dir)

        self.logger.log(f"Data er nu hentet og analyseret", status=1)

        self.buttons['reorder_points'].setEnabled(True)

    def reorder_points(self):
        from analyse_data import analyse_data
        from basic_functions import load_json

        self.logger.log(f"Kører UI til at redigere rækkefølge af målepunkter", 2, status=2)

        if self.buttons['transient_gui'].isEnabled():
            if os.path.exists(os.path.join(self.cache_main_dir, "API", "project_sensor_dict_final.json")):
                old_keys = load_json(os.path.join(self.cache_main_dir, "API", "project_sensor_dict_final.json")).keys()
            else:
                old_keys = None
        else:
            old_keys = None
            

        self.reorder_measuring_points = reorder_MeasuringPoints_UI(self.cache_main_dir)
        res = self.reorder_measuring_points.exec()

        if res == QDialog.Accepted:
            
            if old_keys:
                os.path.exists(os.path.join(self.cache_main_dir, "API", "project_sensor_dict_final.json"))
                new_keys = load_json(os.path.join(self.cache_main_dir, "API", "project_sensor_dict_final.json")).keys()
                for old, new in zip(old_keys, new_keys):
                    if old != new:
                        self.logger.log(f"Rækkefølge af målepunkter er ændret!", 2, status=2)
                        self.logger.log(f"Kører ny analyse af data", status=2)
                        analyse_data(self.cache_main_dir, True)

                        break
            
            self.buttons['transient_gui'].setEnabled(True)
            self.logger.log(f"Rækkefølge af målepunkter er nu gemt", status=1)
        else:
            self.logger.log("UI er annuleret",2,1)

    def project_info(self):
        self.logger.log(f"Kører UI til at redigere 'Indledning'", 2, status=2)

        self.introduction_window = introduction_UI(self.collected_data, self.cache_main_dir)

        res = self.introduction_window.exec()

        if res == QDialog.Accepted:
            self.logger.log(f"Kapitel 1 - 'Indledning' er nu gemt", status=1)
            
    
            self.buttons['work_info'].setEnabled(True)
        else:
            self.logger.log("UI er annulleret", 2, 1)

    def work_info(self):
        self.logger.log(f"Kører UI til at redigere 'Anlægsarbejde'", 2, status=2)

        self.work_info_window = work_info_UI(self.cache_main_dir)
        res = self.work_info_window.exec()

        if res == QDialog.Accepted:
            self.logger.log(f"Kapitel 2 - 'Anlægsarbejde' er nu gemt.", status=1)
        
            self.buttons['image_selector'].setEnabled(True)
        else:
            self.logger.log("UI er annulleret", 2, 1)

    def image_selector(self):
        from Image_Selection import image_selector
        self.logger.log(f"Kører UI til at vælge oversigtsfotos", 2, status=2)

        image_selector(self.cache_main_dir)

        self.buttons['edit_mp_text_gui'].setEnabled(True)
        self.buttons['measurement_condition'].setEnabled(True)
        self.buttons['limit_construction_damage'].setEnabled(True)
        self.buttons['create_conclusion'].setEnabled(True)
        self.buttons['initial_mp_result_text'].setEnabled(True)
        
        self.logger.log(f"Kapitel 3 - 'Oversigtsfotos' er nu gemt.", status=1)
        
    def measurement_condition(self):
        self.logger.log(f"Kører UI til at redigere 'Målekonditioner'", 2, status=2)

        self.measurement_conditions_window = measuringConditions_UI(self.collected_data, self.cache_main_dir)

        res = self.measurement_conditions_window.exec()
        if res == QDialog.Accepted:
            self.logger.log(f"Kapitel 4 - 'Målekonditioner' er nu gemt.", status=1)
        else:
            self.logger.log("UI er annulleret", 2, 1)
        
    def limit_construction_damage_main(self):
        self.logger.log(f"Kører UI til at redigere 'Grænseværdi for bygningsskader'", 2, status=2)

        self.limit_construction_damage_window = limitConstructionDamage_UI(self.collected_data, self.cache_main_dir)

        res = self.limit_construction_damage_window.exec()
        if res == QDialog.Accepted:
            self.logger.log(f"Kapitel 5 - 'Grænseværdi for bygningsskader' er nu gemt.", status=1)
        else:
            self.logger.log("UI er annulleret", 2, 1)
        
    def initial_mp_result_text_main(self):
        self.logger.log(f"Kører UI til at redigere indledende tekst til 'Måleresultater'", 2, status=2)

        self.initial_MP_result_text_window = initial_MP_result_text(self.collected_data, self.cache_main_dir)

        res = self.initial_MP_result_text_window.exec()
        if res == QDialog.Accepted:
            self.logger.log(f"Kapitel 6 - Indledende tekst til 'Måleresultater' er nu gemt.", status=1)
        else:
            self.logger.log("UI er annulleret", 2, 1)
        
    def transient_gui(self):
        from TransientUI import TransientUI
        from basic_functions import yes_no_cancel_operation
        from create_transient_information import create_transient_plots, create_result_text

        self.logger.log(f"Kører UI til at analysere transienter", 2, status=2)
        filenames = ["trans_dict_final.json", "trans_dict.json"]
        
        self.trans_dict_final_path, self.trans_dict_path = [os.path.join(self.cache_main_dir, "Results", file) for file in filenames]

        if os.path.exists(self.trans_dict_final_path):
            answer = yes_no_cancel_operation("Transienter eksisterer allerede", "Transienterne er behandlet før. \n Vil du fortsætte med disse resultater?")
        else:
            answer = ""
        
        if answer == "Yes":
            self.logger.log(f"Transienter eksisterer allerede og bliver genanalyseret", 2)
            self.logger.log(f"Resultat tekst for hvert målepunkt bliver lavet")
            create_result_text(self.cache_main_dir)
            self.logger.log(f"Resultat plots for hvert målepunkt som indeholder reelle transienter bliver lavet")
            create_transient_plots(self.cache_main_dir)
            self.buttons['project_info'].setEnabled(True)
        else:
            self.logger.log(f"Transienter bliver analyseret", 2)

            self.transient_window = TransientUI(self.collected_data["project_ID"], self.collected_data["project_atr"], self.collected_data["project_name"], 
                                                self.cache_main_dir, self.collected_data["output_folder"], self.transient_folder)
            res = self.transient_window.exec()
            
            if res == QDialog.Accepted:
                self.logger.log(f"Transienter er analyseret!",2)
                self.logger.log(f"Resultat tekst for hvert målepunkt bliver lavet")
                create_result_text(self.cache_main_dir)
                self.logger.log(f"Resultat plots for hvert målepunkt som indeholder reelle transienter bliver lavet")
                create_transient_plots(self.cache_main_dir)
                self.buttons['project_info'].setEnabled(True)
                self.logger.log(f"Transienter er analyseret og resultat plots er lavet", 2, status=1)
            else:
                self.logger.log("UI er annulleret", 2, 1)
        
    def edit_mp_text_gui(self):
        self.logger.log(f"Kører UI til at redigere resultat tekst for målepunkter", 2, status=2)

        # Open the EditMPTextGUI window
        self.edit_mp_text_window = EditMPTextGUI(self.cache_main_dir)
        self.edit_mp_text_window.exec()

        self.logger.log(f"Kapitel 3 - 'Resultat tekst for målepunkter' er nu gemt.", status=1)

    def create_conclusion(self):
        self.logger.log(f"Kører UI til at redigere 'Konklusion'", 2, status=2)
        
        self.conclusion_window = conclusionUI(self.collected_data, self.cache_main_dir)

        res = self.conclusion_window.exec()
        if res == QDialog.Accepted:
            self.logger.log(f"Kapitel 7 - 'Konklusionen' er nu gemt.", status=1)
            
            self.buttons['generate_report'].setEnabled(True)
        else:
            self.logger.log("UI er annulleret", 2, 1)

    def generate_report(self):
        from ReportGeneration import ReportGeneration
        self.logger.log(f"Genererer rapport!", 2, status=2)
        
        ReportGeneration(self.cache_main_dir, self.collected_data)
        
        self.logger.log(f"{self.collected_data['pdf_path']} er lavet. \n Husk at tjekke om bilag fra InfraNet er indsat korrekt!", 2, status=1)


    def log_usage(self):
        from datetime import datetime
        import getpass

        try:
            log_path = r"O:\Organisation\DK_1551\Konstruktioner\INIT\MLHU\Afrapportering_GUI_v1"
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.user = getpass.getuser()
            
            log = os.path.join(log_path, "log.log")
            with open(log, "a") as f:
                f.write(f"{timestamp}\t{self.user.upper()}\n")
        except:
            pass


if __name__ == '__main__':
    import time
    import sys
    from basic_functions import set_error_handling

    set_error_handling()
    app = QApplication(sys.argv)
    
    drive = "O:"
    splash_file = os.path.join("A000000", "A004371", "3_Pdoc", "Afrapportering","files","splash_screen.png")
    splash_file = os.path.normpath(drive + os.sep + splash_file)

    if not os.path.exists(splash_file):
        QMessageBox.critical(None, "O-drive", f"Vær sikker på du er koblet til O-drevet, før du kører det her program!")
        raise ConnectionError("Your PC is not connected to the O:-drive")  
    
    pixmap = QPixmap(splash_file)

    splash = QSplashScreen(pixmap)
    splash.show()

    time.sleep(2.5)

    ex = NavigationApp()
    ex.show()
    ex.log_usage()

    splash.finish(ex)

    sys.exit(app.exec())