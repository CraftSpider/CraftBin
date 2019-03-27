
import PIL.Image as Image
import PIL.ImageDraw as ImageDraw
import PIL.ImageColor as Color
import sys
import utils.argparser as argparse
import minecraft.state as state
import minecraft.blockstate as blockstate
import minecraft.model as model
import minecraft.schematic as schema

from pathlib import Path


BASE_COLOR = Color.getrgb("white")
BORDER_COLOR = Color.getrgb("black")
HELP_MESSAGE = """Usage:
    schema2png.py [options] <input filename> [output filename]
Description:
    schema2png takes minecraft schematic files and converts them to PNG representations. Optionally, the output can 
    include a key of block names or a count of each block type required.
    
    Input filename does not need the `.schematic` on the end, though if two files with the same name exist, one without
    the extension and one with the extension, the file without the extension will be chosen.
Options:
    -k  --key            Include a key at the bottom of the image - Alpha/WIP
    -c  --count          Include a block count at the bottom of the image - Alpha/WIP
    --no-blueprint       Don't include the blueprint. If this flag is used, either -k or -c must be used
    --line=[num]         Number of layers per line in the output. Defaults to 10
    --resrc=[path]       Path to the resource pack directory. Defaults to "./assets"
    --img-bounds=[num]   Number of blocks between the edge of the image and the blueprint. Defaults to 3
    --layer-bounds=[num] Number of blocks between each layer of the blueprint. Defaults to 2
    --block-size=[num]   Texture size of the blocks. Defaults to 16, same as minecraft default texture pack
Examples:
    schema2png -kc --line=5
    Will generate a blueprint with a key and a block count, with 5 layers per line
    
    schema2png --block-size=32 --resrc=./faithful32/assets
    Will generate a blueprint with 32 pixel blocks, using textures from the faithful32 directory
    
    schema2png --layers-bounds=1 --img-bounds=0 
"""


# Settings, filled in by argument parsing
LINE_SIZE = 10
IMAGE_BOUNDARY = 3
LAYER_BOUNDARY = 2


def get_texture(namespace, block, data):
    config = state.get_config()
    if data == -1:
        return Image.open(config.resource_path / f"{block}.png")

    try:
        b_state = blockstate.Blockstate.get_blockstate(namespace, block)
    except FileNotFoundError:
        raise schema.SchematicError(f"Invalid block {namespace}:{block} with data {data}") from None

    # Parse get model from blockstate
    x = 0
    y = 0
    if b_state.is_variant():
        variant = b_state.get_variant(normal=None)
        if variant is None:
            if b_state.has_variable("axis"):
                data = data >> 2
                if data == 0:
                    variant = b_state.get_variant(axis="y")
                elif data == 1:
                    variant = b_state.get_variant(axis="x")
                elif data == 2:
                    variant = b_state.get_variant(axis="z")
                elif data == 3:
                    variant = b_state.get_variant(axis="none")
            else:
                variant = b_state.variants[next(iter(b_state.variants))]
        x = variant.x
        y = variant.y
        b_model = variant.model
    else:
        b_model = model.Model.get_model(namespace, "block/cube_all")

    img = b_model.get_top(x=x, y=y, z=0)
    if img is None:
        img = b_model.get_sprite()
    if img is None:
        return Image.open(config.resource_path / "null.png")
    else:
        return img


def draw_grid(img):
    config = state.get_config()
    draw = ImageDraw.Draw(img)

    for x in range(0, img.width, config.ef_size):
        for y in range(0, img.height, config.ef_size):
            draw.rectangle((x, y, x + config.ef_size, y + config.ef_size), outline=BORDER_COLOR)


def generate_grid(schematic):
    print("Generating blueprint grid")
    config = state.get_config()

    # Calculate image sizes
    layer_width = config.ef_size * schematic.width
    layer_length = config.ef_size * schematic.length

    num_rows = ((schematic.height - 1) // LINE_SIZE) + 1
    num_columns = schematic.height if num_rows == 1 else LINE_SIZE

    img_width = (2 * IMAGE_BOUNDARY * config.ef_size) +\
                (num_columns * layer_width) +\
                ((num_columns - 1) * LAYER_BOUNDARY * config.ef_size) + 1

    img_height = (2 * IMAGE_BOUNDARY * config.ef_size) +\
                 (num_rows * layer_length) +\
                 ((num_rows - 1) * LAYER_BOUNDARY * config.ef_size) + 1

    img = Image.new("RGB", (img_width, img_height), BASE_COLOR)

    # Draw grid lines
    draw_grid(img)

    return img


def generate_blueprint(schematic):
    print("Generating blueprint")
    config = state.get_config()

    img = generate_grid(schematic)

    for h in range(schematic.height):
        print(f"Placing layer {h+1}")
        base_x = (IMAGE_BOUNDARY * config.ef_size) +\
                 (schematic.width * config.ef_size * (h % LINE_SIZE)) +\
                 (LAYER_BOUNDARY * config.ef_size * (h % LINE_SIZE))

        base_y = (IMAGE_BOUNDARY * config.ef_size) +\
                 (schematic.height * config.ef_size * (h // LINE_SIZE)) +\
                 (LAYER_BOUNDARY * config.ef_size * (h // LINE_SIZE))

        for z in range(schematic.length):
            for x in range(schematic.width):

                # Get block at position
                namespace, block, data = schematic.get_block(x, h, z)
                texture = get_texture(namespace, block, data)

                # Paste texture
                mask = None
                if texture.mode == "RGBA":
                    mask = texture.split()[3]
                paste_x = base_x + (x * config.ef_size) + 1
                paste_y = base_y + (z * config.ef_size) + 1
                img.paste(texture, (paste_x, paste_y), mask=mask)

    return img


def generate_key(schematic):
    print("Generating key")

    # TODO: Generate names


def generate_count(schematic):
    print("Generating count")

    counts = {}

    for x in range(schematic.width):
        for y in range(schematic.height):
            for z in range(schematic.length):
                namespace, block, data = schematic.get_block(x, y, z)
                key = f"{namespace}:{block}"
                if key not in counts:
                    counts[key] = 0
                counts[key] += 1

    print(counts)

    # TODO: Generate image of correct size

    # TODO: Place blocks and names plus counts


def create_image(schematic, parser):
    print("Creating blueprint")

    no_print = parser.has_flag(long="no-blueprint")
    do_key = parser.has_flag(short="k", long="key")
    do_count = parser.has_flag(short="c", long="count")
    if no_print and not (do_key or do_count):
        raise SystemError("Cannot specify no-blueprint without either a key or a count")

    blueprint = None
    key = None
    count = None
    if not no_print:
        blueprint = generate_blueprint(schematic)
    if do_key:
        key = generate_key(schematic)
    if do_count:
        count = generate_count(schematic)

    return blueprint


def setup_globals(parser):
    global LINE_SIZE, IMAGE_BOUNDARY, LAYER_BOUNDARY
    LINE_SIZE = int(parser.get_option("line", LINE_SIZE))
    IMAGE_BOUNDARY = int(parser.get_option("img-bounds", IMAGE_BOUNDARY))
    LAYER_BOUNDARY = int(parser.get_option("layer-bounds", LAYER_BOUNDARY))

    config = state.get_config()
    resource = parser.get_option("resrc", None)
    if resource is not None:
        config.resource_path = Path(resource)
    block_size = parser.get_option("block_size", None)
    if block_size is not None:
        config.block_size = int(block_size)


def main():
    """
        The main function of the program. Performs little logic, but calls other functions in order:
        Parse input
        Setup global variables
        Load schematic
        Generate image
        Save image
    """
    parser = argparse.ArgParser(sys.argv)

    if len(parser.args) == 0:
        print(HELP_MESSAGE)
        return 1

    setup_globals(parser)

    schematic = schema.load_schematic(parser.get_arg(0))
    if schematic is None:
        print("Input file not found")
        return 1
    config = state.get_config()
    schematic.load_datamap(config.resource_path / "datamap.json")

    img = create_image(schematic, parser)
    img.save(parser.get_arg(1, None) or "blueprint.png")


if __name__ == "__main__":
    sys.exit(main())
