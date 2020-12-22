import numpy as np
from xml.dom import minidom

print("Initialized")
root = minidom.Document()


def tag(tag_name, **kwargs):
    _tag = root.createElement(tag_name)
    for key, name in kwargs.items():
        _tag.setAttribute(key, name)
    return _tag


def find_inertia(mesh_shape, size, m):
    ixx, iyy, izz, ixy, iyz, ixz = 0, 0, 0, 0, 0, 0
    if mesh_shape == 'cylinder':
        # TODO: Check which axis defines the height
        length = size[0]
        radius = size[1]
        ixx = (m/12)*(length**2)
        iyy = 0
        izz = (m/12)*(length**2)
        ixy = 0
        ixz = 0
        iyz = 0
    elif mesh_shape == 'box':
        x = size[0]
        y = size[1]
        z = size[2]
        ixx = (m / 12) * (y ** 2 + z ** 2)
        iyy = (m / 12) * (x ** 2 + z ** 2)
        izz = (m / 12) * (x ** 2 + y ** 2)
        ixy = 0
        ixz = 0
        iyz = 0

    return ixx, iyy, izz, ixy, iyz, ixz


def create_link(name, mesh_type_info, mass=0.1, xyz=(0, 0, 0), rpy=(0, 0, 0)):
    """
    :param:
    name: Link Name
    mesh_type_info: Tuple(mesh_shape,shape_size)
    mass: mass value, default value is 0.1
    :return:
    minidom object
    """

    link = tag('link', name=name)
    geometry_visual = tag('geometry')
    geometry_collision = tag('geometry')
    collision = tag('collision')
    inertial = tag('inertial')
    visual = tag('visual')
    origin_visual = tag('origin', xyz=f"{xyz[0]} {xyz[1]} {xyz[2]}", rpy=f"{rpy[0]} {rpy[1]} {rpy[2]}")
    origin_collision = tag('origin', xyz=f"{xyz[0]} {xyz[1]} {xyz[2]}", rpy=f"{rpy[0]} {rpy[1]} {rpy[2]}")
    # TODO: Check if origin_inertial is similar to origin_visual/origin_collision
    origin_inertial = tag('origin', xyz=f"{xyz[0]} {xyz[1]} {xyz[2]}", rpy=f"{rpy[0]} {rpy[1]} {rpy[2]}")

    if mesh_type_info[0] == "box":
        size = mesh_type_info[1]
        geometry_visual.appendChild(tag(mesh_type_info[0], size=f"{size[0]} {size[1]} {size[2]}"))
        geometry_collision.appendChild(tag(mesh_type_info[0], size=f"{size[0]} {size[1]} {size[2]}"))
    elif mesh_type_info[0] == "cylinder":
        size = mesh_type_info[1]
        geometry_visual.appendChild(tag(mesh_type_info[0], length=f"{size[0]}", radius=f"{size[1]}"))
        geometry_collision.appendChild(tag(mesh_type_info[0], length=f"{size[0]}", radius=f"{size[1]}"))

    # Adding Visual tag w/ geometry, mesh
    visual.appendChild(origin_visual)
    visual.appendChild(geometry_visual)

    # Adding Collision tag w/ geometry,mesh
    collision.appendChild(origin_collision)
    collision.appendChild(geometry_collision)

    # Adding Inertial tag w/ mass, inertia
    inertial.appendChild(origin_inertial)
    inertial.appendChild(tag('mass', value=f"{mass}"))
    # TODO Implement Inertia Function based on mesh_shape, shape_size and mass
    ixx, iyy, izz, ixy, iyz, ixz = find_inertia(mesh_type_info[0], mesh_type_info[1], mass)
    inertial.appendChild(tag('inertia', ixx=f"{ixx}", iyy=f"{iyy}", izz=f"{izz}", ixy=f"{ixy}", iyz=f"{iyz}", ixz=f"{ixz}"))
    link.appendChild(visual)
    link.appendChild(collision)
    link.appendChild(inertial)
    return link


def create_joint(name, joint_type, parent_link, child_link, xyz=(0, 0, 0), rpy=(0, 0, 0), axis=(0, 0, 0)):
    """
    :param:

    :return:
    """
    joint = tag('joint', name=name, type=joint_type)
    parent = tag('parent', link=parent_link)
    child = tag('child', link=child_link)
    origin = tag('origin', xyz=f"{xyz[0]} {xyz[1]} {xyz[2]}", rpy=f"{rpy[0]} {rpy[1]} {rpy[2]}")
    ax = tag('axis', xyz=f"{axis[0]} {axis[1]} {axis[2]}")
    joint.appendChild(parent)
    joint.appendChild(child)
    joint.appendChild(origin)
    joint.appendChild(ax)

    return joint


if __name__ == '__main__':
    robot = tag('robot', name="MNP")
    # Creating Link/Joint to attach Arm to the world
    world = tag('link', name='world')
    fixed = create_joint('anchor', 'fixed', 'world', 'base')
    base = create_link('base', ("cylinder", (0.1, 0.05)), mass=0.5, xyz=(0, 0, 0.05), rpy=(1.57, 0, 0))
    lower_arm = create_link('lower_arm', ("box", (0.1, 0.05, 0.5)), mass=0.5, xyz=(0, 0, 0.3))
    upper_arm = create_link('upper_arm', ("box", (0.1, 0.05, 0.5)), mass=0.5, xyz=(0, 0, 0.3))
    base_jnt = create_joint('base_jnt', 'continuous', 'base', 'lower_arm', xyz=(0, 0, 0.05), axis=(0, 1, 0))
    elbow_jnt = create_joint('elbow_jnt', 'continuous', 'lower_arm', 'upper_arm', xyz=(0, 0, 0.6), axis=(0, 1, 0))
    root.appendChild(robot)
    robot.appendChild(world)
    robot.appendChild(base)
    robot.appendChild(lower_arm)
    robot.appendChild(upper_arm)
    robot.appendChild(fixed)
    robot.appendChild(base_jnt)
    robot.appendChild(elbow_jnt)
    xml_str = root.toprettyxml(indent="\t")
    save_path_file = 'decor.urdf'
    with open(save_path_file, "w") as f:
        f.write(xml_str)

