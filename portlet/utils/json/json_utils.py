import json


class JsonUtils:
    """
     Json utils class
    """
    @staticmethod
    def load_json_file(file_path: str) -> dict:
        """
        Load a json file
        :param file_path: The path of the file to load
        :return: The json file
        """
        with open(file_path) as json_file:
            return json.load(json_file)

    @staticmethod
    def loads(json_string: str) -> dict:
        """
        Load a json string
        :param json_string: The json string to load
        :return: The json string
        """
        return json.loads(json_string)

    @staticmethod
    def save_json_file(file_path: str, json_data: dict):
        """
        Save a json file
        :param file_path: The path of the file to save
        :param json_data: The json data to save
        """
        with open(file_path, 'w') as outfile:
            json.dump(json_data, outfile)

    @staticmethod
    def dumps(obj) -> str:
        """
        Serialize an object to a JSON string
        :param obj: Object to serialize
        :return: JSON string
        """
        return json.dumps(obj)
