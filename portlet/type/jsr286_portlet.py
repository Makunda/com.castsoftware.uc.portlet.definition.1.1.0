import cast
from cast.analysers import CustomObject

from portlet.enumerations.portlet_enum import PortletType
from portlet.sys_logging.system_logger import SystemLogger
from portlet.type.base_bookmark import BaseBookmark
from portlet.type.base_portlet import BasePortlet
from portlet.utils.dict_utils import DictUtils
from portlet.utils.json.json_utils import JsonUtils
from portlet.utils.xml_portlet_util import XMLPortletUtils

LOGGER = SystemLogger("JSR286Portlet Global Logger")

class JSR286Portlet(BasePortlet):
    """
    JSR286 Portlet
    """

    def __init__(self, file_path: str,
                 portlet_name: str,
                 portlet_classes: [str],
                 view_templates: [str],
                 resource_bundles: [str],
                 display_name: str = "",
                 supported_mime_types: [str] = None,
                 supported_portlet_modes: [str] = None,
                 title: str = "",
                 short_title: str = "",
                 keywords: str = ""):

        # Call to super class
        super().__init__(file_path,
                         portlet_name,
                         view_templates,
                         portlet_classes,
                         resource_bundles,
                         display_name,
                         portlet_type=PortletType.JSR286)

        self.supported_mime_types = supported_mime_types
        self.supported_portlet_modes = supported_portlet_modes
        self.title = title
        self.short_title = short_title
        self.keywords = keywords

    def get_title(self):
        return self.title

    def get_short_title(self):
        return self.short_title

    def get_keywords(self):
        return self.keywords

    def get_supported_mime_types(self):
        return self.supported_mime_types

    def get_supported_portlet_modes(self):
        return self.supported_portlet_modes

    def get_full_name(self):
        """
        Get the full name of the portlet
        """
        return "%s/%s" % (self.get_file_path(), self.get_name())

    def get_description_info(self):
        """
        Concatenate the description info from the portlet classes
        """
        description_info = "" + \
                           "<p><b>Supported Mimes Types:</b>{mimes}</p>\n".format(
                               mimes=self.get_supported_mime_types()) + \
                           "<p><b>Portlet Modes:</b> {portlet_modes}</p>".format(
                               portlet_modes=self.get_supported_portlet_modes()) + \
                           "<p><b>Keywords:</b> {keywords}</p>".format(keywords=self.get_keywords())
        return description_info

    def get_dict(self):
        return {
            "file_path": self.file_path,
            "portlet_name": self.get_name(),
            "display_name": self.get_display_name(),
            "view_templates": self.get_view_template_list(),
            "portlet_classes": self.get_portlet_class_list(),
            "resource_bundles": self.get_resource_bundles(),
            "description_info": self.get_description_info(),
            "supported_mime_types": self.supported_mime_types,
            "supported_portlet_modes": self.supported_portlet_modes,
            "title": self.title,
            "short_title": self.short_title,
            "keywords": self.keywords
        }

    @staticmethod
    def deserialize(json_string) -> 'JSR286Portlet':
        """
        Deserialize the JSON string to a JSR286Portlet object
        :param json_string: JSON string
        :return: JSR286Portlet object
        """
        data = JsonUtils.loads(json_string)

        portlet = JSR286Portlet(file_path=DictUtils.get_value(data, "file_path", ""),
                                portlet_name=DictUtils.get_value(data, "portlet_name", ""),
                                portlet_classes=DictUtils.get_value(data, "portlet_classes", []),
                                view_templates=DictUtils.get_value(data, "view_templates", []),
                                resource_bundles=DictUtils.get_value(data, "resource_bundles", []),
                                display_name=DictUtils.get_value(data, "display_name", ""),
                                supported_mime_types=DictUtils.get_value(data, "supported_mime_types", []),
                                supported_portlet_modes=DictUtils.get_value(data, "supported_portlet_modes", []),
                                title=DictUtils.get_value(data, "title", ""),
                                short_title=DictUtils.get_value(data, "short_title", ""),
                                keywords=DictUtils.get_value(data, "keywords", []))

        # if the portlet has a bookmark, add it to the dict
        if "bookmark" in data:
            portlet.set_bookmark(BaseBookmark.deserialize(data["bookmark"]))

        return portlet

    def persist_portlet(self, parent_file=None):
        """
        Persist the portlet to the database
        :param parent_file:
        :param portlet: Portlet to persist
        :return: None
        """
        # Assert that the parent is not None
        assert parent_file is not None

        # Properties
        full_name = "%s/%s" % (self.get_file_path(), self.get_name())

        # Create the object for the portlet
        # jobObject = cast.analysers.CustomObject()
        #                                     jobObject.set_name(jobName)
        #                                     jobObject.set_fullname("%s/%s" % (filepath, jobName))
        #                                     jobObject.set_type('ZEKEJob')
        #                                     jobObject.set_parent(file)
        #                                     jobObject.save()
        portlet_obj = cast.analysers.CustomObject()
        portlet_obj.set_name(self.get_name())
        portlet_obj.set_fullname(full_name)
        portlet_obj.set_type(self.get_portlet_type_val())
        portlet_obj.set_guid("%s FileObject_GUID %s" % (self.get_file_path(), portlet_obj.fullname))

        portlet_obj.set_parent(parent_file)
        # Save the object
        portlet_obj.save()

        # LOG OBJECT SAVED
        LOGGER.info("Portlet object saved: %s" % str(portlet_obj))

        try:
            # Set the bookmark for the parent file
            base_bookmark = self.get_base_bookmark()

            # Set the bookmark if applicable
            if base_bookmark is not None:
                bookmark = base_bookmark.to_bookmark(parent_file)
                portlet_obj.save_position(bookmark)

        except Exception as e:
            LOGGER.error("Error while setting the parent for %s: %s" % (full_name, e))

        # Persist the portlet properties
        try:
            portlet_obj.save_property("PortletProperties.display_name", self.get_display_name())
            portlet_obj.save_property("PortletProperties.title", self.get_title())
            portlet_obj.save_property("PortletProperties.short_title", self.get_short_title())
            portlet_obj.save_property("PortletProperties.description", self.get_description_info())
            portlet_obj.save_property("PortletProperties.keywords", self.get_keywords())
        except Exception as e:
            LOGGER.error("Error while saving the portlet properties for %s: %s" % (full_name, e))

        return portlet_obj

    @staticmethod
    def parse_portlet_definition(file_path: str, portlet_element) -> 'JSR286Portlet':
        """
        Parse the portlet definition
        :param file_path: Path to the portlet file
        :param portlet_element: XML node containing the portlet definition
        :return:
        """

        if portlet_element is None:
            raise ValueError("No 'portlet' element found")

        portlet_name = portlet_element.findtext('portlet-name', default="")
        display_name = portlet_element.findtext('display-name', default="")
        portlet_classes = portlet_element.findall('portlet-class')
        resource_bundles = portlet_element.findall('resource_bundles')
        view_templates = XMLPortletUtils.get_jsp_view_candidates(portlet_element)
        supported_mime_types = portlet_element.findall("supports/mime-type")
        supported_portlet_modes = portlet_element.findall("supports/portlet-mode")
        title = portlet_element.findtext("portlet-info/title", default="")
        short_title = portlet_element.findtext("portlet-info/short-title", default="")
        keywords = portlet_element.findtext("portlet-info/keywords", default="")

        supported_mime_types = [mime_type.text for mime_type in supported_mime_types]
        supported_portlet_modes = [portlet_mode.text for portlet_mode in supported_portlet_modes]

        # Create the portlet object
        return JSR286Portlet(file_path=file_path,
                             portlet_name=portlet_name,
                             portlet_classes=[portlet_class.text for portlet_class in portlet_classes],
                             view_templates=view_templates,
                             resource_bundles=resource_bundles,
                             display_name=display_name,
                             supported_mime_types=supported_mime_types,
                             supported_portlet_modes=supported_portlet_modes,
                             title=title,
                             short_title=short_title,
                             keywords=keywords)
