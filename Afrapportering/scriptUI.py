# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'login_windowcuOkqa.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

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

from basic_functions import load_json
from basic_functions import save_json

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
    def __init__(self, credential, token, collected_data, parent=None):
        super().__init__(parent)

        self.credential = credential
        self.token = token
        self.collected_data = collected_data

        self.logger = get_logger()


        self.drive = "O:"

        self.files_path = os.path.join("A000000", "A004371", "3_Pdoc", "Afrapportering")
        self.logo_path = os.path.join(self.files_path, "files", "Logo_no_background.png")
        self.questionmark_path = os.path.join(self.files_path, "files", "question_mark.png")
        self.infraIDhelp_path = os.path.join(self.files_path, "files", "INFRA_ID.jpg")
        self.path_project_path = os.path.join(self.files_path, "files", "saved_projects")

        self.logo_img = os.path.normpath(self.drive + os.sep + self.logo_path)
        self.questionmark_img = os.path.normpath(self.drive + os.sep + self.questionmark_path)
        self.infraIDhelp_img = os.path.normpath(self.drive + os.sep + self.infraIDhelp_path)
        self.path_project_list = os.path.normpath(self.drive + os.sep + self.path_project_path)
        
        self.setupUi(self)

    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(435, 750)
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

        self.ATR_label = QLabel(Dialog)
        self.ATR_label.setObjectName(u"ATR_label")

        self.gridLayout.addWidget(self.ATR_label, 2, 1, 1, 1)

        self.ATR_entry = QLineEdit(Dialog)
        self.ATR_entry.setObjectName(u"ATR_entry")
        self.ATR_entry.setAlignment(Qt.AlignCenter)
        self.ATR_entry.setEnabled(False)

        self.gridLayout.addWidget(self.ATR_entry, 2, 3, 1, 1, Qt.AlignmentFlag.AlignHCenter)

        self.Project_label = QLabel(Dialog)
        self.Project_label.setObjectName(u"Project_label")

        self.gridLayout.addWidget(self.Project_label, 3, 1, 1, 1)

        self.Project_entry = QLineEdit(Dialog)
        self.Project_entry.setObjectName(u"Project_entry")
        self.Project_entry.setAlignment(Qt.AlignCenter)
        self.Project_entry.setEnabled(False)
        self.Project_entry.textChanged.connect(self.update_report_title)

        self.gridLayout.addWidget(self.Project_entry, 3, 3, 1, 1)

        self.project_manual_entry = QLineEdit(Dialog)
        self.project_manual_entry.setObjectName(u"project_final_entry")
        self.project_manual_entry.setAlignment(Qt.AlignCenter)
        self.project_manual_entry.textChanged.connect(self.update_report_title)

        self.gridLayout.addWidget(self.project_manual_entry, 4, 3, 1, 1)

        self.tooltip_projectname = HoverImageLabel(display_image=self.questionmark_img, content_type="text", content="Udfyld kun, hvis en anden titel skal bruges til afrapporteringen")

        self.gridLayout.addWidget(self.tooltip_projectname, 4, 4, 1, 1)

        self.Titel_label = QLabel(Dialog)
        self.Titel_label.setObjectName(u"Titel_label")

        self.gridLayout.addWidget(self.Titel_label, 5, 1, 1, 1)

        self.Titel_entry = QTextEdit(Dialog)
        self.Titel_entry.setObjectName(u"Titel_entry")
        self.Titel_entry.setEnabled(False)
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.Titel_entry.sizePolicy().hasHeightForWidth())
        self.Titel_entry.setSizePolicy(sizePolicy1)
        self.Titel_entry.setMaximumSize(QSize(16777215, 75))
        self.Titel_entry.setAutoFillBackground(False)

        self.gridLayout.addWidget(self.Titel_entry, 5, 3, 1, 1)

        self.Documentnr_label = QLabel(Dialog)
        self.Documentnr_label.setObjectName(u"Documentnr_label")

        self.gridLayout.addWidget(self.Documentnr_label, 6, 1, 1, 1)

        self.Documentnr_entry = QLineEdit(Dialog)
        self.Documentnr_entry.setObjectName(u"Documentnr_entry")
        self.Documentnr_entry.setAlignment(Qt.AlignCenter)
        self.Documentnr_entry.setText("1")
        self.Documentnr_entry.textChanged.connect(self.update_report_title)

        self.gridLayout.addWidget(self.Documentnr_entry, 6, 3, 1, 1, Qt.AlignmentFlag.AlignHCenter)

        self.tooltip_versionnr = HoverImageLabel(display_image=self.questionmark_img, content_type="text", content="Ret kun, hvis andet dokumentnr. skal bruges til afrapporteringen")

        self.gridLayout.addWidget(self.tooltip_versionnr, 6, 4, 1, 1, Qt.AlignmentFlag.AlignHCenter)

        self.versionnr_label = QLabel(Dialog)
        self.versionnr_label.setObjectName(u"versionnr_label")

        self.gridLayout.addWidget(self.versionnr_label, 7, 1, 1, 1)

        self.versionnr_entry = QLineEdit(Dialog)
        self.versionnr_entry.setObjectName(u"versionnr_entry")
        self.versionnr_entry.setAlignment(Qt.AlignCenter)
        self.versionnr_entry.setText("1")
        self.versionnr_entry.textChanged.connect(self.update_report_title)

        self.gridLayout.addWidget(self.versionnr_entry, 7, 3, 1, 1, Qt.AlignmentFlag.AlignHCenter)

        self.tooltip_versionnr = HoverImageLabel(display_image=self.questionmark_img, content_type="text", content="Ret kun, hvis andet versionsnr. skal bruges til afrapporteringen")

        self.gridLayout.addWidget(self.tooltip_versionnr, 7, 4, 1, 1, Qt.AlignmentFlag.AlignHCenter)

        self.documentname_label = QLabel(Dialog)
        self.documentname_label.setObjectName(u"documentname_label")

        self.gridLayout.addWidget(self.documentname_label, 8, 1, 1, 1)

        self.documentname_entry_final = QLineEdit(Dialog)
        self.documentname_entry_final.setObjectName(u"documentname_entry_final")
        self.documentname_entry_final.setEnabled(False)
        self.documentname_entry_final.setClearButtonEnabled(False)
        self.documentname_entry_final.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.documentname_entry_final, 8, 3, 1, 1)

        self.customer_label = QLabel(Dialog)
        self.customer_label.setObjectName(u"customer_label")

        self.gridLayout.addWidget(self.customer_label, 9, 1, 1, 1)

        self.customer_entry = QLineEdit(Dialog)
        self.customer_entry.setObjectName(u"customer_entry")
        self.customer_entry.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.customer_entry, 9, 3, 1, 1)

        self.created_label = QLabel(Dialog)
        self.created_label.setObjectName(u"created_label")

        self.gridLayout.addWidget(self.created_label, 10, 1, 1, 1)

        self.created_entry = QLineEdit(Dialog)
        self.created_entry.setObjectName(u"created_entry")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.created_entry.sizePolicy().hasHeightForWidth())
        self.created_entry.setSizePolicy(sizePolicy)
        self.created_entry.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.created_entry, 10, 3, 1, 1, Qt.AlignmentFlag.AlignHCenter)

        self.controlled_label = QLabel(Dialog)
        self.controlled_label.setObjectName(u"controlled_label")

        self.gridLayout.addWidget(self.controlled_label, 11, 1, 1, 1)

        self.checked_entry = QLineEdit(Dialog)
        self.checked_entry.setObjectName(u"checked_entry")
        sizePolicy.setHeightForWidth(self.checked_entry.sizePolicy().hasHeightForWidth())
        self.checked_entry.setSizePolicy(sizePolicy)
        self.checked_entry.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.checked_entry, 11, 3, 1, 1, Qt.AlignmentFlag.AlignHCenter)

        self.approved_label = QLabel(Dialog)
        self.approved_label.setObjectName(u"approved_label")

        self.gridLayout.addWidget(self.approved_label, 12, 1, 1, 1)
        
        self.approved_entry = QLineEdit(Dialog)
        self.approved_entry.setObjectName(u"approved_entry")
        sizePolicy.setHeightForWidth(self.approved_entry.sizePolicy().hasHeightForWidth())
        self.approved_entry.setSizePolicy(sizePolicy)
        self.approved_entry.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.approved_entry, 12, 3, 1, 1, Qt.AlignmentFlag.AlignHCenter)

        self.date_label = QLabel(Dialog)
        self.date_label.setObjectName(u"date_label")

        self.gridLayout.addWidget(self.date_label, 13, 1, 1, 1)

        self.date_entry = QDateEdit(Dialog)
        self.date_entry.setObjectName(u"date_entry")
        sizePolicy.setHeightForWidth(self.date_entry.sizePolicy().hasHeightForWidth())
        self.date_entry.setSizePolicy(sizePolicy)
        self.date_entry.setAlignment(Qt.AlignCenter)
        self.date_entry.setDate(QDate.currentDate())
        self.date_entry.setDisplayFormat("yyyy-MM-dd")

        self.gridLayout.addWidget(self.date_entry, 13, 3, 1, 1, Qt.AlignmentFlag.AlignHCenter)

        self.output_label = QLabel(Dialog)
        self.output_label.setObjectName(u"output_label")

        self.gridLayout.addWidget(self.output_label, 14, 1, 1, 1)

        self.output_entry = QLineEdit(Dialog)
        self.output_entry.setObjectName(u"output_entry")

        self.gridLayout.addWidget(self.output_entry, 14, 3, 1, 1)

        self.browse_button = QPushButton(Dialog)
        self.browse_button.setObjectName(u"browse_button")
        self.browse_button.clicked.connect(self.browse_folder)

        self.gridLayout.addWidget(self.browse_button, 14, 4, 1, 1)

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

    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.output_entry.setText(folder)

    def on_id_entry(self):
        self.project_id = self.InfraID_entry.text()
        self.path_project_json = os.path.join(self.path_project_list, f"{self.project_id}.json")

        if self.collected_data != None and self.project_id == self.collected_data["project_ID"]:
            self.final_data = self.collected_data
            self.project_reentry = True
        else:
            if os.path.exists(self.path_project_json):
                self.final_data = load_json(self.path_project_json)
                self.project_reentry = True
            else:
                self.final_data = {}
                self.project_reentry = False

        if self.project_id:
            self.update_project_details()
    
    def update_project_details(self):
        from basic_functions import project_ID_to_ATR
        # Fetch details from API
        try:
            self.atr, self.name, self.customer = project_ID_to_ATR(self.project_id, self.credential, self.token)
        except:
            self.atr, self.name, self.customer = None, None, None
        
        

        if self.atr and self.name:
            self.ATR_entry.setText(self.atr)
            self.Project_entry.setText(self.name)
            self.customer_entry.setText(self.customer)
        
        if self.project_reentry:
            self.documentnr_number = str(int(self.final_data["documentnr"].split(".")[1]))
            self.versionnr_number = f'{float(self.final_data["versionsnr"]):.1f}'
            self.Documentnr_entry.setText(self.documentnr_number)
            self.versionnr_entry.setText(self.versionnr_number)
            self.customer_entry.setText(self.final_data["customer"])
            self.created_entry.setText(self.final_data["created"])
            self.checked_entry.setText(self.final_data["checked"])
            self.approved_entry.setText(self.final_data["approved"])

    def update_report_title(self):
        import re
        # Debugging print to check if the function is called

        # Get the project name from the relevant variable
        self.project_name = self.project_manual_entry.text() if self.project_manual_entry.text() else self.Project_entry.text()
        self.documentnr = self.Documentnr_entry.text() if self.Documentnr_entry.text() else "1"
        self.versionnr = self.versionnr_entry.text() if self.versionnr_entry.text() else "1"

        match = re.search(r'\d+$', self.documentnr)  # Find the last sequence of digits
        if match:
            self.documentnr = match.group()  # Extract the matched digits
        else:
            self.documentnr = '1'  # Default to '1' if no digits found

        # Format documentnr as a three-digit number

        self.documentnr = f"{int(self.documentnr):03d}"
        self.versionnr = f"{float(self.versionnr):.1f}"
        
        self.Titel_entry.clear()
        self.Titel_entry.setAlignment(Qt.AlignCenter)
        self.Titel_entry.insertPlainText(f"Vibrationsovervågning,\n{self.project_name}")

        if self.versionnr == "1.0":
            self.documentname_entry_final.setText(f"{self.ATR_entry.text()}.{self.documentnr}")
        else:
            self.documentname_entry_final.setText(f"{self.ATR_entry.text()}.{self.documentnr}_{self.versionnr}")
        
    def on_cancel_pressed(self):
        self.reject()

    def validate_and_proceed(self):
        self.date = self.date_entry.date()

        self.date = self.date.toString('yyyy-MM-dd')

        if self.final_data != {}:
            try:
                self.final_data.update({
                "project_ID": self.InfraID_entry.text(),
                "project_atr": self.ATR_entry.text(),
                "project_name": self.project_manual_entry.text() if self.project_manual_entry.text() else self.Project_entry.text(),
                "city": self.project_manual_entry.text().split(",")[1][1:] if self.project_manual_entry.text() else self.Project_entry.text().split(",")[1][1:],
                "road": self.project_manual_entry.text().split(",")[0] if self.project_manual_entry.text() else self.Project_entry.text().split(",")[0],
                "versionsnr": self.versionnr,
                "documentnr": self.documentname_entry_final.text(),
                "customer": self.customer_entry.text(),
                "created": self.created_entry.text(),
                "checked": self.checked_entry.text(),
                "approved": self.approved_entry.text(),
                "date_submitted": self.date,
                "output_folder": self.output_entry.text()
                })
            except:
                self.final_data.update({
                "project_ID": self.InfraID_entry.text(),
                "project_atr": self.ATR_entry.text(),
                "project_name": self.project_manual_entry.text() if self.project_manual_entry.text() else self.Project_entry.text(),
                "city": "",
                "road": "",
                "versionsnr": self.versionnr,
                "documentnr": self.documentname_entry_final.text(),
                "customer": self.customer_entry.text(),
                "created": self.created_entry.text(),
                "checked": self.checked_entry.text(),
                "approved": self.approved_entry.text(),
                "date_submitted": self.date,
                "output_folder": self.output_entry.text()
                })

        else:
            try:
                self.final_data = {
                "project_ID": self.InfraID_entry.text(),
                "project_atr": self.ATR_entry.text(),
                "project_name": self.project_manual_entry.text() if self.project_manual_entry.text() else self.Project_entry.text(),
                "city": self.project_manual_entry.text().split(",")[1][1:] if self.project_manual_entry.text() else self.Project_entry.text().split(",")[1][1:],
                "road": self.project_manual_entry.text().split(",")[0] if self.project_manual_entry.text() else self.Project_entry.text().split(",")[0],
                "versionsnr": self.versionnr,
                "documentnr": self.documentname_entry_final.text(),
                "customer": self.customer_entry.text(),
                "created": self.created_entry.text(),
                "checked": self.checked_entry.text(),
                "approved": self.approved_entry.text(),
                "date_submitted": self.date,
                "output_folder": self.output_entry.text()
                }
            except:
                self.final_data = {
                "project_ID": self.InfraID_entry.text(),
                "project_atr": self.ATR_entry.text(),
                "project_name": self.project_manual_entry.text() if self.project_manual_entry.text() else self.Project_entry.text(),
                "city": "",
                "road": "",
                "versionsnr": self.versionnr,
                "documentnr": self.documentname_entry_final.text(),
                "customer": self.customer_entry.text(),
                "created": self.created_entry.text(),
                "checked": self.checked_entry.text(),
                "approved": self.approved_entry.text(),
                "date_submitted": self.date,
                "output_folder": self.output_entry.text()
                }
        
        if any(value == "" for key, value in self.final_data.items() if key not in {"city", "road"}):
            self.logger.log("Mindst et felt er ikke udfyldt. Udfyld venligst alle felter (Udover 'Projekt' hvis dette ikke er relevant)")
            return

        check_drive, _ = os.path.splitdrive(self.final_data["output_folder"])

        if check_drive != "C:":
            self.logger.log("Output-stien skal være på C: drevet! Ret venligst dette.")
            return


        self.accept()
    
    def get_data(self):    
        self.final_data["pdf_path"] = os.path.join(self.final_data["output_folder"], f"{self.final_data['documentnr']}.pdf")

        self.onedrive_ui_window = OneDrive_linkUI(self.final_data["pdf_path"], self.final_data)
        res = self.onedrive_ui_window.exec()
        if res == QDialog.Accepted:
            self.final_data["onedrive_link"] = self.onedrive_ui_window.get_data()

        save_json(self.final_data, self.path_project_json)

        return self.final_data
    
    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        #self.tooltip_versionnr.setText(QCoreApplication.translate("Dialog", u"?", None))
        self.ATR_label.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p>ATR:</p></body></html>", None))
        self.Project_label.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p>Projekt:</p></body></html>", None))
        self.controlled_label.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p>Kontrolleret:</p></body></html>", None))
        self.Titel_label.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p>Titel:</p></body></html>", None))
        #self.tooltip_projectname.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"center\">?</p></body></html>", None))
        self.created_label.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p>Udarbejdet:</p></body></html>", None))
        self.date_label.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p>Udgivelsesdato:</p></body></html>", None))
        self.browse_button.setText(QCoreApplication.translate("Dialog", u"Browse", None))
        self.customer_label.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p>Kunde:</p></body></html>", None))
        self.Documentnr_label.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p>Dokumentnr.:</p></body></html>", None))
        self.approved_label.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p>Godkendt:</p></body></html>", None))
        self.documentname_label.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p>Dokumentnavn:</p></body></html>", None))
        self.InfraID_label.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p>INFRA ID:</p></body></html>", None))
        self.versionnr_label.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p>Versionsnr.:</p></body></html>", None))
        self.output_label.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p>Output sti:</p></body></html>", None))
        #self.tooltip_ID.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"center\">?</p></body></html>", None))
        self.cancel_button.setText(QCoreApplication.translate("Dialog", u"Annuller", None))
        self.continue_button.setText(QCoreApplication.translate("Dialog", u"Forts\u00e6t", None))
        self.created_by_label.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"center\">Udarbejdet af MLHU</p></body></html>", None))
        #self.image_placeholder.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"center\">TextLabel</p></body></html>", None))
        self.empty_label_placeholder.setText("")

class OneDrive_linkUI(QDialog):
    def __init__(self, pdf_path, collected_data, parent=None):
        super().__init__(parent)

        self.pdf_path = pdf_path
        self.collected_data = collected_data

        self.initial_settings()

        self.setupUi(self)

    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(448, 173)
        self.verticalLayout_2 = QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label, 0, Qt.AlignmentFlag.AlignHCenter)

        self.pdf_path_label = QLabel(Dialog)
        self.pdf_path_label.setObjectName(u"label_2")

        self.verticalLayout.addWidget(self.pdf_path_label, 0, Qt.AlignmentFlag.AlignHCenter)

        self.label_3 = QLabel(Dialog)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout.addWidget(self.label_3, 0, Qt.AlignmentFlag.AlignHCenter)

        self.lineEdit = QLineEdit(Dialog)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setAlignment(Qt.AlignCenter)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy)
        self.lineEdit.setMinimumSize(QSize(400, 0))
        self.lineEdit.setMaximumSize(QSize(250, 16777215))
        try:
            self.lineEdit.setText(self.collected_data["onedrive_link"] if self.collected_data != {} else "")
        except KeyError:
            self.lineEdit.setText("")

        self.verticalLayout.addWidget(self.lineEdit, 0, Qt.AlignmentFlag.AlignHCenter)

        self.continue_button = QPushButton(Dialog)
        self.continue_button.setObjectName(u"pushButton")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.continue_button.sizePolicy().hasHeightForWidth())
        self.continue_button.setSizePolicy(sizePolicy1)
        self.continue_button.clicked.connect(self.on_submit)

        self.verticalLayout.addWidget(self.continue_button, 0, Qt.AlignmentFlag.AlignHCenter)


        self.verticalLayout_2.addLayout(self.verticalLayout)


        self.retranslateUi(Dialog)

    def initial_settings(self):
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas

        if not os.path.exists(self.pdf_path):
            c = canvas.Canvas(self.pdf_path, pagesize=letter)
            c.save()
        
    def on_submit(self):
        if self.clean_url():
            self.accept()

    def clean_url(self):
        import re
        self.url = self.lineEdit.text()

        if self.url != "":
            self.cleaned_url = self.url.replace("%C3%A6", "æ")
            self.cleaned_url = self.cleaned_url.replace("%C3%B8", "ø")
            self.cleaned_url = self.cleaned_url.replace("%C3%A5", "å")
            self.cleaned_url = self.cleaned_url.replace("%C3%85", "Å")
            

            self.cleaned_url = re.sub(r'%[0-9A-Fa-f]{2}', lambda m: m.group(0) if m.group(0) == '%20' else '', self.cleaned_url)
            self.cleaned_url = self.cleaned_url.replace('%20', ' ')  # Convert %20 back to a space
            self.cleaned_url = re.sub(r':b:/r/', '', self.cleaned_url)  # Remove ":b:/r/"
            self.cleaned_url = re.sub(r'\?.*$', '', self.cleaned_url)  # Remove query parameters starting from "?"
            return True
        else:
            QMessageBox.warning(None, None, f"Indtast en Onedrive sti")
            return False
    
    def get_data(self):
        return self.cleaned_url

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"En ny fil er lavet her:", None))
        self.pdf_path_label.setText(QCoreApplication.translate("Dialog", u"{}".format(self.pdf_path), None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"Kopier Onedrive-stien ned herunder:", None))
        self.continue_button.setText(QCoreApplication.translate("Dialog", u"Forts\u00e6t", None))
    # retranslateUi

class reorder_MeasuringPoints_UI(QDialog):
    def __init__(self, cache_main_dir, parent=None):
        super().__init__(parent)

        self.cache_main_dir = cache_main_dir

        self.info_dict = load_json(os.path.join(cache_main_dir, "API", "project_sensor_dict_final.json"))
        self.info_first_dict = load_json(os.path.join(cache_main_dir, "API", "project_sensor.json"))
        self.trans_dict = load_json(os.path.join(cache_main_dir, "Results", "trans_dict.json"))

        self.adresses = list(self.info_dict.keys())

        # Create a mapping of base addresses to their subaddresses
        self.base_to_subs = {}
        for address in self.adresses:
            base_address = address.split('_')[0]
            if base_address not in self.base_to_subs:
                self.base_to_subs[base_address] = []
            self.base_to_subs[base_address].append(address)

        self.setupUi(self)

    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(317, 563)
        self.verticalLayout_2 = QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.titel_label = QLabel(Dialog)
        self.titel_label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.titel_label)

        self.number_adress_label = QLabel(Dialog)
        self.number_adress_label.setObjectName(u"label_2")
        self.number_adress_label.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"center\"><span style=\" font-size:11pt;\">Antal m\u00e5lepunkter: {}</span></p></body></html>".format(len(self.base_to_subs)), None))
        

        self.verticalLayout.addWidget(self.number_adress_label)

        self.scrollArea = QScrollArea(Dialog)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 295, 449))
        self.verticalLayout_3 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")

        self.list_addresses()

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(-1, 0, -1, -1)

        self.cancel_button = QPushButton(Dialog)
        self.cancel_button.setObjectName(u"pushButton")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.cancel_button.sizePolicy().hasHeightForWidth())
        self.cancel_button.setSizePolicy(sizePolicy1)
        self.cancel_button.clicked.connect(self.on_cancel_pressed)

        self.horizontalLayout.addWidget(self.cancel_button)

        self.continue_button = QPushButton(Dialog)
        self.continue_button.setObjectName(u"pushButton_2")
        self.continue_button.setSizePolicy(sizePolicy1)
        self.continue_button.clicked.connect(self.submit_reorder)

        self.horizontalLayout.addWidget(self.continue_button)


        self.verticalLayout_2.addLayout(self.horizontalLayout)


        self.retranslateUi(Dialog)

    def list_addresses(self):
        self.entries = []
        self.variables = {}
        self.sub_adresses_entries = {}

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")

        self.gridLayout.setColumnMinimumWidth(1, 5)
        self.gridLayout.setColumnMinimumWidth(2, 125)

        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        
        row = 0

        for i, address in enumerate(self.base_to_subs):
            label = QLabel(self.scrollAreaWidgetContents)
            label.setObjectName(u"label")
            label.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-weight:700;\">{}</span></p></body></html>".format(address), None))

            self.gridLayout.addWidget(label, row, 1, 1, 1)

            self.variables[address] = QLineEdit(self.scrollAreaWidgetContents)
            self.variables[address].setObjectName(u"lineEdit")
            sizePolicy.setHeightForWidth(self.variables[address].sizePolicy().hasHeightForWidth())
            self.variables[address].setSizePolicy(sizePolicy)
            self.variables[address].setMaximumSize(QSize(50, 10000))
            self.variables[address].textChanged.connect(self.sync_text)

            self.gridLayout.addWidget(self.variables[address], row, 2, 1, 1)#, Qt.AlignmentFlag.AlignHCenter)

            self.entries.append((address, self.variables[address]))

            row += 1
            for sub_address in sorted(self.base_to_subs[address]):
                if "_" in sub_address:
                    label = QLabel(self.scrollAreaWidgetContents)
                    label.setObjectName(u"label")
                    label.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-weight:700;\">{}</span></p></body></html>".format(sub_address), None))

                    self.gridLayout.addWidget(label, row, 1, 1, 1)

                    self.sub_adresses_entries[sub_address] = QLineEdit(self.scrollAreaWidgetContents)
                    self.sub_adresses_entries[sub_address].setObjectName(u"lineEdit")
                    sizePolicy.setHeightForWidth(self.sub_adresses_entries[sub_address].sizePolicy().hasHeightForWidth())
                    self.sub_adresses_entries[sub_address].setSizePolicy(sizePolicy)
                    self.sub_adresses_entries[sub_address].setMaximumSize(QSize(50, 10000))
                    self.sub_adresses_entries[sub_address].setEnabled(False)

                    self.entries.append((sub_address, self.sub_adresses_entries[sub_address]))

                    self.gridLayout.addWidget(self.sub_adresses_entries[sub_address], row, 2, 1, 1)#, Qt.AlignmentFlag.AlignHCenter)

                    row += 1


        self.verticalSpacer = QSpacerItem(20, 5, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer)

        self.verticalLayout_3.addLayout(self.gridLayout)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout.addWidget(self.scrollArea)


        self.verticalLayout_2.addLayout(self.verticalLayout)

    def sync_text(self):
        for sub_address in self.sub_adresses_entries:
            base_adress = sub_address.split('_')[0]
            if self.variables[base_adress].text():
                self.sub_adresses_entries[sub_address].setText(self.variables[base_adress].text())
            else:
                self.sub_adresses_entries[sub_address].setText("")

    def on_cancel_pressed(self):
        self.reject()

    def submit_reorder(self):
        try:
            self.new_order = []
            self.base_positions = {}

            for address, entry in self.entries:
                if "_" not in address:
                    position = int(entry.text()) - 1
                    self.base_positions[address] = position
                else:
                    base_address = address.split('_')[0]
                    if base_address in self.base_positions:
                        position = self.base_positions[base_address]
                    else:
                        raise ValueError(f"Base address for {address} not found")
                    
                self.new_order.append((position, address))
            
            self.new_order.sort(key=lambda x: x[0])

            self.reordered_addresses = []
            self.positions_seen = set()

            for position, address in self.new_order:
                if position not in self.positions_seen:
                    self.reordered_addresses.append(address)
                    self.positions_seen.add(position)
                else:
                    base_address = address.split('_')[0]
                    for i, existing_address in enumerate(self.reordered_addresses):
                        if existing_address == base_address:
                            self.reordered_addresses.insert(i+1, address)
                            break
            

            self.reordered_info_dict = {address: self.info_dict[address] for address in self.reordered_addresses}
            self.reordered_info_first_dict = {address: self.info_first_dict[address] for address in self.reordered_addresses}
            self.reordered_trans_dict = {address: self.trans_dict[address] for address in self.reordered_addresses}

            save_json(self.reordered_info_dict, os.path.join(self.cache_main_dir, "API", "project_sensor_dict_final.json"))
            save_json(self.reordered_info_first_dict, os.path.join(self.cache_main_dir, "API", "project_sensor.json"))
            save_json(self.reordered_trans_dict, os.path.join(self.cache_main_dir, "Results", "trans_dict.json"))
        except ValueError:
            QMessageBox.critical(None, None, f"Indtast venligst en gyldig position (1 til {len(self.base_to_subs)}) for {address}")

        self.accept()

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"R\u00e6kkef\u00f8lge af m\u00e5lepunkter", None))
        self.titel_label.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"center\"><span style=\" font-size:16pt; font-weight:700;\">R\u00e6kkef\u00f8lge af m\u00e5lepunkter</span></p></body></html>", None))
        
        self.cancel_button.setText(QCoreApplication.translate("Dialog", u"Annuller", None))
        self.continue_button.setText(QCoreApplication.translate("Dialog", u"Forts\u00e6t", None))
    # retranslateUi

class introduction_UI(QDialog):
    def __init__(self, collected_data, cache_main_dir, parent=None):
        super().__init__(parent)

        self.collected_data = collected_data
        self.cache_main_dir = cache_main_dir

        self.file_text = os.path.join(self.cache_main_dir, "Rapport", "Tekst", "Indledning.md")

        self.initial_settings()

        self.setupUi(self)

    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")

        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)


        Dialog.resize(370, 630)
        self.verticalLayout_2 = QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(-1, -1, -1, 0)
        self.info_label = QLabel(Dialog)
        self.info_label.setObjectName(u"info_label")

        self.verticalLayout.addWidget(self.info_label)

        self.textEdit = QTextEdit(Dialog)
        self.textEdit.setObjectName(u"textEdit")

        self.verticalLayout.addWidget(self.textEdit)

        self.verticalSpacer = QSpacerItem(20, 5, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(-1, 0, -1, -1)

        self.customer_label = QLabel(Dialog)
        self.customer_label.setObjectName(u"customer_label")

        self.gridLayout.addWidget(self.customer_label, 0, 1, 1, 1)

        self.customer_entry = QLineEdit(Dialog)
        self.customer_entry.setObjectName(u"customer_entry")
        self.customer_entry.setMaximumSize(QSize(250, 100))
        self.customer_entry.setText(self.predefined_values["CUSTOMER"])
        self.customer_entry.setEnabled(False)

        self.gridLayout.addWidget(self.customer_entry, 0, 2, 1, 1, Qt.AlignmentFlag.AlignHCenter)

        self.road_label = QLabel(Dialog)
        self.road_label.setObjectName(u"road_label")

        self.gridLayout.addWidget(self.road_label, 1, 1, 1, 1)

        self.road_entry = QLineEdit(Dialog)
        self.road_entry.setObjectName(u"road_entry")
        self.road_entry.setMaximumSize(QSize(250, 100))
        self.road_entry.setText(self.predefined_values["ROAD"])
        self.road_entry.setEnabled(False)

        self.gridLayout.addWidget(self.road_entry, 1, 2, 1, 1, Qt.AlignmentFlag.AlignHCenter)

        self.horizontalSpacer_2 = QSpacerItem(10, 20, QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_2, 2, 0, 1, 1)

        self.city_label = QLabel(Dialog)
        self.city_label.setObjectName(u"city_label")

        self.gridLayout.addWidget(self.city_label, 2, 1, 1, 1)

        self.city_entry = QLineEdit(Dialog)
        self.city_entry.setObjectName(u"city_entry")
        self.city_entry.setMaximumSize(QSize(250, 100))
        self.city_entry.setText(self.predefined_values["CITY"])
        self.city_entry.setEnabled(False)

        self.gridLayout.addWidget(self.city_entry, 2, 2, 1, 1, Qt.AlignmentFlag.AlignHCenter)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 2, 3, 1, 1)

        self.dateFrom_label = QLabel(Dialog)
        self.dateFrom_label.setObjectName(u"dateFrom_label")

        self.gridLayout.addWidget(self.dateFrom_label, 3, 1, 1, 1)

        self.dateFrom_entry = QLineEdit(Dialog)
        self.dateFrom_entry.setObjectName(u"dateFrom_entry")
        self.dateFrom_entry.setMaximumSize(QSize(250, 100))
        self.dateFrom_entry.setText(self.predefined_values["DATE_FROM"])
        self.dateFrom_entry.setEnabled(False)

        self.gridLayout.addWidget(self.dateFrom_entry, 3, 2, 1, 1, Qt.AlignmentFlag.AlignHCenter)

        self.dateTo_label = QLabel(Dialog)
        self.dateTo_label.setObjectName(u"dateTo_label")

        self.gridLayout.addWidget(self.dateTo_label, 4, 1, 1, 1)

        self.dateTo_entry = QLineEdit(Dialog)
        self.dateTo_entry.setObjectName(u"dateTo_entry")
        self.dateTo_entry.setMaximumSize(QSize(250, 100))
        self.dateTo_entry.setText(self.predefined_values["DATE_TO"])
        self.dateTo_entry.setEnabled(False)

        self.gridLayout.addWidget(self.dateTo_entry, 4, 2, 1, 1, Qt.AlignmentFlag.AlignHCenter)

        self.verticalLayout.addLayout(self.gridLayout)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(-1, -1, -1, 0)
        self.cancel_button = QPushButton(Dialog)
        self.cancel_button.setObjectName(u"cancel_button")
        sizePolicy.setHeightForWidth(self.cancel_button.sizePolicy().hasHeightForWidth())
        self.cancel_button.setSizePolicy(sizePolicy)
        self.cancel_button.setMaximumSize(QSize(75, 100))
        self.cancel_button.clicked.connect(self.on_cancel_pressed)

        self.horizontalLayout.addWidget(self.cancel_button)

        self.continue_button = QPushButton(Dialog)
        self.continue_button.setObjectName(u"continue_button")
        self.continue_button.setMaximumSize(QSize(75, 100))
        self.continue_button.clicked.connect(self.on_continue_pressed)

        self.horizontalLayout.addWidget(self.continue_button)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.update_text()

        self.retranslateUi(Dialog)

    def initial_settings(self):

        self.predefined_values = {
        "CUSTOMER": self.collected_data["customer"],
        "ROAD": self.collected_data["road"],
        "CITY": self.collected_data["city"],
        "DATE_FROM": self.collected_data["date_from"],
        "DATE_TO": self.collected_data["date_to"]
        }

        self.row_names = ["Kunde", "Vej", "By", "Arbejde", "Dato fra", "Dato til"]

        if os.path.exists(self.file_text):
            self.template_text = open(self.file_text, "r", encoding="utf-8").read()
        else:
            self.template_text = (
                "COWI A/S har foretaget vibrationsovervågning for {CUSTOMER} af udvalgte "
                "ejendomme langs {ROAD} i {TOWN} i forbindelse med #ARBEJDE#.\n\n"
                "Målingerne har haft til hensigt at sammenholde den påførte vibrationspåvirkning "
                "på ejendommene med gældende grænseværdi.\n\n"
                "Måleinstrumenterne er placeret på repræsentative ejendomme tæt på kritiske aktiviteter, "
                "mens der i hele perioden er udført arbejder langs {ROAD} i {TOWN}. Målingerne udelukker "
                "derfor ikke, at der kan have været en ikke uvæsentlig vibrationspåvirkning på øvrige ejendomme.\n\n"
                "Måleperioden har været d. {day_from}. {month_from} {year_from} – {day_to}. {month_to} {year_to}."
            )

    def parse_dates(self, date_str):
        from basic_functions import month_danish

        try:
            day, month, year = date_str.split(".")
            day = str(int(day))
            return day, month_danish(int(month)), year
        except ValueError:
            return "??", "Ukendt måned", "????"  # Return placeholders if date format is invalid

    def update_text(self):
        #global values
        # Get current values for dates and parse them
        day_from, month_from, year_from = self.parse_dates(self.dateFrom_entry.text())
        day_to, month_to, year_to = self.parse_dates(self.dateTo_entry.text())
        
        # Gather values from input fields (manual entries or predefined)
        values = {
            "CUSTOMER": self.customer_entry.text() or self.predefined_values["CUSTOMER"],
            "ROAD": self.road_entry.text() or self.predefined_values["ROAD"],
            "TOWN": self.city_entry.text() or self.predefined_values["TOWN"],
            "day_from": day_from, "month_from": month_from, "year_from": year_from,
            "day_to": day_to, "month_to": month_to, "year_to": year_to
        }

        self.collected_data["road"] = values["ROAD"]
        self.collected_data["city"] = values["TOWN"]
        self.collected_data["customer"] = values["CUSTOMER"]
        #data["work"] = values["WORK"]
        

        # Update the text area with formatted text
        self.formatted_text = self.template_text.format(**values)

        self.textEdit.setPlainText(self.formatted_text)

    def on_cancel_pressed(self):
        self.reject()

    def on_continue_pressed(self):

        with open(self.file_text, "w", encoding="utf-8") as f:
            f.write(self.textEdit.toPlainText())

        self.accept()

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Indledning", None))
        self.info_label.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; font-weight:700;\">Forslag til kapitel 1 <br/></span><span style=\" font-size:14pt; font-weight:700; font-style:italic;\">Indledning</span></p></body></html>", None))
        self.city_label.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">By</p></body></html>", None))
        self.customer_label.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">Kunde</p></body></html>", None))
        self.dateTo_label.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">Dato til</p></body></html>", None))
        self.dateFrom_label.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">Dato fra</p></body></html>", None))
        self.road_label.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">Vej</p></body></html>", None))
        self.cancel_button.setText(QCoreApplication.translate("Dialog", u"Annuller", None))
        self.continue_button.setText(QCoreApplication.translate("Dialog", u"Forts\u00e6t", None))

class work_info_UI(QDialog):
    def __init__(self, cache_main_dir, parent=None):
        super().__init__(parent)

        self.cache_main_dir = cache_main_dir

        self.file_path = os.path.join(self.cache_main_dir, "Rapport","Tekst","Anlægsarbejde.md") 

        self.initial_settings()

        self.setupUi(self)

    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")

        Dialog.resize(460, 550)
        self.verticalLayout_2 = QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(-1, -1, -1, 0)
        self.info_label = QLabel(Dialog)
        self.info_label.setObjectName(u"info_label")

        self.verticalLayout.addWidget(self.info_label)

        self.textEdit = QTextEdit(Dialog)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setText(self.predefined_text)
        for activity in self.activities:
            self.textEdit.append(f"• {activity}")

        self.verticalLayout.addWidget(self.textEdit)

        self.verticalSpacer = QSpacerItem(20, 5, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label, 0, Qt.AlignmentFlag.AlignHCenter)

        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setSpacing(7)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(-1, 10, -1, -1)
        
        self.comboBoxes = []
        for activity in self.activities:
            self.add_input_field(Dialog, activity)


        self.verticalLayout.addLayout(self.verticalLayout_3)

        self.verticalSpacer_2 = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(-1, -1, -1, 0)
        self.remove_work_button = QPushButton(Dialog)
        self.remove_work_button.setObjectName(u"remove_work_button")
        self.remove_work_button.setMinimumSize(QSize(100, 0))
        self.remove_work_button.setMaximumSize(QSize(100, 100))
        self.remove_work_button.clicked.connect(self.remove_input_field)

        self.gridLayout.addWidget(self.remove_work_button, 0, 1, 1, 1, Qt.AlignmentFlag.AlignHCenter)

        self.add_work_button = QPushButton(Dialog)
        self.add_work_button.setObjectName(u"add_work_button")
        sizePolicy.setHeightForWidth(self.add_work_button.sizePolicy().hasHeightForWidth())
        self.add_work_button.setSizePolicy(sizePolicy)
        self.add_work_button.setMinimumSize(QSize(100, 0))
        self.add_work_button.setMaximumSize(QSize(125, 100))
        self.add_work_button.clicked.connect(lambda checked, d = Dialog, a = self.activities[0]: self.add_input_field(d, a))

        self.gridLayout.addWidget(self.add_work_button, 0, 0, 1, 1, Qt.AlignmentFlag.AlignHCenter)

        self.cancel_button = QPushButton(Dialog)
        self.cancel_button.setObjectName(u"cancel_button")
        sizePolicy.setHeightForWidth(self.cancel_button.sizePolicy().hasHeightForWidth())
        self.cancel_button.setSizePolicy(sizePolicy)
        self.cancel_button.setMinimumSize(QSize(75, 0))
        self.cancel_button.setMaximumSize(QSize(75, 100))
        self.cancel_button.clicked.connect(self.on_cancel_pressed)

        self.gridLayout.addWidget(self.cancel_button, 1, 0, 1, 1, Qt.AlignmentFlag.AlignHCenter)

        self.continue_button = QPushButton(Dialog)
        self.continue_button.setObjectName(u"continue_button")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.continue_button.sizePolicy().hasHeightForWidth())
        self.continue_button.setSizePolicy(sizePolicy1)
        self.continue_button.setMinimumSize(QSize(75, 0))
        self.continue_button.clicked.connect(self.on_submit)

        self.gridLayout.addWidget(self.continue_button, 1, 1, 1, 1, Qt.AlignmentFlag.AlignHCenter)

        self.verticalLayout.addLayout(self.gridLayout)

        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(Dialog)

    def initial_settings(self):
        drive = "O:"
        path_to_options = os.path.join("A000000", "A004371", "3_Pdoc", "Afrapportering", "files", "saved_work_suggestions")
        option_file = os.path.join(path_to_options, "saved_work_suggestions.txt")
        option_file = os.path.normpath(drive + os.sep + option_file)     

        with open(option_file, "r", encoding="utf-8") as f:
            self.input_value_options = f.read().splitlines()

        
        if os.path.exists(self.file_path):
            with open(self.file_path, "r", encoding="utf-8") as f:
                self.content = f.read()
            
            lines = self.content.splitlines()

            self.predefined_text = lines[0]

            self.activities = [line.strip("- ") for line in lines[1:]] 
        
        else:
            self.predefined_text = "Entreprenørens arbejde har bestået af følgende overordnede aktiviteter:\n"
            self.activities = ["Jordarbejder", "Kloakarbejder", "Komprimeringsarbejder", "Asfalt og andre belægningsarbejder"]

    def add_input_field(self, Dialog, activity):
        
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)

        comboBox = QComboBox(Dialog)
        comboBox.addItems(self.input_value_options)
        comboBox.setObjectName(u"comboBox")
        sizePolicy.setHeightForWidth(comboBox.sizePolicy().hasHeightForWidth())
        comboBox.setSizePolicy(sizePolicy)
        comboBox.setMinimumSize(QSize(250, 0))
        comboBox.setMaximumSize(QSize(500, 100))
        comboBox.setEditable(True)
        comboBox.setCurrentText(activity)
        comboBox.currentTextChanged.connect(self.update_text)
 
        self.verticalLayout_3.addWidget(comboBox, 0, Qt.AlignmentFlag.AlignHCenter)

        self.comboBoxes.append(comboBox)

        self.update_text()

    def remove_input_field(self):
        if self.comboBoxes:
            self.verticalLayout_3.removeWidget(self.comboBoxes[-1])
            self.comboBoxes[-1].deleteLater()
            self.comboBoxes.pop()

        self.update_text()

    def on_cancel_pressed(self):
        self.reject()

    def on_submit(self):

        content = self.predefined_text + "\n"

        for var in self.activities:
            content += f"- {var}\n"

        if self.file_path:
            with open(self.file_path, "w", encoding="utf-8") as f:
                f.write(content)

        self.accept()
    
    def update_text(self):
        content = self.textEdit.toPlainText()

        lines = content.splitlines()

        self.predefined_text = lines[0]

        self.activities = [box.currentText() for box in self.comboBoxes] 

        self.textEdit.clear()
        self.textEdit.setText(f"{self.predefined_text}" + "\n")
        for activity in self.activities:
            self.textEdit.append(f"• {activity}")

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Anl\u00e6gsarbejde", None))
        self.info_label.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; font-weight:700;\">Forslag til kapitel 2 <br/></span><span style=\" font-size:14pt; font-weight:700; font-style:italic;\">Anl\u00e6gsarbejde</span></p></body></html>", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-size:10pt; font-weight:700;\">Forslag til anl\u00e6gsarbejde</span></p></body></html>", None))
        self.remove_work_button.setText(QCoreApplication.translate("Dialog", u"Fjern arbejde", None))
        self.add_work_button.setText(QCoreApplication.translate("Dialog", u"Tilf\u00f8j arbejde", None))
        self.cancel_button.setText(QCoreApplication.translate("Dialog", u"Annuller", None))
        self.continue_button.setText(QCoreApplication.translate("Dialog", u"Forts\u00e6t", None))

class measuringConditions_UI(QDialog):
    def __init__(self, collected_data, cache_main_dir, parent=None):
        super().__init__(parent)
        
        self.collected_data = collected_data
        self.cache_main_dir = cache_main_dir

        self.file_text = os.path.join(self.cache_main_dir, "Rapport", "Tekst", "Målekonditioner.md")

        self.initial_settings()

        self.setupUi(self)

    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")

        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)


        Dialog.resize(370, 630)
        self.verticalLayout_2 = QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(-1, -1, -1, 0)
        self.info_label = QLabel(Dialog)
        self.info_label.setObjectName(u"info_label")

        self.verticalLayout.addWidget(self.info_label)

        self.textEdit = QTextEdit(Dialog)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setPlainText(self.template_text)

        self.verticalLayout.addWidget(self.textEdit)

        self.verticalSpacer = QSpacerItem(20, 5, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(-1, 0, -1, -1)

        self.customer_label = QLabel(Dialog)
        self.customer_label.setObjectName(u"customer_label")

        self.gridLayout.addWidget(self.customer_label, 0, 1, 1, 1)

        self.customer_entry = QLineEdit(Dialog)
        self.customer_entry.setObjectName(u"customer_entry")
        self.customer_entry.setMaximumSize(QSize(250, 100))
        self.customer_entry.setText(self.predefined_values["CUSTOMER"])
        self.customer_entry.setEnabled(False)

        self.gridLayout.addWidget(self.customer_entry, 0, 2, 1, 1, Qt.AlignmentFlag.AlignHCenter)

        self.road_label = QLabel(Dialog)
        self.road_label.setObjectName(u"road_label")

        self.gridLayout.addWidget(self.road_label, 1, 1, 1, 1)

        self.road_entry = QLineEdit(Dialog)
        self.road_entry.setObjectName(u"road_entry")
        self.road_entry.setMaximumSize(QSize(250, 100))
        self.road_entry.setText(self.predefined_values["ROAD"])
        self.road_entry.setEnabled(False)

        self.gridLayout.addWidget(self.road_entry, 1, 2, 1, 1, Qt.AlignmentFlag.AlignHCenter)

        self.horizontalSpacer_2 = QSpacerItem(10, 20, QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_2, 2, 0, 1, 1)

        self.city_label = QLabel(Dialog)
        self.city_label.setObjectName(u"city_label")

        self.gridLayout.addWidget(self.city_label, 2, 1, 1, 1)

        self.city_entry = QLineEdit(Dialog)
        self.city_entry.setObjectName(u"city_entry")
        self.city_entry.setMaximumSize(QSize(250, 100))
        self.city_entry.setText(self.predefined_values["CITY"])
        self.city_entry.setEnabled(False)

        self.gridLayout.addWidget(self.city_entry, 2, 2, 1, 1, Qt.AlignmentFlag.AlignHCenter)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 2, 3, 1, 1)

        self.dateFrom_label = QLabel(Dialog)
        self.dateFrom_label.setObjectName(u"dateFrom_label")

        self.gridLayout.addWidget(self.dateFrom_label, 3, 1, 1, 1)

        self.dateFrom_entry = QLineEdit(Dialog)
        self.dateFrom_entry.setObjectName(u"dateFrom_entry")
        self.dateFrom_entry.setMaximumSize(QSize(250, 100))
        self.dateFrom_entry.setText(self.predefined_values["DATE_FROM"])
        self.dateFrom_entry.setEnabled(False)

        self.gridLayout.addWidget(self.dateFrom_entry, 3, 2, 1, 1, Qt.AlignmentFlag.AlignHCenter)

        self.dateTo_label = QLabel(Dialog)
        self.dateTo_label.setObjectName(u"dateTo_label")

        self.gridLayout.addWidget(self.dateTo_label, 4, 1, 1, 1)

        self.dateTo_entry = QLineEdit(Dialog)
        self.dateTo_entry.setObjectName(u"dateTo_entry")
        self.dateTo_entry.setMaximumSize(QSize(250, 100))
        self.dateTo_entry.setText(self.predefined_values["DATE_TO"])
        self.dateTo_entry.setEnabled(False)

        self.gridLayout.addWidget(self.dateTo_entry, 4, 2, 1, 1, Qt.AlignmentFlag.AlignHCenter)

        self.verticalLayout.addLayout(self.gridLayout)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(-1, -1, -1, 0)
        self.cancel_button = QPushButton(Dialog)
        self.cancel_button.setObjectName(u"cancel_button")
        sizePolicy.setHeightForWidth(self.cancel_button.sizePolicy().hasHeightForWidth())
        self.cancel_button.setSizePolicy(sizePolicy)
        self.cancel_button.setMaximumSize(QSize(75, 100))
        self.cancel_button.clicked.connect(self.on_cancel_pressed)

        self.horizontalLayout.addWidget(self.cancel_button)

        self.continue_button = QPushButton(Dialog)
        self.continue_button.setObjectName(u"continue_button")
        self.continue_button.setMaximumSize(QSize(75, 100))
        self.continue_button.clicked.connect(self.on_continue_pressed)

        self.horizontalLayout.addWidget(self.continue_button)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(Dialog)

    def initial_settings(self):
        import shutil

        self.predefined_values = {
        "CUSTOMER": self.collected_data["customer"],
        "ROAD": self.collected_data["road"],
        "CITY": self.collected_data["city"],
        "DATE_FROM": self.collected_data["date_from"],
        "DATE_TO": self.collected_data["date_to"]
        }

        self.row_names = ["Kunde", "Vej", "By", "Arbejde", "Dato fra", "Dato til"]

        if not os.path.exists(self.file_text):
            self.drive = "O:"
            self.file_path_org = os.path.join("A000000", "A004371", "3_Pdoc", "Afrapportering", "files")
            self.file_path_org = os.path.normpath(self.drive + os.sep + self.file_path_org)
            self.file_path_org = os.path.join(self.file_path_org, "Tekst", "Målekonditioner.md")

            shutil.copy(self.file_path_org, self.file_text)
            
        self.template_text = open(self.file_text, "r", encoding="utf-8").read()

    def on_cancel_pressed(self):
        self.reject()

    def on_continue_pressed(self):

        with open(self.file_text, "w", encoding="utf-8") as f:
            f.write(self.textEdit.toPlainText())

        self.accept()

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Målekonditioner", None))
        self.info_label.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; font-weight:700;\">Forslag til kapitel 4 <br/></span><span style=\" font-size:14pt; font-weight:700; font-style:italic;\">M\u00e5lekonditioner</span></p></body></html>", None))
        self.city_label.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">By</p></body></html>", None))
        self.customer_label.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">Kunde</p></body></html>", None))
        self.dateTo_label.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">Dato til</p></body></html>", None))
        self.dateFrom_label.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">Dato fra</p></body></html>", None))
        self.road_label.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">Vej</p></body></html>", None))
        self.cancel_button.setText(QCoreApplication.translate("Dialog", u"Annuller", None))
        self.continue_button.setText(QCoreApplication.translate("Dialog", u"Forts\u00e6t", None))

class limitConstructionDamage_UI(QDialog):
    def __init__(self, collected_data, cache_main_dir, parent=None):
        super().__init__(parent)

        self.cache_main_dir = cache_main_dir
        self.collected_data = collected_data

        self.file_text_1 = os.path.join(self.cache_main_dir, "Rapport", "Tekst", "GrænseværdiForBygningskader.md")
        self.file_text_2 = os.path.join(self.cache_main_dir, "Rapport", "Tekst", "GrænseværdiForBygningskader_2.md")

        self.initial_settings()
        
        self.setupUi(self)
        
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")

        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        
        Dialog.resize(460, 650)

        self.verticalLayout_2 = QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(-1, -1, -1, 0)

        self.info_label = QLabel(Dialog)
        self.info_label.setObjectName(u"info_label")

        self.verticalLayout.addWidget(self.info_label)

        self.textEdit_1 = QTextEdit(Dialog)
        self.textEdit_1.setObjectName(u"textEdit_2")
        self.textEdit_1.setPlainText(self.template_text_1)

        self.verticalLayout.addWidget(self.textEdit_1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(-1, -1, -1, 0)
        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.horizontalLayout_2.addItem(self.verticalSpacer_2)

        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")

        self.horizontalLayout_2.addWidget(self.label, 0, Qt.AlignmentFlag.AlignHCenter)

        self.verticalSpacer = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.verticalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.textEdit_2 = QTextEdit(Dialog)
        self.textEdit_2.setObjectName(u"textEdit_2")
        self.textEdit_2.setPlainText(self.template_text_2)

        self.verticalLayout.addWidget(self.textEdit_2)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(-1, 0, -1, -1)

        self.customer_label = QLabel(Dialog)
        self.customer_label.setObjectName(u"customer_label")

        self.gridLayout.addWidget(self.customer_label, 0, 1, 1, 1)

        self.customer_entry = QLineEdit(Dialog)
        self.customer_entry.setObjectName(u"customer_entry")
        self.customer_entry.setSizePolicy(sizePolicy)
        self.customer_entry.setMaximumSize(QSize(250, 100))
        sizePolicy.setHeightForWidth(self.customer_entry.sizePolicy().hasHeightForWidth())
        self.customer_entry.setText(self.predefined_values["CUSTOMER"])
        self.customer_entry.setEnabled(False)

        self.gridLayout.addWidget(self.customer_entry, 0, 2, 1, 1, Qt.AlignmentFlag.AlignHCenter)

        self.road_label = QLabel(Dialog)
        self.road_label.setObjectName(u"road_label")

        self.gridLayout.addWidget(self.road_label, 1, 1, 1, 1)

        self.road_entry = QLineEdit(Dialog)
        self.road_entry.setObjectName(u"road_entry")
        self.road_entry.setMaximumSize(QSize(250, 100))
        self.road_entry.setText(self.predefined_values["ROAD"])
        self.road_entry.setEnabled(False)

        self.gridLayout.addWidget(self.road_entry, 1, 2, 1, 1, Qt.AlignmentFlag.AlignHCenter)

        self.horizontalSpacer_2 = QSpacerItem(10, 20, QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_2, 2, 0, 1, 1)

        self.city_label = QLabel(Dialog)
        self.city_label.setObjectName(u"city_label")

        self.gridLayout.addWidget(self.city_label, 2, 1, 1, 1)

        self.city_entry = QLineEdit(Dialog)
        self.city_entry.setObjectName(u"city_entry")
        self.city_entry.setMaximumSize(QSize(250, 100))
        self.city_entry.setText(self.predefined_values["CITY"])
        self.city_entry.setEnabled(False)

        self.gridLayout.addWidget(self.city_entry, 2, 2, 1, 1, Qt.AlignmentFlag.AlignHCenter)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 2, 3, 1, 1)

        self.dateFrom_label = QLabel(Dialog)
        self.dateFrom_label.setObjectName(u"dateFrom_label")

        self.gridLayout.addWidget(self.dateFrom_label, 3, 1, 1, 1)

        self.dateFrom_entry = QLineEdit(Dialog)
        self.dateFrom_entry.setObjectName(u"dateFrom_entry")
        self.dateFrom_entry.setMaximumSize(QSize(250, 100))
        self.dateFrom_entry.setText(self.predefined_values["DATE_FROM"])
        self.dateFrom_entry.setEnabled(False)

        self.gridLayout.addWidget(self.dateFrom_entry, 3, 2, 1, 1, Qt.AlignmentFlag.AlignHCenter)

        self.dateTo_label = QLabel(Dialog)
        self.dateTo_label.setObjectName(u"dateTo_label")

        self.gridLayout.addWidget(self.dateTo_label, 4, 1, 1, 1)

        self.dateTo_entry = QLineEdit(Dialog)
        self.dateTo_entry.setObjectName(u"dateTo_entry")
        self.dateTo_entry.setMaximumSize(QSize(250, 100))
        self.dateTo_entry.setText(self.predefined_values["DATE_TO"])
        self.dateTo_entry.setEnabled(False)

        self.gridLayout.addWidget(self.dateTo_entry, 4, 2, 1, 1, Qt.AlignmentFlag.AlignHCenter)

        self.verticalLayout.addLayout(self.gridLayout)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(-1, -1, -1, 0)

        self.cancel_button = QPushButton(Dialog)
        self.cancel_button.setObjectName(u"cancel_button")
        sizePolicy.setHeightForWidth(self.cancel_button.sizePolicy().hasHeightForWidth())
        self.cancel_button.setSizePolicy(sizePolicy)
        self.cancel_button.setMaximumSize(QSize(75, 100))
        self.cancel_button.clicked.connect(self.on_cancel_pressed)

        self.horizontalLayout.addWidget(self.cancel_button)

        self.continue_button = QPushButton(Dialog)
        self.continue_button.setObjectName(u"continue_button")
        self.continue_button.setMaximumSize(QSize(75, 100))
        self.continue_button.clicked.connect(self.on_continue_pressed)

        self.horizontalLayout.addWidget(self.continue_button)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.verticalLayout_2.addLayout(self.verticalLayout)


        self.retranslateUi(Dialog)

    def initial_settings(self):
        import shutil

        self.predefined_values = {
        "CUSTOMER": self.collected_data["customer"],
        "ROAD": self.collected_data["road"],
        "CITY": self.collected_data["city"],
        "DATE_FROM": self.collected_data["date_from"],
        "DATE_TO": self.collected_data["date_to"]
        }

        self.row_names = ["Kunde", "Vej", "By", "Arbejde", "Dato fra", "Dato til"]
        
        self.drive = "O:"

        if not os.path.exists(self.file_text_1):
            self.file_path_org = os.path.join("A000000", "A004371", "3_Pdoc", "Afrapportering", "files")
            self.file_path_org = os.path.normpath(self.drive + os.sep + self.file_path_org)
            self.file_path_org = os.path.join(self.file_path_org, "Tekst", "GrænseværdiForBygningskader.md")

            shutil.copy(self.file_path_org, self.file_text_1)
        
        if not os.path.exists(self.file_text_2):
            self.file_path_org = os.path.join("A000000", "A004371", "3_Pdoc", "Afrapportering", "files")
            self.file_path_org = os.path.normpath(self.drive + os.sep + self.file_path_org)
            self.file_path_org = os.path.join(self.file_path_org, "Tekst", "GrænseværdiForBygningskader_2.md")

            shutil.copy(self.file_path_org, self.file_text_2)


        self.template_text_1 = open(self.file_text_1, "r", encoding="utf-8").read()
        self.template_text_2 = open(self.file_text_2, "r", encoding="utf-8").read()

    def on_cancel_pressed(self):
        self.reject()

    def on_continue_pressed(self):

        with open(self.file_text_1, "w", encoding="utf-8") as f:
            f.write(self.textEdit_1.toPlainText())

        with open(self.file_text_2, "w", encoding="utf-8") as f:
            f.write(self.textEdit_2.toPlainText())

        self.accept()

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Gr\u00e6nsev\u00e6rdi for bygningskonstruktioner", None))
        self.info_label.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; font-weight:700;\">Forslag til kapitel 5 <br/></span><span style=\" font-size:14pt; font-weight:700; font-style:italic;\">Gr\u00e6nsev\u00e6rdier for bygningskonstruktioner</span></p></body></html>", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-size:10pt; font-style:italic;\">Figur</span></p></body></html>", None))
        self.city_label.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">By</p></body></html>", None))
        self.dateFrom_label.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">Dato fra</p></body></html>", None))
        self.customer_label.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">Kunde</p></body></html>", None))
        self.road_label.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">Vej</p></body></html>", None))
        self.dateTo_label.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">Dato til</p></body></html>", None))
        self.cancel_button.setText(QCoreApplication.translate("Dialog", u"Annuller", None))
        self.continue_button.setText(QCoreApplication.translate("Dialog", u"Forts\u00e6t", None))

class initial_MP_result_text(QDialog):
    def __init__(self, collected_data, cache_main_dir, parent=None):
        super().__init__(parent)
        
        self.collected_data = collected_data
        self.cache_main_dir = cache_main_dir

        self.file_text = os.path.join(self.cache_main_dir, "Rapport", "Tekst", "Måleresultater_start.md")

        self.trans_dict = load_json(os.path.join(self.cache_main_dir, "Results", "trans_dict_final.json"))

        self.initial_settings()

        self.setupUi(self)

    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")

        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)


        Dialog.resize(370, 630)
        self.verticalLayout_2 = QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(-1, -1, -1, 0)
        self.info_label = QLabel(Dialog)
        self.info_label.setObjectName(u"info_label")

        self.verticalLayout.addWidget(self.info_label)

        self.textEdit = QTextEdit(Dialog)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setPlainText(self.template_text)

        self.verticalLayout.addWidget(self.textEdit)

        self.verticalSpacer = QSpacerItem(20, 5, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(-1, 0, -1, -1)

        self.customer_label = QLabel(Dialog)
        self.customer_label.setObjectName(u"customer_label")

        self.gridLayout.addWidget(self.customer_label, 0, 1, 1, 1)

        self.customer_entry = QLineEdit(Dialog)
        self.customer_entry.setObjectName(u"customer_entry")
        self.customer_entry.setMaximumSize(QSize(250, 100))
        self.customer_entry.setText(self.predefined_values["CUSTOMER"])
        self.customer_entry.setEnabled(False)

        self.gridLayout.addWidget(self.customer_entry, 0, 2, 1, 1, Qt.AlignmentFlag.AlignHCenter)

        self.road_label = QLabel(Dialog)
        self.road_label.setObjectName(u"road_label")

        self.gridLayout.addWidget(self.road_label, 1, 1, 1, 1)

        self.road_entry = QLineEdit(Dialog)
        self.road_entry.setObjectName(u"road_entry")
        self.road_entry.setMaximumSize(QSize(250, 100))
        self.road_entry.setText(self.predefined_values["ROAD"])
        self.road_entry.setEnabled(False)

        self.gridLayout.addWidget(self.road_entry, 1, 2, 1, 1, Qt.AlignmentFlag.AlignHCenter)

        self.horizontalSpacer_2 = QSpacerItem(10, 20, QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_2, 2, 0, 1, 1)

        self.city_label = QLabel(Dialog)
        self.city_label.setObjectName(u"city_label")

        self.gridLayout.addWidget(self.city_label, 2, 1, 1, 1)

        self.city_entry = QLineEdit(Dialog)
        self.city_entry.setObjectName(u"city_entry")
        self.city_entry.setMaximumSize(QSize(250, 100))
        self.city_entry.setText(self.predefined_values["CITY"])
        self.city_entry.setEnabled(False)

        self.gridLayout.addWidget(self.city_entry, 2, 2, 1, 1, Qt.AlignmentFlag.AlignHCenter)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 2, 3, 1, 1)

        self.dateFrom_label = QLabel(Dialog)
        self.dateFrom_label.setObjectName(u"dateFrom_label")

        self.gridLayout.addWidget(self.dateFrom_label, 3, 1, 1, 1)

        self.dateFrom_entry = QLineEdit(Dialog)
        self.dateFrom_entry.setObjectName(u"dateFrom_entry")
        self.dateFrom_entry.setMaximumSize(QSize(250, 100))
        self.dateFrom_entry.setText(self.predefined_values["DATE_FROM"])
        self.dateFrom_entry.setEnabled(False)

        self.gridLayout.addWidget(self.dateFrom_entry, 3, 2, 1, 1, Qt.AlignmentFlag.AlignHCenter)

        self.dateTo_label = QLabel(Dialog)
        self.dateTo_label.setObjectName(u"dateTo_label")

        self.gridLayout.addWidget(self.dateTo_label, 4, 1, 1, 1)

        self.dateTo_entry = QLineEdit(Dialog)
        self.dateTo_entry.setObjectName(u"dateTo_entry")
        self.dateTo_entry.setMaximumSize(QSize(250, 100))
        self.dateTo_entry.setText(self.predefined_values["DATE_TO"])
        self.dateTo_entry.setEnabled(False)

        self.gridLayout.addWidget(self.dateTo_entry, 4, 2, 1, 1, Qt.AlignmentFlag.AlignHCenter)

        self.verticalLayout.addLayout(self.gridLayout)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(-1, -1, -1, 0)
        self.cancel_button = QPushButton(Dialog)
        self.cancel_button.setObjectName(u"cancel_button")
        sizePolicy.setHeightForWidth(self.cancel_button.sizePolicy().hasHeightForWidth())
        self.cancel_button.setSizePolicy(sizePolicy)
        self.cancel_button.setMaximumSize(QSize(75, 100))
        self.cancel_button.clicked.connect(self.on_cancel_pressed)

        self.horizontalLayout.addWidget(self.cancel_button)

        self.continue_button = QPushButton(Dialog)
        self.continue_button.setObjectName(u"continue_button")
        self.continue_button.setMaximumSize(QSize(75, 100))
        self.continue_button.clicked.connect(self.on_continue_pressed)

        self.horizontalLayout.addWidget(self.continue_button)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(Dialog)

    def initial_settings(self):
        import shutil
        import string

        self.predefined_values = {
        "CUSTOMER": self.collected_data["customer"],
        "ROAD": self.collected_data["road"],
        "CITY": self.collected_data["city"],
        "DATE_FROM": self.collected_data["date_from"],
        "DATE_TO": self.collected_data["date_to"]
        }

        self.row_names = ["Kunde", "Vej", "By", "Arbejde", "Dato fra", "Dato til"]

        if not os.path.exists(self.file_text):
            self.drive = "O:"
            self.file_path_org = os.path.join("A000000", "A004371", "3_Pdoc", "Afrapportering", "files")
            self.file_path_org = os.path.normpath(self.drive + os.sep + self.file_path_org)
            self.file_path_org = os.path.join(self.file_path_org, "Tekst", "Måleresultater_start.md")

            shutil.copy(self.file_path_org, self.file_text)
            
        self.template_text = open(self.file_text, "r", encoding="utf-8").read()

        if len(self.trans_dict) == 1:
            self.template_text = self.template_text.replace("BILAG_START-BILAG_SLUT", f"{string.ascii_uppercase[0]}")
        else:
            self.template_text = self.template_text.replace("BILAG_START", f"{string.ascii_uppercase[0]}").replace("BILAG_SLUT",f"{string.ascii_uppercase[len(self.trans_dict)-1]}")

    def on_cancel_pressed(self):
        self.reject()

    def on_continue_pressed(self):
        with open(self.file_text, "w", encoding="utf-8") as f:
            f.write(self.textEdit.toPlainText())

        self.accept()

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"M\u00e5leresultater", None))
        self.info_label.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; font-weight:700;\">Forslag til kapitel 6 <br/></span><span style=\" font-size:14pt; font-weight:700; font-style:italic;\">M\u00e5leresultater</span></p></body></html>", None))
        self.city_label.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">By</p></body></html>", None))
        self.customer_label.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">Kunde</p></body></html>", None))
        self.dateTo_label.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">Dato til</p></body></html>", None))
        self.dateFrom_label.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">Dato fra</p></body></html>", None))
        self.road_label.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">Vej</p></body></html>", None))
        self.cancel_button.setText(QCoreApplication.translate("Dialog", u"Annuller", None))
        self.continue_button.setText(QCoreApplication.translate("Dialog", u"Forts\u00e6t", None))

class edit_mp_text(QDialog):
    def __init__(self, cache_main_dir, adresse, parent=None):
        super().__init__(parent)
        
        self.cache_main_dir = cache_main_dir
        self.adresse = adresse

        self.trans_dict = load_json(os.path.join(self.cache_main_dir, "Results", "trans_dict_final.json"))
        self.text_final_path = os.path.join(self.cache_main_dir,"Rapport","Tekst", f"{self.adresse}")

        self.initial_settings()

        self.setupUi(self)

    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")

        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)

        Dialog.resize(450, 775)
        self.verticalLayout_2 = QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(-1, -1, -1, 0)
        self.info_label = QLabel(Dialog)
        self.info_label.setObjectName(u"info_label")

        self.verticalLayout.addWidget(self.info_label)

        self.setup_textboxes(Dialog)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(-1, 0, -1, -1)

        self.n_transients_label = QLabel(Dialog)
        self.n_transients_label.setObjectName(u"customer_label")

        self.gridLayout.addWidget(self.n_transients_label, 0, 1, 1, 1)

        self.n_transients_entry = QLineEdit(Dialog)
        self.n_transients_entry.setObjectName(u"n_transients")
        self.n_transients_entry.setMaximumSize(QSize(250, 100))
        self.n_transients_entry.setText(str(self.predefined_values["N_TRANSIENTS"]))
        self.n_transients_entry.setEnabled(False)
        self.n_transients_entry.setStyleSheet("border: none; background: transparent;")

        self.gridLayout.addWidget(self.n_transients_entry, 0, 2, 1, 1, Qt.AlignmentFlag.AlignHCenter)

        self.reel_transients_label = QLabel(Dialog)
        self.reel_transients_label.setObjectName(u"road_label")

        self.gridLayout.addWidget(self.reel_transients_label, 1, 1, 1, 1)

        self.reel_transients_entry = QLineEdit(Dialog)
        self.reel_transients_entry.setObjectName(u"road_entry")
        self.reel_transients_entry.setMaximumSize(QSize(250, 100))
        self.reel_transients_entry.setText(str(self.predefined_values["N_REEL"]))
        self.reel_transients_entry.setEnabled(False)
        self.reel_transients_entry.setStyleSheet("border: none; background: transparent;")

        self.gridLayout.addWidget(self.reel_transients_entry, 1, 2, 1, 1, Qt.AlignmentFlag.AlignHCenter)

        self.horizontalSpacer_2 = QSpacerItem(10, 20, QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_2, 2, 0, 1, 1)

        self.arb_transients_label = QLabel(Dialog)
        self.arb_transients_label.setObjectName(u"city_label")

        self.gridLayout.addWidget(self.arb_transients_label, 2, 1, 1, 1)

        self.arb_transients_entry = QLineEdit(Dialog)
        self.arb_transients_entry.setObjectName(u"city_entry")
        self.arb_transients_entry.setMaximumSize(QSize(250, 100))
        self.arb_transients_entry.setText(str(self.predefined_values["N_ARBE"]))
        self.arb_transients_entry.setEnabled(False)
        self.arb_transients_entry.setStyleSheet("border: none; background: transparent;")
        

        self.gridLayout.addWidget(self.arb_transients_entry, 2, 2, 1, 1, Qt.AlignmentFlag.AlignHCenter)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 2, 3, 1, 1)

        self.slag_transients_label = QLabel(Dialog)
        self.slag_transients_label.setObjectName(u"dateFrom_label")

        self.gridLayout.addWidget(self.slag_transients_label, 3, 1, 1, 1)

        self.slag_transients_entry = QLineEdit(Dialog)
        self.slag_transients_entry.setObjectName(u"dateFrom_entry")
        self.slag_transients_entry.setMaximumSize(QSize(250, 100))
        self.slag_transients_entry.setText(str(self.predefined_values["N_SLAG"]))
        self.slag_transients_entry.setEnabled(False)
        self.slag_transients_entry.setStyleSheet("border: none; background: transparent;")

        self.gridLayout.addWidget(self.slag_transients_entry, 3, 2, 1, 1, Qt.AlignmentFlag.AlignHCenter)

        self.above_limit_5_label = QLabel(Dialog)
        self.above_limit_5_label.setObjectName(u"dateTo_label")

        self.gridLayout.addWidget(self.above_limit_5_label, 4, 1, 1, 1)

        self.above_limit_5_entry = QLineEdit(Dialog)
        self.above_limit_5_entry.setObjectName(u"dateTo_entry")
        self.above_limit_5_entry.setMaximumSize(QSize(250, 100))
        self.above_limit_5_entry.setText(self.predefined_values["ABOVE_LIMIT_5"])
        self.above_limit_5_entry.setEnabled(False)
        self.above_limit_5_entry.setStyleSheet("border: none; background: transparent;")

        self.gridLayout.addWidget(self.above_limit_5_entry, 4, 2, 1, 1, Qt.AlignmentFlag.AlignHCenter)

        self.verticalLayout.addLayout(self.gridLayout)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(-1, -1, -1, 0)
        self.cancel_button = QPushButton(Dialog)
        self.cancel_button.setObjectName(u"cancel_button")
        sizePolicy.setHeightForWidth(self.cancel_button.sizePolicy().hasHeightForWidth())
        self.cancel_button.setSizePolicy(sizePolicy)
        self.cancel_button.setMaximumSize(QSize(75, 100))
        self.cancel_button.clicked.connect(self.on_cancel_pressed)

        self.horizontalLayout.addWidget(self.cancel_button)

        self.continue_button = QPushButton(Dialog)
        self.continue_button.setObjectName(u"continue_button")
        self.continue_button.setMaximumSize(QSize(75, 100))
        self.continue_button.clicked.connect(self.on_continue_pressed)

        self.horizontalLayout.addWidget(self.continue_button)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(Dialog)

    def initial_settings(self):
        self.trans_dict_adresse = self.trans_dict[self.adresse]

        self.predefined_values = {
            "N_TRANSIENTS": self.trans_dict_adresse["Reel"]+self.trans_dict_adresse["Arbe"]+self.trans_dict_adresse["Slag"],
            "N_REEL": self.trans_dict_adresse["Reel"],
            "N_ARBE": self.trans_dict_adresse["Arbe"],
            "N_SLAG": self.trans_dict_adresse["Slag"],
            "ABOVE_LIMIT_5": "Ja" if self.trans_dict_adresse["above_limit_5"] == True else "Nej"
            }
    

        self.text_pieces = []

        self.text_files = [os.path.join(self.text_final_path, file) for file in os.listdir(self.text_final_path)]

        for text_file in self.text_files:
            with open(text_file, "r", encoding="utf-8") as f:
                text = f.read()
            
            self.text_pieces.append((text, text_file))

    def setup_textboxes(self, Dialog):
        self.textEdits = {}

        for i, text_file in enumerate(self.text_files):
            text = open(text_file, "r", encoding="utf-8").read()

            self.textEdits[i] = QTextEdit(Dialog)
            self.textEdits[i].setObjectName(u"textEdit")
            self.textEdits[i].setPlainText(text)

            self.verticalLayout.addWidget(self.textEdits[i])

            verticalSpacer = QSpacerItem(20, 5, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)
            self.verticalLayout.addItem(verticalSpacer)

    def on_cancel_pressed(self):
        self.reject()

    def on_continue_pressed(self):
        from logger import get_logger

        for i, text_file in enumerate(self.text_files):
            with open(text_file, "w", encoding="utf-8") as f:
                f.write(self.textEdits[i].toPlainText())

        self.logger = get_logger()
        self.logger.log("Tekst til '{}' er gemt.".format(self.adresse))

        self.accept()

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"M\u00e5leresultater", None))
        self.info_label.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; font-weight:700;\">Forslag for tekst til <br/></span><span style=\" font-size:14pt; font-weight:700; font-style:italic;\">{}</span></p></body></html>".format(self.adresse), None))
        self.n_transients_label.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">Antal overskridelser</p></body></html>", None))
        self.reel_transients_label.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">Reelle overskridelser</p></body></html>", None))
        self.arb_transients_label.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">Arb. t\u00e6t ved måler</p></body></html>", None))
        self.slag_transients_label.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">Antal slag</p></body></html>", None))
        self.above_limit_5_label.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">Over Zeile 2</p></body></html>", None))
        self.cancel_button.setText(QCoreApplication.translate("Dialog", u"Annuller", None))
        self.continue_button.setText(QCoreApplication.translate("Dialog", u"Forts\u00e6t", None))

class EditMPTextGUI(QDialog):
    def __init__(self, cache_main_dir, parent=None):
        super().__init__(parent)
        
        self.cache_main_dir = cache_main_dir
        
        self.initUI()

    def initUI(self):
        list_adresses = load_json(os.path.join(self.cache_main_dir, "Results", "trans_dict_final.json")).keys()

        self.setWindowTitle('Tekst til målepunkt')
        self.setGeometry(200, 200, 300, 150)

        layout = QVBoxLayout()

        # Label for instructions
        label = QLabel('Vælg et målepunkt:', self)
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        # ComboBox for names
        self.combo_box = QComboBox(self)
        # Suppose `self.parent.names` contains the names you want to show in the drop-down

        #self.names = ["MP1", "MP2", "MP3", "MP4"]  # Replace with actual list if available
        self.combo_box.addItems(list_adresses)
        layout.addWidget(self.combo_box)

        # Proceed Button
        self.proceed_button = QPushButton('Fortsæt', self)
        self.proceed_button.clicked.connect(self.on_proceed)
        layout.addWidget(self.proceed_button)

        # Proceed Button
        self.cancel_button = QPushButton('Afslut', self)
        self.cancel_button.clicked.connect(self.on_cancel)
        layout.addWidget(self.cancel_button)

        self.setLayout(layout)

    def on_proceed(self):
        selected_name = self.combo_box.currentText()
        dialog = edit_mp_text(self.cache_main_dir, selected_name, self)  # Create instance
        dialog.exec()  # Show the dialog and wait for it to close

    def on_cancel(self):
        self.close()

class conclusionUI(QDialog):
    def __init__(self, collected_data, cache_main_dir, parent=None):
        super().__init__(parent)
        
        self.cache_main_dir = cache_main_dir
        self.collected_data = collected_data

        self.trans_dict = load_json(os.path.join(self.cache_main_dir, "Results", "trans_dict_final.json"))
        self.sensor_dict = load_json(os.path.join(self.cache_main_dir, "API", "project_sensor_dict_final.json"))
        self.text_final_path = os.path.join(self.cache_main_dir,"Rapport","Tekst")

        self.initial_settings()

        self.setupUi(self)

    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")

        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)

        Dialog.resize(450, 775)
        self.verticalLayout_2 = QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(-1, -1, -1, 0)
        self.info_label = QLabel(Dialog)
        self.info_label.setObjectName(u"info_label")

        self.verticalLayout.addWidget(self.info_label)

        self.setup_textboxes(Dialog)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(-1, 0, -1, -1)

        self.customer_label = QLabel(Dialog)
        self.customer_label.setObjectName(u"customer_label")

        self.gridLayout.addWidget(self.customer_label, 0, 1, 1, 1)

        self.customer_entry = QLineEdit(Dialog)
        self.customer_entry.setObjectName(u"n_transients")
        self.customer_entry.setMaximumSize(QSize(250, 100))
        self.customer_entry.setText(str(self.collected_data["customer"]))
        self.customer_entry.setEnabled(False)
        self.gridLayout.addWidget(self.customer_entry, 0, 2, 1, 1, Qt.AlignmentFlag.AlignHCenter)

        self.road_label = QLabel(Dialog)
        self.road_label.setObjectName(u"road_label")

        self.gridLayout.addWidget(self.road_label, 1, 1, 1, 1)

        self.road_entry = QLineEdit(Dialog)
        self.road_entry.setObjectName(u"road_entry")
        self.road_entry.setMaximumSize(QSize(250, 100))
        self.road_entry.setText(str(self.collected_data["road"]))
        self.road_entry.setEnabled(False)

        self.gridLayout.addWidget(self.road_entry, 1, 2, 1, 1, Qt.AlignmentFlag.AlignHCenter)

        self.horizontalSpacer_2 = QSpacerItem(10, 20, QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_2, 2, 0, 1, 1)

        self.city_label = QLabel(Dialog)
        self.city_label.setObjectName(u"city_label")

        self.gridLayout.addWidget(self.city_label, 2, 1, 1, 1)

        self.city_entry = QLineEdit(Dialog)
        self.city_entry.setObjectName(u"city_entry")
        self.city_entry.setMaximumSize(QSize(250, 100))
        self.city_entry.setText(str(self.collected_data["city"]))
        self.city_entry.setEnabled(False)
        

        self.gridLayout.addWidget(self.city_entry, 2, 2, 1, 1, Qt.AlignmentFlag.AlignHCenter)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 2, 3, 1, 1)

        self.date_from_label = QLabel(Dialog)
        self.date_from_label.setObjectName(u"dateFrom_label")

        self.gridLayout.addWidget(self.date_from_label, 3, 1, 1, 1)

        self.date_from_entry = QLineEdit(Dialog)
        self.date_from_entry.setObjectName(u"dateFrom_entry")
        self.date_from_entry.setMaximumSize(QSize(250, 100))
        self.date_from_entry.setText(str(self.collected_data["date_from"]))
        self.date_from_entry.setEnabled(False)

        self.gridLayout.addWidget(self.date_from_entry, 3, 2, 1, 1, Qt.AlignmentFlag.AlignHCenter)

        self.date_to_label = QLabel(Dialog)
        self.date_to_label.setObjectName(u"dateTo_label")

        self.gridLayout.addWidget(self.date_to_label, 4, 1, 1, 1)

        self.date_to_entry = QLineEdit(Dialog)
        self.date_to_entry.setObjectName(u"dateTo_entry")
        self.date_to_entry.setMaximumSize(QSize(250, 100))
        self.date_to_entry.setText(self.collected_data["date_to"])
        self.date_to_entry.setEnabled(False)

        self.gridLayout.addWidget(self.date_to_entry, 4, 2, 1, 1, Qt.AlignmentFlag.AlignHCenter)

        self.verticalLayout.addLayout(self.gridLayout)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(-1, -1, -1, 0)
        self.cancel_button = QPushButton(Dialog)
        self.cancel_button.setObjectName(u"cancel_button")
        sizePolicy.setHeightForWidth(self.cancel_button.sizePolicy().hasHeightForWidth())
        self.cancel_button.setSizePolicy(sizePolicy)
        self.cancel_button.setMaximumSize(QSize(75, 100))
        self.cancel_button.clicked.connect(self.on_cancel_pressed)

        self.horizontalLayout.addWidget(self.cancel_button)

        self.continue_button = QPushButton(Dialog)
        self.continue_button.setObjectName(u"continue_button")
        self.continue_button.setMaximumSize(QSize(75, 100))
        self.continue_button.clicked.connect(self.on_continue_pressed)

        self.horizontalLayout.addWidget(self.continue_button)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(Dialog)

    def initial_settings(self):
        from basic_functions import yes_no_cancel_operation
        self.drive = "O:"
        self.files_path = os.path.join("A000000", "A004371", "3_Pdoc", "Afrapportering", "files")
        self.files_path = os.path.normpath(self.drive + os.sep + self.files_path)

        self.limits = [self.sensor_dict[adresse]["limit"] for adresse in self.sensor_dict]

        if all(limit == 3 for limit in self.limits):
            self.chap_5_limit = "vibrationsfølsomme"
            self.dual = False
        elif any(limit == 3 for limit in self.limits) and any(limit == 5 for limit in self.limits):
            self.chap_5_limit = "vibrationsfølsomme og normale"
            self.dual = True
        elif all(limit == 5 for limit in self.limits):
            self.chap_5_limit = "normale"
            self.dual = False
        else:
            self.chap_5_limit = "ukendt"
            self.dual = False

        self.Slag = 0
        self.Reel = 0
        self.above_5_limit_counter = 0

        i = 1
        for adresse, detail in self.trans_dict.items():
            self.Slag = self.Slag + detail["Slag"]
            self.Reel = self.Reel + detail["Reel"] + detail["Arbe"]

            for transient in detail["Transienter"]:
                i += 1
                if transient["above_limit_5"] == True:
                    self.above_5_limit_counter += 1

        self.text_pieces = []

        if self.Reel == 0: 
            text_final_file = os.path.join(self.text_final_path, "Konklusion_1.md")
            if not os.path.exists(text_final_file):
                text_file = os.path.join(self.files_path, "Tekst", "Konklusion_ingen_transient.md")
                with open(text_file, "r", encoding='utf-8') as file:
                    text = file.read()
                
                text = text.replace("REEL_NOREEL", "" if self.Slag == 0 else " reelle")
                text = text.replace("RESPEKTIVE", "de respektive" if self.dual else "den")
                text = text.replace("ER_FLAG", "er" if self.dual else "")
                text = text.replace("VIB_ELLER_NORMAL", self.chap_5_limit)

                with open(text_final_file, "w", encoding='utf-8') as file:
                    file.write(text)

            self.text_pieces.append(text_final_file)


        elif self.Reel != 0:
            text_final_file = os.path.join(self.text_final_path, "Konklusion_1.md")
            if not os.path.exists(text_final_file):
                text_file = os.path.join(self.files_path, "Tekst", "Konklusion_transient.md")
                with open(text_file, "r", encoding='utf-8') as file:
                    text = file.read()
                
                text = text.replace("N_REEL_TRANSIENT", f"{self.Reel}")
                text = text.replace("HÆNDELSE/HÆNDELSER", "hændelse" if self.Reel == 1 else "hændelser")
                text = text.replace("RESPEKTIVE", "de respektive" if self.dual else "den")
                text = text.replace("ER_FLAG", "er" if self.dual else "")
                text = text.replace("VIB_ELLER_NORMAL", self.chap_5_limit)
                text = text.replace("HÆNDELSEN/HÆNDELSERNE", "Hændelsen" if self.Reel == 1 else "Hændelserne")

                with open(text_final_file, "w", encoding='utf-8') as file:
                    file.write(text)

                text_file = os.path.join(self.files_path, "Tekst", "Konklusion_transient_caption.md")
                with open(text_file, "r", encoding='utf-8') as file:
                    text = file.read()

                text = text.replace("OVERSKRIDELSE/OVERSKRIDELSER", "Overskridelse" if self.Reel == 1 else "Overskridelser")
                text = text.replace("VIB_ELLER_NORMAL", self.chap_5_limit)

                text_final_file = os.path.join(self.text_final_path, "Konklusion_caption.md")

                with open(text_final_file, "w", encoding='utf-8') as file:
                    file.write(text)

            self.text_pieces.append(text_final_file)

            answer = yes_no_cancel_operation("Konklusion", "Kan overskridelsen/overskridelserne \nkategoriseres som mindre/kortvarige \noverskridelser?")
            if answer == "Yes":
                text_final_file = os.path.join(self.text_final_path, "Konklusion_2.md")
                if not os.path.exists(text_final_file):
                    text_file = os.path.join(self.files_path, "Tekst", "Konklusion_transient_2.md")
                    with open(text_file, "r", encoding='utf-8') as file:
                        text = file.read()
                    
                    text = text.replace("HÆNDELSE/HÆNDELSER", "hændelse" if self.Reel == 1 else "hændelser")
                    text = text.replace("OVERSKRIDELSE/OVERSKRIDELSER", "overskridelse" if self.Reel == 1 else "overskridelser")
                    text = text.replace("VIB_ELLER_NORMAL", self.chap_5_limit)

                    with open(text_final_file, "w", encoding='utf-8') as file:
                        file.write(text)

                self.text_pieces.append(text_final_file)

            elif answer == "No" and os.path.exists(os.path.join(self.text_final_path, "Konklusion_2.md")):
                os.remove(os.path.join(self.text_final_path, "Konklusion_2.md"))
        

        if self.above_5_limit_counter > 0:
            text_final_file = os.path.join(self.text_final_path, "Konklusion_above_5.md")
            if not os.path.exists(text_final_file):
                text_file = os.path.join(self.files_path, "Tekst", "Konklusion_above_5.md")
                with open(text_file, "r", encoding='utf-8') as file:
                    text = file.read()
                
                text = text.replace("HÆNDELSE/HÆNDELSER", "hændelse" if self.above_5_limit_counter == 1 else "hændelser")

                with open(text_final_file, "w", encoding='utf-8') as file:
                    file.write(text)
        
            self.text_pieces.append(text_final_file)

            
            text_final_file = os.path.join(self.text_final_path, "Konklusion_caption_above_5.md")
            if not os.path.exists(text_final_file):
                text_file = os.path.join(self.files_path, "Tekst", "Konklusion_transient_caption_above_5.md")
                with open(text_file, "r", encoding='utf-8') as file:
                    text = file.read()

                text = text.replace("OVERSKRIDELSE/OVERSKRIDELSER", "Overskridelse" if self.above_5_limit_counter == 1 else "Overskridelser")

                with open(text_final_file, "w", encoding='utf-8') as file:
                    file.write(text)
        
            self.text_pieces.append(text_final_file)
        

        answer = yes_no_cancel_operation("Konklusion","Har arbejdet været i en større udstrækning \n f.eks. seperat kloakering?")

        if answer == "Yes":
            text_final_file = os.path.join(self.text_final_path, "Konklusion_3.md")
            if not os.path.exists(text_final_file):
                text_file = os.path.join(self.cache_main_dir, "Rapport", "Tekst", "Indledning.md")
                with open(text_file, "r", encoding='utf-8') as file:
                    text = file.read()
                
                text = text.split('\n\n')[2]

                with open(text_final_file, "w", encoding='utf-8') as file:
                    file.write(text)

            self.text_pieces.append(text_final_file)

        elif answer == "No" and os.path.exists(os.path.join(self.text_final_path, "Konklusion_3.md")):
            os.remove(os.path.join(self.text_final_path, "Konklusion_3.md"))

    def setup_textboxes(self, Dialog):
        self.textEdits = {}

        for i, text_file in enumerate(self.text_pieces):
            text = open(text_file, "r", encoding="utf-8").read()

            self.textEdits[i] = QTextEdit(Dialog)
            self.textEdits[i].setObjectName(u"textEdit")
            self.textEdits[i].setPlainText(text)

            self.verticalLayout.addWidget(self.textEdits[i])

            verticalSpacer = QSpacerItem(20, 5, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)
            self.verticalLayout.addItem(verticalSpacer)

    def on_cancel_pressed(self):
        self.reject()

    def on_continue_pressed(self):

        for i, text_file in enumerate(self.text_pieces):
            with open(text_file, "w", encoding="utf-8") as f:
                f.write(self.textEdits[i].toPlainText())

        self.accept()

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Konklusion", None))
        self.info_label.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; font-weight:700;\">Forslag til kapitel 7 <br/></span><span style=\" font-size:14pt; font-weight:700; font-style:italic;\">Konklusion</span></p></body></html>", None))
        self.customer_label.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">Kunde</p></body></html>", None))
        self.road_label.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">Vej</p></body></html>", None))
        self.city_label.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">By</p></body></html>", None))
        self.date_from_label.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">Dato fra</p></body></html>", None))
        self.date_to_label.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">Dato til</p></body></html>", None))
        self.cancel_button.setText(QCoreApplication.translate("Dialog", u"Annuller", None))
        self.continue_button.setText(QCoreApplication.translate("Dialog", u"Forts\u00e6t", None))


#if __name__ == "__main__":
#
#    drive = "O:"
#
#    cache_main_dir = "A000000\\A004371\\3_Pdoc\\Afrapportering\\A223276-094 - Bakkelygade m.fl., Nørresundby"
#
#    cache_main_dir = os.path.join(drive, os.sep, cache_main_dir)
#
#    saved_data_dir = "A000000\\A004371\\3_Pdoc\\Afrapportering\\files\\saved_projects\\109418.json"
#
#    collected_data = load_json(os.path.join(drive, os.sep, saved_data_dir))
#
#    app = QApplication(sys.argv)
#    #"42882", "141635c7532e819727546481365f4c9448006bd23fbd69d98968f1b7dc07062a", None
#    ui = work_info_UI(cache_main_dir)
#
#    #ui.show()
#    
#    if ui.exec() == QDialog.Accepted:
        print("OK")
#    else:
        print("Cancel")

#
#    #print(cred, token)
#
#    sys.exit()