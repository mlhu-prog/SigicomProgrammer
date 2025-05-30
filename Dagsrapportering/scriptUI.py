
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QTextCursor,
    QFont, QFontDatabase, QGradient, QIcon, QEnterEvent, QTextBlockFormat,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QDialog, QGridLayout, QGraphicsView,
    QLabel, QLineEdit, QPushButton, QSizePolicy, QTextEdit, QHBoxLayout, QLayout, QDateEdit,
    QSpacerItem, QVBoxLayout, QWidget, QFileDialog, QScrollArea, QMessageBox, QComboBox)

import os

from logger import get_logger

class HoverWidget(QLabel):
    def __init__(self, content_type, content):
        """Tooltip window that shows an image or text when hovered."""
        super().__init__()
        
        self.setAttribute(Qt.WA_DeleteOnClose)  # Ensures widget closes properly

        layout = QVBoxLayout(self)
        self.setWindowFlags(Qt.ToolTip | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        if content_type == "image" and content:
            # Load and display image
            pixmap = QPixmap(content)
            if not pixmap.isNull():
                image_label = QLabel()
                image_label.setPixmap(pixmap.scaled(482, 700, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                layout.addWidget(image_label)
        elif content_type == "text" and content:
            # Display text tooltip
            text_label = QLabel(content)
            text_label.setStyleSheet("background: white; border: 1px solid black; padding: 5px; font-size: 16px;")
            layout.addWidget(text_label)

    def show_at(self, pos: QPoint):
        """Show tooltip window at a specific position."""
        self.move(pos + QPoint(10, 10))  # Offset slightly from cursor
        self.show()

class HoverImageLabel(QLabel):
    def __init__(self, display_image, content_type="image", content=None, parent=None):
        """
        QLabel that displays an image and shows a tooltip (image or text) when hovered.

        :param display_image: Image file to show in the QLabel.
        :param content_type: Type of hover content ("image" or "text").
        :param content: Image path or text to show when hovered.
        """
        super().__init__(parent)
        self.setMouseTracking(True)
        self.hover_window = None
        self.content_type = content_type
        self.content = content

        # Set the main image for display
        pixmap = QPixmap(display_image)
        if not pixmap.isNull():
            self.setPixmap(pixmap.scaled(15, 15, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.setAlignment(Qt.AlignCenter)
            
    def enterEvent(self, event: QEnterEvent):
        """Show tooltip when mouse enters the QLabel."""
        self.show_tooltip(event)

    def leaveEvent(self, event):
        """Close tooltip when mouse leaves the QLabel."""
        if self.hover_window:
            self.hover_window.close()
            self.hover_window = None
        super().leaveEvent(event)

    def show_tooltip(self, event):
        """Display the tooltip window when hovering over the QLabel."""
        if self.hover_window is None and self.content:
            self.hover_window = HoverWidget(self.content_type, self.content)
            pos = event.globalPosition().toPoint()  # Fix: Use globalPosition() in PySide6
            self.hover_window.show_at(pos)

class loginWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.drive = "O:"

        self.files_path = os.path.join("A000000", "A004371", "3_Pdoc", "Afrapportering")
        self.logo_path = os.path.join(self.files_path, "files", "Logo_no_background.png")

        self.logo_img = os.path.normpath(self.drive + os.sep + self.logo_path)

        self.setupUi(self)

    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(296, 336)
        self.verticalLayout_2 = QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_3)

        self.credentials_label_2 = QLabel(Dialog)
        self.credentials_label_2.setObjectName(u"credentials_label_2")

        self.verticalLayout.addWidget(self.credentials_label_2)

        self.credentials_entry = QLineEdit(Dialog)
        self.credentials_entry.setEchoMode(QLineEdit.Password)
        self.credentials_entry.setAlignment(Qt.AlignCenter)
        self.credentials_entry.setObjectName(u"credentials_entry")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.credentials_entry.sizePolicy().hasHeightForWidth())
        self.credentials_entry.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.credentials_entry, 0, Qt.AlignmentFlag.AlignHCenter)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_4)

        self.token_label = QLabel(Dialog)
        self.token_label.setObjectName(u"token_label")

        self.verticalLayout.addWidget(self.token_label)

        self.token_entry = QLineEdit(Dialog)
        self.token_entry.setEchoMode(QLineEdit.Password)
        self.token_entry.setAlignment(Qt.AlignCenter)
        self.token_entry.setObjectName(u"token_entry")
        sizePolicy.setHeightForWidth(self.token_entry.sizePolicy().hasHeightForWidth())
        self.token_entry.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.token_entry, 0, Qt.AlignmentFlag.AlignHCenter)

        self.verticalSpacer_5 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_5)

        self.saveLogin_checkbox = QCheckBox(Dialog)
        self.saveLogin_checkbox.setObjectName(u"saveLogin_checkbox")

        self.verticalLayout.addWidget(self.saveLogin_checkbox, 0, Qt.AlignmentFlag.AlignHCenter)

        self.updateLogin_checkbox = QCheckBox(Dialog)
        self.updateLogin_checkbox.setObjectName(u"updateLogin_checkbox")

        self.verticalLayout.addWidget(self.updateLogin_checkbox, 0, Qt.AlignmentFlag.AlignHCenter)

        self.verticalSpacer_6 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_6)

        self.login_button = QPushButton(Dialog)
        self.login_button.setObjectName(u"login_button")
        sizePolicy.setHeightForWidth(self.login_button.sizePolicy().hasHeightForWidth())
        self.login_button.setSizePolicy(sizePolicy)
        self.login_button.clicked.connect(self.validate_and_proceed)

        self.verticalLayout.addWidget(self.login_button, 0, Qt.AlignmentFlag.AlignHCenter)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.hyperlink = QLabel(Dialog)
        self.hyperlink.setObjectName(u"hyperlink")
        self.hyperlink.setText('<a href="https://cowidk.infralogin.com/api/v1/user/0/token">Hent Credential og Token her</a>')
        self.hyperlink.setOpenExternalLinks(True)
        self.hyperlink.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.hyperlink)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        img = QLabel()
        pixmap = QPixmap(self.logo_img)

        desired_width = 100  # change this to your desired width
        desired_height = 100  # change this to your desired height

        # Scale the pixmap
        scaled_pixmap = pixmap.scaled(desired_width, desired_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        img.setPixmap(scaled_pixmap)
        img.setAlignment(Qt.AlignCenter)
        #img.setPixmap(pixmap)
        self.verticalLayout.addWidget(img)


        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.credentials_file = self.get_credentials_file_path()
        self.load_saved_credentials()

        self.retranslateUi(Dialog)

    def get_credentials_file_path(self):
        home_dir = os.path.expanduser("~")
        if os.name == 'nt':  # Windows
            app_data_dir = os.getenv('APPDATA', home_dir)
            credentials_dir = os.path.join(app_data_dir, 'Sigicom')
        else:  # Unix-like systems
            credentials_dir = os.path.join(home_dir, '.Sigicom')

        # Create the directory if it doesn't exist
        os.makedirs(credentials_dir, exist_ok=True)
        
        return os.path.join(credentials_dir, 'credentials.txt')

    def save_credentials(self, credentials, token):
        with open(self.credentials_file, 'w') as file:
            file.write(f"{credentials}\n{token}")

    def load_saved_credentials(self):
        if os.path.exists(self.credentials_file):
            with open(self.credentials_file, 'r') as file:
                lines = file.readlines()
                if len(lines) >= 2:
                    self.credentials_entry.setText(lines[0].strip()), self.token_entry.setText(lines[1].strip())

    def validate_and_proceed(self):
        # Basic validation
        if not self.credentials_entry.text() or not self.token_entry.text():
            QMessageBox.critical(None, None, f"Indtast venligst både credentials og en token")
            return

        # Handle Update Credentials checkbox
        if self.updateLogin_checkbox.isChecked():
            if os.path.exists(self.credentials_file):

                os.remove(self.credentials_file)

                self.save_credentials(self.credentials_entry.text(), self.token_entry.text())

        # Save credentials to file if checkbox is selected
        if self.saveLogin_checkbox.isChecked():
            self.save_credentials(self.credentials_entry.text(), self.token_entry.text())

        # Close the login window
        self.accept()

    def get_login(self):
        return self.credentials_entry.text(), self.token_entry.text()

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Login", None))
        self.credentials_label_2.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"center\"><span style=\" font-weight:700;\">Credentials:</span></p></body></html>", None))
        self.token_label.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"center\"><span style=\" font-weight:700;\">Token:</span></p></body></html>", None))
        self.saveLogin_checkbox.setText(QCoreApplication.translate("Dialog", u"Gem login", None))
        self.updateLogin_checkbox.setText(QCoreApplication.translate("Dialog", u"Opdater login", None))
        self.login_button.setText(QCoreApplication.translate("Dialog", u"Login", None))
        #self.hyperlink.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"center\">Label</p></body></html>", None))

class input_UI(QDialog):
    def __init__(self, credential, token, project_id, date, output_dir, parent=None):
        super().__init__(parent)

        self.atr = None
        self.name = None
        self.date = date
        self.project_id = project_id
        self.output_dir = output_dir

        self.credential = credential
        self.token = token

        self.drive = "O:"

        self.logger = get_logger()

        self.logger.log("Åbner input-vindue",2)

        self.files_path = os.path.join("A000000", "A004371", "3_Pdoc", "Dagsrapportering")
        self.logo_path = os.path.join(self.files_path, "files", "Logo_no_background.png")
        self.questionmark_path = os.path.join(self.files_path, "files", "question_mark.png")
        self.infraIDhelp_path = os.path.join(self.files_path, "files", "INFRA_ID.jpg")
        self.path_project_path = os.path.join(self.files_path, "files")

        self.logo_img = os.path.normpath(self.drive + os.sep + self.logo_path)
        self.questionmark_img = os.path.normpath(self.drive + os.sep + self.questionmark_path)
        self.infraIDhelp_img = os.path.normpath(self.drive + os.sep + self.infraIDhelp_path)
        self.path_project_list = os.path.normpath(self.drive + os.sep + self.path_project_path)
        
        self.initial_settings()

        self.setupUi(self)

    def initial_settings(self):
        with open(os.path.join(self.path_project_list, "saved_projects.txt"), 'r', encoding='utf-8') as f:
            self.input_values_options = f.read().splitlines()

    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(350, 360)
        self.verticalLayout_2 = QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setVerticalSpacing(20)
        self.gridLayout.setContentsMargins(-1, 0, -1, -1)

        self.InfraID_label = QLabel(Dialog)
        self.InfraID_label.setObjectName(u"InfraID_label")

        self.gridLayout.addWidget(self.InfraID_label, 1, 1, 1, 1)

        self.InfraID_entry = QLineEdit(Dialog)
        self.InfraID_entry.setObjectName(u"InfraID_entry")
        self.InfraID_entry.setAlignment(Qt.AlignCenter)
        self.InfraID_entry.textChanged.connect(self.on_id_entry)

        self.gridLayout.addWidget(self.InfraID_entry, 1, 3, 1, 1, Qt.AlignmentFlag.AlignHCenter)

        self.tooltip_ID = HoverImageLabel(display_image=self.questionmark_img, content_type="image", content=self.infraIDhelp_img)

        self.gridLayout.addWidget(self.tooltip_ID, 1, 4, 1, 1)

        self.saved_ID_label = QLabel(Dialog)
        self.saved_ID_label.setObjectName(u"ATR_label")

        self.gridLayout.addWidget(self.saved_ID_label, 2, 1, 1, 1)

        self.saved_ID_combobox = QComboBox(Dialog)
        self.saved_ID_combobox.setObjectName(u"ATR_entry")
        self.saved_ID_combobox.addItems(self.input_values_options)
        self.saved_ID_combobox.setEditable(True)
        self.saved_ID_combobox.setCurrentText(self.project_id if self.project_id else "")
        self.saved_ID_combobox.currentIndexChanged.connect(self.on_saved_ID_entry)

        self.gridLayout.addWidget(self.saved_ID_combobox, 2, 3, 1, 1, Qt.AlignmentFlag.AlignHCenter)

        self.Project_label = QLabel(Dialog)
        self.Project_label.setObjectName(u"Project_label")

        self.gridLayout.addWidget(self.Project_label, 3, 1, 1, 1)

        self.Project_entry = QLineEdit(Dialog)
        self.Project_entry.setObjectName(u"Project_entry")
        self.Project_entry.setAlignment(Qt.AlignCenter)
        self.Project_entry.setEnabled(False)

        self.gridLayout.addWidget(self.Project_entry, 3, 3, 1, 1)

        self.date_label = QLabel(Dialog)
        self.date_label.setObjectName(u"date_label")

        self.gridLayout.addWidget(self.date_label, 4, 1, 1, 1)

        self.date_entry = QDateEdit(Dialog)
        self.date_entry.setObjectName(u"date_entry")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        sizePolicy.setHeightForWidth(self.date_entry.sizePolicy().hasHeightForWidth())
        self.date_entry.setSizePolicy(sizePolicy)
        self.date_entry.setAlignment(Qt.AlignCenter)
        self.date_entry.setDate(QDate.fromString(self.date, "yyyy-MM-dd") if self.date else QDate.currentDate())
        self.date_entry.setDisplayFormat("yyyy-MM-dd")

        self.gridLayout.addWidget(self.date_entry, 4, 3, 1, 1, Qt.AlignmentFlag.AlignHCenter)        
        
        self.tooltip_date = HoverImageLabel(display_image=self.questionmark_img, content_type="text", content="Den angivne dato skal være en hverdag!\nProgrammet rapporterer for dagen/dagene forinden.\nEr den angivet dato en mandag, regnes fredag til og med søndag.")

        self.gridLayout.addWidget(self.tooltip_date, 4, 4, 1, 1)

        self.output_label = QLabel(Dialog)
        self.output_label.setObjectName(u"output_label")

        self.gridLayout.addWidget(self.output_label, 5, 1, 1, 1)

        self.output_entry = QLineEdit(Dialog)
        self.output_entry.setObjectName(u"output_entry")
        self.output_entry.setText(self.output_dir if self.output_dir else "")

        self.gridLayout.addWidget(self.output_entry, 5, 3, 1, 1)

        self.browse_button = QPushButton(Dialog)
        self.browse_button.setObjectName(u"browse_button")
        self.browse_button.clicked.connect(self.browse_folder)

        self.gridLayout.addWidget(self.browse_button, 5, 4, 1, 1)

        self.openPDF_label = QLabel(Dialog)
        self.openPDF_label.setObjectName(u"openPDF_label")

        self.gridLayout.addWidget(self.openPDF_label, 6, 1, 1, 1)

        self.gridLayout.setColumnMinimumWidth(4, 25)

        self.verticalLayout_2.addLayout(self.gridLayout)

        self.verticalSpacer_2 = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)

        self.verticalLayout_2.addItem(self.verticalSpacer_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setSizeConstraint(QLayout.SizeConstraint.SetMaximumSize)
        self.horizontalLayout.setContentsMargins(-1, 0, -1, -1)
        self.cancel_button = QPushButton(Dialog)
        self.cancel_button.setObjectName(u"cancel_button")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.cancel_button.sizePolicy().hasHeightForWidth())
        self.cancel_button.setSizePolicy(sizePolicy2)
        self.cancel_button.clicked.connect(self.on_cancel_pressed)

        self.horizontalLayout.addWidget(self.cancel_button)

        self.continue_button = QPushButton(Dialog)
        self.continue_button.setObjectName(u"continue_button")
        sizePolicy2.setHeightForWidth(self.continue_button.sizePolicy().hasHeightForWidth())
        self.continue_button.setSizePolicy(sizePolicy2)
        self.continue_button.clicked.connect(self.validate_and_proceed)

        self.horizontalLayout.addWidget(self.continue_button)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)
        self.gridLayout_2.setContentsMargins(-1, 0, -1, 11)
        self.created_by_label = QLabel(Dialog)
        self.created_by_label.setObjectName(u"created_by_label")

        self.gridLayout_2.addWidget(self.created_by_label, 0, 1, 1, 1)

        self.image_placeholder = QLabel()
        pixmap = QPixmap(self.logo_img)

        desired_width = 100  # change this to your desired width
        desired_height = 100  # change this to your desired height

        # Scale the pixmap
        scaled_pixmap = pixmap.scaled(desired_width, desired_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.image_placeholder.setPixmap(scaled_pixmap)
        self.image_placeholder.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.image_placeholder, 0, 2, 1, 1)

        self.empty_label_placeholder = QLabel(Dialog)
        self.empty_label_placeholder.setObjectName(u"empty_label_placeholder")

        self.gridLayout_2.addWidget(self.empty_label_placeholder, 0, 0, 1, 1)


        self.verticalLayout_2.addLayout(self.gridLayout_2)

        self.retranslateUi(Dialog)

        self.on_saved_ID_entry()
        
    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.output_entry.setText(folder)

    def on_id_entry(self):
        if self.InfraID_entry.text():
            self.project_id = self.InfraID_entry.text()
            self.saved_ID_combobox.setCurrentText("")
        
        self.path_project_json = os.path.join(self.path_project_list, f"{self.project_id}.json")

        if self.project_id:
            self.update_project_details()
    
    def on_saved_ID_entry(self):
        if self.saved_ID_combobox.currentText():
            self.project_id = self.saved_ID_combobox.currentText()
            self.InfraID_entry.setText("")

            self.path_project_json = os.path.join(self.path_project_list, f"{self.project_id}.json")

        if self.project_id:
            self.update_project_details()

    def update_project_details(self):
        from basic_functions import project_ID_to_ATR
        try:
            self.atr, self.name = project_ID_to_ATR(self.project_id, self.credential, self.token)
        except:
            self.atr, self.name = None, None

        if self.atr and self.name:
            self.Project_entry.setText(self.name)
    
    def on_cancel_pressed(self):
        self.reject()

    def validate_and_proceed(self):
        
        if self.atr is None:
            QMessageBox.critical(None, None, f"Projektet findes ikke i INFRA")
            return

        if self.output_entry.text() == "":
            QMessageBox.critical(None, None, f"Indtast venligst en output sti")
            return

        if self.project_id not in self.input_values_options:
            self.input_values_options.append(self.project_id)

            with open(os.path.join(self.path_project_list, "saved_projects.txt"), 'a', encoding='utf-8') as f:
                f.write(f"{self.project_id}\n")

        self.date = self.date_entry.date()

        self.date = self.date.toString('yyyy-MM-dd')

        self.accept()
    
    def get_data(self):    
        return self.atr, self.name, self.project_id, self.date, self.output_entry.text()
    
    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dagsrapportering", None))
        self.saved_ID_label.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p>Gemt ID:</p></body></html>", None))
        self.Project_label.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p>Projekt:</p></body></html>", None))
        self.date_label.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p>Dato:</p></body></html>", None))
        
        self.browse_button.setText(QCoreApplication.translate("Dialog", u"Browse", None))
        self.InfraID_label.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p>INFRA ID:</p></body></html>", None))
        self.output_label.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p>Output sti:</p></body></html>", None))
        self.cancel_button.setText(QCoreApplication.translate("Dialog", u"Annuller", None))
        self.continue_button.setText(QCoreApplication.translate("Dialog", u"Forts\u00e6t", None))
        self.created_by_label.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"center\">Udarbejdet af MLHU</p></body></html>", None))
        self.empty_label_placeholder.setText("")

class resultWindow_UI(QDialog):
    def __init__(self, df, cache_main_dir, cache_date, project_ID, output_dir, datetime_input, credential, token, parent=None):
        super().__init__(parent)

        self.df = df
        self.cache_main_dir = cache_main_dir
        self.cache_date = cache_date
        self.project_ID = project_ID
        self.output_dir = output_dir
        self.datetime_input = datetime_input
        self.credential = credential
        self.token = token

        self.logger = get_logger()

        self.logger.log("Åbner resultat-vindue", 2)

        self.initial_settings()

        self.setupUi(self)

        self.show()
        self.raise_()

    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")

        Dialog.resize(1230, 470)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setVerticalSpacing(6)
        self.gridLayout.setContentsMargins(-1, -1, -1, 0)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)

        self.adresse_label = QLabel(Dialog)
        self.adresse_label.setObjectName(u"adresse_label")
        self.adresse_label.setMaximumSize(QSize(16777215, 25))

        self.horizontalLayout.addWidget(self.adresse_label, 0, Qt.AlignmentFlag.AlignHCenter)

        self.postcode_label = QLabel(Dialog)
        self.postcode_label.setObjectName(u"postcode_label")
        self.postcode_label.setMaximumSize(QSize(16777215, 25))

        self.horizontalLayout.addWidget(self.postcode_label, 0, Qt.AlignmentFlag.AlignHCenter)

        self.limit_label = QLabel(Dialog)
        self.limit_label.setObjectName(u"limit_label")
        self.limit_label.setMaximumSize(QSize(16777215, 25))

        self.horizontalLayout.addWidget(self.limit_label, 0, Qt.AlignmentFlag.AlignHCenter)

        self.maxVib_mms_label = QLabel(Dialog)
        self.maxVib_mms_label.setObjectName(u"maxVib_mms_label")
        self.maxVib_mms_label.setMaximumSize(QSize(16777215, 25))

        self.horizontalLayout.addWidget(self.maxVib_mms_label, 0, Qt.AlignmentFlag.AlignHCenter)

        self.maxVib_per_label = QLabel(Dialog)
        self.maxVib_per_label.setObjectName(u"maxVib_per_label")
        self.maxVib_per_label.setMaximumSize(QSize(16777215, 25))

        self.horizontalLayout.addWidget(self.maxVib_per_label, 0, Qt.AlignmentFlag.AlignHCenter)

        self.Vib_mms_label = QLabel(Dialog)
        self.Vib_mms_label.setObjectName(u"Vib_mms_label")
        self.Vib_mms_label.setMaximumSize(QSize(16777215, 25))

        self.horizontalLayout.addWidget(self.Vib_mms_label, 0, Qt.AlignmentFlag.AlignHCenter)

        self.Vib_per_label = QLabel(Dialog)
        self.Vib_per_label.setObjectName(u"Vib_per_label")
        self.Vib_per_label.setMaximumSize(QSize(16777215, 25))

        self.horizontalLayout.addWidget(self.Vib_per_label, 0, Qt.AlignmentFlag.AlignHCenter)

        self.remove_meas_label = QLabel(Dialog)
        self.remove_meas_label.setObjectName(u"remove_meas_label")

        self.horizontalLayout.addWidget(self.remove_meas_label, 0, Qt.AlignmentFlag.AlignHCenter)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.scrollArea = QScrollArea(Dialog)
        self.scrollArea.setObjectName(u"scrollArea")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 1194, 388))
        self.gridLayout_3 = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(-1, 0, -1, -1)

        self.create_tabel()


        self.gridLayout_3.addLayout(self.gridLayout_2, 2, 0, 1, 1)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.gridLayout.addWidget(self.scrollArea, 0, 1, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(-1, -1, -1, 0)

        self.remove_button = QPushButton(Dialog)
        self.remove_button.setObjectName(u"pushButton_2")
        self.remove_button.clicked.connect(self.apply_exclusion)

        self.horizontalLayout_2.addWidget(self.remove_button, 0, Qt.AlignmentFlag.AlignHCenter)

        self.submit_btn = QPushButton(Dialog)
        self.submit_btn.setObjectName(u"pushButton")
        self.submit_btn.clicked.connect(self.on_submit_pressed)

        self.horizontalLayout_2.addWidget(self.submit_btn, 0, Qt.AlignmentFlag.AlignHCenter)

        self.gridLayout.addLayout(self.horizontalLayout_2, 3, 1, 1, 1)

        self.verticalLayout.addLayout(self.gridLayout)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)

    def initial_settings(self):
        import re
        def clean_address(address):
            # Use a regular expression to remove the superscript parts
            return re.sub(r'<super>\d+\)</super>', '', address).strip()
        self.df = self.df.iloc[:, [0, 1, 2, 6, 7, 8, 9]].copy()

        self.df['Adresse'] = self.df['Adresse'].apply(clean_address)

    def create_tabel(self):
        self.inpt_adresse = {}
        self.inpt_postcode = {}
        self.inpt_limit = {}
        self.inpt_maxVib_mms = {}
        self.inpt_maxVib_per = {}
        self.inpt_Vib_mms = {}
        self.inpt_Vib_per = {}
        self.inpt_checkbox = {}
        
        n = 0
        for i, row in self.df.iterrows():
            adresse = row["Adresse"]

            self.inpt_adresse[adresse] = QLabel(self.scrollAreaWidgetContents)
            self.inpt_adresse[adresse].setObjectName(u"inpt_adresse")
            self.inpt_adresse[adresse].setText(QCoreApplication.translate("Dialog", u"{}".format(row["Adresse"]), None))

            self.gridLayout_2.addWidget(self.inpt_adresse[adresse], n, 0, 1, 1)

            self.inpt_postcode[adresse] = QLabel(self.scrollAreaWidgetContents)
            self.inpt_postcode[adresse].setObjectName(u"inpt_postcode")
            self.inpt_postcode[adresse].setText(QCoreApplication.translate("Dialog", u"{}".format(row["Postnummer"]), None))

            self.gridLayout_2.addWidget(self.inpt_postcode[adresse], n, 1, 1, 1)

            self.inpt_limit[adresse] = QLabel(self.scrollAreaWidgetContents)
            self.inpt_limit[adresse].setObjectName(u"inpt_limit")
            self.inpt_limit[adresse].setText(QCoreApplication.translate("Dialog", u"{}".format(row["Grænse værdi"]), None))
            self.inpt_limit[adresse].setAlignment(Qt.AlignmentFlag.AlignHCenter)

            self.gridLayout_2.addWidget(self.inpt_limit[adresse], n, 2, 1, 1)

            self.inpt_maxVib_mms[adresse] = QLabel(self.scrollAreaWidgetContents)
            self.inpt_maxVib_mms[adresse].setObjectName(u"inpt_maxVib_mms")
            self.inpt_maxVib_mms[adresse].setText(QCoreApplication.translate("Dialog", u"{}".format(row["Maks vib. [mm/s]"]), None))
            self.inpt_maxVib_mms[adresse].setAlignment(Qt.AlignmentFlag.AlignHCenter)

            self.gridLayout_2.addWidget(self.inpt_maxVib_mms[adresse], n, 3, 1, 1)

            self.inpt_maxVib_per[adresse] = QLabel(self.scrollAreaWidgetContents)
            self.inpt_maxVib_per[adresse].setObjectName(u"inpt_maxVib_per")
            self.inpt_maxVib_per[adresse].setText(QCoreApplication.translate("Dialog", u"{}".format(row["Maks vib. [%]"]), None))
            self.inpt_maxVib_per[adresse].setAlignment(Qt.AlignmentFlag.AlignHCenter)

            self.gridLayout_2.addWidget(self.inpt_maxVib_per[adresse], n, 4, 1, 1)

            self.inpt_Vib_mms[adresse] = QLabel(self.scrollAreaWidgetContents)
            self.inpt_Vib_mms[adresse].setObjectName(u"inpt_Vib_mms")
            self.inpt_Vib_mms[adresse].setText(QCoreApplication.translate("Dialog", u"{}".format(row["Vib. [mm/s]"]), None))
            self.inpt_Vib_mms[adresse].setAlignment(Qt.AlignmentFlag.AlignHCenter)

            self.gridLayout_2.addWidget(self.inpt_Vib_mms[adresse], n, 5, 1, 1)

            self.inpt_Vib_per[adresse] = QLabel(self.scrollAreaWidgetContents)
            self.inpt_Vib_per[adresse].setObjectName(u"inpt_Vib_per")
            self.inpt_Vib_per[adresse].setText(QCoreApplication.translate("Dialog", u"{}".format(row["Vib. [%]"]), None))
            self.inpt_Vib_per[adresse].setAlignment(Qt.AlignmentFlag.AlignHCenter)

            self.gridLayout_2.addWidget(self.inpt_Vib_per[adresse], n, 6, 1, 1)


            self.inpt_checkbox[adresse] = QCheckBox(self.scrollAreaWidgetContents)
            self.inpt_checkbox[adresse].setObjectName(u"inpt_checkbox")
            self.inpt_checkbox[adresse].setText("")

            self.gridLayout_2.addWidget(self.inpt_checkbox[adresse], n, 7, 1, 1, Qt.AlignmentFlag.AlignHCenter)
        
            n += 1


        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer, n, 4, 1, 1)

    def apply_exclusion(self):
        import pandas as pd
        from Dagsrapport_main import Dagsrapport

        self.logger.log("Fjerner målinger",2)
        def update_flag_for_address(address, cache_main_dir, cache_date):
            adress_result_file = os.path.join(cache_main_dir, f"{address}",f"{cache_date}","Ascii","data_resultat.dat")
            
            if os.path.exists(adress_result_file):
                df_result = pd.read_csv(adress_result_file, sep="\t", header=0)
                exclude_time = df_result["Tidspunkt"]

            timeseries_file = os.path.join(cache_main_dir, f"{address}",f"{cache_date}","Ascii","data_flagged.dat")
            if os.path.exists(timeseries_file):
                df = pd.read_csv(timeseries_file, sep="\t", header=0)
                col_org = df.columns.tolist()
                col = col_org
                col[0] = "Tidspunkt"
                df.columns = col
                df.loc[df['Tidspunkt'] == exclude_time.values[0], 'Flag'] = 1
                df.columns = col_org
                df.to_csv(timeseries_file, sep="\t", index=False)
            else:
                QMessageBox.critical(None, "Fil ikke fundet", f"Tidsserien for {address} eksisterer ikke.")
                return
            
        if not any(self.inpt_checkbox[adresse].isChecked() for adresse in self.inpt_checkbox.keys()):
            self.logger.log("Ingen målinger er markeret.")
            self.logger.log("Hvis der ikke skal fjernes målinger så benyt 'Anvend resultater'")
            return

        for adresse in self.inpt_adresse.keys():
            if self.inpt_checkbox[adresse].isChecked():
                self.logger.log("Fjerner højeste måling fra {}".format(adresse))
                # Update the flag for the address
                update_flag_for_address(adresse, self.cache_main_dir, self.cache_date)
        
        self.logger.log("Laver ny dagsrapport, uden ekskluderede målinger", 2, 2)
        instance = Dagsrapport(self.project_ID, self.datetime_input, self.output_dir, self.credential, self.token)

        self.out_file_pdf, _, _, self.df = instance.gather_outputs()

        self.reject()

    def get_latest_results(self):
        return self.out_file_pdf, self.df

    def on_submit_pressed(self):
        self.logger.log("Resultatet er accepteret!",2)

        self.accept()

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.adresse_label.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-weight:700;\">Adresse</span></p></body></html>", None))
        self.postcode_label.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-weight:700;\">Postnummer</span></p></body></html>", None))
        self.limit_label.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-weight:700;\">Gr\u00e6nsev\u00e6rdi</span></p></body></html>", None))
        self.maxVib_mms_label.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-weight:700;\">Maks vib. [mm/s]</span></p></body></html>", None))
        self.maxVib_per_label.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-weight:700;\">Maks vib. [%]</span></p></body></html>", None))
        self.Vib_mms_label.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-weight:700;\">Vib. [mm/s]</span></p></body></html>", None))
        self.Vib_per_label.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-weight:700;\">Vib. [%]</span></p></body></html>", None))
        self.remove_meas_label.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-weight:700;\">Fjern m\u00e5ling</span></p></body></html>", None))
        self.remove_button.setText(QCoreApplication.translate("Dialog", u"Fjern m\u00e5linger", None))
        self.submit_btn.setText(QCoreApplication.translate("Dialog", u"Anvend resultater", None))
