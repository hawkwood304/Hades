import sys

import maya.OpenMaya as om
import maya.cmds as cm
import maya.mel as mel
import pymel.core as pm

list_tail_name = [
    '_JNT',
    '_Jnt',
    '_jnt',
    '_BND',
    '_Bnd',
    '_bnd',
    '_Jt',
    '_CON',
    '_Con',
    '_con',
    '_CTRL',
    '_Ctrl'
    '_ctrl',
    '_LOC',
    '_Loc',
    '_loc',
    '_GRP',
    '_Grp',
    '_grp'
]


def Match(position=False, rotation=False, scale=False):
    """

    Args:
        position: chose to turn on match transform or not
        rotation: chose to turn on match rotation or not
        scale: chose to turn on match scale or not

    Returns: match objects selection to location of the last object we chose

    """

    selection = cm.ls(sl=True)

    if len(selection) < 2:
        return om.MGlobal.displayError("This argument need at lest two object to work with")

    else:
        for obj in selection[:-1]:
            cm.matchTransform(obj, selection[-1], position=position, rotation=rotation, scale=scale)

    sys.stdout.write("Match completed\n")


def MatchPivotTransform():
    """

    Returns: match pivot of the objects selection to the location pivot of the lost object

    """

    selection = cm.ls(sl=True)

    if len(selection) < 2:
        return om.MGlobal.displayError("This argument need at lest two object to work with")

    else:
        for obj in selection[:-1]:
            cm.matchTransform(obj, selection[-1], pivots=True)

    sys.stdout.write("Match completed\n")


def ControlLocatorGroup(SecondControl=False):
    """

    Returns: create curve control, locator, group for each object we chose in scene

    """

    selection = cm.ls(sl=True)

    for item in selection:
        if 'End' in str(item):
            continue
        else:
            for each in list_tail_name:
                if str(each) in item:
                    base_name = item.replace(str(each), "")
                else:
                    base_name = item

            par = cm.listRelatives(item, p=True)

            grp = cm.group(em=True, w=True, n="{}_offset".format(base_name))
            loc = cm.spaceLocator(p=(0, 0, 0), n="{}_loc".format(base_name))
            con_1 = cm.circle(ch=0, n='{}_con1'.format(base_name), r=10, nr=[1, 0, 0])

            cm.parent(loc, grp)
            cm.parent(con_1, loc)

            if SecondControl:
                con_2 = cm.circle(ch=0, n='{}_con2'.format(base_name), r=5, nr=[1, 0, 0])
                cm.parent(con_2, con_1)

            if par is not None:
                cm.parent(grp, par)

            cm.matchTransform(grp, item)
            cm.makeIdentity(grp, a=True, s=1)
            if SecondControl:
                cm.parent(item, con_2)
            else:
                cm.parent(item, con_1)
            cm.setAttr('{}Shape.visibility'.format(loc[0]), 0)


def LocatorGroup():
    """

    Returns: create a locator and group for each object we chose in scene

    """
    selection = cm.ls(sl=True)

    for item in selection:
        if 'End' in str(item):
            continue
        else:
            for each in list_tail_name:
                if str(each) in item:
                    base_name = item.replace(str(each), "")
                else:
                    base_name = item

            par = cm.listRelatives(item, p=True)

            grp = cm.group(em=True, w=True, n="{}_offset".format(base_name))
            loc = cm.spaceLocator(p=(0, 0, 0), n="{}_loc".format(base_name))

            cm.parent(loc, grp)

            if par is not None:
                cm.parent(grp, par)

            cm.matchTransform(grp, item)
            cm.makeIdentity(grp, a=True, s=1)

            cm.parent(item, loc)
            cm.setAttr('{}Shape.visibility'.format(loc[0]), 0)


def Locator():
    """

    Returns: create a locator for each object we chose in scene

    """
    selection = cm.ls(sl=True)

    for item in selection:
        if 'End' in str(item):
            continue
        else:
            for each in list_tail_name:
                if str(each) in item:
                    base_name = item.replace(str(each), "")
                else:
                    base_name = item

            par = cm.listRelatives(item, p=True)

            loc = cm.spaceLocator(p=(0, 0, 0), n="{}_loc".format(base_name))

            if par is not None:
                cm.parent(loc, par)
            cm.matchTransform(loc, item)
            cm.makeIdentity(loc, a=True, s=1)

            cm.parent(item, loc)


def Group():
    """

    Returns: create a group for each object we chose in scene

    """
    selection = cm.ls(sl=True)

    for item in selection:
        if 'End' in str(item):
            continue
        else:
            for each in list_tail_name:
                if str(each) in item:
                    base_name = item.replace(str(each), "")
                else:
                    base_name = item

            par = cm.listRelatives(item, p=True)

            grp = cm.group(em=True, w=True, n="{}_offset".format(base_name))

            if par is not None:
                cm.parent(grp, par)

            cm.matchTransform(grp, item)
            cm.makeIdentity(grp, a=True, s=1)

            cm.parent(item, grp)


def LocatorOnVertex():
    """

    Returns: crete a locator follow vertex we chose before

    """

    selection = cm.ls(sl=True)
    print selection
    if len(selection) != 1 or '.vtx[' not in str(selection[0]):
        return om.MGlobal.displayError("Please chose only one vertex")
    if ':' in str(selection[0]):
        return om.MGlobal.displayError("Please chose only one vertex")

    loc = cm.spaceLocator()
    grp = cm.group(loc[0])

    constraint = cm.pointOnPolyConstraint(selection[0], grp)
    mapUV = cm.polyListComponentConversion(selection[0], fv=True, tuv=True)
    mapCoord = cm.polyEditUV(mapUV[0], q=True, u=True, v=True)
    constraintAttr = cm.listAttr(constraint[0], ud=True)

    cm.setAttr('{}.{}'.format(constraint[0], constraintAttr[1]), mapCoord[0])
    cm.setAttr('{}.{}'.format(constraint[0], constraintAttr[2]), mapCoord[1])

    cm.select(loc)


def LockUnlock(Transform=False, Rotation=False, Scale=False):
    """

    Returns: lock attribute or unlock attribute object we chose in scene

    """

    selection = cm.ls(sl=True)

    if len(selection) < 1:
        return om.MGlobal.displayError("Please chose at least a object to work with")

    for item in selection:
        if Transform:
            tx = cm.getAttr("{}.tx".format(item), lock=True)
            ty = cm.getAttr("{}.ty".format(item), lock=True)
            tz = cm.getAttr("{}.tz".format(item), lock=True)
            if tx and ty and tz:
                cm.setAttr("{}.tx".format(item), lock=False)
                cm.setAttr("{}.ty".format(item), lock=False)
                cm.setAttr("{}.tz".format(item), lock=False)
            else:
                cm.setAttr("{}.tx".format(item), lock=True)
                cm.setAttr("{}.ty".format(item), lock=True)
                cm.setAttr("{}.tz".format(item), lock=True)

        if Rotation:
            rx = cm.getAttr("{}.rx".format(item), lock=True)
            ry = cm.getAttr("{}.ry".format(item), lock=True)
            rz = cm.getAttr("{}.rz".format(item), lock=True)
            if rx and ry and rz:
                cm.setAttr("{}.rx".format(item), lock=False)
                cm.setAttr("{}.ry".format(item), lock=False)
                cm.setAttr("{}.rz".format(item), lock=False)
            else:
                cm.setAttr("{}.rx".format(item), lock=True)
                cm.setAttr("{}.ry".format(item), lock=True)
                cm.setAttr("{}.rz".format(item), lock=True)

        if Scale:
            sx = cm.getAttr("{}.sx".format(item), lock=True)
            sy = cm.getAttr("{}.sy".format(item), lock=True)
            sz = cm.getAttr("{}.sz".format(item), lock=True)
            if sx and sy and sz:
                cm.setAttr("{}.sx".format(item), lock=False)
                cm.setAttr("{}.sy".format(item), lock=False)
                cm.setAttr("{}.sz".format(item), lock=False)
            else:
                cm.setAttr("{}.sx".format(item), lock=True)
                cm.setAttr("{}.sy".format(item), lock=True)
                cm.setAttr("{}.sz".format(item), lock=True)


def FKForSelected():
    """

    Returns: Create FK control for all object under the object we chose from first palace

    """
    selection = cm.ls(sl=True)
    if len(selection) == 1:
        cm.select(hi=True)
        selNew = cm.ls(sl=True, type='joint')
        dupList = []
        for obj in selNew:
            if 'End' not in str(obj):
                dupList.append(obj)
            else:
                continue

        cm.duplicate(dupList, rr=True, po=True)
        sel_new = cm.rename('FK_{}'.format(selection[0]))
        if cm.objExists('FKConstrainsSystem'):
            pass
        else:
            cm.group(em=True, name='FKConstrainsSystem')
        cm.select(sel_new, hi=True)
        sel_1 = cm.ls(sl=True)
        sel_1.sort(key=len, reverse=True)
        for i in sel_1:
            short_name = i.split('|')[-1]
            new_name = 'FK_{}'.format(short_name)
            if 'FK_' not in str(short_name):
                cm.rename(i, new_name)
                pointConstraints = cm.pointConstraint(new_name, short_name)
                orientConstraints = cm.orientConstraint(new_name, short_name)
                scaleConstraints = cm.scaleConstraint(new_name, short_name)
                cm.parent(pointConstraints, 'FKConstrainsSystem')
                cm.parent(orientConstraints, 'FKConstrainsSystem')
                cm.parent(scaleConstraints, 'FKConstrainsSystem')
            else:
                continue
        constrains_1 = cm.parentConstraint(sel_new, selection)
        constrains_2 = cm.scaleConstraint(sel_new, selection)

        cm.parent(constrains_1, 'FKConstrainsSystem')
        cm.parent(constrains_2, 'FKConstrainsSystem')
        cm.select(sel_new, hi=True)
        ControlLocatorGroup()
        hasParent = bool(cm.listRelatives('{}_GRP'.format(sel_new), parent=True))
        if hasParent is True:
            cm.select('{}_GRP'.format(sel_new))
            cm.parent(w=True)
        else:
            pass
    else:
        cm.warning('Just chose the root of the bone')


def ParentAll():
    """

    Returns: Parent all object selected one by one

    """
    selection = cm.ls(sl=True)

    for i in range(0, len(selection)):
        cm.parent(selection[i + 1], selection[i], relative=True)


def SelectAll(text):
    """

    Returns: Select all object have that string in name

    """
    if len(text) == 0:
        return om.MGlobal.displayError("Please write down object name you want to find in scene")
    try:
        cm.select("*{0}*".format(text))
        selection = cm.ls(sl=True)
    except:
        return om.MGlobal.displayWarning("There is none object have :'{0}' in name".format(text))
