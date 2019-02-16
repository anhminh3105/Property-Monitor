from PyQt5 import QtCore, QtWidgets, QtGui, uic
import sys
import setup
import pandas as pd

class Climatewindow(QtWidgets.QWidget):
    def __init__(self, previous):
        QtWidgets.QWidget.__init__(self)
        self.previous = previous
        self.ui = uic.loadUi("climate.ui")
        self.headerLayout = QtWidgets.QGridLayout()
        self.back_button = ClickLabel()
        self.setting = ClickLabel()
        self.back_button.setPixmap(QtGui.QPixmap('button/back.png'))
        self.setting.setPixmap(QtGui.QPixmap('button/setting.png'))
        self.back_button.clicked.connect(self.back)
        self.headerLayout.addWidget(self.back_button,0,0,0,5)
        self.headerLayout.addWidget(self.setting,0,6)
        self.ui.header.setLayout(self.headerLayout)
        
        self.min_temp = None;
        self.max_temp = None;
        self.min_humid = None;
        self.max_humid = None;
        self.min_soil = None;
        self.max_soil = None;
        self.min_pressure = None;
        self.max_pressure = None;
        self.update()
        self.checkThreadTimer = QtCore.QTimer()
        self.checkThreadTimer.setInterval(3000)
        self.checkThreadTimer.timeout.connect(self.update)
        self.checkThreadTimer.start()

    def back(self):
        self.checkThreadTimer.stop()
        self.previous.setVisible(True)
        self.ui.setVisible(False)
    
    def update(self):
        """Soil moisture level"""
        try:
            data = pd.read_csv(setup.soil_csv)
            val = int(data.iloc[-1]['Value'])
            if self.min_soil is None or self.max_soil is None:
                self.min_soil = val
                self.max_soil = val
            if val > self.max_soil:
                self.max_soil = val
            elif val < self.min_soil:
                self.min_soil = val
            text = str(val) + '%'
            self.ui.soil_value.setText(text)
            text = str(self.max_soil) + '% / ' + str(self.min_soil) + '%'
            self.ui.soil_range.setText(text)
            if val <= 50 and val > 40:    #Normal
                #self.ui.soil_image.setPixmap(QtGui.QPixmap('other_image/safe.png'))
                self.ui.soil_status.setText("Normal moisture")
                self.ui.soil.setStyleSheet("""
                    .QWidget {
                        background-color: rgb(148, 255, 136);
                    }""")
            elif val < 40 and val >= 30:  ##Warning
                #self.ui.soil_image.setPixmap(QtGui.QPixmap('other_image/warning.png'))
                self.ui.soil_status.setText("Low moisture")
                self.ui.soil.setStyleSheet("""
                    .QWidget {
                            background-color: rgb(255, 237, 136);
                    }""")
            elif val < 30:     #Lower severe condition
                #self.ui.soil_image.setPixmap(QtGui.QPixmap('other_image/dry.png'))
                self.ui.soil_status.setText("Too dry")
                self.ui.soil.setStyleSheet("""
                    .QWidget {
                            background-color: rgb(255, 62, 101);
                    }""")
            elif val > 50:     #Upper severe condition
                #self.ui.soil_image.setPixmap(QtGui.QPixmap('other_image/flood.png'))
                self.ui.soil_status.setText("Too much water")
                self.ui.soil.setStyleSheet("""
                    .QWidget {
                            background-color: rgb(255, 62, 101);
                    }""")
        except:
            print("Unexpected error at update soil:", sys.exc_info()[0])
        """----------------------"""
        
        """Humidity level"""
        try:
            data = pd.read_csv(setup.humid_csv)
            val = int(data.iloc[-1]['Value'])
            if self.min_humid is None or self.max_humid is None:
                self.min_humid = val
                self.max_humid = val
            if val > self.max_humid:
                self.max_humid = val
            elif val < self.min_humid:
                self.min_humid = val
            text = str(val) + '%'
            self.ui.humidity_value.setText(text)
            text = str(self.max_humid) + '% / ' + str(self.min_humid) + '%'
            self.ui.humidity_range.setText(text)
            if val <= 50 and val > 40:    #Normal
                #self.ui.humidity_image.setPixmap(QtGui.QPixmap('other_image/safe.png'))
                self.ui.humidity_status.setText("Normal humidity")
                self.ui.humidity.setStyleSheet("""
                    .QWidget {
                        background-color: rgb(148, 255, 136);
                    }""")
            elif val <= 40 and val > 25:  #Lower warning
                #self.ui.humidity_image.setPixmap(QtGui.QPixmap('other_image/warning.png'))
                self.ui.humidity_status.setText("Low humidity")
                self.ui.humidity.setStyleSheet("""
                    .QWidget {
                            background-color: rgb(255, 237, 136);
                    }""")
            elif val <= 70 and val > 50:  #Upper warning
                #self.ui.humidity_image.setPixmap(QtGui.QPixmap('other_image/warning.png'))
                self.ui.humidity_status.setText("High humidity")
                self.ui.humidity.setStyleSheet("""
                    .QWidget {
                            background-color: rgb(255, 237, 136);
                    }""")
            elif val > 70:     #Upper severe condition
                #self.ui.humidity_image.setPixmap(QtGui.QPixmap('other_image/rain.png'))
                self.ui.humidity_status.setText("Too high humidity")
                self.ui.humidity.setStyleSheet("""
                    .QWidget {
                            background-color: rgb(255, 62, 101);
                    }""")
            else:       #Lower severe condition
                #self.ui.humidity_image.setPixmap(QtGui.QPixmap('other_image/dry.png'))
                self.ui.humidity_status.setText("Too dry")
                self.ui.humidity.setStyleSheet("""
                    .QWidget {
                            background-color: rgb(255, 62, 101);
                    }""")
        except:
            print("Unexpected error at update humidity:", sys.exc_info()[0])
        """----------------------"""
        
        """Temperature level"""
        try:
            data = pd.read_csv(setup.temp_csv)
            val = int(data.iloc[-1]['Value'])
            if self.min_temp is None or self.max_temp is None:
                self.min_temp = val
                self.max_temp = val
            if val > self.max_temp:
                self.max_temp = val
            elif val < self.min_temp:
                self.min_temp = val
            text = str(val) + chr(176) + 'C'
            self.ui.temperature_value.setText(text)
            text = str(self.max_temp) + chr(176) + 'C / ' + str(self.min_temp) + chr(176) + 'C'
            self.ui.temperature_range.setText(text)
            if val <= 25 and val > 19:    #Normal
                #self.ui.temperature_image.setPixmap(QtGui.QPixmap('other_image/safe.png'))
                self.ui.temperature_status.setText("Normal temperature")
                self.ui.temperature.setStyleSheet("""
                    .QWidget {
                        background-color: rgb(148, 255, 136);
                    }""")
            elif val <= 35 and val > 25:  #Upper Warning
                #self.ui.temperature_image.setPixmap(QtGui.QPixmap('other_image/warning.png'))
                self.ui.temperature_status.setText("High temperature")
                self.ui.temperature.setStyleSheet("""
                    .QWidget {
                            background-color: rgb(255, 237, 136);
                    }""")
            elif val <= 19 and val > 15:  ##Lower warning
                #self.ui.temperature_image.setPixmap(QtGui.QPixmap('other_image/warning.png'))
                self.ui.temperature_status.setText("Low temperature")
                self.ui.temperature.setStyleSheet("""
                    .QWidget {
                            background-color: rgb(255, 237, 136);
                    }""")
            elif val > 35:     #Upper Severe condition
                #self.ui.temperature_image.setPixmap(QtGui.QPixmap('other_image/fire.png'))
                self.ui.temperature_status.setText("Too hot")
                self.ui.temperature.setStyleSheet("""
                    .QWidget {
                            background-color: rgb(255, 62, 101);
                    }""")
            else:       #Lower Severe condition
                #self.ui.temperature_image.setPixmap(QtGui.QPixmap('other_image/freeze.png'))
                self.ui.temperature_status.setText("Too cold")
                self.ui.temperature.setStyleSheet("""
                    .QWidget {
                            background-color: rgb(255, 62, 101);
                    }""")
        except:
            print("Unexpected error at update temperature:", sys.exc_info()[0])
        """----------------------"""
        
        """Air Pressure level"""
        try:
            data = pd.read_csv(setup.pressure_csv)
            val = int(data.iloc[-1]['Value']/100)
            if self.min_pressure is None or self.max_pressure is None:
                self.min_pressure = val
                self.max_pressure = val
            if val > self.max_pressure:
                self.max_pressure = val
            elif val < self.min_pressure:
                self.min_pressure = val
            text = str(val) + 'hPa'
            self.ui.pressure_value.setText(text)
            text = str(self.max_pressure) + ' / ' + str(self.min_pressure)
            self.ui.pressure_range.setText(text)
            #self.ui.temperature_image.setPixmap(QtGui.QPixmap('other_image/safe.png'))
            self.ui.pressure_status.setText("Normal pressure")
            self.ui.pressure.setStyleSheet("""
                .QWidget {
                    background-color: rgb(148, 255, 136);
                }""")
        except:
            print("Unexpected error at update pressure:", sys.exc_info()[0])
        """----------------------"""
        
class ClickLabel(QtWidgets.QLabel):
    clicked = QtCore.pyqtSignal()
    def mouseReleaseEvent(self, event):
        self.clicked.emit()
        QtWidgets.QLabel.mouseReleaseEvent(self, event)