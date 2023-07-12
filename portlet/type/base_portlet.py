import json

from cast.application import File

from portlet.data.PropertyItem import PropertyItem
from portlet.enumerations.portlet_enum import PortletType
from portlet.type.base_bookmark import BaseBookmark


class BasePortlet:
    """
    Base class for all portlets. This class is abstract and should not be instantiated directly.
    """

    def __init__(self,
                 file_path: str,
                 portlet_name: str,
                 view_templates: [str],
                 portlet_classes: [str],
                 resource_bundles: [str],
                 display_name: str = "",
                 description_info: str = "",
                 portlet_type: PortletType = PortletType.GENERIC):

        if portlet_classes is None:
            portlet_classes = []
        if view_templates is None:
            view_templates = []

        self.file_path = file_path
        self.portlet_name = portlet_name
        self.display_name = display_name
        self.view_templates = view_templates
        self.portlet_classes = portlet_classes
        self.resource_bundles = resource_bundles
        self.description_info = description_info

        # Type of the portlet
        self.portlet_type = portlet_type

        # Parent Object
        self.parent = None
        self.bookmark = None

    def get_guid(self):
        """
        Get the guid of the portlet
        """
        return "%s FileObject_GUID %s" % (self.get_file_path(), self.get_full_name())

    def get_portlet_type(self):
        return self.portlet_type

    def get_portlet_type_val(self):
        return self.portlet_type.value

    def get_file_path(self):
        return self.file_path

    def get_name(self):
        return self.portlet_name

    def get_display_name(self):
        return self.display_name

    def get_resource_bundles(self):
        return self.resource_bundles

    def get_view_template_list(self) -> [str]:
        return self.view_templates

    def get_portlet_class_list(self) -> [str]:
        return self.portlet_classes

    def get_description_info(self):
        return self.description_info

    def get_base_bookmark(self) -> BaseBookmark or None:
        return self.bookmark

    def set_parent(self, parent):
        self.parent = parent

    def get_parent(self) -> File:
        return self.parent

    def get_full_name(self):
        """
        Get the full name of the portlet
        """
        return "%s/%s" % (self.get_file_path(), self.get_name())

    def set_bookmark(self, bookmark: BaseBookmark):
        """
        Set the bookmark for the portlet
        :param bookmark: Bookmark object
        """
        self.bookmark = bookmark

    def get_properties(self):
        """
        Get the properties for the portlet
        :return: Dict of properties
        """
        return [
            PropertyItem("PortletProperties.description", self.get_description_info()),
        ]

    def serialize(self):
        """
        Serialize the portlet to a JSON string
        :return:  JSON string
        """
        data = {
            "portlet_type": self.get_portlet_type().value,
            "file_path": self.file_path,
            "portlet_name": self.get_name(),
            "display_name": self.get_display_name(),
            "view_templates": self.get_view_template_list(),
            "portlet_classes": self.get_portlet_class_list(),
            "resource_bundles": self.get_resource_bundles(),
            "description_info": self.get_description_info()
        }

        # if the portlet has a bookmark, add it to the dict
        if self.bookmark is not None:
            data["bookmark"] = self.bookmark.serialize()

        # convert the dict to a json string
        return json.dumps(data)

    @staticmethod
    def deserialize(json_string):
        """
        Deserialize a JSON string to a portlet object
        :param json_string: JSON string
        :return: Portlet object
        """
        # convert the json string to a dict
        data = json.loads(json_string)

        # create a portlet object from the dict
        portlet = BasePortlet(
            file_path=data.get("file_path"),
            portlet_name=data.get("portlet_name"),
            display_name=data.get("display_name"),
            view_templates=data.get("view_templates"),
            portlet_classes=data.get("portlet_classes"),
            resource_bundles=data.get("resource_bundles"),
            description_info=data.get("description_info"),
            portlet_type=PortletType.get_portlet_type(data.get("portlet_type"))
        )

        # if the portlet has a bookmark, add it to the portlet
        if "bookmark" in data:
            portlet.set_bookmark(BaseBookmark.deserialize(data["bookmark"]))

        return portlet

    def persist_portlet(self):
        """
        Persist the portlet to the database
        """
        pass
