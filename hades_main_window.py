from PySide2 import QtWidgets, QtCore, QtGui
from shiboken2 import wrapInstance
import maya.OpenMaya as om
import maya.OpenMayaUI as omui
import os
from Hades.Layouts import hades_rig_layouts, hades_mocap_layouts

reload(hades_rig_layouts)
reload(hades_mocap_layouts)


# noinspection PyAttributeOutsideInit
class HadesMainWindow(QtWidgets.QDialog):
    WINDOW_TITLE = "Hades v0.1"

    dlg_instance = None

    @classmethod
    def display(cls):
        if not cls.dlg_instance:
            cls.dlg_instance = HadesMainWindow()

        if cls.dlg_instance.isHidden():
            cls.dlg_instance.show()

        else:
            cls.dlg_instance.raise_()
            cls.dlg_instance.activateWindow()

    @classmethod
    def maya_main_window(cls):
        """

        Returns: The Maya main window widget as a Python object

        """
        main_window_ptr = omui.MQtUtil.mainWindow()
        return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)

    def __init__(self):
        super(HadesMainWindow, self).__init__(self.maya_main_window())

        self.setWindowTitle(self.WINDOW_TITLE)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        self.geometry = None

        self.setMinimumSize(500, 600)

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    def create_widgets(self):
        self.contents_tab = QtWidgets.QTabWidget()
        # self.contents_tab.setTabPosition(self.contents_tab.West)

        self.about_btn = QtWidgets.QPushButton("About")
        self.close_btn = QtWidgets.QPushButton("Close")

        rig_tab = hades_rig_layouts.RigMainWidget()
        mocap_tab = hades_mocap_layouts.MocapMainWidget()

        self.contents_tab.insertTab(0, rig_tab, "Rig Toolkit")
        self.contents_tab.insertTab(1, mocap_tab, "Mocap Toolkit")

    def create_layouts(self):
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.about_btn)
        button_layout.addWidget(self.close_btn)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(self.contents_tab)
        main_layout.addLayout(button_layout)

    def create_connections(self):
        self.close_btn.clicked.connect(self.close)

    def showEvent(self, e):
        super(HadesMainWindow, self).showEvent(e)

        if self.geometry:
            self.restoreGeometry(self.geometry)

    def closeEvent(self, e):
        super(HadesMainWindow, self).closeEvent(e)

        self.geometry = self.saveGeometry()
