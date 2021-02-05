from PySide2 import QtWidgets, QtCore, QtGui
from Thi.Layout.Custom import QLine
from Thi.Content import Connection
reload(QLine)
reload(Connection)


# noinspection PyAttributeOutsideInit
class ConnectionWidget(QtWidgets.QWidget):

    def __init__(self):
        super(ConnectionWidget, self).__init__()

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    def create_widgets(self):
        self.connections_sector_lb = QtWidgets.QLabel('Connection Table')

    def create_layouts(self):
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(QLine.QHLineName(name='Connection Table'))
        main_layout.addWidget(Connection.ConnectionTable())

    def create_connections(self):
        pass
