import maya.OpenMaya as om
import maya.cmds as cm
import pymel.core as pm
import sys

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


def relocation_pivot():
    """

    Returns: Pivot of object to world pivot at 0, 0, 0

    """

    selections = cm.ls(sl=True)

    if len(selections) < 1:
        return om.MGlobal.displayError("This function need at lest two object to work with")

    for selection in selections:
        cm.xform(selection, pivots=[0, 0, 0], worldSpace=True)

    sys.stdout.write("Re zero pivot completed.\n")


def create_control():
    """

    Returns: Create one simple control for all object under selected

    """

    selections = cm.ls(selection=True)

    if len(selections) < 1:
        return om.MGlobal.displayError("This function need at lest two object to work with")

    for selection in selections:
        if "End" in str(selection):
            continue
        else:
            for each_name in list_tail_name:
                if str(each_name) in selection:
                    base_name = selection.replace(str(each_name), "")
                else:
                    base_name = selection

            parent = cm.listRelatives(selection, parent=True)

            group_orient = cm.group(empty=True, world=True, name="{0}_orient".format(base_name))
            group_offset = cm.group(empty=True, world=True, name="{0}_offset".format(base_name))

            main_control = cm.circle(constructionHistory=False, name="{0}_mainCtr".format(base_name), radius=10,
                                     normal=[1, 0, 0])

            cm.parent(group_offset, group_orient)
            cm.parent(main_control, group_offset)

            if parent is not None:
                cm.parent(group_orient, parent)

            cm.matchTransform(group_orient, selection)
            cm.makeIdentity(group_offset, apply=True, scale=True)

            cm.parent(selection, main_control)

    sys.stdout.write("Create control completed.\n")


def create_double_control():
    """

    Returns: Create two simple control for all object under selected

    """

    selections = cm.ls(selection=True)

    if len(selections) < 1:
        return om.MGlobal.displayError("This function need at lest two object to work with")

    for selection in selections:
        if "End" in str(selection):
            continue
        else:
            for each_name in list_tail_name:
                if str(each_name) in selection:
                    base_name = selection.replace(str(each_name), "")
                else:
                    base_name = selection

            parent = cm.listRelatives(selection, parent=True)

            group_orient = cm.group(empty=True, world=True, name="{0}_orient".format(base_name))
            group_offset = cm.group(empty=True, world=True, name="{0}_offset".format(base_name))

            main_control = cm.circle(constructionHistory=False, name="{0}_mainCtr".format(base_name), radius=10,
                                     normal=[1, 0, 0])
            sup_control = cm.circle(constructionHistory=False, name="{0}_supCtr".format(base_name), radius=5,
                                    normal=[1, 0, 0])

            cm.parent(group_offset, group_orient)
            cm.parent(main_control, group_offset)
            cm.parent(sup_control, main_control)

            if parent is not None:
                cm.parent(group_orient, parent)

            cm.matchTransform(group_orient, selection)
            cm.makeIdentity(group_offset, apply=True, scale=True)

            cm.parent(selection, sup_control)

    sys.stdout.write("Create double control completed.\n")


def create_group_orient():
    """

    Returns: Create one simple group for all object under selected

    """

    selections = cm.ls(selection=True)

    if len(selections) < 1:
        return om.MGlobal.displayError("This function need at lest two object to work with")

    for selection in selections:
        if "End" in str(selection):
            continue
        else:
            for each_name in list_tail_name:
                if str(each_name) in selection:
                    base_name = selection.replace(str(each_name), "")
                else:
                    base_name = selection

            parent = cm.listRelatives(selection, parent=True)

            group_orient = cm.group(empty=True, world=True, name="{0}_orient".format(base_name))

            if parent is not None:
                cm.parent(group_orient, parent)

            cm.matchTransform(group_orient, selection)
            cm.makeIdentity(group_orient, apply=True, scale=True)
            cm.parent(selection, group_orient)

    sys.stdout.write("Create group orient completed.\n")


def create_double_group():
    """

    Returns: Create two simple control for all object under selected

    """

    selections = cm.ls(selection=True)

    if len(selections) < 1:
        return om.MGlobal.displayError("This function need at lest two object to work with")

    for selection in selections:
        if "End" in str(selection):
            continue
        else:
            for each_name in list_tail_name:
                if str(each_name) in selection:
                    base_name = selection.replace(str(each_name), "")
                else:
                    base_name = selection

            parent = cm.listRelatives(selection, parent=True)

            group_orient = cm.group(empty=True, world=True, name="{0}_orient".format(base_name))
            group_offset = cm.group(empty=True, world=True, name="{0}_offset".format(base_name))

            cm.parent(group_offset, group_orient)

            if parent is not None:
                cm.parent(group_orient, parent)

            cm.matchTransform(group_orient, selection)
            cm.makeIdentity(group_orient, apply=True, scale=True)

            cm.parent(selection, group_offset)

    sys.stdout.write("Create double group completed.\n")


def simple_FK_selected():
    """

    Returns: Create FK control for all object under the object we select from first palace

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
        constrains_1 = cm.pointConstraint(sel_new, selection)
        constrains_2 = cm.orientConstraint(sel_new, selection)
        constrains_3 = cm.scaleConstraint(sel_new, selection)

        cm.parent(constrains_1, 'FKConstrainsSystem')
        cm.parent(constrains_2, 'FKConstrainsSystem')
        cm.parent(constrains_3, 'FKConstrainsSystem')
        cm.select(sel_new, hi=True)
        create_control()
        hasParent = bool(cm.listRelatives('{}_GRP'.format(sel_new), parent=True))
        if hasParent is True:
            cm.select('{}_GRP'.format(sel_new))
            cm.parent(w=True)
        else:
            pass

        sys.stdout.write("Create simple FK completed.\n")

    else:
        cm.warning('Please only chose the root of the bone')


def parent_selected():
    """

    Returns: Parent all object selected one by one

    """
    selection = cm.ls(sl=True)

    if len(selection) < 2:
        return om.MGlobal.displayError("This function need at lest two object to work with")

    for i in range(0, len(selection)):
        cm.parent(selection[i + 1], selection[i], relative=False)

    sys.stdout.write("Parent completed.\n")


def match_pivot_transform():
    """

    Returns: match pivot of the objects selection to the location pivot of the lost object

    """

    selection = cm.ls(sl=True)

    if len(selection) < 2:
        return om.MGlobal.displayError("This function need at lest two object to work with")

    else:
        for obj in selection[:-1]:
            cm.matchTransform(obj, selection[-1], pivots=True)

    sys.stdout.write("Match completed.\n")


def match_location(position=False, rotation=False, scale=False):
    """

    Args:
        position: chose to turn on match transform or not
        rotation: chose to turn on match rotation or not
        scale: chose to turn on match scale or not

    Returns: match objects selection to location of the last object we chose

    """

    selection = cm.ls(sl=True)

    if len(selection) < 2:
        return om.MGlobal.displayError("This function need at lest two object to work with")

    else:
        for obj in selection[:-1]:
            cm.matchTransform(obj, selection[-1], position=position, rotation=rotation, scale=scale)

    sys.stdout.write("Match completed.\n")


def lock_unlock(transform=False, rotation=False, scale=False, all_attribute=False):
    """

    Args:
        transform: Only lock/unlock transform
        rotation: Only lock/unlock rotation
        scale: Only lock/unlock scale
        all_attribute: lock/unlock all transform, rotation, scale

    Returns: lock attribute or unlock attribute object we chose in scene

    """

    selections = pm.ls(selection=True)

    if len(selections) < 1:
        return om.MGlobal.displayError("Please chose at least a object to work with")

    for selection in selections:
        rx = selection.rx.isLocked()
        ry = selection.ry.isLocked()
        rz = selection.rz.isLocked()
        tx = selection.tx.isLocked()
        ty = selection.ty.isLocked()
        tz = selection.tz.isLocked()
        sx = selection.sx.isLocked()
        sy = selection.sy.isLocked()
        sz = selection.sz.isLocked()

        if transform:

            if tx and ty and tz:
                selection.tx.setLocked(False)
                selection.ty.setLocked(False)
                selection.tz.setLocked(False)

            else:
                selection.tx.setLocked(True)
                selection.ty.setLocked(True)
                selection.tz.setLocked(True)

        if rotation:

            if rx and ry and rz:
                selection.rx.setLocked(False)
                selection.ry.setLocked(False)
                selection.rz.setLocked(False)

            else:
                selection.rx.setLocked(True)
                selection.ry.setLocked(True)
                selection.rz.setLocked(True)

        if scale:

            if sx and sy and sz:
                selection.sx.setLocked(False)
                selection.sy.setLocked(False)
                selection.sz.setLocked(False)

            else:
                selection.sx.setLocked(True)
                selection.sy.setLocked(True)
                selection.sz.setLocked(True)

        if all_attribute:

            if tx and ty and tz and rx and ry and rz and sx and sy and sz:
                selection.tx.setLocked(False)
                selection.ty.setLocked(False)
                selection.tz.setLocked(False)
                selection.rx.setLocked(False)
                selection.ry.setLocked(False)
                selection.rz.setLocked(False)
                selection.sx.setLocked(False)
                selection.sy.setLocked(False)
                selection.sz.setLocked(False)

            else:
                selection.tx.setLocked(True)
                selection.ty.setLocked(True)
                selection.tz.setLocked(True)
                selection.rx.setLocked(True)
                selection.ry.setLocked(True)
                selection.rz.setLocked(True)
                selection.sx.setLocked(True)
                selection.sy.setLocked(True)
                selection.sz.setLocked(True)

    sys.stdout.write("Complete.\n")


def freezy_transformations(translate=False, rotate=False, scale=False):
    """

    Args:
        translate: Only freezy translate
        rotate: Only freezy rotate
        scale: Only freezy scale

    Returns: Zero back attribute of transform node

    """
    selections = pm.ls(selection=True)

    if len(selections) < 1:
        return om.MGlobal.displayError("Please chose at least a object to work with")

    for selection in selections:
        pm.makeIdentity(selection, apply=True, preserveNormals=True, normal=0, translate=translate, rotate=rotate,
                        scale=scale)

    sys.stdout.write("Complete.\n")


def create_attribute_visibility():
    """

    Returns: Create attribute to separate visibility

    """
    selections = cm.ls(sl=True)

    if len(selections) < 1:
        return om.MGlobal.displayError("Please chose at least a object to work with")

    for selection in selections:
        cm.select(selection)
        cm.addAttr(longName="____MAIN____", niceName="____MAIN____", attributeType="enum", enumName="0", keyable=False)
        cm.addAttr(longName="____EXTRA____", niceName="____EXTRA____", attributeType="enum", enumName="0",
                   keyable=False)
        cm.addAttr(longName="____SUB____", niceName="____SUB____", attributeType="enum", enumName="0", keyable=False)

        cm.setAttr("{0}.____MAIN____".format(selection), edit=True, channelBox=True)
        cm.setAttr("{0}.____EXTRA____".format(selection), edit=True, channelBox=True)
        cm.setAttr("{0}.____SUB____".format(selection), edit=True, channelBox=True)

    sys.stdout.write("Complete.\n")


def up_down_attribute(up=False, down=False):
    """

    Args:
        up: Set the selected attribute go up 1 index in the main channel box
        down: Set the selected attribute go down 1 index in the main channel box

    Returns: Relocation of selected attribute in main channel box

    """
    selections = pm.ls(sl=True)
    if len(selections) != 1:
        return om.MGlobal.displayError("This function only work with one object per time")

    selection = selections[0]

    selected_attr = pm.channelBox("mainChannelBox", query=True, selectedMainAttributes=True)
    list_attr = pm.listAttr(selection, userDefined=True, locked=True)

    if len(list_attr) > 0:
        for attr in list_attr:
            pm.setAttr("{0}.{1}".format(selection, attr), lock=False)

    if down:
        if len(selected_attr) > 1:
            selected_attr.reverse()
            sort = selected_attr
        if len(selected_attr) == 1:
            sort = selected_attr
        for i in sort:
            attr_list = pm.listAttr(selection, userDefined=True)
            attr_list_size = len(attr_list)
            attr_position = attr_list.index(i)
            pm.deleteAttr(selection, attribute=attr_list[attr_position])
            pm.undo()

            for x in range(attr_position + 2, attr_list_size, 1):
                pm.deleteAttr(selection, attribute=attr_list[x])
                pm.undo()

    if up:
        for i in selected_attr:
            attr_list = pm.listAttr(selection, userDefined=True)
            attr_list_size = len(attr_list)
            attr_position = attr_list.index(i)
            if attr_list[attr_position - 1]:
                pm.deleteAttr(selection, attribute=attr_list[attr_position - 1])
                pm.undo()
            for x in range(attr_position + 1, attr_list_size, 1):
                pm.deleteAttr(selection, attribute=attr_list[x])
                pm.undo()

    if len(list_attr) > 0:
        for attr in list_attr:
            pm.setAttr("{0}.{1}".format(selection, attr), lock=True)

    sys.stdout.write("Complete.\n")