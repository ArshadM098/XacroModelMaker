from xml.dom import minidom
import numpy as np


class RobotURDF:

    def __init__(self, robot_name):
        self.robot_name = robot_name
        self.root = minidom.Document()
        self.xml = self.root.createElement('robot')
        self.xml.setAttribute('name', robot_name)
        self.root.appendChild(self.xml)
        self.num_links = 0
        self.num_joints = 0
        self.links = np.empty(self.num_links, dtype=object)
        self.joints = np.empty(self.num_joints, dtype=object)

    def create_link(self, name, g_shape, size, mass, xyz=(0, 0, 0), rpy=(0, 0, 0)):
        li = self._tag('link')
        li.setAttribute('name', name)
        o = self.create_origin(xyz, rpy)

        geometry = None
        if g_shape == 'cylinder':
            geometry = self.create_cylinder()

        elif g_shape == 'box':
            geometry = self.create_box()
        # TODO: Fix The Error
        collision = self._tag('collision')
        collision.appendChild(o)
        collision.appendChild(geometry)

        visual = self._tag('visual')
        visual.appendChild(o)
        visual.appendChild(geometry)

        inertial = self._tag('inertial')
        m = self._tag('mass')
        m.setAttribute('value', 1)
        inertia = self.get_inertia(g_shape, size, mass)
        inertial.appendChild(o)
        inertial.appendChild(m)
        inertial.appendChild(inertia)

        li.appendChild(collision)
        li.appendChild(visual)
        li.appendChild(inertial)

        self.links = np.append(self.links, li)
        self.num_links = self.links.shape[0]

    def create_joint(self, name, joint_type, parent_link, child_link, xyz=(0,0,0), rpy=(0,0,0)):
        j = self._tag('joint')
        # Adding Name and Type Attributes to the joint
        j.setAttribute('name', name)
        j.setAttribute('type', joint_type)

        # Adding Parent/Child Links to the Joint
        parent = self._tag('parent')
        parent.setAttribute('link', parent_link)
        j.appendChild(parent)
        child = self._tag('child')
        child.setAttribute('link', child_link)
        j.appendChild(child)

        # Adding origin values to the joint
        o = self.create_origin(xyz, rpy)
        j.appendChild(o)

        self.joints = np.append(self.joints, j)
        self.num_joints = self.joints.shape[0]

    def create_cylinder(self, len_rad=(1, 1)):
        cy = self._tag('cylinder')
        # cy.setAttribute('length', len_rad[0])
        # cy.setAttribute('radius', len_rad[1])
        g = self._tag('geometry')
        g.appendChild(cy)
        return g

    def create_box(self, size=(1, 1, 1)):
        box = self._tag('cylinder')
        box.setAttribute('size', f'{size[0]} {size[1]} {size[2]}')
        g = self._tag('geometry')
        g.appendChild(box)
        return g

    def create_origin(self, xyz, rpy):
        origin = self._tag('origin')
        origin.setAttribute('xyz', f'{xyz[0]} {xyz[1]} {xyz[2]}')
        origin.setAttribute('rpy', f'{rpy[0]} {rpy[1]} {rpy[2]}')
        return origin

    def get_inertia(self, g_shape, size, m):
        inertia = self._tag('inertia')

        if g_shape == 'cylinder':
            # TODO: Check which axis defines the height
            l = size[0]
            r = size[1]
            ixx = (m/12)*(l**2)
            iyy = 0
            izz = (m/12)*(l**2)
            ixy = 0
            ixz = 0
            iyz = 0
        elif g_shape == 'box':
            x = size[0]
            y = size[1]
            z = size[2]
            ixx = (m / 12) * (y ** 2 + z ** 2)
            iyy = (m / 12) * (x ** 2 + z ** 2)
            izz = (m / 12) * (x ** 2 + y ** 2)
            ixy = 0
            ixz = 0
            iyz = 0

        inertia.setAttribute('ixx', ixx)
        inertia.setAttribute('iyy', iyy)
        inertia.setAttribute('izz', izz)
        inertia.setAttribute('ixy', ixy)
        inertia.setAttribute('ixz', ixz)
        inertia.setAttribute('iyz', iyz)

        return inertia

    def _tag(self, tag_type):  # Create a simple tag from self.root.CreateElement
        tag = self.root.createElement(tag_type)
        return tag

    def xml_compile(self):
        print(f'Compiling XML')

        # Appending Links as Child
        for i in range(self.num_links):
            self.xml.appendChild(self.links[i])

        for i in range(self.num_joints):
            self.xml.appendChild(self.joints[i])

        self._write_to_file('urdf_gen.urdf')

    def _write_to_file(self, filename):
        xml_str = self.root.toprettyxml(indent="\t")
        save_path_file = filename
        with open(save_path_file, "w") as f:
            f.write(xml_str)


r1 = RobotURDF('Citric')
# r1.create_link('RightArm', 'box', (1, 1, 1), 0.1)
r1.create_link('LeftArm', 'cylinder', (1, 0.5), 0.1)
# r1.create_joint('torso', 'continuous', 'RightArm', 'LeftArm')
r1.xml_compile()















