import maya.cmds as cm
import pymel.core as pm
import sys
import os
import maya.OpenMaya as om


def create_T_pose():
    current_selection = pm.ls(sl=True)
    if len(current_selection) != 1:
        return om.MGlobal.displayError("Please select root bone")

    cm.currentTime(0)

    pm.select(hi=True, add=True)

    selections = pm.ls(selection=True)

    for selection in selections:
        selection.rx.set(0)
        selection.ry.set(0)
        selection.rz.set(0)
        pm.setKeyframe(selection)

    sys.stdout.write("TPose create")
