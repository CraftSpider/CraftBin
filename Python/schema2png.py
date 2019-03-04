
import PIL.Image as Image
import PIL.ImageDraw as ImageDraw
import sys
import copy
import json
import nbt.nbt as nbt

from pathlib import Path
from typing import List

DEFAULT_RESOURCE_DIR = Path("./assets")
DEFAULT_LINE_SIZE = 10

BASE_COLOR = "#FFFFFF"
BORDER_COLOR = "#000000"
HELP_MESSAGE = """Usage:
    schema2png.py [options] <filename>
Description:
    schema2png takes minecraft schematic files and converts them to PNG representations
Options:
    -k  --key      Include a key at the bottom of the image
    -c  --count    Include a block count at the bottom of the image
    --line=[num]   Number of layers per line in the output. Defaults to 10
    --resrc=[path] Path to the resource pack directory. Defaults to "./assets"
"""

IMAGE_BOUNDARY = 3
LAYER_BOUNDARY = 2
BLOCK_SIZE = 16


# Settings, filled in by argument parsing
line_size = DEFAULT_LINE_SIZE
resource_path = DEFAULT_RESOURCE_DIR


class ArgParser:

    def __init__(self, args: List[str]):
        self.source = args[0]
        args = args[1:]

        self.args = []
        self.flags = []
        self.options = {}

        for arg in args:
            if arg.startswith("--"):
                if "=" in arg:
                    pair = arg.split("=")
                    self.options[pair[0]] = pair[1]
                else:
                    self.flags.append(arg[2:])
            elif arg.startswith("-"):
                for char in arg[1:]:
                    self.flags.append(char)
            else:
                self.args.append(arg)

    def get_arg(self, pos):
        return self.args[pos]

    def has_flag(self, *, short=None, long=None):
        return (short in self.flags) or (long in self.flags)

    def has_option(self, name):
        return name in self.options

    def get_option(self, name, default=None):
        return self.options.get(name, default)


class Element:

    __slots__ = ("begin", "end", "faces")

    def __init__(self, data):
        self.begin = data["from"]
        self.end = data["to"]
        self.faces = copy.deepcopy(data["faces"])


class Model:

    __slots__ = ("namespace", "name", "_effective_data", "_raw_data", "parent", "textures", "ambient_occlusion",
                 "elements")

    MODELS = {}

    def __init__(self, namespace, name, data):
        self.namespace = namespace
        self.name = name
        self._raw_data = data
        self.parent = None
        if "parent" in data:
            self.parent = self.get_model(namespace, data["parent"])
        data = self._get_effective()

        self._effective_data = data
        self.ambient_occlusion = data.get("ambientocclusion", True)
        self.elements = data.get("elements", [])
        self.textures = data.get("textures", None)

    def __repr__(self):
        return f"Model(name: {self.name}, parent: {self.parent.name if self.parent else None})"

    def _get_effective(self):
        data = copy.deepcopy(self._raw_data)
        if self.parent is not None:
            par_data = copy.deepcopy(self.parent._effective_data)
            par_texs = par_data.get("textures", {})
            par_data.update(data)
            par_texs.update(data.get("textures", {}))
            par_data["textures"] = par_texs
            data = par_data
        return data

    def _resolve_texture(self, name):
        tex = self.textures.get(name, "")
        while tex.startswith("#"):
            tex = self.textures.get(tex[1:], "")
        return tex or None

    def inherits(self, name):
        if name == self.name:
            return True
        elif self.parent is None:
            return False
        else:
            return self.parent.inherits(name)

    def get_top(self, *, x=0, y=0, z=0):
        # TODO: Generate model, rotate XYZ, handle sides
        tex_base = resource_path / self.namespace / "textures"

        # Perform vector rotation to find new up side

        if self.inherits("block/cube"):
            tex = self._resolve_texture("up")
            if tex is None:
                return None
            return Image.open(tex_base / (self._resolve_texture("up") + ".png"))

        elif "all" in self.textures:
            tex_path = tex_base / f"{self.textures['all']}.png"
            return Image.open(tex_path)
        elif "texture" in self.textures:
            tex_path = tex_base / f"{self.textures['texture']}.png"
            return Image.open(tex_path)

    def get_sprite(self):
        return None

    @classmethod
    def get_model(cls, namespace, name):
        if name not in cls.MODELS:
            with open(resource_path / namespace / "models" / f"{name}.json") as file:
                data = json.load(file)
            cls.MODELS[name] = Model(namespace, name, data)
        return cls.MODELS[name]


def get_blockstate(namespace, b_id):
    if not hasattr(get_blockstate, "blockstates"):
        get_blockstate.blockstates = {}
    blockstates = get_blockstate.blockstates
    path = resource_path / namespace / "blockstates" / (b_id + ".json")
    if b_id not in blockstates:
        with open(path) as file:
            blockstates[path] = json.load(file)
    return blockstates[path]


def apply_datamap(namespace, b_id, data):
    if not hasattr(apply_datamap, "datamap"):
        with open(resource_path / "datamap.json") as file:
            apply_datamap.datamap = json.load(file)
    datamap = apply_datamap.datamap

    ns_data = datamap.get(namespace, None)
    if ns_data is None:
        return namespace, b_id, data

    block_data = ns_data.get(b_id, None)
    if block_data is None:
        return namespace, b_id, data

    tex = block_data.get("texture", None)
    if tex is not None:
        return "", tex, data

    map_data = block_data.get("data", None)
    if map_data is not None:
        ref_data = data
        data_bits = block_data.get("data_bits", None)
        if data_bits is not None:
            ref_data = data & data_bits
        new_name = map_data.get(str(ref_data), None)
        b_id = new_name
        return namespace, b_id, data

    return namespace, b_id, data


def get_texture(namespace, b_id, data):

    namespace, b_id, data = apply_datamap(namespace, b_id, data)

    if namespace == "":
        return Image.open(resource_path / f"{b_id}.png")

    blockstate = get_blockstate(namespace, b_id)

    # Parse get model from blockstate
    model = None
    x = None
    y = None
    z = None
    variants = blockstate.get("variants", None)
    if variants:
        variant = None
        if "normal" in variants:
            variant = variants["normal"]
        else:
            # TODO: Fix this hack
            first_name = next(iter(variants))
            if first_name.startswith("axis"):
                data = data >> 2
                if data == 0:
                    variant = variants["axis=y"]
                elif data == 1:
                    variant = variants["axis=z"]
                elif data == 2:
                    variant = variants["axis=x"]
                elif data == 3:
                    variant = variants["axis=none"]
            else:
                variant = variants[first_name]
        x = variant.get("x", 0)
        y = variant.get("y", 0)
        z = variant.get("z", 0)
        model = Model.get_model(namespace, "block/" + variant["model"])
    else:
        model = Model.get_model(namespace, "block/cube_all")

    img = model.get_top(x=x, y=y, z=z)
    if img is None:
        img = model.get_sprite()
    if img is None:
        return Image.open(resource_path / "null.png")
    else:
        return img


def draw_grid(img, size=BLOCK_SIZE):
    draw = ImageDraw.Draw(img)
    ef_size = size + 1

    for x in range(0, img.width, ef_size):
        for y in range(0, img.height, ef_size):
            draw.rectangle((x, y, x+ef_size, y+ef_size), outline=BORDER_COLOR)


def generate_base(schematic):
    print("Generating blueprint base")

    width = schematic["Width"].value
    height = schematic["Height"].value
    length = schematic["Length"].value

    ef_size = BLOCK_SIZE + 1

    # Calculate image sizes
    layer_width = ef_size*width
    layer_length = ef_size*length

    num_rows = ((height - 1) // line_size) + 1
    num_columns = height if num_rows == 1 else line_size

    img_width = (2 * IMAGE_BOUNDARY * ef_size) +\
                (num_columns * layer_width) +\
                ((num_columns - 1) * LAYER_BOUNDARY * ef_size) + 1

    img_height = (2 * IMAGE_BOUNDARY * ef_size) +\
                 (num_rows * layer_length) +\
                 ((num_rows - 1) * LAYER_BOUNDARY * ef_size) + 1

    img = Image.new("RGB", (img_width, img_height), BASE_COLOR)

    # Draw grid lines
    draw_grid(img)

    return img


def create_image(schematic, parser):
    print("Creating blueprint")

    img = generate_base(schematic)

    place_blocks(img, schematic)

    if parser.has_flag(short="k", long="key"):
        generate_key(schematic)
    if parser.has_flag(short="c", long="count"):
        generate_count(schematic)

    return img


def place_blocks(img, schematic):
    print("Placing blocks")

    width = schematic["Width"].value
    height = schematic["Height"].value
    length = schematic["Length"].value

    if "SchematicaMapping" not in schematic:
        print("MCEdit generated schematics not yet supported")
        sys.exit(1)
    map_tag = schematic["SchematicaMapping"]

    ef_size = BLOCK_SIZE + 1

    for h in range(height):
        print(f"Placing layer {h+1}")
        base_x = (IMAGE_BOUNDARY * ef_size) +\
                 (width * ef_size * (h % line_size)) +\
                 (LAYER_BOUNDARY * ef_size * (h % line_size))

        base_y = (IMAGE_BOUNDARY * ef_size) +\
                 (height * ef_size * (h // line_size)) +\
                 (LAYER_BOUNDARY * ef_size * (h // line_size))

        for x in range(width):
            for z in range(length):

                # Get block at position
                pos = (h * length + z) * width + x
                block = schematic["Blocks"][pos]
                data = schematic["Data"][pos]

                # Get texture for block
                name = "null"
                for tag_name in map_tag:
                    if map_tag[tag_name].value == block:
                        name = tag_name
                        break

                namespace, b_id = name.split(":")

                texture = get_texture(namespace, b_id, data)

                # Paste texture
                mask = None
                if texture.mode == "RGBA":
                    mask = texture.split()[3]
                paste_x = base_x + (x * ef_size) + 1
                paste_y = base_y + (z * ef_size) + 1
                img.paste(texture, (paste_x, paste_y), mask=mask)


def generate_key(schematic):
    print("Generating key")


def generate_count(schematic):
    print("Generating count")


def main():
    global line_size, resource_path

    parser = ArgParser(sys.argv)

    if len(parser.args) == 0:
        print(HELP_MESSAGE)
        return 1

    filename = Path(parser.args[0])
    schematic = nbt.NBTFile(filename)

    line_size = parser.get_option("line", DEFAULT_LINE_SIZE)
    resource_path = parser.get_option("resrc", DEFAULT_RESOURCE_DIR)

    if schematic.name != "Schematic":
        print("NBT file not recognized as a schematic")
        return 1

    img = create_image(schematic, parser)

    img.save("blueprint.png")


if __name__ == "__main__":
    sys.exit(main())