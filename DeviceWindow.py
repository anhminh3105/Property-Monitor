from PyQt5 import QtCore, QtWidgets, QtGui, uic
import csv
import setup
import paho.mqtt.client as mqtt
#import QtQuick.Controls

class DeviceWindow(QtWidgets.QWidget):
    def __init__(self, previous):
        QtWidgets.QWidget.__init__(self)
        self.previous = previous
        self.ui = uic.loadUi("device.ui")
        
        self.back_button = ClickLabel()
        self.back_button.setPixmap(QtGui.QPixmap('button/back.png'))
        self.ui.headerLayout.addWidget(self.back_button,0,0,0,4)
        self.back_button.clicked.connect(self.back)
        
        self.table = QtWidgets.QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(['Device', 'Location', 'Status'])
        self.ui.bodyLayout.addWidget(self.table)
        self.header = self.table.horizontalHeader()
        self.header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        self.header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        self.header.setStyleSheet('::section{background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,stop:0 #616161,stop: 0.5 #505050,stop: 0.6 #434343, stop:1 #656565);color: white;padding-left: 4px;border: 1px solid #6c6c6c;}')
        self.table.verticalHeader().hide()
        
        self.device = []
        self.update()
        
        self.table.setStyleSheet("""
                        .QTableWidget {
                                background-color: transparent;
                        }""")
        
        #Configuration for light adjustment
        self.table.cellDoubleClicked.connect(self.doubleClicked)
        self.ui.splitter.setSizes([480, 0])
        self.mode = ClickLabel('AUTO')
        self.mode.setStyleSheet('color: white;')
        self.collapse = ClickLabel('OK')
        self.collapse.setStyleSheet('color: white;')
        self.mode.setAlignment(QtCore.Qt.AlignCenter)
        self.font = QtGui.QFont()
        self.font.setBold(True)
        self.font.setPixelSize(18)
        self.mode.setFont(self.font)
        self.collapse.setFont(self.font)
        self.collapse.setAlignment(QtCore.Qt.AlignCenter)
        self.slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(5)
        self.ui.light_adjust_layout.addWidget(self.mode)
        self.ui.light_adjust_layout.addWidget(self.slider)
        self.ui.light_adjust_layout.addWidget(self.collapse)
        self.ui.light_adjust_layout.setStretch(0, 2)
        self.ui.light_adjust_layout.setStretch(1, 5)
        self.ui.light_adjust_layout.setStretch(2, 1)
        self.collapse.clicked.connect(lambda: self.ui.splitter.setSizes([480, 0]))
        self.mode.clicked.connect(self.modeChange)
        self.ui.light_adjust_label.setStyleSheet('color: white;')
        self.ui.light_adjust_label.setFont(self.font)
        self.slider.valueChanged.connect(self.lightControl)
        
        #Configure timer
        self.checkThreadTimer = QtCore.QTimer()
        self.checkThreadTimer.setInterval(3000)
        self.checkThreadTimer.timeout.connect(self.update)
        self.checkThreadTimer.start()
        
        #Setup MQTT
        self.client = mqtt.Client()
        # client.on_connect = on_connect
        self.client.username_pw_set(setup.mqtt_username,setup.mqtt_password)
        self.client.connect(host=setup.mqtt_broker_ip, port=setup.port, keepalive=60)
        
    def back(self):
        self.checkThreadTimer.stop()
        self.previous.setVisible(True)
        self.ui.setVisible(False)
    
    def update(self):   #Read data from device.csv and update self.device list
        self.device.clear() #Empty the list for new update
        with open(setup.device_csv, 'r') as deviceCSV:
            device = csv.reader(deviceCSV, delimiter = ',')
            for row in device:
                self.device.append(row)
        self.display()
                
    def display(self):
        self.table.setRowCount(0)
        for i in range(len(self.device)):
            self.table.insertRow(i)
            name = QtWidgets.QTableWidgetItem(self.device[i][0])
            location = QtWidgets.QTableWidgetItem(self.device[i][2])
            if int(self.device[i][3]) == 1:
                status = QtWidgets.QTableWidgetItem("Enable")
            elif int(self.device[i][3]) == 0:
                status = QtWidgets.QTableWidgetItem("Disable")
            else:
                status = QtWidgets.QTableWidgetItem("Unknown")

            #Set Color
            name.setForeground(QtGui.QBrush(QtGui.QColor('white')))
            location.setForeground(QtGui.QBrush(QtGui.QColor('white')))
            if int(self.device[i][3]) == 1:
                status.setForeground(QtGui.QBrush(QtGui.QColor('lightblue')))
            elif int(self.device[i][3]) == 0:
                status.setForeground(QtGui.QBrush(QtGui.QColor('red')))
            else:
                status.setForeground(QtGui.QBrush(QtGui.QColor('white')))
            
            #Set Text Alignment
            name.setTextAlignment(QtCore.Qt.AlignCenter)
            location.setTextAlignment(QtCore.Qt.AlignCenter)
            status.setTextAlignment(QtCore.Qt.AlignCenter)
            
            #Disable Editting
            name.setFlags(QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled)
            location.setFlags(QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled)
            status.setFlags(QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled)
            
            #Set Item to Table
            self.table.setItem(i, 0, name)
            self.table.setItem(i, 1, location)
            self.table.setItem(i, 2, status)
    
    def doubleClicked(self, row, col):
        #item = self.table.item(row, col)
        print('Device: ', self.device[row][0], '\nCode: ', self.device[row][1], '\nLocation: ', self.device[row][2], '\nStatus: ', self.device[row][3])
        if(self.device[row][1] == 'KEYES2560_PIR'):
            self.ui.splitter.setSizes([480, 1])
            text = self.device[row][0] + ' light adjustment'
            self.ui.light_adjust_label.setText(text)
    
    def lightControl(self):
        if self.mode.text() == 'MANUAL':
            if self.slider.value() < 3:
                self.client.loop_start()
                self.client.publish(topic="LED", payload="10")
                self.client.loop_stop(force=False)
            else:
                self.client.loop_start()
                self.client.publish(topic="LED", payload="11")
                self.client.loop_stop(force=False)
        elif self.mode.text() == 'AUTO':
            pass
        
    def modeChange(self):
        if self.mode.text() == 'MANUAL':
            self.mode.setText('AUTO')
            self.client.loop_start()
            self.client.publish(topic="LED", payload="00")
            self.client.loop_stop(force=False)
        else:
            self.mode.setText('MANUAL')
            if self.slider.value() < 3:
                self.client.loop_start()
                self.client.publish(topic="LED", payload="10")
                self.client.loop_stop(force=False)
            else:
                self.client.loop_start()
                self.client.publish(topic="LED", payload="11")
                self.client.loop_stop(force=False)
    
class ClickLabel(QtWidgets.QLabel):
    clicked = QtCore.pyqtSignal()
    def mouseReleaseEvent(self, event):
        self.clicked.emit()
        QtWidgets.QLabel.mouseReleaseEvent(self, event)
            