from cast.application import Application, CustomObject

from portlet.enumerations.portlet_enum import PortletType
from portlet.objects.file_finder import FileFinder
from portlet.sys_logging.system_logger import SystemLogger
from portlet.type.base_portlet import BasePortlet
from portlet.type.jsr168_portlet import JSR168Portlet
from portlet.type.jsr286_portlet import JSR286Portlet


class PortletMaterializer:
    """
    This class is used to materialize portlets in the application
    """

    def __init__(self, application: Application):
        self._logger = SystemLogger(__name__)
        self._application = application

        self._file_finder = FileFinder(application)

    def deserialize(self, file_content: str) -> [BasePortlet]:
        """
        Deserialize the file content and materialize the portlets in the application
        """

        # Deserialize the file content as Base portlets. Each line is a portlet
        base_portlets = []
        for line in file_content.splitlines():
            base_portlets.append((BasePortlet.deserialize(line), line))

        # Log the amount of portlets to materialize
        self._logger.info("Materializing [%s] portlets." % len(base_portlets))

        success, errors = 0, 0
        portlets = []
        # Based on the type, persist the portlet in the application
        for (base_portlet, content) in base_portlets:
            try:
                if base_portlet.get_portlet_type() == PortletType.JSR168:
                    portlets.append(self.materialize_jsr_168(content))
                elif base_portlet.get_portlet_type() == PortletType.JSR286:
                    portlets.append(self.materialize_jsr_286(content))
                elif base_portlet.get_portlet_type() == PortletType.JSR286:
                    portlets.append(self.materialize_ibm(content))
                else:
                    self._logger.error("Could not materialize portlet with type [%s]" % base_portlet.type)

                success += 1
            except Exception as e:
                self._logger.error("Could not materialize portlet with content [%s]" % content)
                self._logger.error(e)
                errors += 1

        # Log the result
        self._logger.info("Successfully materialized [%s] portlets. Failed operations [%s]." % (success, errors))

        # Return the list of custom objects
        return portlets

    def materialize_jsr_168(self, content: str) -> JSR168Portlet:
        """
        Materialize a JSR 168 portlet in the application
        :param content: The content of the portlet
        """
        # Log the deserialize operation
        self._logger.info("Deserializing JSR-168 portlet.")

        jsr_168_portlet = JSR168Portlet.deserialize(content)

        # Find parent file
        parent_file = self._file_finder.find_file_by_path(jsr_168_portlet.get_file_path())
        jsr_168_portlet.set_parent(parent_file)

        # Persist the portlet in the application
        return jsr_168_portlet

    def materialize_jsr_286(self, content: str) -> JSR286Portlet:
        """
        Materialize a JSR 286 portlet in the application
        :param application: The application to materialize the portlet in
        :param content: The content of the portlet
        """
        # Log the deserialize operation
        self._logger.info("Deserializing JSR-286 portlet.")

        jsr_286_portlet = JSR286Portlet.deserialize(content)

        # Find parent file
        parent_file = self._file_finder.find_file_by_path(jsr_286_portlet.get_file_path())
        jsr_286_portlet.set_parent(parent_file)

        # Persist the portlet in the application
        return jsr_286_portlet

    def materialize_ibm(self, content: str):
        """
        Materialize an IBM portlet in the application
        :param application: The application to materialize the portlet in
        :param content: The content of the portlet
        """
        self._logger.error("IBM portlets are not supported yet")
