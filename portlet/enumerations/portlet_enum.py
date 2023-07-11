from enum import Enum


class PortletType(Enum):
    GENERIC = "GENERIC"
    JSR168 = "JSR168Portlet"
    JSR286 = "JSR286Portlet"
    IBM = "IBM"
    OTHER = "Other"

    @staticmethod
    def get_portlet_type(string: str):
        if string == "GENERIC":
            return PortletType.GENERIC
        elif string == "JSR168Portlet":
            return PortletType.JSR168
        elif string == "JSR286Portlet":
            return PortletType.JSR286
        elif string == "IBM":
            return PortletType.IBM
        else:
            return PortletType.OTHER
