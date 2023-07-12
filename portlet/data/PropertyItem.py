
class PropertyItem:
    """
    PropertyItem class
    """

    def __init__(self, name, value):
        self.name = name
        self.value = value

    def get_name(self):
        return self.name

    def get_value(self):
        return self.value

    def __str__(self):
        return self.name + "=" + self.value