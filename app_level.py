'''
Created on 6/27/2023

@author: Hugo JOBY - HJO
'''
import cast
from cast.application import ApplicationLevelExtension, create_link
from cast.application import CustomObject # @UnresolvedImport

import definitions
from portlet.objects.file_finder import FileFinder
from portlet.objects.object_finder import ObjectFinder
from portlet.serialization.portlet_materializer import PortletMaterializer
from portlet.sys_logging.system_logger import SystemLogger


class LinkObject:
    def __init__(self, linkType, callerObject, calledObject):
        self.linkType = linkType
        self.callerObject = callerObject
        self.calledObject = calledObject


class ApplicationExtension(ApplicationLevelExtension):
    """
    This class is the entry point of the application level extension.
    """

    def __init__(self):
        # Runtime variables
        self.nbNewClasses = 0
        self.nbNewLinks = 0
        self.project = None

        # Loading the Java elements communicating with the portlets
        self.jvCls = {}
        self.jspPgs = {}

        self.linkObjects = []
        self.portlet_type = ["JSR286Portlet", "JSR168Portlet"]

        # Other and utils
        self.logger = SystemLogger(__name__)

    def start_application(self, application):
        self.logger.info("===============  Portlet Definition Analyzer : Beginning of Execution ===============")

    def find_portlet(self, application, full_name: str):
        """"
        Load the code of the Java elements that could potentially be called
        :param application: The application to load the Java elements from
        :param full_name: The fullname of the portlet
        """
        object_types = ObjectFinder(application).find_objects_by_types(self.portlet_type)

        for target in object_types:
            if target.get_fullname() == full_name:
                return target

        return None

    def load_java_classes_and_interfaces(self, application, target_type: [str]):
        """"
        Load the code of the Java elements that could potentially be called
        :param application: The application to load the Java elements from
        :param target_type: The type of the Java elements to load
        """
        object_types = ObjectFinder(application).find_objects_by_types(target_type)

        for target in object_types:
            target_fullname = target.get_fullname()
            target_type = target.get_type()
            # sys_logging.info(" - %s [%s]" % (target_name, target_type))
            self.jvCls[target_fullname] = target

    def load_jsp_pages(self, application, target_type: [str]):
        """"
        Load the code of the JSP pages that could potentially be called
        :param application: The application to load the JSP pages from
        :param target_type: The type of the JSP pages to load
        """
        object_types = ObjectFinder(application).find_objects_by_types(target_type)
        for target in object_types:
            target_fullname = target.get_fullname()
            target_type = target.get_type()
            # sys_logging.info(" - %s [%s]" % (target_name, target_type))
            self.jspPgs[target_fullname] = target

    def get_intermediate_file_content(self) -> str:
        """
        Deserialize the intermediate file containing the portlets and return the list of portlets
        :return: The list of portlets
        """
        self.logger.info(
            "[PORTLET DESERIALIZATION] Starting the deserialization of the file at '%s'." % definitions.INTERMEDIATE_FILE)
        with self.get_intermediate_file(definitions.INTERMEDIATE_FILE) as f:
            self.logger.info("[PORTLET DESERIALIZATION] File opened.")

            # If the file is empty, return an empty list and log it
            if f is None:
                self.logger.info("[PORTLET DESERIALIZATION] File is empty.")

            # Read the file entirely
            content = ""
            for line in f:
                content += line

            # Deserialize the file
            return content

    def load_data(self, application):
        """
            Load the object we need to link
        """
        # Load the code of the Java elements that could potentially be called
        self.logger.info("[JAVA LOAD] Loading Java elements ( classes, interfaces, etc. ) ...")
        self.load_java_classes_and_interfaces(application, ['JV_CLASS', 'JV_GENERIC_CLASS', 'GROUP_JAVA_CLASS', 'JV_INST_CLASS'])
        self.logger.info("[JAVA LOAD] Done. Found %d Java elements." % len(self.jvCls))

        # Load Jsp pages
        self.logger.info("[JSP LOAD] Loading JSP elements ( tags, servlets, pages ) ...")
        self.load_jsp_pages(application, ['JSP_TAG_LIB', 'JSP_BEAN', 'JSP_SERVLET', 'JSP_PROPERTIES_FILE'])
        self.logger.info("[JSP LOAD] Done. Found %d JSP elements." % len(self.jspPgs))

    def end_application_create_objects(self, application):
        """
        This method is called at the end of the application creation.
        :param application:  The application object
        :return:
        """
        self.logger.info("=============== Portlet Definition Analyzer : End Application Create Objects ===============")
        self.load_data(application)

        portlet_materializer = PortletMaterializer(application)

        # Find the parent file of the portlet
        for pro in application.get_projects():
            if pro.get_type() == 'JavaPortletCASTProject':
                self.logger.info("Found plugin project %s" % pro.get_fullname())
                self.project = pro
                break

        # Deserialize the list of portlet
        file_content = self.get_intermediate_file_content()
        portlets = portlet_materializer.deserialize(file_content)

        success = 0
        failure = 0

        # Create the list of links
        self.logger.info("[PORTLET CREATION] Starting the portlet creation phase.")
        for portlet in portlets:
            try:
                # Find portlet object with the same full name
                portlet_obj = self.find_portlet(application, portlet.get_full_name())
                if portlet_obj is None:
                    self.logger.error("Could not find portlet object with full name [%s]." % portlet.get_full_name())
                    continue

                # Link the portlet to the Java elements
                for class_element in portlet.get_portlet_class_list():
                    if class_element in self.jvCls.keys():
                        self.linkObjects.append(LinkObject('callLink', portlet_obj, self.jvCls[class_element]))
                    else:
                        self.logger.info("Could not find and link class [%s]." % class_element)

                # Link the portlet to the JSP elements
                for jsp_element in portlet.get_view_template_list():
                    if jsp_element in self.jspPgs.keys():
                        self.linkObjects.append(LinkObject('callLink', portlet_obj, self.jspPgs[jsp_element]))
                    else:
                        self.logger.info("Could not find and link JSP element [%s]." % jsp_element)

                # Link the portlet to the JSP elements
                for resource in portlet.get_resource_bundles():
                    if resource in self.jvCls.keys():
                        self.linkObjects.append(LinkObject('callLink', portlet_obj, self.jvCls[resource]))
                    else:
                        self.logger.info("Could not find and link class [%s]" % resource)

                self.nbNewClasses += 1
                success += 1
            except Exception as e:
                failure += 1
                self.logger.error('Could not persist portlet with name [%s]. Reason: %s.' % (portlet.get_name(), str(e)), e)

            # Every 5 portlets, log the amount of portlets successfully persisted and get the ratio of portlets successfully persisted
            if success % 5 == 0:
                self.logger.info(''
                                 'Successfully persisted %d portlets' % success)
                self.logger.info('Ratio of portlets successfully persisted: %d/%d' % (success, success + failure))

        self.logger.info("[PORTLET CREATION] End of the portlet creation phase. Portlets created: %d" % success)

        success_link = 0
        failure_link = 0

        # Create the links between the portlets and the Java elements
        self.logger.info("[LINK CREATION] Starting the link creation phase.")

        for linkObject in self.linkObjects:
            try:
                # Create the link between the portlet and the Java / JSP elements
                create_link(linkObject.linkType, linkObject.callerObject, linkObject.calledObject)
                self.nbNewLinks += 1
                success_link += 1
            except Exception as e:
                self.logger.error('Could not create link between [%s] and [%s].' % (
                    linkObject.callerObject, linkObject.calledObject), e)
                failure_link += 1

            # Every 5 links, log the amount of links successfully created and get the ratio of links successfully created
            if success_link % 5 == 0:
                self.logger.info(
                    'Ratio of links successfully created: %d/%d' % (success_link, success_link + failure_link))

        self.logger.info("[LINK CREATION] Done. New Links created: %d" % self.nbNewLinks)

    def end_application(self, application):
        """
        This method is called at the end of the application analysis.
        """
        self.logger.info("=============== Portlet Definition Analyzer : End Application ===============")