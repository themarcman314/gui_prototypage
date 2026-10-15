import sys
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import QTimer, Qt, Signal, QObject
import pyqtgraph as pg
import datetime

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Security Dashboard")
        self.dashboard = Dashboard()
        self.setCentralWidget(self.dashboard)

class AppState(QObject):
    armed_status_changed = Signal(bool)

    def __init__(self):
        super().__init__()
        self._is_armed = False

        @property
        def is_armed(self):
            return self._is_armed

        @is_armed.setter
        def is_armed(self, value: bool):
            if self._is_armed != value:
                self._is_armed = value
                self.armed_status_changed.emit(value)

class Dashboard(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.state = AppState()

        self.user_auth = SystemAuth()
        self.security_logs = SecurityLogs()
        self.system_armed = SystemArmed()
        self.pir_motion = PirMotion()
        self.ambient_environment = AmbientEnvironment()
        self.manual_controls = ManualControls()
        self.ultrasonic_distance = UltrasonicDistance()

        #self.security_logs = Tile("Recent Security Logs")
        #self.system_armed = Tile("Armed status")
        #self.pir_motion = Tile("PIR Motion Detector")
        #self.ambient_environment = Tile("Ambient environment")
        #self.manual_controls = Tile("Manual Controls")
        #self.ultrasonic_distance = Tile("Ultrasonic Distance")

        self._layout_setup()


    # consider using grid layout as an alternative as it is likely more intuitive
    def _layout_setup(self):
        main_layout = QtWidgets.QVBoxLayout(self)
        top_layout = QtWidgets.QHBoxLayout()
        center_top = QtWidgets.QVBoxLayout()
        top_center_top = QtWidgets.QHBoxLayout()
        bottom_center_top = QtWidgets.QHBoxLayout()
        main_layout.addWidget(self.security_logs)
        main_layout.insertLayout(0,top_layout)
        main_layout.setStretch(0,2)
        main_layout.setStretch(1,1)

        top_layout.insertWidget(0, self.system_armed)
        top_layout.insertWidget(1, self.user_auth)
        top_layout.insertLayout(1, center_top)
        top_layout.setStretch(0,1)
        top_layout.setStretch(1,2)
        top_layout.setStretch(2,1)

        center_top.insertLayout(0, top_center_top)
        center_top.insertLayout(1, bottom_center_top)
        center_top.setStretch(0,2)
        center_top.setStretch(1,1)

        top_center_top.insertWidget(0, self.pir_motion)
        top_center_top.insertWidget(1, self.ultrasonic_distance)
        top_center_top.setStretch(0, 1)
        top_center_top.setStretch(1, 2)

        bottom_center_top.insertWidget(0, self.ambient_environment)
        bottom_center_top.insertWidget(1, self.manual_controls)
        bottom_center_top.setStretch(0, 2)
        bottom_center_top.setStretch(1, 1)



class Tile(QtWidgets.QFrame):
    def __init__(self, bg_color: str = "#1e222a", border_color: str = "#3b4252"):
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
        #label = QtWidgets.QLabel(self)
        #label.setText(title)
        #label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        #label.setMargin(10)

        # or create a new widget for only the tile
        # title is always above the widget
        #label_layout = QtWidgets.QVBoxLayout(self)
        #label = QtWidgets.QLabel(title)
        #label.setAlignment(label_allignment)
        #label.setAlignment(Qt.AlignmentFlag.AlignTop)
        #label_layout.addWidget(label)
class SystemArmed(Tile):
    def __init__(self):
        super().__init__()
        tile_layout = QtWidgets.QVBoxLayout(self)
        now = datetime.datetime.now()
        self.time = QtWidgets.QLabel(now.strftime('%H:%M:%S'), alignment=Qt.AlignmentFlag.AlignHCenter)
        tile_layout.insertWidget(0, self.time)
        #self.armed_status_label = QtWidgets.QLabel(, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._on_second)
        self.timer.start(1000)

    def _on_second(self):
        now = datetime.datetime.now()
        self.time.setText(now.strftime('%H:%M:%S'))



class ManualControls(Tile):
    def __init__(self):
        super().__init__()
        tile_layout = QtWidgets.QVBoxLayout(self)
        label = QtWidgets.QLabel("Manual Controls", alignment=Qt.AlignmentFlag.AlignTop)
        tile_layout.insertWidget(0, label)

class PirMotion(Tile):
    def __init__(self):
        super().__init__()
        tile_layout = QtWidgets.QVBoxLayout(self)
        label = QtWidgets.QLabel("PIR Motion Sensor", alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        tile_layout.insertWidget(0, label)

class AmbientEnvironment(Tile):
    def __init__(self):
        super().__init__()
        tile_layout = QtWidgets.QVBoxLayout(self)
        label = QtWidgets.QLabel("Ambient Environment", alignment=Qt.AlignmentFlag.AlignTop)
        tile_layout.insertWidget(0, label)


class SecurityLogs(Tile):
    def __init__(self):
        super().__init__()
        tile_layout = QtWidgets.QVBoxLayout(self)
        label = QtWidgets.QLabel("Recent Security Logs", alignment=Qt.AlignmentFlag.AlignTop)
        tile_layout.insertWidget(0, label)



class UltrasonicDistance(Tile):
    def __init__(self):
        super().__init__()
        tile_layout = QtWidgets.QVBoxLayout(self)
        label = QtWidgets.QLabel("Ultrasonic Distance", alignment=Qt.AlignmentFlag.AlignTop)
        self.plot_widget = pg.PlotWidget( labels={'bottom': ('Time', 's'), 'left': ('Distance', 'cm')})
        tile_layout.insertWidget(0,label)
        tile_layout.addWidget(self.plot_widget)
        data = [2,4,1,8]
        self.plot_widget.plot(data)


class SystemAuth(Tile):
    armed = True

    def __init__(self):
        super().__init__()
        tile_layout = QtWidgets.QVBoxLayout(self)

        label = QtWidgets.QLabel("User Authentication")
        passwd_text = QtWidgets.QLabel("Enter Password:")
        passwd_box = QtWidgets.QLineEdit(echoMode=QtWidgets.QLineEdit.EchoMode.Password)
        self.toggle_btn = QtWidgets.QPushButton("Disarm System" if self.armed == True else "Arm System")
        self.toggle_btn.clicked.connect(self._on_toggle)

        # use QFormLayout in order to wrap passwd text and box together
        form_layout = QtWidgets.QFormLayout()
        form_layout.setRowWrapPolicy(QtWidgets.QFormLayout.RowWrapPolicy.WrapAllRows)
        form_layout.addRow(passwd_text, passwd_box)

        tile_layout.insertWidget(0,label, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        tile_layout.insertLayout(1,form_layout)
        tile_layout.insertWidget(2, self.toggle_btn, alignment=Qt.AlignmentFlag.AlignCenter)

    def _on_toggle(self):
        self.armed = not(self.armed)
        new_text = "Disarm System" if self.armed == True else "Arm System"
        self.toggle_btn.setText(new_text)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    widget = MainWindow()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())
