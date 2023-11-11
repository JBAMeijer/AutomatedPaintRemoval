from PySide2 import QtWidgets
from PySide2.QtCore import Qt, QPoint, QRect, QSize
from PySide2.QtGui import QPixmap, QPainter, QColor, QPen, QImage, QColor

class ScribbleArea(QtWidgets.QWidget):
    def __init__(self, parent = None):
        super(ScribbleArea, self).__init__(parent)
        self.modified = False
        self.scribbling = False
        self.myPenWidth = 30
        self.myPenColor = Qt.green
        self.image = QImage()
        self.lastPoint = QPoint()

        self.setAttribute(Qt.WA_StaticContents)
        
    def setPenColor(self, newColor):
        self.myPenColor = newColor
    
    def setPenWidth(self, newWidth):
        self.myPenWidth = newWidth

    def clearImage(self):
        self.image.fill(Qt.white)
        self.modified = True
        self.update()

    def mousePressEvent(self, ev):
        if ev.button() == Qt.LeftButton:
            self.lastPoint = ev.pos()
            self.scribbling = True
    
    def mouseMoveEvent(self, ev):
        if (ev.buttons() & Qt.LeftButton) and self.scribbling:
            self.drawLineTo(ev.pos())

    def mouseReleaseEvent(self, ev):
        if ev.button() == Qt.LeftButton and self.scribbling:
            self.drawLineTo(ev.pos())
            self.scribbling = False

    def paintEvent(self, ev):
        painter = QPainter(self)
        dirtyRect = ev.rect()
        painter.drawImage(dirtyRect, self.image, dirtyRect)
    
    def resizeEvent(self, ev):
        if self.width() > self.image.width() or self.height() > self.image.height():
            newWidth = max(self.width() + 128, self.image.width())
            newHeight = max(self.height() + 128, self.image.height())
            self.resizeImage(QSize(newWidth, newHeight))
            self.update()
        #QtWidgets.QWidget.resizeEvent(ev)

    def drawLineTo(self, endPoint):
        painter = QPainter(self.image)
        painter.setPen(QPen(self.myPenColor, self.myPenWidth, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        painter.drawLine(self.lastPoint, endPoint)
        self.modified = True

        rad = (self.myPenWidth / 2) + 2
        self.update(QRect(self.lastPoint, endPoint).normalized().adjusted(-rad, -rad, +rad, +rad))
        self.lastPoint = endPoint
    
    def resizeImage(self, newSize):
        if self.image.size() == newSize:
            return
        
        newImage = QImage(newSize, QImage.Format_RGB32)
        newImage.fill(Qt.white)
        painter = QPainter(newImage)
        painter.drawImage(QPoint(0, 0), self.image)
        self.image = newImage


def max(first, second):
    if first > second:
        return first
    else:
        return second