from PyQt5 import QtCore, QtWidgets, QtGui, uic
import cv2
from pyqtgraph import ImageView

class StreamWindow(QtWidgets.QWidget):
    def __init__(self, previous, camera = None):
        QtWidgets.QWidget.__init__(self)
        self.previous = previous
        self.camera = camera
        self.ui = uic.loadUi("basic_report_form.ui")
        #self.layout = QtWidgets.QVBoxLayout(self.ui.body)
        self.image_view = ImageView()
        self.ui.bodyLayout.addWidget(self.image_view)
        
        self.back_button = ClickLabel()
        self.back_button.setPixmap(QtGui.QPixmap('button/back.png'))
        self.ui.headerLayout.addWidget(self.back_button,0,0,0,4)
        self.back_button.clicked.connect(self.back)
        
        self.checkThreadTimer = QtCore.QTimer()
        self.checkThreadTimer.setInterval(100)
        self.checkThreadTimer.timeout.connect(self.update_image)
        self.checkThreadTimer.start()

    def update_image(self):
        frame = self.camera.get_frame()
        image = cv2.transpose(frame)
        self.image_view.setImage(image)
    
    def back(self):
        self.previous.setVisible(True)
        self.ui.setVisible(False)
        self.checkThreadTimer.stop()
        self.camera.close_camera()

class Camera:
    def __init__(self, cam_num):
        self.cam_num = cam_num
        self.cap = None

    def initialize(self):
        self.cap = cv2.VideoCapture(self.cam_num)
        if (self.cap.isOpened()== False): 
            print("Error opening video stream or file")
            return False
        return True
    
    def get_frame(self):
        ret, self.last_frame = self.cap.read()
        return self.last_frame

    def acquire_movie(self, num_frames):
        movie = []
        for _ in range(num_frames):
            movie.append(self.get_frame())
        return movie

    def set_brightness(self, value):
        self.cap.set(cv2.CAP_PROP_BRIGHTNESS, value)
    
    def get_brightness(self):
        return self.cap.get(cv2.CAP_PROP_BRIGHTNESS)

    def __str__(self):
        return 'OpenCV Camera {}'.format(self.cam_num)
    
    def close_camera(self):
        self.cap.release()

class ClickLabel(QtWidgets.QLabel):
    clicked = QtCore.pyqtSignal()
    def mouseReleaseEvent(self, event):
        self.clicked.emit()
        QtWidgets.QLabel.mouseReleaseEvent(self, event)