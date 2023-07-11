from cast.analysers import CustomObject

from portlet.enumerations.portlet_enum import PortletType
from portlet.sys_logging.system_logger import SystemLogger
from portlet.type.base_bookmark import BaseBookmark
from portlet.type.base_portlet import BasePortlet
from portlet.utils.json.json_utils import JsonUtils
from portlet.utils.xml_portlet_util import XMLPortletUtils

LOGGER = SystemLogger("JSR168Portlet Global Logger")

class JSR168Portlet(BasePortlet):
    """
    JSR168 Portlet
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
                         portlet_type=PortletType.JSR168)

        self.supported_mime_types = supported_mime_types
        self.supported_portlet_modes = supported_portlet_modes
        self.title = title
        self.short_title = short_title
        self.keywords = keywords

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

    def get_description_info(self):
        """
        Concatenate the description info from the portlet classes
        """
        description_info = "" + \
                           "<p><b>Supported Mimes Types:</b>{mimes}</p>\n".format(mimes=self.get_supported_mime_types()) +\
                           "<p><b>Portlet Modes:</b> {portlet_modes}</p>".format(portlet_modes=self.get_supported_portlet_modes()) + \
                           "<p><b>Keywords:</b> {keywords}</p>".format(keywords=self.get_keywords())
        return description_info

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

    @staticmethod
    def deserialize(json_string) -> 'JSR168Portlet':
        """
        Deserialize a JSON string to a portlet object
        :param json_string: JSON string
        :return: Portlet object
        """
        # convert the json string to a dict
        data = JsonUtils.loads(json_string)

        # create a portlet object from the dict
        portlet = JSR168Portlet(file_path=data["file_path"],
                                portlet_name=data["portlet_name"],
                                portlet_classes=data["portlet_classes"],
                                view_templates=data["view_templates"],
                                resource_bundles=data["resource_bundles"],
                                display_name=data["display_name"],
                                supported_mime_types=data["supported_mime_types"],
                                supported_portlet_modes=data["supported_portlet_modes"],
                                title=data["title"],
                                short_title=data["short_title"],
                                keywords=data["keywords"])

        # if the portlet has a bookmark, add it to the dict
        if "bookmark" in data:
            portlet.set_bookmark(BaseBookmark.deserialize(data["bookmark"]))

        # return the portlet object
        return portlet

    def persist_portlet(self, parent_file=None):
        """
        Persist the portlet to the database
        :param parent_file:
        :param portlet: Portlet to persist
        :return: None
        """
        # Properties
        full_name = "%s/%s" % (self.get_file_path(), self.get_name())

        # Create the object for the portlet
        portlet_obj = CustomObject()
        portlet_obj.set_name(self.get_name())
        portlet_obj.set_fullname(full_name)
        portlet_obj.set_type(self.get_portlet_type_val())
        portlet_obj.set_guid("%s FileObject_GUID %s" % (self.get_file_path(), portlet_obj.fullname))

        try:
            # Set the parent file
            if parent_file is not None:
                portlet_obj.set_parent(parent_file)

                # Set the bookmark for the parent file
                base_bookmark = self.get_base_bookmark()

                # Set the bookmark if applicable
                if base_bookmark is not None:
                    bookmark = base_bookmark.to_bookmark(parent_file)
                    portlet_obj.save_position(bookmark)

        except Exception as e:
            LOGGER.error("Error while setting the parent for %s: %s" % (full_name, e))

        # Save the object
        portlet_obj.save()

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
    def parse_portlet_definition(file_path: str, portlet_element):
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
        return JSR168Portlet(file_path=file_path,
                             portlet_name=portlet_name,
                             portlet_classes=[portlet_class.text for portlet_class in portlet_classes],
                             view_templates=view_templates,
                             resource_bundles=[resource_bundle.text for resource_bundle in resource_bundles],
                             display_name=display_name,
                             supported_mime_types=supported_mime_types,
                             supported_portlet_modes=supported_portlet_modes,
                             title=title,
                             short_title=short_title,
                             keywords=keywords)
