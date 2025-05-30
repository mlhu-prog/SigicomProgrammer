# log_window.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QApplication, QLineEdit, QSizePolicy
from PySide6.QtCore import Qt

class LogWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Log")
        self.resize(600, 400)
        layout = QVBoxLayout()
        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)
        layout.addWidget(self.text_area)

        self.process_line = QLineEdit()
        self.process_line.setText("Status:")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.process_line.sizePolicy().hasHeightForWidth())
        self.process_line.setSizePolicy(sizePolicy)
        self.process_line.setAlignment(Qt.AlignLeft)
        self.process_line.setReadOnly(True)
        self.process_line.setStyleSheet(
                                        "QLineEdit {"
                                        " border: none;"
                                        " background: transparent;"
                                        " selection-background-color: #cccccc;"  # Optional: visible selection
                                        "}"
                                    )
        self.process_line.setFrame(False)  # Removes the frame if present
        
        layout.addWidget(self.process_line, Qt.AlignmentFlag.AlignLeft)

        self.setLayout(layout)

        self.log_messages = []

    def log(self, message, style=1, status=2):
        if style == 1:
            formatted = f"{message}"
        else:
            formatted = f"<b><span style='font-size:10pt'>{message}</span></b>"

        if status == 1:
            self.process_line.setText(f"Status: klar")
        else:
            self.process_line.setText(f"Status: arbejder")


        self.text_area.append(formatted)
        self.log_messages.append(message)
        QApplication.processEvents()  # Update the GUI immediately

        if style == 2:
            self.popup()


    def popup(self):
        self.show()
        self.raise_()

    def get_log_messages(self):
        return "\n".join(self.log_messages)
