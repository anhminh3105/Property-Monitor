from PyQt5 import QtCore, QtWidgets, QtGui, uic
from numpy import genfromtxt
import pyqtgraph as pg
import setup
import datetime, sys
import send_mail as mail
import pandas as pd

class Reportwindow(QtWidgets.QWidget):
    def __init__(self, previous):
        QtWidgets.QWidget.__init__(self)
        self.previous = previous
        self.ui = uic.loadUi("basic_report_form.ui")
        '''self.ui.setStyleSheet("""
        .QWidget {
            background-color: rgb(20, 20, 20);
            }
        """)'''
        
        #Create environment for plotting data
        self.graph = pg.PlotWidget()
        #self.plotLayout = QtWidgets.QVBoxLayout()
        self.ui.bodyLayout.addWidget(self.graph)
        self.ui.bodyLayout.setContentsMargins(1,1,1,1)
        
        #Create options on header
        self.email = ClickLabel()
        self.temperature = ClickLabel()
        self.humidity = ClickLabel()
        self.pressure = ClickLabel()
        self.soil = ClickLabel()
        self.back_button = ClickLabel()
        self.type_change = ClickLabel()
        self.type_change.setStyleSheet('color: white')
        self.email.setPixmap(QtGui.QPixmap('button/email.png'))
        self.temperature.setPixmap(QtGui.QPixmap('button/temperature.png'))
        self.humidity.setPixmap(QtGui.QPixmap('button/humidity.png'))
        self.pressure.setPixmap(QtGui.QPixmap('button/pressure.png'))
        self.soil.setPixmap(QtGui.QPixmap('button/soil.png'))
        self.back_button.setPixmap(QtGui.QPixmap('button/back.png'))
        self.ui.headerLayout.setColumnStretch(0,4)
        self.ui.headerLayout.setColumnStretch(1,1)
        self.ui.headerLayout.setColumnStretch(2,1)
        self.ui.headerLayout.setColumnStretch(3,1)
        self.ui.headerLayout.setColumnStretch(4,1)
        self.ui.headerLayout.setColumnStretch(5,1)
        self.type_change.setText("Daily")
        font = QtGui.QFont()
        font.setBold(True)
        font.setPixelSize(20)
        self.type_change.setFont(font)
        self.ui.headerLayout.addWidget(self.back_button,0,0,0,3)
        self.ui.headerLayout.addWidget(self.email,0,1)
        self.ui.headerLayout.addWidget(self.temperature,0,2)
        self.ui.headerLayout.addWidget(self.humidity,0,3)
        self.ui.headerLayout.addWidget(self.pressure,0,4)
        self.ui.headerLayout.addWidget(self.soil,0,5)
        self.ui.headerLayout.addWidget(self.type_change,0,6)
        self.email.clicked.connect(self.sendEmail)
        self.temperature.clicked.connect(lambda: self.change_data_type('temp'))
        self.humidity.clicked.connect(lambda: self.change_data_type('humid'))
        self.soil.clicked.connect(lambda: self.change_data_type('soil'))
        self.pressure.clicked.connect(lambda: self.change_data_type('pressure'))
        self.back_button.clicked.connect(self.back)
        self.type_change.clicked.connect(self.changeType)
        
        self.data_type = None
        
        #Configure timer
        self.checkThreadTimer = QtCore.QTimer()
        self.checkThreadTimer.setInterval(1000)
        self.checkThreadTimer.timeout.connect(self.plot)
        self.checkThreadTimer.start()
    
    def change_data_type(self, data_type):
        self.data_type = data_type
    
    def sendEmail(self):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setText("Sending Email")
        if mail.send_mail():
            msg.setInformativeText("Email sent successfully")
        else:
            msg.setInformativeText("Sending email failed")
        msg.setWindowTitle("Message Box")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
        msg.exec_()
        
    def plot(self):
        try:
            data = None
            current = datetime.datetime.now()
            plot_type = self.type_change.text().lower()
            if(self.data_type is not None):
                url = 'database/' + self.data_type + '_' + plot_type + '.csv'
                try:
                    df = pd.read_csv(url)
                except:
                    return
                data = df.loc[:, 'Value']
                self.graph.plot(data, clear=True)
                if plot_type == 'hourly':
                    self.graph.setLimits(xMax=25, xMin=0, yMax = 120000, yMin=-50)
                    if self.data_type == 'temp':
                        self.graph.setLabels(left=('Celcius Degree', 'oC'), bottom=(current.strftime('%A, %dth %B, %Y'), 'hour'))
                    elif self.data_type == 'humid' or self.data_type == 'soil':
                        self.graph.setLabels(left=('Percentage', '%'), bottom=(current.strftime('%A, %dth %B, %Y'), 'hour'))
                    elif self.data_type == 'pressure':
                        self.graph.setLabels(left=('HectoPascal', 'hPa'), bottom=(current.strftime('%A, %dth %B, %Y'), 'hour'))
                    else:
                        pass
                elif plot_type == 'daily':
                    self.graph.setLimits(xMax=32, xMin=0, yMax = 120000, yMin=-50)
                    if self.data_type == 'temp':
                        self.graph.setLabels(left=('Celcius Degree', 'oC'), bottom=(current.strftime('%B'), 'day'))
                    elif self.data_type == 'humid' or self.data_type == 'soil':
                        self.graph.setLabels(left=('Percentage', '%'), bottom=(current.strftime('%B'), 'day'))
                    elif self.data_type == 'pressure':
                        self.graph.setLabels(left=('HectoPascal', 'hPa'), bottom=(current.strftime('%B'), 'day'))
                    else:
                        pass
                elif plot_type == 'monthly':
                    self.graph.setLimits(xMax=13, xMin=0, yMax = 120000, yMin=-50)
                    if self.data_type == 'temp':
                        self.graph.setLabels(left=('Celcius Degree', 'oC'), bottom=(current.strftime('%Y'), 'month'))
                    elif self.data_type == 'humid' or self.data_type == 'soil':
                        self.graph.setLabels(left=('Percentage', '%'), bottom=(current.strftime('%Y'), 'month'))
                    elif self.data_type == 'pressure':
                        self.graph.setLabels(left=('HectoPascal', 'hPa'), bottom=(current.strftime('%Y'), 'month'))
                    else:
                        pass
                elif plot_type == 'minutely':
                    self.graph.setLimits(xMax=61, xMin=0, yMax = 120000, yMin=-50)
                    if self.data_type == 'temp':
                        self.graph.setLabels(left=('Celcius Degree', 'oC'), bottom=(current.strftime('%I %p'), 'minute'))
                    elif self.data_type == 'humid' or self.data_type == 'soil':
                        self.graph.setLabels(left=('Percentage', '%'), bottom=(current.strftime('%I %p'), 'minute'))
                    elif self.data_type == 'pressure':
                        self.graph.setLabels(left=('HectoPascal', 'hPa'), bottom=(current.strftime('%I %p'), 'minute'))
                    else:
                        pass
                else:
                    pass
        except:
            print("Unexpected error at plot:", sys.exc_info()[0])
            

    
    def back(self):
        self.checkThreadTimer.stop()
        self.previous.setVisible(True)
        self.ui.setVisible(False)

    def changeType(self):
        if self.type_change.text() == "Daily":
            self.type_change.setText("Monthly")
        elif self.type_change.text() == "Monthly":
            self.type_change.setText("Minutely")
        elif self.type_change.text() == "Minutely":
            self.type_change.setText("Hourly")
        else:
            self.type_change.setText("Daily")

class ClickLabel(QtWidgets.QLabel):
    clicked = QtCore.pyqtSignal()
    def mouseReleaseEvent(self, event):
        self.clicked.emit()
        QtWidgets.QLabel.mouseReleaseEvent(self, event)