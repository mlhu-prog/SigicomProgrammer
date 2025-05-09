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
import sys

from logger import get_logger

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

        #self.

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

class output_entry_UI(QDialog):
    def __init__(self, token, credentials, parent=None):
        super().__init__(parent)

        self.token = token
        self.credentials = credentials
        self.logger = get_logger()
        
        self.setupUi(self)


    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(400, 100)
        self.verticalLayout_2 = QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")

        self.info_label = QLabel(Dialog)
        self.info_label.setObjectName(u"info_label")
        self.info_label.setText("V\u00e6lg en mappe til kalibreringsrapporten")
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.gridLayout.addWidget(self.info_label, 0, 0, 1, 4)

        self.output_label = QLabel(Dialog)
        self.output_label.setObjectName(u"output_label")

        self.gridLayout.addWidget(self.output_label, 1, 0, 1, 1, Qt.AlignmentFlag.AlignHCenter)

        self.output_entry = QLineEdit(Dialog)
        self.output_entry.setObjectName(u"browse_entry")

        self.gridLayout.addWidget(self.output_entry, 1, 1, 1, 2)

        self.browse_button = QPushButton(Dialog)
        self.browse_button.setObjectName(u"browse_button")
        self.browse_button.clicked.connect(self.browse_folder)

        self.gridLayout.addWidget(self.browse_button, 1, 3, 1, 1, Qt.AlignmentFlag.AlignHCenter)

        self.cancel_button = QPushButton(Dialog)
        self.cancel_button.setObjectName(u"pushButton_2")
        self.cancel_button.clicked.connect(self.on_cancel_pressed)

        self.gridLayout.addWidget(self.cancel_button, 2, 1, 1, 1, Qt.AlignmentFlag.AlignHCenter)

        self.continue_button = QPushButton(Dialog)
        self.continue_button.setObjectName(u"pushButton")
        self.continue_button.clicked.connect(self.on_submit)

        self.gridLayout.addWidget(self.continue_button, 2, 2, 1, 1)

        self.verticalLayout_2.addLayout(self.gridLayout)


        self.retranslateUi(Dialog)


    def on_cancel_pressed(self):
        self.reject()

    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.output_entry.setText(folder)

    def on_submit(self):
        self.accept()

    def get_output_entry(self):
        return self.output_entry.text()
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Outputsti", None))
        self.cancel_button.setText(QCoreApplication.translate("Dialog", u"Afbryd", None))
        self.output_label.setText(QCoreApplication.translate("Dialog", u"Output sti", None))
        self.browse_button.setText(QCoreApplication.translate("Dialog", u"Browse", None))
        self.continue_button.setText(QCoreApplication.translate("Dialog", u"Forts\u00e6t", None))
    # retranslateUi

