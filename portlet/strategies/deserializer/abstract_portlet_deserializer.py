import abc

from portlet.type.base_portlet import BasePortlet


class AbstractPortletDeserializer(abc.ABC):

    @abc.abstractmethod
    def deserialize_portlets(self, file_path) -> [BasePortlet]:
        """
        Deserialize the portlet and save it to the database
        :param file_path:  The path to the file that needs to be parsed
        :return:
        """
        pass