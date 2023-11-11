import sys
from PySide2.QtWidgets import *
from PySide2.QtCore import Qt, SIGNAL, SLOT, QFile, qDebug, QTime, QCoreApplication, QEventLoop
from PySide2.QtMultimedia import QCamera, QCameraImageCapture, QVideoFrame, QImageEncoderSettings
from PySide2.QtGui import QPixmap, QImage, QWindow
from .MainWindowUI import Ui_MainWindow
from PaintDialogFiles.PaintDialog import PaintDialog
import numpy as np
import cv2 as cv

class MainWindow(QMainWindow):
    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.homebtn.clicked.connect(self.on_homebtn_clicked)
        self.ui.simbtn.clicked.connect(self.on_simbtn_clicked)
        self.ui.manualbtn.clicked.connect(self.on_manualbtn_clicked)

        self.ui.startbtn.clicked.connect(self.on_startbtn_clicked)
        self.ui.stopbtn.clicked.connect(self.on_stopbtn_clicked)

        self.ui.exitui.triggered.connect(self.on_window_closed)

        self.ui.capturebtn.clicked.connect(self.on_capturebtn_clicked)
        self.ui.sinorcon.stateChanged.connect(self.on_sinorcon_stateChanged)
        self.ui.capturesstopbtn.clicked.connect(self.on_capturesstopbtn_clicked)

        self.ui.cameraviewbtn.clicked.connect(self.on_imageview_changed)
        self.ui.procesviewbtn.clicked.connect(self.on_imageview_changed)

        self.stop = False
        self.continuousRun = False

        self.camera = QCamera()
        self.imageCapture = QCameraImageCapture(self.camera)
        self.imageCapture.imageCaptured.connect(self.newImageFromWebcam)

        imageSettings = QImageEncoderSettings()
        imageSettings.setCodec("bmp")
        self.imageCapture.setEncodingSettings(imageSettings)

        self.imageCapture.setBufferFormat(QVideoFrame.Format_RGB24)
        self.camera.setCaptureMode(QCamera.CaptureVideo)
        self.camera.start()

        print("Found")

    def on_Primebtn_Clicked(self):
        qDebug("Yes")

    def on_homebtn_clicked(self):
        qDebug("Home")
        self.ui.stackedWidget.setCurrentIndex(0)

    def on_simbtn_clicked(self):
        qDebug("Sim")
        self.ui.stackedWidget.setCurrentIndex(1)

    def on_manualbtn_clicked(self):
        qDebug("Manual")
        self.ui.stackedWidget.setCurrentIndex(2)

    def on_startbtn_clicked(self):
        qDebug("This is the start button")
        dialog = PaintDialog(self)
        if (dialog.exec_() == 1):
            image = dialog.scribbleArea.image

    def on_stopbtn_clicked(self):
        qDebug("This is the stop button")

    def on_capturebtn_clicked(self):
        qDebug("Capture buttonPressed")
        if self.ui.sinorcon.checkState() is Qt.Unchecked:
            self.runSingle()
        elif self.ui.sinorcon.checkState() is Qt.Checked:
            if self.continuousRun is False:
                self.continuousRun = True
                self.runContinous()

    def on_sinorcon_stateChanged(self, state):
        if state == 0:
            self.ui.capturesstopbtn.setEnabled(False)
        elif state == 2:
            self.ui.capturesstopbtn.setEnabled(True)

    def on_capturesstopbtn_clicked(self):
        self.stop = True

    def on_imageview_changed(self):
        if self.ui.cameraviewbtn.isChecked() is True:
            self.ui.imageviewstack.setCurrentIndex(0)
        else:
            self.ui.imageviewstack.setCurrentIndex(1)

    def runSingle(self):
        if self.imageCapture.isReadyForCapture():
            path = "{}/capture.bmp"
            self.imageCapture.capture(path.format(qApp.applicationDirPath()))

    def runContinous(self):
        qDebug("Yes")
        while(not self.stop and self.ui.sinorcon.checkState() == Qt.Checked):
            if self.imageCapture.isReadyForCapture():
                path = "{}/capture.bmp"
                self.imageCapture.capture(path.format(qApp.applicationDirPath()))

            self.delay_ms(10)
        self.stop = False
        self.continuousRun = False

    def newImageFromWebcam(self, id, image):
        if image.isNull():
            return

        width = self.ui.imageview.width()
        height = self.ui.imageview.height()

        self.ui.imageview.setPixmap(QPixmap.fromImage(image).scaled(width, height,Qt.KeepAspectRatio))

        self.vision(image)


    def on_window_closed(self):
        qDebug("Closing")
        self.imageCapture.cancelCapture()
        self.stop = True
        self.delay_ms(200)
        self.camera.stop()
        self.camera.unload()

        self.close()

    def delay_ms(self, ms: int):
        delta = QTime.currentTime().addMSecs(ms)
        while(QTime.currentTime() < delta):
            QCoreApplication.processEvents(QEventLoop.AllEvents, 10)

    def vision(self, image):
        arr = self.toNumpyArray(image)

        gray = cv.cvtColor(arr, cv.COLOR_BGR2GRAY)

        img = self.toQImage(gray)

        self.showProcessedImage(img)

    def showProcessedImage(self, image):
        width = self.ui.imageviewprocessed.width()
        height = self.ui.imageviewprocessed.height()

        self.ui.imageviewprocessed.setPixmap(QPixmap.fromImage(image).scaled(width, height,Qt.KeepAspectRatio))

    def toNumpyArray(self, image):
        width = image.width()
        height = image.height()

        ptr = image.constBits()
        arr = np.array(ptr).reshape(height, width, 4)
        return arr

    def toQImage(self, arr):
        img = QImage(arr, arr.shape[1], arr.shape[0], QImage.Format_Grayscale8)
        return img