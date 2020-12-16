from xml.dom import minidom
import numpy as np
import os


class RobotURDF:

    def __init__(self, robot_name):
        self.root = minidom.Document()
        self.xml = self.root.createElement('root')
        self.root.appendChild(self.xml)
        self.num_links = 0
        self.num_joints = 0
        self.links = np.empty(self.num_links, dtype=object)
        self.joints = np.empty(self.num_joints, dtype=object)

    def create_link(self, name):
        l = self._tag('link', name)
        self.links = np.append(self.links, l)
        self.num_links = self.links.shape[0]

    def create_joint(self, name):
        j = self._tag('joint', name)
        self.joints = np.append(self.joints, j)
        self.num_joints = self.joints.shape[0]

    def _tag(self, tag_type, name):
        tag = self.root.createElement(tag_type)
        tag.setAttribute('name', name)
        return tag

    def xml_compile(self):
        print(f'Compiling XML')

        # Appending Links as Child
        for i in range(self.num_links):
            self.xml.appendChild(self.links[i])

        for i in range(self.num_joints):
            self.xml.appendChild(self.joints[i])

        self._write_to_file('roboturdf_gen.urdf')

    def _write_to_file(self, filename):
        xml_str = self.root.toprettyxml(indent="\t")
        save_path_file = filename
        with open(save_path_file, "w") as f:
            f.write(xml_str)


r1 = RobotURDF('Citric')
r1.create_link('RightArm')
r1.create_link('LeftArm')
r1.create_link('RightLeg')
r1.create_link('LeftLeg')
r1.xml_compile()














