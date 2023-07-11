from portlet.determinator.portlet_determinator import PortletDeterminator
from portlet.enumerations.portlet_enum import PortletType

from portlet.sys_logging.system_logger import SystemLogger
from portlet.strategies.deserializer.jsr286_deserializer import JSR286Deserializer
from portlet.type.base_portlet import BasePortlet

portletLogger = SystemLogger("PortletStrategy")


class PortletStrategy:
    """
    Deserializes a portlet based on its type and saves it to the database
    """

    @staticmethod
    def deserialize_portlet(file_path: str) -> [BasePortlet]:
        """
        Use the portlet determinator to get the type, then based on the type save it
        :param file_path: Path to the file that needs to be parsed
        :return: The list of objects that have been created
        """

        # Read the file
        try:
            with open(file_path, "r") as f:
                xml_content = f.read()
        except FileNotFoundError:
            portletLogger.error("Could not find file " + str(file_path) + ". Nothing has been parsed.")
            return []

        # Determine the type of the portlet if it exists in the file
        portlet_type = PortletDeterminator.determine_portlet_type(xml_content)

        portletLogger.debug("Found portlet type: " + str(portlet_type))

        # Parse the portlet based on the type on log it
        if portlet_type == PortletType.JSR286:
            portletLogger.info("A JSR 286 portlet has been detected. Parsing file: " + str(file_path) + ".")
            return JSR286Deserializer().deserialize_portlets(file_path)
        elif portlet_type == PortletType.JSR168:
            portletLogger.warning("A JSR 169 portlet has been detected. This type of portlet is not supported yet. File: " + str(file_path))
        elif portlet_type == PortletType.IBM:
            portletLogger.warning("An IBM portlet has been detected. This type of portlet is not supported yet. File: " + str(file_path))
        elif portlet_type == PortletType.GENERIC:
            portletLogger.warning("An other portlet has been detected. This type of portlet is not supported yet. File: " + str(file_path))
        else:
            portletLogger.error("Could not determine the type of portlet in " + str(file_path) + ". Nothing has been parsed.")
            return []
