from PySide2 import QtWidgets, QtCore, QtGui
from shiboken2 import wrapInstance
from Thi.Content import About
from Thi.Layout import MeshWidget, ControlWidget, ConnectionWidget, GeneralWidget

import os
import maya.cmds as cm
import maya.OpenMaya as om
import maya.OpenMayaUI as omui

reload(About)
reload(MeshWidget)
reload(ControlWidget)
reload(ConnectionWidget)
reload(GeneralWidget)


class HorizontalTabBar(QtWidgets.QTabBar):

    def tabSizeHint(self, index):
        s = QtWidgets.QTabBar.tabSizeHint(self, index)
        s.transpose()
        return s

    def paintEvent(self, event):
        painter = QtWidgets.QStylePainter(self)
        opt = QtWidgets.QStyleOptionTab()

        for i in range(self.count()):
            self.initStyleOption(opt, i)
            painter.drawControl(QtWidgets.QStyle.CE_TabBarTabShape, opt)
            painter.save()

            s = opt.rect.size()
            s.transpose()
            r = QtCore.QRect(QtCore.QPoint(), s)
            r.moveCenter(opt.rect.center())
            opt.rect = r

            c = self.tabRect(i).center()
            painter.translate(c)
            painter.rotate(90)
            painter.translate(-c)
            painter.drawControl(QtWidgets.QStyle.CE_TabBarTabLabel, opt)
            painter.restore()


# noinspection PyMethodMayBeStatic,PyAttributeOutsideInit,PyMethodOverriding
class MainWindow(QtWidgets.QDialog):
    WINDOW_TITLE = "Animost v1.0"

    SCRIPTS_DIR = cm.internalVar(userScriptDir=True)
    ICON_DIR = os.path.join(SCRIPTS_DIR, 'Thi/Icon')

    dlg_instance = None

    @classmethod
    def display(cls):
        if not cls.dlg_instance:
            cls.dlg_instance = MainWindow()

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
        super(MainWindow, self).__init__(self.maya_main_window())

        self.setWindowTitle(self.WINDOW_TITLE)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        self.geometry = None

        self.setMinimumSize(400, 500)
        self.setMaximumSize(400, 500)
        self.create_widget()
        self.create_layouts()
        self.create_connections()

    def create_widget(self):
        self.content_tab = QtWidgets.QTabWidget()
        # self.content_tab.setTabBar(HorizontalTabBar(self.content_tab))
        self.content_tab.setTabPosition(self.content_tab.West)

        self.about_btn = QtWidgets.QPushButton("About")
        self.close_btn = QtWidgets.QPushButton("Close")

        mesh_tab = MeshWidget.MeshWidget()
        control_tab = ControlWidget.ControlWidget()
        connection_tab = ConnectionWidget.ConnectionWidget()
        general_tab = GeneralWidget.GeneralWidget()

        self.content_tab.insertTab(0, general_tab, "General")
        self.content_tab.insertTab(1, mesh_tab, "Mesh")
        self.content_tab.insertTab(2, control_tab, "Control")
        self.content_tab.insertTab(3, connection_tab, "Connection")

    def create_layouts(self):
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.about_btn)
        button_layout.addWidget(self.close_btn)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(self.content_tab)
        main_layout.addLayout(button_layout)

    def create_connections(self):
        self.about_btn.clicked.connect(About.About)
        self.close_btn.clicked.connect(self.close)

    def showEvent(self, e):
        super(MainWindow, self).showEvent(e)

        if self.geometry:
            self.restoreGeometry(self.geometry)

    def closeEvent(self, e):
        super(MainWindow, self).closeEvent(e)

        self.geometry = self.saveGeometry()
