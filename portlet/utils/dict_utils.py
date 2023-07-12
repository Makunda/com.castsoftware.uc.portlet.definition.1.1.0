

class DictUtils:

    @staticmethod
    def get_value(dictionary, key, default_value=""):
        if key in dictionary:
            return dictionary[key]
        else:
            return default_value