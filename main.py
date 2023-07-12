"""
Created on 6/27/2023

@author: Hugo JOBY - HJO
"""
import cast_upgrade_1_6_16 # @UnusedImport
import cast.analysers.ua
from cast.analysers import log, CustomObject

from definitions import INTERMEDIATE_FILE


from portlet.sys_logging.system_logger import SystemLogger
from portlet.strategies.portlet_stategy import PortletStrategy


class PortletAnalysisLevel(cast.analysers.ua.Extension):
    """
    This class is the entry point of the analyzer for the portlet definition
    """

    def __init__(self):
        self.NbCreatedPortlet = 0
        self.intermediateFile = None

        self.logger = SystemLogger("PortletDefinitionAnalyzer")

    def start_analysis(self):
        print("===============  Portlet Definition Analyzer : Beginning of Execution ===============")
        self.logger.info("===============  Portlet Definition Analyzer : Beginning of Execution ===============")

        # Open the file
        self.intermediateFile = self.get_intermediate_file(INTERMEDIATE_FILE)
        self.logger.debug("The shared results will be stored in: " + str(INTERMEDIATE_FILE))

        try:
            options = cast.analysers.get_ua_options()               #@UndefinedVariable dynamically added
            if not 'JavaPortlet' in options:
                # SQLScript language not selected : inactive
                self.active = False
            else:
                # options :
                self.extensions = options['JavaPortlet'].extensions
        except:
            pass

    def end_analysis(self):
        self.logger.info('Number of portlet objects created : ' + str(self.NbCreatedPortlet))
        self.logger.info("=============== Portlet Definition Analyzer : End of Execution ===============")

    def append_portlet_definition(self, portlet):
        """
        Append the portlet definition to the intermediate file
        :param portlet: The portlet to append
        :return:
        """
        self.intermediateFile.write(portlet.serialize() + "\n")

    def start_file(self, file):
        """
        Start the analysis of a file and process it if it is a portlet definition
        :param file:  The file to analyze
        :return: None
        """
        try:
            filepath = file.get_path()

            # Log the file processing
            log.info("[Java Portlets] Parsing file %s..." % filepath)
            self.logger.debug("Now Processing XML file: " + str(filepath))

            # Ignore the file if the
            if not filepath.endswith('.xml'):
                return

            # Ignore the file if it is a web.xml or a pom.xml
            if "web.xml" in filepath or "pom.xml" in filepath:
                return

            # If the file is
            if filepath.endswith('.xml'):

                # Process the file
                created_portlets = PortletStrategy.deserialize_portlet(filepath)
                self.NbCreatedPortlet += len(created_portlets)

                # If the len of the created portlets is 0, then the file is not a portlet definition, return
                if len(created_portlets) == 0:
                    return

                # Log amount of portlets created for this file
                self.logger.info("Created " + str(len(created_portlets)) + " portlets for file " + str(
                    filepath) + ". Total portlets created: " + str(self.NbCreatedPortlet))

                # Use the intermediate file to store the portlet definition and the java class called
                for portlet in created_portlets:
                    # Attach the parent file to the portlet
                    portlet.set_parent(file)

                    self.append_portlet_definition(portlet)
                    self.logger.debug("Portlet definition saved to intermediate file" + str(portlet.get_name()))

                    # Persist the portlet
                    # Create the portlet
                    portlet_obj = CustomObject()
                    portlet_obj.set_name(portlet.get_name())
                    portlet_obj.set_fullname(portlet.get_full_name())
                    portlet_obj.set_type(portlet.get_portlet_type().value)
                    portlet_obj.set_guid(portlet.get_guid())

                    portlet_obj.set_parent(portlet.get_parent())
                    portlet_obj.save()

                    try:
                        # Set the bookmark for the parent file
                        base_bookmark = portlet.get_base_bookmark()

                        # Set the bookmark if applicable
                        if base_bookmark is not None:
                            bookmark = base_bookmark.to_bookmark(portlet.get_parent())
                            portlet_obj.save_position(bookmark)

                    except Exception as e:
                        self.logger.error("Error while setting the parent for %s: %s" % (portlet.get_name(), e))

                    # Iterate over the list of properties and save them
                    for prop in portlet.get_properties():
                        portlet_obj.save_property(prop.get_name(), prop.get_value())


        except Exception as e:
            self.logger.error("Error while processing file: " + str(file.get_path()) + " Error: " + str(e))
