from PySide2 import QtWidgets, QtCore, QtGui
from Thi.Layout.Custom import QLine, QPaletteTable
import maya.cmds as cm
import maya.OpenMaya as om

from Thi.Content import Control

reload(Control)
reload(QLine)
reload(QPaletteTable)


# noinspection PyAttributeOutsideInit
class ControlWidget(QtWidgets.QWidget):

    def __init__(self):
        super(ControlWidget, self).__init__()

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    def create_widgets(self):
        self.first_keyframes_lb = QtWidgets.QLabel("First keyframes:")
        self.last_keyframes_lb = QtWidgets.QLabel("Last keyframes:")
        self.first_keyframes_le = QtWidgets.QLineEdit()
        self.last_keyframes_le = QtWidgets.QLineEdit()
        self.clean_btn = QtWidgets.QPushButton("Clean Keyframes")

    def create_layouts(self):
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addStretch()
        main_layout.setDirection(QtWidgets.QBoxLayout.BottomToTop)
        # main_layout.addWidget(QPaletteTable.QPaletteCustom())
        # main_layout.addLayout(QLine.QHLineName("Color Override"))
        main_layout.addWidget(CustomTool())
        main_layout.addLayout(QLine.QHLineName('Custom Tool'))
        main_layout.addWidget(ControlCreate())
        main_layout.addLayout(QLine.QHLineName('Control Create'))
        main_layout.addWidget(MatchLocation())
        main_layout.addLayout(QLine.QHLineName('Match Location'))

    def create_connections(self):
        pass


# noinspection PyAttributeOutsideInit
class MatchLocation(QtWidgets.QWidget):

    def __init__(self):
        super(MatchLocation, self).__init__()

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    def create_widgets(self):
        self.match_btn = QtWidgets.QPushButton("Match")
        self.lock_unlock_btn = QtWidgets.QPushButton("Lock - Unlock")

        self.match_all_rb = QtWidgets.QRadioButton("All")
        self.match_all_rb.setChecked(True)
        self.match_transform_rb = QtWidgets.QRadioButton("Transform")
        self.match_rotation_rb = QtWidgets.QRadioButton("Rotation")
        self.match_scale_rb = QtWidgets.QRadioButton("Scale")

    def create_layouts(self):
        main_layout = QtWidgets.QGridLayout(self)
        main_layout.addWidget(self.match_btn, 0, 3, 1, 2)
        main_layout.addWidget(self.lock_unlock_btn, 1, 3, 1, 2)

        main_layout.addWidget(self.match_all_rb, 0, 0, 1, 1)
        main_layout.addWidget(self.match_transform_rb, 0, 1, 1, 1)
        main_layout.addWidget(self.match_rotation_rb, 1, 0, 1, 1)
        main_layout.addWidget(self.match_scale_rb, 1, 1, 1, 1)

    def create_connections(self):
        self.match_btn.clicked.connect(self.Match)
        self.lock_unlock_btn.clicked.connect(self.LockUnlock)

    def Match(self):
        if self.match_all_rb.isChecked():
            Control.Match(position=True, rotation=True, scale=True)
        elif self.match_transform_rb.isChecked():
            Control.Match(position=True)
        elif self.match_rotation_rb.isChecked():
            Control.Match(rotation=True)
        elif self.match_scale_rb.isChecked():
            Control.Match(scale=True)

    def LockUnlock(self):
        if self.match_all_rb.isChecked():
            Control.LockUnlock(Transform=True, Rotation=True, Scale=True)
        elif self.match_transform_rb.isChecked():
            Control.LockUnlock(Transform=True)
        elif self.match_rotation_rb.isChecked():
            Control.LockUnlock(Rotation=True)
        elif self.match_scale_rb.isChecked():
            Control.LockUnlock(Scale=True)


# noinspection PyAttributeOutsideInit
class ControlCreate(QtWidgets.QWidget):
    control_options = {
        "Grp Loc 2Ctr": "2CLG",
        "Grp Loc 1Ctr": "1CLG",
        "Grp Loc": "LG",
        "Grp": "G",
        "Loc": "L"
    }

    def __init__(self):
        super(ControlCreate, self).__init__()

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    def create_widgets(self):

        self.control_option_combobox = QtWidgets.QComboBox()
        for control_option in sorted(self.control_options):
            self.control_option_combobox.addItem(control_option)

        self.create_btn = QtWidgets.QPushButton("Create")
        self.FK_create_btn = QtWidgets.QPushButton("FK Create")
        self.loc_on_vertex_btn = QtWidgets.QPushButton("Locator on Vertex")
        self.match_pivots_btn = QtWidgets.QPushButton("Match Pivot Transform")

    def create_layouts(self):
        main_layout = QtWidgets.QVBoxLayout(self)

        first_layout = QtWidgets.QHBoxLayout()
        first_layout.addWidget(self.control_option_combobox)
        first_layout.addWidget(self.create_btn)
        first_layout.addWidget(self.FK_create_btn)

        main_layout.addLayout(first_layout)

    def create_connections(self):

        self.create_btn.clicked.connect(self.Create)
        self.FK_create_btn.clicked.connect(Control.FKForSelected)

    def Create(self):
        current_text = self.control_option_combobox.currentText()
        current_option = self.control_options[current_text]
        if current_option == "2CLG":
            Control.ControlLocatorGroup(True)
        elif current_option == "1CLG":
            Control.ControlLocatorGroup()
        elif current_option == "LG":
            Control.LocatorGroup()
        elif current_option == "L":
            Control.Locator()
        elif current_option == "G":
            Control.Group()


# noinspection PyAttributeOutsideInit
class CustomTool(QtWidgets.QWidget):

    def __init__(self):
        super(CustomTool, self).__init__()

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    def create_widgets(self):
        self.select_le = QtWidgets.QLineEdit()
        self.clear_select_le = QtWidgets.QPushButton("Clear")

        self.parent_btn = QtWidgets.QPushButton("Parent All")
        self.match_pivot_btn = QtWidgets.QPushButton("Match Pivot Transform")
        self.loc_on_vertex_btn = QtWidgets.QPushButton("Locator on Vertex")

    def create_layouts(self):
        main_layout = QtWidgets.QVBoxLayout(self)

        first_layout = QtWidgets.QHBoxLayout()
        form_layout = QtWidgets.QFormLayout()
        form_layout.addRow('Name:', self.select_le)
        first_layout.addLayout(form_layout)
        first_layout.addWidget(self.clear_select_le)

        second_layout = QtWidgets.QHBoxLayout()
        second_layout.addWidget(self.parent_btn)
        second_layout.addWidget(self.match_pivot_btn)
        second_layout.addWidget(self.loc_on_vertex_btn)

        main_layout.addLayout(first_layout)
        main_layout.addLayout(second_layout)

    def create_connections(self):
        self.select_le.returnPressed.connect(self.current_name)
        self.clear_select_le.clicked.connect(self.select_le.clear)

        self.parent_btn.clicked.connect(Control.ParentAll)
        self.match_pivot_btn.clicked.connect(Control.MatchPivotTransform)
        self.loc_on_vertex_btn.clicked.connect(Control.LocatorOnVertex)

    def current_name(self):
        name = self.select_le.text()
        Control.SelectAll(name)
