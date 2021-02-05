from PySide2 import QtCore, QtWidgets, QtGui
from shiboken2 import wrapInstance

import maya.cmds as cm
import maya.OpenMayaUI as omui


# noinspection PyUnresolvedReferences
def maya_main_window():
    """
    Return the Maya main window widget as a Python object
    """
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)


# noinspection PyAttributeOutsideInit
class About(QtWidgets.QDialog):

    def __init__(self, parent=maya_main_window()):
        super(About, self).__init__(parent)
        try:
            cm.deleteUI('About')
        except:
            pass

        self.setWindowTitle('About')
        self.setObjectName('About')
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        self.setMinimumSize(100, 100)

        self.create_widget()
        self.create_layouts()
        self.create_connections()
        self.show()

    def create_widget(self):
        self.about_lbl = QtWidgets.QLabel("Animost Tool is some thing i want to do in a long time\n"
                                          "This is all my tool I write or buy use for work\n"
                                          "Hope this will help you\n"
                                          "Thi")
        self.about_lbl.setAlignment(QtCore.Qt.AlignCenter)

        self.close_btn = QtWidgets.QPushButton('Close')

    def create_layouts(self):
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(self.about_lbl)
        main_layout.addWidget(self.close_btn)

    def create_connections(self):
        self.close_btn.clicked.connect(self.close)
