from cast.application import Application, File

from portlet.sys_logging.system_logger import SystemLogger


class FileFinder:
    """
    This class is used to find files in the application
    """

    def __init__(self, application: Application):
        self._application = application

        # Other and utils
        self.logger = SystemLogger(__name__)

    def find_file_by_path(self, file_path: str) -> File or None:
        """
        Find a file by its path in the application
        :param file_path:  Path of the file to find
        :return:  File object
        """
        files_in_app = self._application.get_files()

        # Iterate over all files in the application and return the one with the matching path
        for file in files_in_app:
            if file.get_path() == file_path:
                return file

        self.logger.error("Could not find File Object with path [%s]." % file_path)
        return None
