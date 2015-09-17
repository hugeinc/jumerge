import xml.etree.ElementTree as ET


class JUnitTestSuite(object):
    root = None

    def __init__(self, file_path, report_type):
        self.step_name = 'name'
        self.status = 'status'
        self.failure_message = 'message'
        self.split_char = ' | '

        tree = ET.parse(file_path)
        self.root = tree.getroot()

        self.add_new_title(report_type)

    def __str__(self):
        return ET.tostring(self.root, 'utf-8')

    def __repr__(self):
        return str(self)

    def add_new_title(self, test_type):
        for index, child in enumerate(self.root):
            class_name = self.split_char
            class_name += test_type
            class_name += self.split_char
            class_name += child.attrib.get('classname')
            self.root[index].attrib['classname'] = class_name

    def add_title(self, test_type, add_child):
        found = False
        for index, child in enumerate(self.root):

            if self.is_same_element(child, add_child):
                class_name = self.split_char + test_type + child.attrib.get('classname')
                self.root[index].attrib['classname'] = class_name
                found = True

        if not found:
            class_name = self.split_char
            class_name += test_type
            class_name += self.split_char
            class_name += add_child.attrib.get('classname')
            add_child.attrib['classname'] = class_name
            self.root.append(add_child)

    def is_same_element(self, node1, node2):
        if node1.attrib.get(self.step_name) == node2.attrib.get(self.step_name):
            if node1.attrib.get(self.status) == node2.attrib.get(self.status):

                if node1.attrib.get(self.status) != 'failed':
                    return True
                try:
                    failure1 = node1.find('failure')
                    if failure1 is not None:
                        failure1 = node1.find('error')
                    failure2 = node2.find('failure')
                    if failure2 is not None:
                        failure2 = node1.find('error')
                    if failure1.attrib.get(self.failure_message) == \
                            failure2.attrib.get(self.failure_message):
                        return True
                except:
                    return False
        return False

    def update_tree(self, file_path, report_type):
        tree = ET.parse(file_path)
        root = tree.getroot()

        for child in root:
            self.add_title(report_type, child)

    def update_status(self):
        count = {"errors": 0, "failures": 0, "skipped": 0, "tests": 0}
        for child in self.root:
            if child.find('failure') is not None:
                count["failures"] += 1
            elif child.find('error') is not None:
                count["errors"] += 1
            elif child.find('skipped') is not None:
                count["skipped"] += 1
            elif child.attrib.get('status') == 'passed':
                pass

        self.root.attrib["errors"] = str(count["errors"])
        self.root.attrib["failures"] = str(count["failures"])
        self.root.attrib["skipped"] = str(count["skipped"])
        pass