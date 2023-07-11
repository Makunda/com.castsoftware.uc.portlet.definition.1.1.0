from cast.application import Bookmark


class BaseBookmark:
    """
    Base class for all bookmark types.
    """

    def __init__(self,
                 start_line: int,
                 start_column: int,
                 end_line: int,
                 end_column: int):
        self.start_line = start_line
        self.start_column = start_column
        self.end_line = end_line
        self.end_column = end_column

    def to_bookmark(self, file):
        """
        Convert the bookmark to a CAST Bookmark object
        :param file:  File object
        """
        return Bookmark(file, self.start_line, self.start_column, self.end_line, self.end_column)

    # Serialize the bookmark to a string
    def serialize(self):
        return {
            "start_line": self.start_line,
            "start_column": self.start_column,
            "end_line": self.end_line,
            "end_column": self.end_column
        }

    # Deserialize the bookmark from a string
    @staticmethod
    def deserialize(json_string):
        return BaseBookmark(json_string["start_line"],
                            json_string["start_column"],
                            json_string["end_line"],
                            json_string["end_column"])


