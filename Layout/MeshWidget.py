import math

from PySide2 import QtWidgets , QtCore

from Thi.Content import Mesh
from Thi.Layout.Custom import QLine

import maya.cmds as cm
import maya.OpenMaya as om

reload(Mesh)
reload(QLine)


# noinspection PyAttributeOutsideInit
class MeshWidget(QtWidgets.QWidget):

    def __init__(self):
        super(MeshWidget , self).__init__()

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    def create_widgets(self):
        self.clean_all_namespace_btn = QtWidgets.QPushButton("Clean All Namespace")

        self.copy_UV_btn = QtWidgets.QPushButton("Copy UV")

        self.skinned_mesh_lb = QtWidgets.QLabel("Assign name to new mesh:")
        self.skinned_mesh_le = QtWidgets.QLineEdit()
        self.skinned_mesh_le.setMaximumWidth(170)

        self.combine_skinned_mesh_btn = QtWidgets.QPushButton("Combine Skinned Mesh")
        self.separate_skinned_mesh_btn = QtWidgets.QPushButton("Separate Skinned Mesh")

        self.transform_skinned_mesh_btn = QtWidgets.QPushButton("Transform Skinned Mesh")
        self.blendshape_generate_btn = QtWidgets.QPushButton("BlendShape Generate")

    def create_layouts(self):
        first_layout = QtWidgets.QGridLayout()
        first_layout.addWidget(self.clean_all_namespace_btn , 0 , 0 , 1 , 1)
        first_layout.addWidget(self.copy_UV_btn , 0 , 1 , 1 , 1)

        second_layout = QtWidgets.QGridLayout()
        second_layout.addWidget(self.skinned_mesh_lb , 0 , 0 , 1 , 1 , QtCore.Qt.AlignCenter)
        second_layout.addWidget(self.skinned_mesh_le , 0 , 1 , 1 , 1)

        second_layout.addWidget(self.combine_skinned_mesh_btn , 1 , 0 , 1 , 1)
        second_layout.addWidget(self.separate_skinned_mesh_btn , 1 , 1 , 1 , 1)

        third_layout = QtWidgets.QGridLayout()
        third_layout.addWidget(self.transform_skinned_mesh_btn , 0 , 0 , 1 , 1)
        third_layout.addWidget(self.blendshape_generate_btn , 0 , 1 , 1 , 1)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addStretch()
        main_layout.setDirection(QtWidgets.QBoxLayout.BottomToTop)
        main_layout.addLayout(third_layout)
        main_layout.addLayout(QLine.QHLineName("Custom Tool"))
        main_layout.addLayout(second_layout)
        main_layout.addLayout(QLine.QHLineName("Skinned Mesh Tool"))
        main_layout.addLayout(first_layout)
        main_layout.addLayout(QLine.QHLineName("Mix Tool"))

    def create_connections(self):
        self.clean_all_namespace_btn.clicked.connect(Mesh.CleanAllNamespace)

        self.copy_UV_btn.clicked.connect(Mesh.CopyUV)

        self.separate_skinned_mesh_btn.clicked.connect(self.SeparateSkinnedMeshProc)
        self.combine_skinned_mesh_btn.clicked.connect(self.CombineSkinnedMeshProc)

        self.transform_skinned_mesh_btn.clicked.connect(Mesh.TransformSkinnedMeshProc)
        self.blendshape_generate_btn.clicked.connect(self.BlendShapeNodeToMesh)

    def SeparateSkinnedMeshProc(self):
        Name = self.skinned_mesh_le.text()
        Mesh.SeparateSkinnedMeshProc(Name)

    def CombineSkinnedMeshProc(self):
        Name = self.skinned_mesh_le.text()
        Mesh.CombineSkinnedMeshProc(Name)

    def BlendShapeNodeToMesh(self):
        selection = cm.ls(sl=True)

        # Check is list selection is empty or not
        if len(selection) == 0:
            return om.MGlobal.displayError("Please select object to work with")

        # Check mesh to get distance
        lattice_check = cm.lattice(selection , dv=(2 , 2 , 2 ,) , oc=True , n="CheckDistance")

        pos_1 = cm.xform("{}.pt[1][1][1]".format(lattice_check[1]) , q=True , ws=True , t=True)
        pos_2 = cm.xform("{}.pt[0][1][1]".format(lattice_check[1]) , q=True , ws=True , t=True)
        pos_3 = cm.xform("{}.pt[1][0][1]".format(lattice_check[1]) , q=True , ws=True , t=True)

        distance_X = math.sqrt(
            pow(pos_1[0] - pos_2[0] , 2) + pow(pos_1[1] - pos_2[1] , 2) + pow(pos_1[2] - pos_2[2] , 2))
        distance_Y = math.sqrt(
            pow(pos_1[0] - pos_3[0] , 2) + pow(pos_1[1] - pos_3[1] , 2) + pow(pos_1[2] - pos_3[2] , 2))

        cm.delete(lattice_check)

        list_BS_name = []

        for mesh_1 in selection:

            history_main = cm.listHistory(mesh_1)

            blendShape_node = cm.ls(history_main , type='blendShape')

            # Check object have blendshape or not
            if len(blendShape_node) == 0:
                pass

            else:

                # Get list name of blendshape we have in first object
                for BS_node_name in blendShape_node:
                    blendShape_node_name = cm.listAttr('{}.w'.format(BS_node_name) , m=True)

                    list_BS_name.extend(blendShape_node_name)

        for mesh_2 in selection:
            blendShape_pd = QtWidgets.QProgressDialog("Generating..." , "Cancel" , 0 ,
                                                      len(list_BS_name) - 1 , self)
            blendShape_pd.setWindowTitle("Generate BlendShape")
            blendShape_pd.setValue(0)
            blendShape_pd.setWindowModality(QtCore.Qt.WindowModal)
            blendShape_pd.show()
            QtCore.QCoreApplication.processEvents()

            for i in range(0 , len(list_BS_name)):

                if blendShape_pd.wasCanceled():
                    break

                blendShape_pd.setLabelText("Generate BS {0}: {1} of {2}".format(mesh_2 , i , len(list_BS_name)))
                blendShape_pd.setValue(i)
                QtCore.QCoreApplication.processEvents()

                history_main = cm.listHistory(mesh_2)

                blendShape_node = cm.ls(history_main , type='blendShape')

                # Check object have blendshape or not
                if len(blendShape_node) == 0:

                    cm.select(mesh_2)
                    BS_mesh_1 = cm.duplicate(n='{0}_{1}_{2}'.format(mesh_2 , "nonBS" , list_BS_name[i]) , rr=True)
                    for item in BS_mesh_1:
                        try:
                            cm.setAttr("{}.tx".format(item) , lock=False)
                            cm.setAttr("{}.ty".format(item) , lock=False)
                            cm.setAttr("{}.tz".format(item) , lock=False)
                            cm.setAttr("{}.rx".format(item) , lock=False)
                            cm.setAttr("{}.ry".format(item) , lock=False)
                            cm.setAttr("{}.rz".format(item) , lock=False)
                            cm.setAttr("{}.sx".format(item) , lock=False)
                            cm.setAttr("{}.sy".format(item) , lock=False)
                            cm.setAttr("{}.sz".format(item) , lock=False)
                        except:
                            continue
                    u = i / 12
                    if u > 0:
                        cm.setAttr('{0}.tx'.format(BS_mesh_1[0]) , ((i - (u * 12) + 1) * distance_X * 1.2) * -1)
                    else:
                        cm.setAttr('{0}.tx'.format(BS_mesh_1[0]) , ((i + 1) * distance_X * 1.2) * -1)

                    cm.setAttr('{0}.ty'.format(BS_mesh_1[0]) , u * distance_Y * 1.2)

                else:
                    for z in blendShape_node:
                        cm.setAttr('{}.envelope'.format(z) , 0)

                    for z in blendShape_node:

                        try:
                            for x in list_BS_name:
                                cm.setAttr('{}.{}'.format(z , x) , 0)
                        except:
                            continue

                        if not cm.getAttr('{}.envelope'.format(z)):
                            cm.setAttr('{}.envelope'.format(z) , 1)

                        if cm.objExists('{}.{}'.format(z , list_BS_name[i])):
                            cm.setAttr('{}.{}'.format(z, list_BS_name[i]), 1)
                            cm.select(mesh_2)
                            BS_mesh_2 = cm.duplicate(n='{0}_{1}_{2}'.format(mesh_2, z , list_BS_name[i]) , rr=True)
                            for item in BS_mesh_2:
                                try:
                                    cm.setAttr("{}.tx".format(item) , lock=False)
                                    cm.setAttr("{}.ty".format(item) , lock=False)
                                    cm.setAttr("{}.tz".format(item) , lock=False)
                                    cm.setAttr("{}.rx".format(item) , lock=False)
                                    cm.setAttr("{}.ry".format(item) , lock=False)
                                    cm.setAttr("{}.rz".format(item) , lock=False)
                                    cm.setAttr("{}.sx".format(item) , lock=False)
                                    cm.setAttr("{}.sy".format(item) , lock=False)
                                    cm.setAttr("{}.sz".format(item) , lock=False)
                                except:
                                    continue
                            u = i / 12
                            if u > 0:
                                cm.setAttr('{0}.tx'.format(BS_mesh_2[0]) , ((i - (u * 12) + 1) * distance_X * 1.2) * -1)
                            else:
                                cm.setAttr('{0}.tx'.format(BS_mesh_2[0]) , ((i + 1) * distance_X * 1.2) * -1)

                            cm.setAttr('{0}.ty'.format(BS_mesh_2[0]) , u * distance_Y * 1.2)

                        else:

                            cm.select(mesh_2)
                            BS_mesh_3 = cm.duplicate(n='{0}_{1}_{2}'.format(mesh_2, z , list_BS_name[i]) , rr=True)
                            for item in BS_mesh_3:
                                try:
                                    cm.setAttr("{}.tx".format(item) , lock=False)
                                    cm.setAttr("{}.ty".format(item) , lock=False)
                                    cm.setAttr("{}.tz".format(item) , lock=False)
                                    cm.setAttr("{}.rx".format(item) , lock=False)
                                    cm.setAttr("{}.ry".format(item) , lock=False)
                                    cm.setAttr("{}.rz".format(item) , lock=False)
                                    cm.setAttr("{}.sx".format(item) , lock=False)
                                    cm.setAttr("{}.sy".format(item) , lock=False)
                                    cm.setAttr("{}.sz".format(item) , lock=False)
                                except:
                                    continue
                            u = i / 12
                            if u > 0:
                                cm.setAttr('{0}.tx'.format(BS_mesh_3[0]) , ((i - (u * 12) + 1) * distance_X * 1.2) * -1)
                            else:
                                cm.setAttr('{0}.tx'.format(BS_mesh_3[0]) , ((i + 1) * distance_X * 1.2) * -1)

                            cm.setAttr('{0}.ty'.format(BS_mesh_3[0]) , u * distance_Y * 1.2)


    def BackUp(self):
        for z in blendShape_node:

            blendShape_node_name = cm.listAttr('{}.w'.format(z) , m=True)

            if not cm.getAttr('{}.envelope'.format(z)):
                cm.setAttr('{}.envelope'.format(z) , 1)

            temporary_list_BS = []

            blendShape_pd = QtWidgets.QProgressDialog("Generating..." , "Cancel" , 0 ,
                                                      len(blendShape_node_name) - 1 , self)
            blendShape_pd.setWindowTitle("Generate BlendShape")
            blendShape_pd.setValue(0)
            blendShape_pd.setWindowModality(QtCore.Qt.WindowModal)
            blendShape_pd.show()
            QtCore.QCoreApplication.processEvents()

            for v in range(0 , len(blendShape_node_name)):
                if blendShape_pd.wasCanceled():
                    break

                blendShape_pd.setLabelText("Generate BS {0}: {1} of {2}".format(z , v , len(blendShape_node_name)))
                blendShape_pd.setValue(v)
                QtCore.QCoreApplication.processEvents()

                for each_BS in blendShape_node_name:
                    cm.setAttr('{0}.{1}'.format(z , each_BS) , 0)

                cm.setAttr('{0}.{1}'.format(z , blendShape_node_name[v]) , 1)
                cm.select(obj)
                BS_mesh = cm.duplicate(n='{0}_{1}'.format(z , blendShape_node_name[v]) , rr=True)
                u = v / 12
                if u > 0:
                    cm.setAttr('{0}.tx'.format(BS_mesh[0]) , ((v - (u * 12) + 1) * distance_X * 1.2) * -1)
                else:
                    cm.setAttr('{0}.tx'.format(BS_mesh[0]) , ((v + 1) * distance_X * 1.2) * -1)

                cm.setAttr('{0}.ty'.format(BS_mesh[0]) , u * distance_Y * 1.2)

                temporary_list_BS.append(BS_mesh[0])

            cm.group(temporary_list_BS , n='{0}_{1}'.format(obj , z) , w=True)

            del temporary_list_BS[:]

            for each_BS in blendShape_node_name:
                cm.setAttr('{0}.{1}'.format(z , each_BS) , 0)
