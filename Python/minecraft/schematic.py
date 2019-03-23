"""
    Class to represent a minecraft schematic file, along with associated
    classes and helpers.
"""

import json
import pathlib
import nbt.nbt as nbt


class SchematicError(Exception):
    pass


class Schematic:

    __slots__ = ("nbt", "height", "width", "length", "id_map", "datamap")

    def __init__(self, file):

        if not isinstance(file, nbt.NBTFile):
            raise TypeError("Schematic file input must be an instance of NBTFile")
        if not file.name == "Schematic":
            raise SchematicError("Invalid NBT file, root tag not Schematic")
        self.nbt = file

        self.length = file["Length"].value
        self.width = file["Width"].value
        self.height = file["Height"].value
        if self.width == 0 or self.height == 0 or self.length == 0:
            raise SchematicError("0 size schematic. File may be corrupted")

        self.id_map = {}
        if "SchematicaMapping" in file:
            map_tag = file["SchematicaMapping"]
            for tag_name in map_tag:
                self.id_map[map_tag[tag_name].value] = tag_name
        elif "BlockIDs" in file:
            map_tag = file["BlockIDs"]
            for block_id in map_tag:
                self.id_map[block_id] = map_tag[block_id]
        else:
            raise SchematicError("Unrecognized Schematic ID mapping format (Are you using MCEdit-2 or Schematica?)")

        self.datamap = None

    def _apply_datamap(self, namespace, block, data):
        if self.datamap is None:
            return namespace, block, data

        ns_data = self.datamap.get(namespace, None)
        if ns_data is None:
            return namespace, block, data

        block_data = ns_data.get(block, None)
        if block_data is None:
            return namespace, block, data

        tex = block_data.get("texture", None)
        if tex is not None:
            return namespace, block, -1

        map_data = block_data.get("data", None)
        if map_data is not None:
            ref_data = data
            data_bits = block_data.get("data_bits", None)
            if data_bits is not None:
                ref_data = data & data_bits
            new_name = map_data.get(str(ref_data), None)
            block = new_name
            return namespace, block, data

        return namespace, block, data

    def load_datamap(self, filename):
        with open(filename) as file:
            self.datamap = json.load(file)

    def get_block(self, x, y, z):
        if 0 >= z > self.length or 0 >= x > self.width or 0 >= y > self.height:
            raise AttributeError("Cannot get block outside of schematic range")

        pos = (y * self.length + z) * self.width + x
        block = self.nbt["Blocks"][pos]
        data = self.nbt["Data"][pos]
        name = self.id_map.get(block, "null")

        namespace, block = name.split(":")
        namespace, block, data = self._apply_datamap(namespace, block, data)
        return namespace, block, data


def load_schematic(path):
    path = pathlib.Path(path)
    file = None
    if path.is_file():
        file = nbt.NBTFile(path)
    path = path.with_suffix(".schematic")
    if path.is_file():
        file = nbt.NBTFile(path)
    if file is not None:
        file = Schematic(file)
    return file
