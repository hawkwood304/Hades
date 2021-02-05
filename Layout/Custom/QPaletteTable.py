from PySide2 import QtWidgets, QtCore, QtGui
from PySide2.QtCore import Signal
import collections

COLOR_LIST = [
    'black',
    'gray',
    'white',
    'brow',
    'maroon',
    'red',
    'coral',
    'siena',
    'peachpuff',
    'darkorange'
]


class MyPalettePushButton(QtWidgets.QPushButton):
    color = QtCore.Signal(str)

    def click(self, e, color):
        super(MyPalettePushButton, self).click(e)
        self.color.emit(color)

    def __init__(self, color):
        super(MyPalettePushButton, self).__init__()

        self.setFixedSize(QtCore.QSize(24, 24))
        self.c = color
        self.setStyleSheet("background-color: {0};".format(color))


# noinspection PyAttributeOutsideInit
class QPaletteCustom(QtWidgets.QWidget):

    def __init__(self):
        super(QPaletteCustom, self).__init__()

        self.create_widget()
        self.create_layouts()
        self.create_connections()

    def create_widget(self):
        self.color_layout = QtWidgets.QHBoxLayout()

        for color in COLOR_LIST:
            self.color_btn = MyPalettePushButton(color)
            self.color_btn.color.connect(self.color_background)
            self.color_layout.addWidget(self.color_btn)

    def create_layouts(self):
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(self.color_layout)

    def create_connections(self):
        pass

    def color_background(self, c):
        print c
