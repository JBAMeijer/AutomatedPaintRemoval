from PySide2 import QtWidgets
from PySide2.QtWidgets import QVBoxLayout
from PySide2.QtCore import Qt, QPoint, QRect, QSize
from PySide2.QtGui import QPixmap, QPainter, QColor, QPen, QImage, QColor
from .ScribbleArea.ScribbleArea import ScribbleArea
from .PaintDialogUI import Ui_Dialog

class PaintDialog(QtWidgets.QDialog):
    def __init__(self, parent = None):
        super(PaintDialog, self).__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.scribbleArea = ScribbleArea(self)
        
        self.ui.verticalLayout.addWidget(self.scribbleArea)
        self.setLayout(self.ui.verticalLayout)
