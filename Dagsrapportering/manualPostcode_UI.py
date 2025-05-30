from PySide6.QtCore import (QCoreApplication, Qt)
from PySide6.QtWidgets import (QDialog, QLabel, QLineEdit, QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout)

class manualPostcode_UI(QDialog):
    def __init__(self, adresse, parent=None):
        super().__init__(parent)

        self.adresse = adresse

        self.setupUi(self)

    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(370, 150)
        self.verticalLayout_2 = QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.information_label = QLabel(Dialog)
        self.information_label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.information_label, 0, Qt.AlignmentFlag.AlignHCenter)

        self.adresse_label = QLabel(Dialog)
        self.adresse_label.setObjectName(u"label_3")

        self.verticalLayout.addWidget(self.adresse_label, 0, Qt.AlignmentFlag.AlignHCenter)

        self.format_label = QLabel(Dialog)
        self.format_label.setObjectName(u"label_2")

        self.verticalLayout.addWidget(self.format_label, 0, Qt.AlignmentFlag.AlignHCenter)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.postcode_edit = QLineEdit(Dialog)
        self.postcode_edit.setObjectName(u"lineEdit")

        self.verticalLayout.addWidget(self.postcode_edit, 0, Qt.AlignmentFlag.AlignHCenter)

        self.cnt_button = QPushButton(Dialog)
        self.cnt_button.setObjectName(u"pushButton")
        self.cnt_button.clicked.connect(self.on_proceed)

        self.verticalLayout.addWidget(self.cnt_button, 0, Qt.AlignmentFlag.AlignHCenter)


        self.verticalLayout_2.addLayout(self.verticalLayout)


        self.retranslateUi(Dialog)

    def on_proceed(self):
        self.accept()

    def get_postcode(self):
        return self.postcode_edit.text()

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Postnummer", None))
        self.information_label.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p>Fejl i program. Angiv manuelt postnummer for;</p></body></html>", None))
        self.adresse_label.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-weight:700;\">{}</span></p></body></html>".format(self.adresse), None))
        self.format_label.setText(QCoreApplication.translate("Dialog", u"Format: 9000 Aalborg", None))
        self.cnt_button.setText(QCoreApplication.translate("Dialog", u"Forts\u00e6t", None))
