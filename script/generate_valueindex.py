#!/usr/bin/env python3
"""Convenience script to auto-generate ValueIndex Enums model from Z-Wave specs."""

import os
import re
from urllib.request import urlopen
from xml.etree.ElementTree import parse


def string_to_camel(word):
    """Convert a string to CamelCase."""
    return "".join(x.capitalize() or "_" for x in word.split("_"))


def string_to_upper_snake(word):
    """Convert string to (upper) SNAKE_CASE."""
    return re.sub("[^a-zA-Z0-9\n\.]", "_", word).upper()


def main() -> None:
    """Run main entrypoint."""
    final_str = '"""ValueIndexes for each CommandClass as Enum"""\n\n'
    final_str += "# WARNING: This code is auto generated from:\n"
    final_str += "# https://raw.githubusercontent.com/OpenZWave/open-zwave/master/config/Localization.xml\n\n\n"

    # parse xml from Open-ZWave to get all Value Indexes per CommandClass
    var_url = urlopen(
        "https://raw.githubusercontent.com/OpenZWave/open-zwave/master/config/Localization.xml"
    )
    xmldoc = parse(var_url)
    for item in xmldoc.getroot():
        if item.tag != "{https://github.com/OpenZWave/open-zwave}CommandClass":
            continue
        command_class_id = item.attrib["id"]
        command_class_label = item.find(
            "{https://github.com/OpenZWave/open-zwave}Label"
        ).text
        command_class_label = string_to_camel(
            command_class_label.replace("COMMAND_CLASS_", "")
        )
        # get all indexes
        values = item.findall("{https://github.com/OpenZWave/open-zwave}Value")
        if not values:
            continue
        # create code block for the enum
        final_str += f"class {command_class_label}ValueIndex(IntEnum):\n"
        final_str += f'    """Enum with all (known) Value indexes for the {command_class_label} CommandClass ({command_class_id})."""\n'
        for value in values:
            value_index = value.attrib["index"]
            value_label = value.find(
                "{https://github.com/OpenZWave/open-zwave}Label"
            ).text
            value_label = string_to_upper_snake(value_label)
            final_str += f"    {value_label} = {value_index}\n"
        # append some whitelines
        final_str += "\n\n"

    filename = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__), "..", "openzwavemqtt", "models", "value_index.py"
        )
    )
    with open(filename, "w") as file:
        file.write(final_str)


if __name__ == "__main__":
    main()
