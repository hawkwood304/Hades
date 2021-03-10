from PySide2 import QtWidgets, QtCore, QtGui
from Hades.Layouts.Custom import hades_QLine
import maya.OpenMaya as om

from Hades.Contents import hades_rig

reload(hades_rig)
reload(hades_QLine)


class RigMainWidget(QtWidgets.QWidget):

    def __init__(self):
        super(RigMainWidget, self).__init__()

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    def create_widgets(self):
        pass

    def create_layouts(self):
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addStretch()
        main_layout.setDirection(QtWidgets.QVBoxLayout.BottomToTop)
        main_layout.addWidget(AttributeWidget())
        main_layout.addLayout(hades_QLine.QHLineName("Attribute"))
        main_layout.addWidget(PivotMixWidget())
        main_layout.addLayout(hades_QLine.QHLineName("Pivot & Mix"))
        main_layout.addWidget(ControlCreateWidget())
        main_layout.addLayout(hades_QLine.QHLineName("Control Create"))
        main_layout.addWidget(MatchLockWidget())
        main_layout.addLayout(hades_QLine.QHLineName("Match Lock"))

    def create_connections(self):
        pass


# noinspection PyAttributeOutsideInit
class ControlCreateWidget(QtWidgets.QWidget):
    CONTROL_OPTIONS = {
        "Double Group": "2GRP",
        "Group": "1GRP",
        "Double Control": "2CTR",
        "Control": "1CTR",
    }

    def __init__(self):
        super(ControlCreateWidget, self).__init__()

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    def create_widgets(self):
        self.control_option_combobox = QtWidgets.QComboBox()
        for control_option in sorted(self.CONTROL_OPTIONS):
            self.control_option_combobox.addItem(control_option)

        self.create_btn = QtWidgets.QPushButton("Create")
        self.simple_FK_btn = QtWidgets.QPushButton("Simple FK")

    def create_layouts(self):
        main_layout = QtWidgets.QVBoxLayout(self)

        first_layout = QtWidgets.QHBoxLayout()
        first_form_layout = QtWidgets.QFormLayout()
        first_form_layout.addRow("Option:", self.control_option_combobox)
        first_layout.addLayout(first_form_layout)
        first_layout.addWidget(self.create_btn)
        first_layout.addWidget(self.simple_FK_btn)

        main_layout.addLayout(first_layout)

    def create_connections(self):
        self.create_btn.clicked.connect(self.create_control)
        self.simple_FK_btn.clicked.connect(hades_rig.simple_FK_selected)

    def create_control(self):
        current_text = self.control_option_combobox.currentText()
        current_option = self.CONTROL_OPTIONS[current_text]
        if current_option == "2GRP":
            hades_rig.create_double_group()
        elif current_option == "1GRP":
            hades_rig.create_group_orient()
        elif current_option == "2CTR":
            hades_rig.create_double_control()
        elif current_option == "1CTR":
            hades_rig.create_control()


# noinspection PyAttributeOutsideInit
class PivotMixWidget(QtWidgets.QWidget):

    def __init__(self):
        super(PivotMixWidget, self).__init__()

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    def create_widgets(self):
        self.re_zero_pivot_btn = QtWidgets.QPushButton("Re Zero Pivot")
        self.parent_btn = QtWidgets.QPushButton("Parent")
        self.match_pivot_btn = QtWidgets.QPushButton("Match Pivot")

    def create_layouts(self):
        main_layout = QtWidgets.QVBoxLayout(self)

        first_layout = QtWidgets.QHBoxLayout()
        first_layout.addWidget(self.re_zero_pivot_btn)
        first_layout.addWidget(self.match_pivot_btn)
        first_layout.addWidget(self.parent_btn)

        main_layout.addLayout(first_layout)

    def create_connections(self):
        self.re_zero_pivot_btn.clicked.connect(hades_rig.relocation_pivot)
        self.match_pivot_btn.clicked.connect(hades_rig.match_pivot_transform)
        self.parent_btn.clicked.connect(hades_rig.parent_selected)


# noinspection PyAttributeOutsideInit
class MatchLockWidget(QtWidgets.QWidget):

    def __init__(self):
        super(MatchLockWidget, self).__init__()

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    def create_widgets(self):
        self.match_btn = QtWidgets.QPushButton("Match")
        self.lock_unlock_btn = QtWidgets.QPushButton("Lock - Unlock")
        self.freezy_btn = QtWidgets.QPushButton("Freezy")

        self.transform_cb = QtWidgets.QCheckBox("Transform")
        self.transform_cb.setChecked(True)
        self.rotation_cb = QtWidgets.QCheckBox("Rotation")
        self.scale_cb = QtWidgets.QCheckBox("Scale")

    def create_layouts(self):
        main_layout = QtWidgets.QVBoxLayout(self)

        btn_layout = QtWidgets.QHBoxLayout()
        btn_layout.addWidget(self.match_btn)
        btn_layout.addWidget(self.lock_unlock_btn)
        btn_layout.addWidget(self.freezy_btn)

        cb_layout = QtWidgets.QHBoxLayout()
        cb_layout.addWidget(self.transform_cb)
        cb_layout.addWidget(self.rotation_cb)
        cb_layout.addWidget(self.scale_cb)

        main_layout.addLayout(btn_layout)
        main_layout.addLayout(cb_layout)

    def create_connections(self):
        self.match_btn.clicked.connect(self.match_location)
        self.lock_unlock_btn.clicked.connect(self.lock_unlock)

    def match_location(self):

        if self.transform_cb.isChecked():
            hades_rig.match_location(position=True)

        if self.rotation_cb.isChecked():
            hades_rig.match_location(rotation=True)

        if self.scale_cb.isChecked():
            hades_rig.match_location(scale=True)

    def lock_unlock(self):

        if self.transform_cb.isChecked():
            hades_rig.lock_unlock(transform=True)

        if self.rotation_cb.isChecked():
            hades_rig.lock_unlock(rotation=True)

        if self.scale_cb.isChecked():
            hades_rig.lock_unlock(scale=True)

    def freezy_transformations(self):
        if self.transform_cb.isChecked():
            hades_rig.freezy_transformations(translate=True)

        if self.rotation_cb.isChecked():
            hades_rig.freezy_transformations(rotate=True)

        if self.scale_cb.isChecked():
            hades_rig.freezy_transformations(scale=True)


# noinspection PyAttributeOutsideInit
class AttributeWidget(QtWidgets.QWidget):

    def __init__(self):
        super(AttributeWidget, self).__init__()

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    def create_widgets(self):
        self.up_btn = QtWidgets.QPushButton("Up")
        self.down_btn = QtWidgets.QPushButton("Down")
        self.create_attribute_visibility_btn = QtWidgets.QPushButton("Visi Attr")

    def create_layouts(self):
        main_layouts = QtWidgets.QVBoxLayout(self)

        first_layout = QtWidgets.QHBoxLayout()

        up_down_layout = QtWidgets.QVBoxLayout()
        up_down_layout.addWidget(self.up_btn)
        up_down_layout.addWidget(self.down_btn)

        first_layout.addLayout(up_down_layout)
        first_layout.addWidget(hades_QLine.QVLine())
        first_layout.addWidget(self.create_attribute_visibility_btn)

        main_layouts.addLayout(first_layout)

    def create_connections(self):
        self.up_btn.clicked.connect(self.up_signal)
        self.down_btn.clicked.connect(self.down_signal)
        self.create_attribute_visibility_btn.clicked.connect(hades_rig.create_attribute_visibility)

    @staticmethod
    def up_signal():
        hades_rig.up_down_attribute(up=True)

    @staticmethod
    def down_signal():
        hades_rig.up_down_attribute(down=True)
