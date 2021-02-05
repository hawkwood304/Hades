import math
import os

from PySide2 import QtWidgets, QtCore, QtGui
from maya.mel import eval
import maya.cmds as cm
import maya.OpenMaya as om
import sys


# noinspection PyAttributeOutsideInit,PyMethodMayBeStatic
class MeshCheckList(QtWidgets.QWidget):

    def __init__(self):
        super(MeshCheckList, self).__init__()

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    def create_widgets(self):
        self.mesh_check_twd = QtWidgets.QListWidget()
        self.mesh_check_twd.setMaximumHeight(100)

        self.check_btn = QtWidgets.QPushButton("Check")
        self.clear_btn = QtWidgets.QPushButton("Clear")

    def create_layouts(self):
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.check_btn)
        button_layout.addWidget(self.clear_btn)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addStretch()
        main_layout.setDirection(QtWidgets.QBoxLayout.BottomToTop)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.mesh_check_twd)

    def create_connections(self):
        self.check_btn.clicked.connect(self.check)
        self.clear_btn.clicked.connect(self.mesh_check_twd.clear)

        self.mesh_check_twd.itemClicked.connect(self.output_mesh_check)

    def check(self):
        self.mesh_check_twd.clear()
        selection = cm.ls(sl=True)
        if len(selection) != 1:
            return om.MGlobal.displayError("Please select only one object per time")

        eval('polyCleanupArgList 4 {"0","2","1","0","1","0","0","0","0","1e-05","0","1e-05","0","1e-05","0","-1","0",'
             '"0"}')
        face_with_more_than_4_sides = cm.ls(sl=True, flatten=True)

        cm.select(selection[0])
        eval('polyCleanupArgList 4 { "0","2","1","0","0","1","0","0","0","1e-05","0","1e-05","0","1e-05","0","-1",'
             '"0","0" };')
        concave_faces = cm.ls(sl=True, flatten=True)

        cm.select(selection[0])
        eval('polyCleanupArgList 4 { "0","2","1","0","0","0","1","0","0","1e-05","0","1e-05","0","1e-05","0","-1",'
             '"0","0" };')
        faces_with_holes = cm.ls(sl=True, flatten=True)

        cm.select(selection[0])
        eval('polyCleanupArgList 4 { "0","2","1","0","0","0","0","1","0","1e-05","0","1e-05","0","1e-05","0","-1",'
             '"0","0" } ')
        non_planar_faces = cm.ls(sl=True, flatten=True)

        face_with_more_than_4_sides_item = '{} - Face with more than 4 sides'.format(len(face_with_more_than_4_sides))

        concave_faces_item = '{} - Concave Faces'.format(len(concave_faces))

        faces_with_holes_item = '{} - Face with holes'.format(len(faces_with_holes))

        non_planar_faces_item = '{} - Non planar faces'.format(len(non_planar_faces))

        MESH_CHECK_ITEM = [
            [face_with_more_than_4_sides_item, face_with_more_than_4_sides],
            [concave_faces_item, concave_faces],
            [faces_with_holes_item, faces_with_holes],
            [non_planar_faces_item, non_planar_faces]
        ]

        for mesh_check_item in MESH_CHECK_ITEM:
            list_wdg_item = QtWidgets.QListWidgetItem(mesh_check_item[0])
            list_wdg_item.setData(QtCore.Qt.UserRole, mesh_check_item[1])
            self.mesh_check_twd.addItem(list_wdg_item)

        cm.select(selection[0])
        cm.selectMode(object=True)

        sys.stdout.write("Checking completed\n")

    def output_mesh_check(self, item):
        list_object = item.data(QtCore.Qt.UserRole)

        cm.select(list_object)


def cam_SKT():
    if cm.getAttr("perspShape.nearClipPlane") == 100:
        cm.setAttr("perspShape.nearClipPlane", 0.100)
        cm.setAttr("perspShape.farClipPlane", 10000)
    else:
        cm.setAttr("perspShape.nearClipPlane", 100)
        cm.setAttr("perspShape.farClipPlane", 100000)

    if cm.getAttr("topShape.nearClipPlane") == 100:
        cm.setAttr("topShape.nearClipPlane", 0.100)
        cm.setAttr("topShape.farClipPlane", 10000)
    else:
        cm.setAttr("topShape.nearClipPlane", 100)
        cm.setAttr("topShape.farClipPlane", 100000)

    if cm.getAttr("frontShape.nearClipPlane") == 100:
        cm.setAttr("frontShape.nearClipPlane", 0.100)
        cm.setAttr("frontShape.farClipPlane", 10000)
    else:
        cm.setAttr("sideShape.nearClipPlane", 100)
        cm.setAttr("sideShape.farClipPlane", 100000)

    sys.stdout.write("Change cam done")


# noinspection PyAttributeOutsideInit
class ExportTool(QtWidgets.QWidget):
    fbxVersions = {
        '2016': 'FBX201600',
        '2014': 'FBX201400',
        '2013': 'FBX201300',
        '2017': 'FBX201700',
        '2018': 'FBX201800',
        '2019': 'FBX201900'
    }

    def __init__(self):
        super(ExportTool, self).__init__()

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    def create_widgets(self):
        self.filepath_lb = QtWidgets.QLabel("File path: ")

        self.filepath_le = QtWidgets.QLineEdit()
        self.select_file_path_btn = QtWidgets.QPushButton('')
        self.select_file_path_btn.setIcon(QtGui.QIcon(':fileOpen.png'))
        self.select_file_path_btn.setToolTip('Select File')

        self.bake_cb = QtWidgets.QCheckBox("Bake Animation")
        self.bake_cb.setChecked(True)
        self.fbxVersion_combobox = QtWidgets.QComboBox()
        for fbxVersion in sorted(self.fbxVersions):
            self.fbxVersion_combobox.addItem(fbxVersion)

        self.export_btn = QtWidgets.QPushButton("Export")

    def create_layouts(self):
        filepath_layout = QtWidgets.QHBoxLayout()
        filepath_layout.addWidget(self.filepath_lb)
        filepath_layout.addWidget(self.filepath_le)
        filepath_layout.addWidget(self.select_file_path_btn)

        option_layout = QtWidgets.QHBoxLayout()
        option_layout.addWidget(self.bake_cb)
        option_layout.addWidget(self.fbxVersion_combobox)
        option_layout.addWidget(self.export_btn)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(filepath_layout)
        main_layout.addLayout(option_layout)

    def create_connections(self):
        self.select_file_path_btn.clicked.connect(self.show_file_select_dialog)
        self.export_btn.clicked.connect(self.export)

    def show_file_select_dialog(self):
        self.file_path = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select directory')

        self.filepath_le.setText(self.file_path)

    def export_option(self, path):
        fbxVersion = self.fbxVersion_combobox.currentText()
        Version = self.fbxVersions[fbxVersion]

        eval("FBXExportSmoothingGroups -v true")
        eval("FBXExportHardEdges -v false")
        eval("FBXExportTangents -v false")
        eval("FBXExportSmoothMesh -v true")
        eval("FBXExportInstances -v false")
        eval("FBXExportReferencedAssetsContent -v false")

        if self.bake_cb.isChecked():
            eval('FBXExportBakeComplexAnimation -v true')
            eval("FBXExportBakeComplexStep -v 1")
        else:
            eval('FBXExportBakeComplexAnimation -v false')

        eval("FBXExportUseSceneName -v false")
        eval("FBXExportQuaternion -v euler")
        eval("FBXExportShapes -v true")
        eval("FBXExportSkins -v true")

        # Constraints
        eval("FBXExportConstraints -v false")
        # Cameras
        eval("FBXExportCameras -v true")
        # Lights
        eval("FBXExportLights -v true")
        # Embed Media
        eval("FBXExportEmbeddedTextures -v false")
        # Connections
        eval("FBXExportInputConnections -v true")
        # Axis Conversion
        eval("FBXExportUpAxis y")
        # Version
        eval('FBXExportFileVersion -v {}'.format(Version))

        # Export!

        eval('FBXExport -f "{0}" -s'.format(path))

    def export(self):
        filepath_raw = self.filepath_le.text()

        filepath = filepath_raw.replace('\\', '/')

        if not os.path.isdir(filepath):
            return om.MGlobal.displayError("File path khong ton tai")

        scene_name = cm.file(q=True, sn=True, shn=True).split('.')[0] or []

        if len(scene_name) == 0:
            return om.MGlobal.displayError("Chua dat ten cho scene anh oi")

        new_filepath = (os.path.join(filepath, scene_name)).replace(os.sep, '/')

        if not os.path.isdir(new_filepath):
            os.mkdir(new_filepath)

        list_export = cm.ls(sl=True)
        if len(list_export) == 0:
            cm.warning('Need at least something to export!!!')
        else:
            list_export.sort(key=len, reverse=True)
            list_rename = []

            for obj in list_export:

                children = cm.listRelatives(obj, children=True, fullPath=True) or []

                if len(children) == 1:
                    child = children[0]
                    objType = cm.objectType(child)

                else:
                    objType = cm.objectType(obj)

                if objType == 'camera':
                    cm.select(obj)
                    cam_name = '{0}_cam.fbx'.format(scene_name)
                    cam_part = (os.path.join(new_filepath, cam_name)).replace(os.sep, '/')
                    self.export_option(path=cam_part)
                else:
                    result = cm.promptDialog(
                        title='FBX Name',
                        message='FBX Name for [{}]'.format(obj),
                        button=['OK', 'Cancel'],
                        defaultButton='OK',
                        cancelButton='Cancel',
                        dismissString='Cancel')

                    if result == 'OK':
                        rename = cm.promptDialog(query=True, text=True)
                        list_rename.append(rename)
                        fbxName = '{0}_{1}.fbx'.format(scene_name, rename)
                        path = (os.path.join(new_filepath, fbxName)).replace(os.sep, '/')

                        cm.select(obj)
                        self.export_option(path=path)
