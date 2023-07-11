from io import StringIO
import xml.etree.ElementTree as ET


class NsXml:
    """Non Sucking XML Parser"""

    @staticmethod
    def parse_file(file_path):
        """
        Parse the XML file and return the root element
        :param file_path:
        :return:
        """
        with open(file_path, 'r') as file:
            xml_content = file.read()
            root = NsXml.parse(xml_content)

        return root

    @staticmethod
    def parse(xml_content):
        """
        Parse the XML content and return the root element
        :param xml_content:
        :return:
        """
        # instead of ET.fromstring(xml)
        it = ET.iterparse(StringIO(xml_content))
        for _, el in it:
            _, _, el.tag = el.tag.rpartition('}')  # strip ns
        return it.root
