import sys

import maya.OpenMaya as om
import maya.cmds as cm
import maya.mel as mel
import pymel.core as pm


def CleanAllNamespace():
    """

    Returns: Clean all the namespace we have in scene and merge it all to root

    """
    cm.namespace(set=':')
    namespaces = cm.namespaceInfo(listOnlyNamespaces=True)
    namespacesMerged = 0
    for name in namespaces:
        if name == "UI":
            continue
        if name == "shared":
            continue
        cm.namespace(removeNamespace=name, mergeNamespaceWithRoot=True)
        namespacesMerged += 1

    sys.stdout.write('Clean Namespace is done\n')


def CopyUV():
    """

    Returns: Copy UV form two object even one have skin weight

    """
    selection = pm.ls(sl=True)

    if len(selection) != 2:
        om.MGlobal.displayError("This argument need exactly two object to work with")
        return

    else:
        history = pm.listHistory(selection[1])
        list_his = pm.ls(history, type='skinCluster')
        if len(list_his) != 0:
            child = pm.listRelatives(selection[1])
            for c in child:
                if 'Orig' in str(c):
                    pm.setAttr('{}.intermediateObject'.format(c), 0)
                    pm.transferAttributes(selection[0], c, transferPositions=0, transferNormals=0, transferUVs=2,
                                          transferColors=2, sampleSpace=4, sourceUvSpace='map1', flipUVs=0)
                    pm.delete(c, ch=True)
                    pm.setAttr('{}.intermediateObject'.format(c), 1)
                    sys.stdout.write('Copy UV is done\n')
                else:
                    pass
        else:
            pm.transferAttributes(selection[0], selection[1], transferPositions=0, transferNormals=0,
                                  transferUVs=2,
                                  transferColors=2, sampleSpace=4, sourceUvSpace='map1', flipUVs=0)
            pm.delete(selection[1], ch=True)
            sys.stdout.write('Copy UV is done\n')


def CombineSkinnedMeshProc(Name):
    """

    Args:
        Name: Name we use for the new mesh we combine

    Returns: Mesh combine with skin weight by all of the object we chose before

    """
    selection = cm.ls(sl=True)
    joint_list = []
    if len(selection) < 2:
        return om.MGlobal.displayError('Please Select at least two skinned Meshes')

    if len(Name) == 0:
        return om.MGlobal.displayError('Please Assign a Name')

    if " " in Name:
        return om.MGlobal.displayError("You are using illegal characters for the name! Space is not allowed")

    if cm.objExists(Name):
        return om.MGlobal.displayError("This name is already in use in scene! Please check again")

    for item in selection:
        findSkinStart = mel.eval('findRelatedSkinCluster {}'.format(item))

        if not cm.objExists(findSkinStart):
            return om.MGlobal.displayError("Please Select at least two skinned Meshes")

        matrix_array = cm.getAttr("{}.matrix".format(findSkinStart), mi=True)

        for i in matrix_array:
            list_connection = cm.connectionInfo("{0}.matrix[{1}]".format(findSkinStart, str(i)),
                                                sourceFromDestination=True)
            joint = list_connection.split(".")
            joint_list.append(joint[0])

    if len(selection) > 0:
        for i in range(1):
            duplicateObj = cm.duplicate(selection)
            createGrp = cm.group(duplicateObj)
            combine = cm.polyUnite(createGrp, name=Name)
            # Delete History
            cm.delete(combine, ch=True)
            # Delete Group
            cm.select(cm.delete(createGrp))
            # New Skin
            cm.skinCluster(joint_list, Name, n=Name + "_SKC")
            # New Select
            cm.select(joint_list, selection, Name, add=True)
            # Transfer Skin Weight
            cm.copySkinWeights(nm=True, sa="closestPoint", ia="closestJoint")
            # Delete
            cm.delete(selection)
            # Select new object
            cm.select(Name)
            # Clean skin not used
            mel.eval('removeUnusedInfluences')
            # Clear select
            cm.select(cl=True)
            sys.stdout.write("Separate is completed\n")


# noinspection PyUnboundLocalVariable
def SeparateSkinnedMeshProc(Name):
    """

    Args:
        Name: Name we use for new mesh we separate

    Returns: All mesh with skin weight separated from the object we chose before

    """
    selection = cm.ls(sl=True)

    if len(selection) != 1:
        return om.MGlobal.displayError('Please Select a Skinned Mesh')

    if len(Name) == 0:
        return om.MGlobal.displayError('Please Assign a Name')

    if " " in Name:
        return om.MGlobal.displayError("You are using illegal characters for the name! Space is not allowed")

    if cm.objExists(Name):
        return om.MGlobal.displayError("This name is already in use in scene! Please check again")

    for item in selection:
        findSkinStart = mel.eval('findRelatedSkinCluster {}'.format(item))

        if not cm.objExists(findSkinStart):
            return om.MGlobal.displayError("Please Select a Skinned Mesh")

    if len(selection) > 0:
        duplicateObj = cm.duplicate(selection, name=Name)

        separate = cm.polySeparate(duplicateObj, name="{}NewSkin*".format(Name), ch=True)
        # Delete history
        cm.delete(separate, ch=True)

        # Clear selection
        cm.select(cl=True)

        # Select new mesh
        cm.select(Name, hi=True)

        # Deselect group
        cm.select(Name, d=True)

        given_list = cm.ls(sl=True)
        mesh = given_list

        for index in range(len(mesh)):
            joints = cm.skinCluster(item, q=True, inf=True)
            for obj in mesh:
                findSkinEnd = mel.eval('findRelatedSkinCluster {}'.format(obj))

                if not cm.objExists(findSkinEnd):
                    cm.skinCluster(obj, joints, name="{}_SKC".format(Name))
                    break

            cm.select(joints, selection, obj, add=True)
            cm.copySkinWeights(nm=True, sa="closestPoint", ia="closestJoint")
            mel.eval('removeUnusedInfluences')

        cm.select(cl=True)
        cm.delete(selection)
        sys.stdout.write("Separate is completed\n")


def TransformSkinnedMeshProc():
    """

    Returns: mesh with skinned weight from mesh we chose before

    """
    selection = cm.ls(sl=True)
    joint_list = []

    if len(selection) != 2:
        return om.MGlobal.displayError("Please chose mesh clean then chose mesh skinned to transform")
    for item in selection[1:]:
        findSkinStart = mel.eval('findRelatedSkinCluster {}'.format(item))

        if not cm.objExists(findSkinStart):
            return om.MGlobal.displayError(
                "Please first select clean mesh you want to transform skin weight then chose mesh with skinned")

        matrix_array = cm.getAttr("{}.matrix".format(findSkinStart), mi=True)

        for i in matrix_array:
            list_connection = cm.connectionInfo("{0}.matrix[{1}]".format(findSkinStart, str(i)),
                                                sourceFromDestination=True)
            joint = list_connection.split(".")
            joint_list.append(joint[0])

        cm.skinCluster(joint_list, selection[0], n="{}_SKC".format(selection[0]))
        cm.select(joint_list, selection, add=True)
        cm.copySkinWeights(nm=True, sa="closestPoint", ia="closestJoint")
        cm.select(selection[0])
        mel.eval('removeUnusedInfluences')

        sys.stdout.write("Transform is done\n")
