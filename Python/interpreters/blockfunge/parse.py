
import enum
import string

from . import types
from .enums import BlockType


NAME_TOKENS = string.ascii_letters + string.digits + "@#[]"


class ParseBlock:

    __slots__ = ("block", "name", "type")

    def __init__(self, block, name):
        self.block = block
        self.name = name
        if name.startswith("#"):
            self.type = BlockType.CLASS
        elif name.startswith("@"):
            self.type = BlockType.EXTERN
        else:
            self.type = BlockType.FUNCTION

    def __repr__(self):
        return f"ParseBlock(pos={self.block}, name={self.name}, type={self.type})"


def syntax_warn(message):
    print("Syntax Warning: " + message)


def syntax_error(message):
    print("Syntax Error: " + message)
    exit(1)


def read_block(arr, top, left):
    end = False
    right = left+1
    bottom = top+1
    while not end:
        char = arr[top][right]
        if char == '\\':
            end = True
        elif char != '-':
            return None
        else:
            right += 1
    end = False
    while not end:
        char = arr[bottom, left]
        if char == '\\':
            end = True
        elif char != '|':
            return None
        else:
            bottom += 1

    for i in range(top+1, bottom):
        char = arr[i][right]
        if char != '|':
            return None
    for i in range(left+1, right):
        char = arr[bottom][i]
        if char != '-':
            return None
    if arr[bottom][right] != '/':
        return None
    return top, left, bottom, right


def read_string(graph, pos):
    out = ""
    while True:
        if graph[pos] in NAME_TOKENS:
            pos = (pos[0], pos[1] - 1)
        else:
            break
    pos = (pos[0], pos[1] + 1)
    while True:
        if graph[pos] in NAME_TOKENS:
            out += graph[pos]
            pos = (pos[0], pos[1] + 1)
        else:
            break
    return out


def get_name(graph, pos):
    arrow_pos = None

    for i in range(pos[0], pos[2]+1):
        if graph[i, pos[1] - 1] == '>':
            arrow_pos = (i, pos[1] - 2)
            break
        elif graph[i, pos[3] + 1] == '<':
            arrow_pos = (i, pos[3] + 2)
            break
    for i in range(pos[1], pos[3]+1):
        if graph[pos[0] - 1, i] == 'v':
            arrow_pos = (pos[0] - 2, i)
            break
        elif graph[pos[2] + 1, i] == '^':
            arrow_pos = (pos[2] + 2, i)
            break

    if arrow_pos is None:
        return None

    return read_string(graph, arrow_pos)


def filter_block(blocks, block):
    for b in blocks:
        if b[0] < block[0] and b[1] < block[1] and b[2] > block[2] and b[3] > block[3]:
            return False
    return True


def parse_blocks(graph):
    blocks = []
    for i in range(len(graph)):
        line = graph[i]
        for j in range(len(line)):
            char = line[j]
            if char == '/':
                result = read_block(graph, i, j)
                if result is not None and filter_block(blocks, result):
                    blocks.append(result)

    out = []
    for block in blocks:
        name = get_name(graph, block)
        if name is None:
            syntax_error(f"All valid blocks must have a name. Block at ({block[0]+1}, {block[1]+1}) missing name")
        out.append(ParseBlock(block, name))

    return out


def parse_functions(graph, blocks):
    out = {}
    for block in blocks:
        if block.type == BlockType.FUNCTION:
            pos = block.block
            func_graph = types.Graph(pos[2] - pos[0] - 1, pos[3] - pos[1] - 1)

            for i in range(pos[0]+1, pos[2]):
                line = ""
                for j in range(pos[1]+1, pos[3]):
                    line += graph[i, j]
                func_graph.append(line)

            func = types.Function(block.name, func_graph)
            out[func.name] = func
    return out


def parse_classes(graph, blocks):
    return {}


def parse_externs(graph, blocks):
    return {}


def parse_graph(graph):
    blocks = parse_blocks(graph)
    functions = parse_functions(graph, blocks)
    classes = parse_classes(graph, blocks)
    externs = parse_externs(graph, blocks)
    return functions, classes, externs


def parse_file(file, main):
    graph = types.Graph()
    for line in file:
        graph.append(line)

    functions, classes, externs = parse_graph(graph)
    if main and "main" not in functions:
        syntax_error("Main file must have main function")

    return functions, classes, externs


if __name__ == "__main__":
    with open("test.hd") as file:
        print(parse_file(file, True))
