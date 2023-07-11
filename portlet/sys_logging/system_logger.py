from cast.analysers import log
import logging


# Class wrapping the cast sys_logging system cast.analysers.log

class SystemLogger(object):

    # Constructor of the class with a name
    def __init__(self, name, origin=None):
        self.name = name
        self.origin = origin

    def info(self, message):
        msg = "[" + self.name + "][INFO] : " + message

        log.info(msg)  # Log a message with a #Info# prefix for the analyzer
        logging.info(msg)

    def warning(self, message):
        msg = "[" + self.name + "][WARNING] : " + message
        log.warning(msg)  # Log a warning message with a #Warning# prefix
        logging.warning(msg)

    def error(self, message, exception=None):
        # Log a warning message with a #Error# prefix
        msg = "[" + self.name + "][ERROR] : " + message
        if exception:
            msg += " : Exception:  " + str(exception)

        log.warning(msg)
        logging.error(msg)

    def critical(self, message):
        msg = "[" + self.name + "][CRITICAL] : " + message
        log.warning(msg)
        logging.critical(msg)

    def debug(self, message):
        msg = "[" + self.name + "][DEBUG] " + message
        log.debug(msg)
        logging.debug(msg)
