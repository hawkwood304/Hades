from PySide2 import QtWidgets
import maya.OpenMaya as om
import maya.cmds as cm
import collections


# noinspection PyAttributeOutsideInit
class ConnectionTable(QtWidgets.QWidget):

    def __init__(self):
        super(ConnectionTable, self).__init__()

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    def create_widgets(self):
        self.input_connections_rb = QtWidgets.QRadioButton('Input Connections')
        self.input_connections_rb.setChecked(True)

        self.output_connections_rb = QtWidgets.QRadioButton('Output Connections')

        self.show_btn = QtWidgets.QPushButton('Show')

        self.connection_lwg = QtWidgets.QListWidget()
        self.connection_lwg.setSelectionMode(QtWidgets.QAbstractItemView.ContiguousSelection)

        self.clear_btn = QtWidgets.QPushButton('Clear')

    def create_layouts(self):
        button_up_layout = QtWidgets.QHBoxLayout()
        button_up_layout.addWidget(self.input_connections_rb)
        button_up_layout.addWidget(self.output_connections_rb)

        button_down_layout = QtWidgets.QHBoxLayout()
        button_down_layout.addWidget(self.show_btn)
        button_down_layout.addWidget(self.clear_btn)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(button_up_layout)
        main_layout.addWidget(self.connection_lwg)
        main_layout.addLayout(button_down_layout)

    def create_connections(self):
        self.connection_lwg.itemSelectionChanged.connect(self.current_selected)

        self.show_btn.clicked.connect(self.show_connections)

        self.clear_btn.clicked.connect(self.clear_connections)

    # noinspection PyUnboundLocalVariable
    def show_connections(self):
        self.connection_lwg.clear()
        self.selection = cm.ls(sl=True)
        if len(self.selection) != 1:
            return om.MGlobal.displayError('Please chose only one object')
        if self.input_connections_rb.isChecked():
            list_connections_raw = cm.listConnections(self.selection[0], source=True, destination=False) or []
            list_connections = list(set(list_connections_raw))
        elif self.output_connections_rb.isChecked():
            list_connections_raw = cm.listConnections(self.selection[0], destination=True, source=False) or []
            list_connections = list(set(list_connections_raw))
        for name in list_connections:
            item = QtWidgets.QListWidgetItem(name)
            self.connection_lwg.addItem(item)

        cm.select(cl=True)

    def clear_connections(self):
        self.connection_lwg.clear()

    def current_selected(self):
        items = self.connection_lwg.selectedItems()

        selected_item = []

        for item in items:
            selected_item.append(item.text())

        cm.select(cl=True)
        cm.select(selected_item)
