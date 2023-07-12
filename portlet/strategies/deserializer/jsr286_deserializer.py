
from portlet.sys_logging.system_logger import SystemLogger
from portlet.strategies.deserializer.abstract_portlet_deserializer import AbstractPortletDeserializer
from portlet.type.base_bookmark import BaseBookmark
from portlet.type.base_portlet import BasePortlet
from portlet.type.jsr286_portlet import JSR286Portlet
from portlet.utils.regex.re_utils import ReUtils
from portlet.utils.xml.nsxml import NsXml


class JSR286Deserializer(AbstractPortletDeserializer):
    """
    Deserializes a JSR286 portlet and saves it to the database
    """

    _logger = SystemLogger("JSR286Deserializer")

    def deserialize_portlets(self, file_path) -> [BasePortlet]:
        """
        Deserialize the portlet and save it to the database
        :param file_path:  The path to the file that needs to be parsed
        :return:
        """

        self._logger.debug("Parsing portlet " + str(file_path) + " as a JSR286 portlet.")

        # Get file content
        with open(file_path, "r") as file:
            file_content = file.read()

        # Use the xml deserialization
        root = NsXml.parse_file(file_path)

        # Log the success and failure
        success = 0
        failure = 0

        # log the root element
        self._logger.debug("Root element: " + str(root))

        # Iterate over all the portlets
        portlets_created = []
        portlet_elements = root.findall(".//portlet")

        # Log the amount of portlets found, if there are none, return
        if len(portlet_elements) == 0:
            self._logger.warning("No portlets found in file. Nothing has been parsed.")
            return []

        self._logger.info("Found " + str(len(portlet_elements)) + " portlets in file " + str(file_path) + ".")

        it = 0
        # Get all the portlets elements in the file
        for portlet_elements in root.findall(".//portlet"):

            it += 1

            # Get the start and end line numbers
            start_line, end_line = ReUtils.find_tag_position(file_content, "portlet", it)

            try:
                # Parse the portlet and save it to the database
                portlet = JSR286Portlet.parse_portlet_definition(file_path, portlet_elements)
                portlet.set_bookmark(BaseBookmark(start_line, -1, end_line, -1))

                portlets_created.append(portlet)

                success += 1
            except Exception as e:
                self._logger.error("Could not parse portlet: " + str(e))
                self._logger.error("Reason: " + str(e))
                failure += 1

        self._logger.info(
            "Successfully parsed " + str(success) + " portlets. Failed to parse " + str(failure) + " portlets.")

        return portlets_created
