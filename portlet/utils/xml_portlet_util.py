

class XMLPortletUtils:
    """
    Utility class for XML portlets
    """

    @staticmethod
    def get_jsp_view_candidates(xml_node) -> [str]:
        """
        Get the list of JSP init params from the XML content
        :param xml_node: Xml root node
        :return: List of JSP pages
        """
        jsp_init_params = []

        init_param_elements = xml_node.findall(".//init-param")
        for init_param_element in init_param_elements:
            value_element = init_param_element.find("value")
            if value_element is not None and value_element.text.endswith(".jsp"):
                init_param = {
                    "name": init_param_element.findtext("name"),
                    "value": value_element.text
                }
                jsp_init_params.append(value_element.text)

        return jsp_init_params
