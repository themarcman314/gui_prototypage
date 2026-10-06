import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import Qt

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        main_layout = QtWidgets.QVBoxLayout(self)
        top_layout = QtWidgets.QHBoxLayout()
        center_top = QtWidgets.QVBoxLayout()
        top_center_top = QtWidgets.QHBoxLayout()
        bottom_center_top = QtWidgets.QHBoxLayout()

        security_logs = Tile("Recent Security Logs")
        user_auth = Tile("User Authentication")
        system_armed = Tile("Armed status")
        pir_motion = Tile("PIR Motion Detector")
        ambient_environment = Tile("Ambient environment")
        manual_controls = Tile("Manual Controls")
        ultrasonic_distance = Tile("Ultrasonic Distance")

        main_layout.addWidget(security_logs)
        main_layout.insertLayout(0,top_layout)
        main_layout.setStretch(0,2)
        main_layout.setStretch(1,1)

        top_layout.insertWidget(0, system_armed)
        top_layout.insertWidget(1, user_auth)
        top_layout.insertLayout(1, center_top)
        top_layout.setStretch(0,1)
        top_layout.setStretch(1,2)
        top_layout.setStretch(2,1)

        center_top.insertLayout(0, top_center_top)
        center_top.insertLayout(1, bottom_center_top)
        center_top.setStretch(0,2)
        center_top.setStretch(1,1)

        top_center_top.insertWidget(0, pir_motion)
        top_center_top.insertWidget(1, ultrasonic_distance)
        top_center_top.setStretch(0, 1)
        top_center_top.setStretch(1, 2)

        bottom_center_top.insertWidget(0, ambient_environment)
        bottom_center_top.insertWidget(1, manual_controls)
        bottom_center_top.setStretch(0, 2)
        bottom_center_top.setStretch(1, 1)



class Tile(QtWidgets.QFrame):
    def __init__(self, title: str, bg_color: str = "#1e222a", border_color: str = "#3b4252"):
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


        # we could use a label for the tile
        label = QtWidgets.QLabel(self)
        label.setText(title)
        label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        label.setMargin(10)

        # or create a new widget for only the tile
        # title is always above the widget
        #label_layout = QtWidgets.QVBoxLayout(self)
        #label = QtWidgets.QLabel(title)
        #label.setAlignment(label_allignment)
        #label_layout.addWidget(label)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    widget = MainWindow()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())
