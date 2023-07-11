
from cast.application import Application, Object


class ObjectFinder:
    """
    Object Finder
    """

    def __init__(self, application: Application):
        self._application = application

    def find_objects_by_types(self, object_type: [str]) -> [Object]:
        """
        Find all objects of a given type in the application
        :param object_type: List of object types to find
        """
        objects = []

        # For each object type, get the list of objects
        for r_type in object_type:

            # Get the list of objects
            for target in self._application.objects().has_type(r_type):
                objects.append(target)

        return objects

