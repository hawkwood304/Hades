import sys
import maya.OpenMaya as om
from PySide2 import QtWidgets, QtCore
import maya.cmds as cm
from Thi.Layout.Custom import QLine
from Thi.Content import General, Control
import math

reload(General)


# noinspection PyAttributeOutsideInit
class GeneralWidget(QtWidgets.QWidget):

    def __init__(self):
        super(GeneralWidget, self).__init__()

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

        self.set_cam_btn = QtWidgets.QPushButton("Cam SKT")
        self.check_symmetry_btn = QtWidgets.QPushButton("Check Symmetry")

    def create_layouts(self):
        last_layout = QtWidgets.QGridLayout()
        last_layout.addWidget(self.match_btn, 0, 3, 1, 2)
        last_layout.addWidget(self.lock_unlock_btn, 1, 3, 1, 2)

        last_layout.addWidget(self.match_all_rb, 0, 0, 1, 1)
        last_layout.addWidget(self.match_transform_rb, 0, 1, 1, 1)
        last_layout.addWidget(self.match_rotation_rb, 1, 0, 1, 1)
        last_layout.addWidget(self.match_scale_rb, 1, 1, 1, 1)

        button_1_layout = QtWidgets.QHBoxLayout()
        button_1_layout.addWidget(self.set_cam_btn)
        button_1_layout.addWidget(self.check_symmetry_btn)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addStretch()
        main_layout.setDirection(QtWidgets.QBoxLayout.BottomToTop)
        main_layout.addLayout(last_layout)
        main_layout.addLayout(QLine.QHLineName("Match Location"))
        main_layout.addWidget(General.ExportTool())
        main_layout.addLayout(QLine.QHLineName("Export Tool"))
        main_layout.addLayout(button_1_layout)
        main_layout.addLayout(QLine.QHLineName("Custom Tool"))
        main_layout.addWidget(General.MeshCheckList())
        main_layout.addLayout(QLine.QHLineName("Clean Mesh Check"))

    def create_connections(self):
        self.set_cam_btn.clicked.connect(General.cam_SKT)

        self.match_btn.clicked.connect(self.Match)
        self.lock_unlock_btn.clicked.connect(self.LockUnlock)

        self.check_symmetry_btn.clicked.connect(self.symmetry_check)

    def symmetry_check(self):
        selection = cm.ls(sl=True)
        if len(selection) != 1:
            return om.MGlobal.displayError("Please chose one object per turn")

        if cm.objExists('closestSampler'):
            cm.delete('closestSampler')

        cm.createNode('closestPointOnMesh', n='closestSampler')
        cm.connectAttr('{}.outMesh'.format(selection[0]), 'closestSampler.inMesh', f=True)

        templateInt = cm.polyEvaluate(selection[0], v=True)

        numberVtx = templateInt
        cm.select(cl=True)

        process_dialog = QtWidgets.QProgressDialog("Waiting to process...", "Cancel", 0, numberVtx, self)
        process_dialog.setWindowTitle("Symmetry Check")
        process_dialog.setValue(0)
        process_dialog.setWindowModality(QtCore.Qt.WindowModal)
        process_dialog.show()
        QtCore.QCoreApplication.processEvents()

        for i in range(0, numberVtx + 1):
            process_dialog.setLabelText("Processing operation: {0} of {1}".format(i, numberVtx))
            process_dialog.setValue(i)
            QtCore.QCoreApplication.processEvents()
            posA = cm.xform('{0}.vtx[{1}]'.format(selection[0], i), q=True, ws=True, t=True)
            if posA[0] > 0.001:
                continue

            cm.setAttr('closestSampler.inPosition', posA[0] * -1, posA[1], posA[2])
            mirrorVtx = cm.getAttr('closestSampler.closestVertexIndex')
            posB = cm.xform('{0}.vtx[{1}]'.format(selection[0], mirrorVtx), q=True, ws=True, t=True)
            dx = posA[0] - (posB[0] * -1)
            dy = posA[1] - posB[1]
            dz = posA[2] - posB[2]
            mag = math.sqrt(dx * dx + dy * dy + dz * dz)
            if mag > 0.001:
                cm.select("{}.vtx[{}]".format(selection[0], i), "{}.vtx[{}]".format(selection[0], mirrorVtx),
                          add=True)

        cm.delete('closestSampler')
        process_dialog.close()
        sys.stdout.write("Checking done")

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
        if self.match_transform_rb.isChecked():
            Control.LockUnlock(Transform=True)
        if self.match_rotation_rb.isChecked():
            Control.LockUnlock(Rotation=True)
        if self.match_scale_rb.isChecked():
            Control.LockUnlock(Scale=True)
