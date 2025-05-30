from PySide6.QtWidgets import QMessageBox
from datetime import datetime

import os

#Project imports
from logger import get_logger
from basic_functions import project_ID_to_ATR

class Dagsrapport:
    def __init__(self, project_ID, date_submitted, output_dir, credential, token):

        self.project_ID = project_ID
        self.date_submitted = date_submitted
        self.output_dir = output_dir

        self.credential = credential
        self.token = token

        self.run()


    def initial_settings(self):

        self.logger = get_logger()

        self.username = "user"
        self.password = ":".join([self.credential, self.token])
    
        self.atr, self.name = project_ID_to_ATR(str(self.project_ID), self.credential, self.token)

        self.main_cache_folder = "O:\\A000000\\A004371\\3_Pdoc\\Dagsrapportering"

    def check_inputs(self):

        if not self.output_dir:
            QMessageBox.critical(None, "Fejl", "Output sti kan ikke være tom!")
            return None
        else:
            os.makedirs(self.output_dir, exist_ok=True)
            
        if not self.atr or not self.name:
            QMessageBox.critical(None, "Fejl", "Projekt ID'et er ikke tilgængeligt i INFRA")
            return None
        else:
            self.cache_folder = f"{self.atr} - {self.name}"

            self.cache_main_dir = os.path.join(self.main_cache_folder, self.cache_folder)
        
        if self.date_submitted.weekday() in [5,6]: #Lørdag eller Søndag
            print("Hej")
            self.logger.log("Fejl! Den angivne dato skal være en hverdag.")
            self.logger.log("Angiv en ny dato under 'Definer projekt'",2,2)
            return None

        return True

    def create_dirs(self):
        self.cache_date = "{}-{}-{}".format(self.date_submitted.year, self.date_submitted.month, self.date_submitted.day)

        os.makedirs(os.path.join(self.cache_main_dir, "API", self.cache_date), exist_ok=True)
        os.makedirs(os.path.join(self.cache_main_dir, "Results", self.cache_date), exist_ok=True)

    def inst_calculate_date_from(self):
        from calculate_date_from import calculate_date_from

        self.date_to, self.date_from, self.date_range, self.output_pdf = calculate_date_from(self.date_submitted, self.output_dir)

        self.date_from_str, self.date_to_str = [datetime.strftime(date,format="%Y-%m-%d %H:%M") for date  in [self.date_from, self.date_to]]

    def inst_get_sensorlist_in_project(self):
        from get_sensorlist import get_sensorlist_in_project

        self.sensor_dict, self.active_sensor_dict, self.inactive_sensor_dict, self.cache_main_dir, self.cache_date = get_sensorlist_in_project(str(self.project_ID), self.username, self.password,
                                                                                                                                               self.atr, self.name, self.date_to, self.date_range,
                                                                                                                                               self.cache_date, self.cache_main_dir)

    def inst_create_search_dict(self):
        from create_search_dict import create_search_dict
        
        self.searches_dict = create_search_dict(str(self.project_ID),self.username,self.password,self.active_sensor_dict,
                                                self.cache_main_dir,self.cache_date,self.date_to_str,self.date_from_str)

    def inst_gather_infra_data(self):
        from gather_infra_data import gather_INFRA_data

        self.data_dict, self.trans_dict, self.info_dict = gather_INFRA_data(self.searches_dict, self.sensor_dict, self.username, 
                                                                            self.password, self.cache_main_dir, self.cache_date)

    def inst_analyse_data(self):
        from dataAnalysis import dataAnalysis

        dataAnalysis(self.cache_main_dir, self.cache_date, self.data_dict, self.info_dict)

    def inst_table_creater(self):
        from table_creater import table_creater

        self.active_final_df, self.inactive_final_df = table_creater(self.cache_main_dir, self.cache_date, self.data_dict, self.info_dict, self.inactive_sensor_dict)

    def inst_create_footnotes(self):
        from report_generation import create_footnotes

        self.logger.log("Fodnoter tilføjes for aktive målepunkter")
        self.active_footnotes_df = create_footnotes(self.active_sensor_dict, self.active_final_df, self.cache_main_dir, self.cache_date, 
                                                    active=True, trans_dict=self.trans_dict, info_dict=self.info_dict)
        
        if self.inactive_sensor_dict:
            self.inactive_footnotes_df = create_footnotes(self.inactive_sensor_dict, self.inactive_final_df, self.cache_main_dir,
                                                          self.cache_date, active=False)
    
    def inst_create_pdf(self):
        from report_generation import build_pdf
        from report_generation import build_pdf_ended_measurements
        from report_generation import merge_pdfs

        if self.inactive_sensor_dict != {}:
            self.logger.log("Bygger PDF for aktive og inaktive målepunkter")
            self.temp_active = os.path.join(self.output_dir,"aktive.pdf")
            self.end_page = build_pdf(self.active_final_df.drop(self.active_final_df.columns[10:],axis=1), self.active_footnotes_df, self.atr, self.name, 
                            self.date_from, self.date_to, self.temp_active)
            
            self.temp_inactive = os.path.join(self.output_dir,"inaktive.pdf")
            
            build_pdf_ended_measurements(self.inactive_final_df.drop(self.inactive_final_df.columns[9:],axis=1), self.inactive_footnotes_df, self.end_page, self.temp_inactive)

            self.pdf_list = [self.temp_active, self.temp_inactive]

            self.logger.log("Sammensætter PDF for aktive og inaktive målepunkter")
            merge_pdfs(self.pdf_list, self.output_pdf)
        else:
            self.logger.log("Bygger PDF for aktive målepunkter")
            build_pdf(self.active_final_df.drop(self.active_final_df.columns[10:],axis=1), self.active_footnotes_df, self.atr, self.name, 
                            self.date_from, self.date_to, self.output_pdf)


    def run(self):

        self.initial_settings()

        if not self.check_inputs():
            self.output_pdf = self.cache_main_dir = self.cache_date = self.active_final_df = None
            return None, None, None, None

        self.create_dirs()

        self.inst_calculate_date_from()

        self.inst_get_sensorlist_in_project()

        self.inst_create_search_dict()

        self.inst_gather_infra_data()        

        self.inst_analyse_data()

        self.inst_table_creater()

        self.inst_create_footnotes()

        self.inst_create_pdf()

    def gather_outputs(self):
        return self.output_pdf, self.cache_main_dir, self.cache_date, self.active_final_df







    


    










        

