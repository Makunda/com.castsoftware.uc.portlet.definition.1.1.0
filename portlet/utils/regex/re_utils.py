import xml.etree.ElementTree as ET

from portlet.sys_logging.system_logger import SystemLogger

LOGGER = SystemLogger("Regex utils Global Logger")


class ReUtils:

    @staticmethod
    def find_tag_position(xml_content: str, tag_name: str, occurrence_number: int) -> (int, int):
        try:
            start_line = None
            end_line = None
            open_tags = []
            found_index = 0

            lines = xml_content.split("\n")

            for line_num, line in enumerate(lines, 1):
                if ("<"+tag_name+">") in line:
                    if start_line is None:
                        # Start line of the element
                        found_index += 1
                        if found_index == occurrence_number:
                            start_line = line_num

                    # Track open tags
                    open_tags.append(tag_name)

                if ("</" + tag_name + ">") in line:
                    # Check if it's the closing tag of the current element
                    if open_tags and open_tags[-1] == tag_name:
                        open_tags.pop()

                        if len(open_tags) == 0 and found_index == occurrence_number:
                            # End line of the element
                            end_line = line_num
                            break

            # If the end line is not found, set it to the last line
            if end_line is None:
                start_line = 0
                end_line = len(lines) - 1

            LOGGER.info("Found tag " + tag_name + " at line " + str(start_line) + " and " + str(end_line))
            return start_line, end_line
        except Exception as e:
            LOGGER.error("Error while finding tag position: " + str(e))
            return 0, 0
