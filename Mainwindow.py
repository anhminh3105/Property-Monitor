from PyQt5 import QtCore, QtWidgets, QtGui, uic
from Reportwindow import Reportwindow
from Climatewindow import Climatewindow
from StreamWindow import StreamWindow, Camera
from DeviceWindow import DeviceWindow
import setup

class Mainwindow(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.ui = uic.loadUi("Mainwindow.ui")
        self.ui.setStyleSheet("""
        .QWidget {
            background-color: rgb(0, 0, 0);
            }
        """)
        self.initialise()
        
        self.ui.headerLayout.addWidget(self.setting, 0, 2)
        self.ui.headerLayout.addWidget(self.help, 0, 1)
        self.setting.setText("SETTINGS")
        self.setting.setStyleSheet('color: white; background-color: rgb(40, 40, 40)')
        self.setting.setAlignment(QtCore.Qt.AlignCenter)
        self.help.setText("HELP")
        self.help.setStyleSheet('color: white; background-color: rgb(40, 40, 40)')
        self.help.setAlignment(QtCore.Qt.AlignCenter)
        self.setting.setFont(self.font)
        self.help.setFont(self.font)
        self.grid = QtWidgets.QGridLayout()
        self.grid.addWidget(self.climate_button, 0, 2)
        self.grid.addWidget(self.security_button, 1, 2)
        self.grid.addWidget(self.report_button, 2, 2)
        self.grid.addWidget(self.device_button, 2, 1)
        self.grid.addWidget(self.power_consumption_button, 2, 0)
        self.grid.addWidget(self.home, 0, 0, 2, 2)
        
        self.ui.mainDisplay.setLayout(self.grid)
        self.grid.setContentsMargins(0,0,0,0)
        self.grid.setVerticalSpacing(3)
        self.grid.setHorizontalSpacing(3)
        self.report_button.clicked.connect(self.report_clicked)
        self.climate_button.clicked.connect(self.climate_clicked)
        self.security_button.clicked.connect(self.security_clicked)
        self.device_button.clicked.connect(self.device_clicked)
    
    def initialise(self):
        self.url = setup.url
        self.home = ClickLabel()
        self.setting = ClickLabel()
        self.help = ClickLabel()
        self.climate_button = ClickLabel()
        self.device_button = ClickLabel()
        self.power_consumption_button = ClickLabel()
        self.report_button = ClickLabel()
        self.security_button = ClickLabel()
        self.ui.vamk.setPixmap(QtGui.QPixmap('other_image/vamok-logo.png'))
        self.climate_button.setPixmap(QtGui.QPixmap('button/climate_button.png'))
        self.device_button.setPixmap(QtGui.QPixmap('button/active_device.png'))
        self.power_consumption_button.setPixmap(QtGui.QPixmap('button/power_consumption_button.png'))
        self.report_button.setPixmap(QtGui.QPixmap('button/report_button.png'))
        self.security_button.setPixmap(QtGui.QPixmap('button/security_button.png'))
        self.home.setPixmap(QtGui.QPixmap('button/home.jpg'))
    
        self.font = QtGui.QFont()
        self.font.setBold(True)
        self.font.setPixelSize(18)
        
    def report_clicked(self):
        self.report_window = Reportwindow(self.ui)
        if setup.window:
            self.report_window.ui.show()
        else:
            self.report_window.ui.showFullScreen()
        self.ui.setVisible(False)
        
    def climate_clicked(self):
        self.climate_window = Climatewindow(self.ui)
        if setup.window:
            self.climate_window.ui.show()
        else:
            self.climate_window.ui.showFullScreen()
        self.ui.setVisible(False)
    
    def security_clicked(self):
        self.camera = Camera(self.url)
        if self.camera.initialize():
            self.stream_window = StreamWindow(self.ui, self.camera)
            if setup.window:
                self.stream_window.ui.show()
            else:
                self.stream_window.ui.showFullScreen()
            self.ui.setVisible(False)
        else:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setText("Camera error")
            msg.setInformativeText("Can not open stream")
            msg.setWindowTitle("ERROR")
            msg.setDetailedText("Error opening video stream or file. Please check the connection carefully!!!")
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
            msg.exec_()
    
    def device_clicked(self):
        self.device_window = DeviceWindow(self.ui)
        if setup.window:
            self.device_window.ui.show()
        else:
            self.device_window.ui.showFullScreen()
        self.ui.setVisible(False)

class ClickLabel(QtWidgets.QLabel):
    clicked = QtCore.pyqtSignal()

    def mousePressEvent(self, event):
        self.clicked.emit()
        QtWidgets.QLabel.mouseReleaseEvent(self, event)