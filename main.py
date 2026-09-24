import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import Qt

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()


        main_layout = QtWidgets.QVBoxLayout(self)

        security_logs = Tile("Recent Security Logs", Qt.AlignmentFlag.AlignTop)
        top_section = Tile("")
        main_layout.addWidget(top_section)
        main_layout.addWidget(security_logs)



class Tile(QtWidgets.QFrame):
    def __init__(self, title: str, label_allignment: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter, bg_color: str = "#1e222a", border_color: str = "#3b4252"):
        super().__init__()
        self.setStyleSheet(f"""
                    QFrame {{
                        background-color: {bg_color};
                        border: 2px solid {border_color};
                        border-radius: 8px;
                    }}
                    QLabel {{
                        color: #ffffff;
                        border: none;
                        font-weight: bold;
                    }}
                """)


        label_layout = QtWidgets.QVBoxLayout(self)
        label = QtWidgets.QLabel(title)
        label.setAlignment(label_allignment)
        label_layout.addWidget(label)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    widget = MainWindow()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())
