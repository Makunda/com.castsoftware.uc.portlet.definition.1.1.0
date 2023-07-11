from random import randint

from portlet.sys_logging.system_logger import SystemLogger
from portlet.type.base_portlet import BasePortlet
from cast.analysers import CustomObject

portlet_persistence_logger = SystemLogger("PortPersistence")

class PortPersistence:
    """
    This class is used to persist the portlets to the database
    """

    @staticmethod
    def persist_portlet(portlet: BasePortlet, parent_file=None):
        """
        Persist the portlet to the database
        :param parent_file:
        :param portlet: Portlet to persist
        :return: None
        """
        # Properties
        full_name = "%s/%s" % (portlet.get_file_path(), portlet.get_name())

        # Create the object for the portlet
        portlet_obj = CustomObject()
        portlet_obj.set_name(portlet.get_name())
        portlet_obj.set_fullname(full_name)
        portlet_obj.set_type(portlet.get_portlet_type_val())
        portlet_obj.set_guid("%s FileObject_GUID %s" % (portlet.get_file_path(), portlet_obj.fullname))

        try:
            # Set the parent file
            if parent_file is not None:
                portlet_obj.set_parent(parent_file)

                # Set the bookmark for the parent file
                base_bookmark = portlet.get_base_bookmark()

                # Set the bookmark if applicable
                if base_bookmark is not None:
                    bookmark = base_bookmark.to_bookmark(parent_file)
                    portlet_obj.save_position(bookmark)

        except Exception as e:
            portlet_persistence_logger.error(
                "Error while setting the parent for %s: %s" % (full_name, e))

        # Save the object
        portlet_obj.save()

        # Persist the portlet properties
        try:
            portlet_obj.save_property("PortletProperties.description", portlet.get_description_info())
        except Exception as e:
            portlet_persistence_logger.error("Error while saving the portlet properties for %s: %s" % (full_name, e))

        return portlet_obj

