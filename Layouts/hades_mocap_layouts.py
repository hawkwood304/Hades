from PySide2 import QtWidgets, QtCore, QtGui
from Hades.Layouts.Custom import hades_QLine
import maya.OpenMaya as om
import pymel.core as pm
import maya.cmds as cm
from maya.mel import eval
import os

from Hades.Contents import hades_mocap

reload(hades_mocap)
reload(hades_QLine)


class MocapMainWidget(QtWidgets.QWidget):

    def __init__(self):
        super(MocapMainWidget, self).__init__()

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    def create_widgets(self):
        pass

    def create_layouts(self):
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addStretch()
        main_layout.setDirection(QtWidgets.QVBoxLayout.BottomToTop)
        main_layout.addWidget(MixTool())
        main_layout.addLayout(hades_QLine.QHLineName("Mix Tool"))
        main_layout.addWidget(AutoRetargetWidget())
        main_layout.addLayout(hades_QLine.QHLineName("Auto Retarget/Export"))

    def create_connections(self):
        pass


# noinspection PyAttributeOutsideInit
class AutoRetargetWidget(QtWidgets.QWidget):
    fbxVersions = {
        '2016': 'FBX201600',
        '2014': 'FBX201400',
        '2013': 'FBX201300',
        '2017': 'FBX201700',
        '2018': 'FBX201800',
        '2019': 'FBX201900'
    }

    def __init__(self):
        super(AutoRetargetWidget, self).__init__()

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    def create_widgets(self):
        self.filepath_le = QtWidgets.QLineEdit()
        self.select_file_path_btn = QtWidgets.QPushButton('')
        self.select_file_path_btn.setIcon(QtGui.QIcon(':fileOpen.png'))
        self.select_file_path_btn.setToolTip('Select File')

        self.name_export_root_le = QtWidgets.QLineEdit()
        self.option_lb = QtWidgets.QLabel("Option:")
        self.clean_raw_data_rb = QtWidgets.QRadioButton("Clean Raw")
        self.clean_raw_data_rb.setChecked(True)
        self.auto_retarget_export_rb = QtWidgets.QRadioButton("Retarget/Export")

        self.executed_btn = QtWidgets.QPushButton("Executed")

    def create_layouts(self):
        filepath_layout = QtWidgets.QHBoxLayout()
        form_1_layout = QtWidgets.QFormLayout()
        form_1_layout.addRow('File path:', self.filepath_le)

        filepath_layout.addLayout(form_1_layout)
        filepath_layout.addWidget(self.select_file_path_btn)

        option_layout = QtWidgets.QHBoxLayout()
        form_2_layout = QtWidgets.QFormLayout()
        form_2_layout.addRow("Export root name:", self.name_export_root_le)

        option_layout.addWidget(self.option_lb)
        option_layout.addWidget(self.clean_raw_data_rb)
        option_layout.addWidget(hades_QLine.QVLine())
        option_layout.addWidget(self.auto_retarget_export_rb)
        option_layout.addLayout(form_2_layout)

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.executed_btn)

        main_layout = QtWidgets.QVBoxLayout(self)

        main_layout.addLayout(filepath_layout)
        main_layout.addLayout(option_layout)
        main_layout.addLayout(button_layout)

    def create_connections(self):
        self.select_file_path_btn.clicked.connect(self.show_file_select_dialog)

        self.executed_btn.clicked.connect(self.executed)

    def executed(self):
        if self.clean_raw_data_rb.isChecked():
            self.clean_raw_data()

        elif self.auto_retarget_export_rb.isChecked():
            self.auto_retarget_export()

    def show_file_select_dialog(self):
        self.filepath = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select directory', '/home')

        self.filepath_le.setText(self.filepath)

    def export_option(self, path):
        # Get maya version and fbx version
        version_maya = cm.about(version=True)
        self.version_fbx = self.fbxVersions.get(version_maya)

        # Option
        eval("FBXExportSmoothingGroups -v true")
        eval("FBXExportHardEdges -v false")
        eval("FBXExportTangents -v false")
        eval("FBXExportSmoothMesh -v true")
        eval("FBXExportInstances -v false")
        eval("FBXExportReferencedAssetsContent -v false")

        eval('FBXExportBakeComplexAnimation -v true')

        eval("FBXExportBakeComplexStep -v 1")

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
        eval('FBXExportFileVersion -v {}'.format(self.version_fbx))

        # Export!
        eval('FBXExport -f "{0}" -s'.format(path))

    def check_parent(self):
        """

        Returns: List of joint who is children under world

        """
        # Get list of all joint in scene
        self.all_joints = pm.ls(type="joint")
        joint_under_world = []

        # Loop through all joint in list
        for joint in self.all_joints:

            if "_" in str(joint):
                base_name = joint.split("_")[-1]
                pm.rename(joint, base_name)

            # Check if joint is under world or not
            joint_parent = pm.listRelatives(joint, allParents=True)
            if len(joint_parent) == 0:
                joint_under_world.append(joint)
            else:
                continue

        # Return list of joint under world
        return joint_under_world

    def get_path_file_mixamo(self):
        """

        Returns: List of path to fbx file

        """
        # Get path of folder
        path = self.filepath_le.text()

        # Get all files path
        files = os.listdir(path)

        fbx_files_path = []

        maya_file_path = []

        # Loop through all files path
        for f in files:

            # Check if file is fbx or not
            if f.endswith(".fbx"):
                new_path = (os.path.join(path, f)).replace(os.sep, '/')
                fbx_files_path.append(new_path)

            elif f.endswith(".ma"):
                maya_file = (os.path.join(path, f)).replace(os.sep, '/')
                maya_file_path.append(maya_file)
            else:
                continue

        # Return list of fbx files path and maya file
        return fbx_files_path, maya_file_path

    def create_directory(self):
        """

        Returns: Create a folder to export new fbx file after fixing

        """
        if self.filepath_le.text() == "":
            om.MGlobal.displayError("Please write down link/path to folder have fbx file")

        # Get path of folder
        path = self.filepath_le.text()

        # Create a path to folder for export fbx
        if self.clean_raw_data_rb.isChecked():
            self.directory = os.path.join(path, "RawDataClean")

        elif self.auto_retarget_export_rb.isChecked():
            self.directory = os.path.join(path, "RetargetExport")

        # Check folder is exist or not
        if not os.path.exists(self.directory):
            os.mkdir(self.directory)

    @staticmethod
    def clean_namespace():
        """

        Returns: Clean all the namespace we have in scene and merge it all to root

        """
        cm.namespace(set=':')
        namespaces = cm.namespaceInfo(listOnlyNamespaces=True)
        namespaces_merged = 0
        for name in namespaces:
            if name == "UI":
                continue
            if name == "shared":
                continue
            cm.namespace(removeNamespace=name, mergeNamespaceWithRoot=True)
            namespaces_merged += 1

    def clean_raw_data(self):
        # Create and check
        self.create_directory()

        # Get all files path
        file_path, maya_file_path = self.get_path_file_mixamo()

        # Loop through all path
        for path in file_path:

            # Create new scene
            cm.file(force=True, newFile=True)

            # Rename path for maya can read
            new_path = path.replace("\\", "/")

            # Import fbx file into scene with out namespace
            cm.file(new_path, i=True, mergeNamespacesOnClash=True, namespace=':')

            cm.currentUnit(time='ntsc')

            self.clean_namespace()

            # Get list joint under world
            list_joints = self.check_parent()

            skipped_file = []

            if pm.objExists("World"):
                world_joint = pm.PyNode("World")
            else:
                # Create a world joint
                world_joint = pm.joint(n="World", r=True)

            # Loop through joint and parent it under world joint
            for joint in list_joints:
                first_key = int(pm.findKeyframe(joint, which='first'))

                last_key = int(pm.findKeyframe(joint, which='last')) + 1

                cm.playbackOptions(animationStartTime=first_key, animationEndTime=last_key, minTime=first_key,
                                   maxTime=last_key)
                pm.parent(joint, world_joint, relative=False)

            # Get fbx file name without the path
            fbx_name = path.split("/")[-1]

            # Set path to new folder export we create
            path_fbx = (os.path.join(self.directory, fbx_name)).replace(os.sep, '/')

            # Export fbx file
            pm.select(world_joint)
            self.export_option(path_fbx)

            # Create new scene again for clean maya
            cm.file(force=True, newFile=True)

    def auto_retarget_export(self):

        if self.name_export_root_le.text() == "":
            return om.MGlobal.displayError("Please write down export root name!")

        # Create and check
        self.create_directory()

        # Get all files path
        files_path, maya_files_path = self.get_path_file_mixamo()

        if len(maya_files_path) != 1:
            om.MGlobal.displayError("There is too many or none maya file in the folder")

        maya_file = maya_files_path[0]

        maya_file_path = maya_file.replace("\\", "/")
        cm.file(maya_file_path, force=True, open=True,
                ignoreVersion=True)

        # Loop through all path
        for path in files_path:
            # Rename path for maya can read
            new_path = path.replace("\\", "/")

            # Import fbx file into scene with out namespace
            cm.file(new_path, i=True, mergeNamespacesOnClash=True, namespace=':')
            cm.currentUnit(time='ntsc')

            first_key = int(cm.findKeyframe("Hips", timeSlider=True, which='first'))

            last_key = int(cm.findKeyframe("Hips", which='last')) + 1

            cm.playbackOptions(animationStartTime=0, animationEndTime=last_key, minTime=0, maxTime=last_key)

            # Get fbx file name without the path
            fbxName = path.split("/")[-1]

            # Set path to new folder export we create
            path_fbx = (os.path.join(self.directory, fbxName)).replace(os.sep, '/')

            # Export fbx file
            name_export_root = self.name_export_root_le.text()
            export_root = pm.PyNode(name_export_root)
            pm.select(export_root)
            self.export_option(path_fbx)


# noinspection PyAttributeOutsideInit
class MixTool(QtWidgets.QWidget):

    def __init__(self):
        super(MixTool, self).__init__()

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    def create_widgets(self):
        self.Tpose_btn = QtWidgets.QPushButton("Tpose Mocap/Mixamo")

    def create_layouts(self):
        main_layout = QtWidgets.QVBoxLayout(self)

        first_layout = QtWidgets.QHBoxLayout()
        first_layout.addWidget(self.Tpose_btn)

        main_layout.addLayout(first_layout)

    def create_connections(self):
        self.Tpose_btn.clicked.connect(hades_mocap.create_T_pose)
