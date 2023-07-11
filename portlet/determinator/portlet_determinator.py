from portlet.enumerations.portlet_enum import PortletType


class PortletDeterminator:
    """
    Determines the type of portlet based on its XML content
    """

    @staticmethod
    def determine_portlet_type(xml_content):
        """
        Determine the type of portlet based on its XML content
        :param xml_content: Content to parse and determine the type of
        :return: PortletType or None if the type could not be determined or the XML content does not contain a portlet
        """
        if "<portlet-app-def" in xml_content:
            return PortletType.IBM
        elif "<portlet-app" in xml_content:
            return PortletType.JSR286
        elif "<portlet-definition" in xml_content:
            return PortletType.JSR168
        elif "portlet" in xml_content:
            return PortletType.OTHER
        else:
            return None
