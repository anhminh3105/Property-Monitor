from PyQt5 import QtCore, QtGui, QtWidgets, uic
from Mainwindow import Mainwindow
import sys
import setup

if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    if len(sys.argv) > 1:
        print(len(sys.argv))
        if sys.argv[1] == 'window':
            setup.window = True
        elif sys.argv[1] == 'fullscreen':
            setup.window = False
        else:
            setup.window = True
    ui = Mainwindow()
    if setup.window:
        ui.ui.show()
    else:
        ui.ui.showFullScreen()
    sys.exit(app.exec_())
