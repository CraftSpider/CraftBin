"""
    Program to read in REL files.
    Refer to http://wiki.tockdom.com/wiki/REL_(File_Format) for more info.

    author: CraftSpider
"""

from typing import Tuple, List, Iterator
from enum import Enum
import pathlib, os


class RelType(Enum):
    R_PPC_NONE = 0
    R_PPC_ADDR32 = 1
    R_PPC_ADDR24 = 2
    R_PPC_ADDR16 = 3
    R_PPC_ADDR16_LO = 4
    R_PPC_ADDR16_HI = 5
    R_PPC_ADDR16_HA = 6
    R_PPC_ADDR14 = 7  # Also 8 and 9
    R_PPC_REL24 = 10
    R_PPC_REL14 = 11  # Also 12 and 13
    R_RVL_NONE = 201
    R_RVL_SECT = 202
    R_RVL_STOP = 203


def hconv(item):
    if isinstance(item, int):
        item = format(item, 'X')
        if item[0] == "-":
            item = "-0x" + item[1:]
        else:
            item = "0x" + item
        return item
    elif isinstance(item, (list, tuple)):
        out = []
        for j in item:
            out.append(hconv(j))
        if isinstance(item, list):
            return str(out)
        elif isinstance(item, tuple):
            return str(tuple(out))
    else:
        hconverter = getattr(item, "__hconv__", None)
        if hconverter:
            item = hconverter()
        return str(item)


def hprint(*args, sep=' ', end='\n', file=None):
    out = []
    for item in args:
        out.append(hconv(item))
    print(*out, sep=sep, end=end, file=file)


class DOL:

    def __init__(self, filename):
        self.filename = filename

        with open(filename, "br") as file:

            self.text_offsets = []
            for _ in range(7):
                self.text_offsets.append(b2d(file.read(4)))
            self.data_offsets = []
            for _ in range(11):
                self.data_offsets.append(b2d(file.read(4)))
            self.text_addresses = []
            for _ in range(7):
                self.text_addresses.append(b2d(file.read(4)))
            self.data_addresses = []
            for _ in range(11):
                self.data_addresses.append(b2d(file.read(4)))
            self.text_sizes = []
            for _ in range(7):
                self.text_sizes.append(b2d(file.read(4)))
            self.data_sizes = []
            for _ in range(11):
                self.data_sizes.append(b2d(file.read(4)))
            self.bss_address = b2d(file.read(4))
            self.bss_size = b2d(file.read(4))
            self.entry_address = b2d(file.read(4))

    def dump_all(self):
        out = "Header:\n"
        out += "  Text Offsets: " + hconv(self.text_offsets) + "\n"
        out += "  Text Addresses: " + hconv(self.text_addresses) + "\n"
        out += "  Text Sizes: " + hconv(self.text_sizes) + "\n"
        out += "  Data Offsets: " + hconv(self.data_offsets) + "\n"
        out += "  Data Addresses: " + hconv(self.data_addresses) + "\n"
        out += "  Data Sizes: " + hconv(self.data_sizes) + "\n"
        out += "  BSS Address: " + hconv(self.bss_address) + "\n"
        out += "  BSS Size: " + hconv(self.bss_size) + "\n"
        out += "  Entry Address: " + hconv(self.entry_address) + "\n"
        return out


class REL:

    imps: List['Imp']
    sections: List['Section']

    def __init__(self, filename):
        self.filename = filename

        with open(filename, "br") as file:
            # Read in the header
            self.id = b2d(file.read(4))
            self.next_module = b2d(file.read(4))
            self.prev_module = b2d(file.read(4))
            self.num_sections = b2d(file.read(4))
            self.section_offset = b2d(file.read(4))
            self.name_offset = b2d(file.read(4))  # Figure out what this is relative to
            self.name_size = b2d(file.read(4))
            self.version = b2d(file.read(4))
            self.bss_size = b2d(file.read(4))
            self.rel_offset = b2d(file.read(4))
            self.imp_offset = b2d(file.read(4))
            self.imp_size = b2d(file.read(4))
            self.prolog_rel = b2d(file.read(1))  # Section which self.prolog is relative to
            self.epilog_rel = b2d(file.read(1))  # Section which self.epilog is relative to
            self.unresolved_rel = b2d(file.read(1))  # Section which self.unresolved is relative to
            file.read(1)  # Skip padding
            self.prolog = b2d(file.read(4))  # Offset to start of prolog function
            self.epilog = b2d(file.read(4))  # Offset to start of epilog function
            self.unresolved = b2d(file.read(4))  # Offset to start of unresolved function
            if self.version >= 2:
                self.align = b2d(file.read(4))
                self.bss_align = b2d(file.read(4))
            else:
                self.align = None
                self.bss_align = None
            if self.version >= 3:
                self.fix_size = b2d(file.read(4))
            else:
                self.fix_size = None
            self.header_size = file.tell()

            # Now we read in the section info
            file.seek(self.section_offset)
            self.sections = []
            for j in range(self.num_sections):
                section = file.read(4)
                gen = bits(section)
                exec = next(gen)  # Furthest right
                i, offset = 1, 0
                for bit in gen:  # everything else
                    offset += bit * (2 ** i)
                    i += 1
                length = b2d(file.read(4))
                self.sections.append(Section(j, offset, exec, length))

            # Read in imp table
            file.seek(self.imp_offset)
            self.imps = []
            for _ in range(self.imp_size // 8):
                module_id = b2d(file.read(4))
                offset = b2d(file.read(4))  # Relative to start of file
                self.imps.append(Imp(module_id, offset))

            # Read in the relocation instructions
            for imp in self.imps:
                file.seek(imp.offset)
                rel_type = RelType.R_RVL_NONE
                while rel_type != RelType.R_RVL_STOP:
                    position = file.tell()
                    prev_offset = b2d(file.read(2))
                    rel_type = RelType(b2d(file.read(1)))
                    section = self.sections[b2d(file.read(1))]
                    offset = b2d(file.read(4))  # Relative to start of section
                    imp.add_reloc(Reloc(imp, position, prev_offset, rel_type, section, offset))

    def used_sections(self):
        used_secs = set()
        for imp in self.imps:
            for rel in imp.instructions:
                used_secs.add(rel.dest_section.id)
        return used_secs

    def section_ranges(self):
        used_secs = self.used_sections()
        read = [(0x0, self.header_size)]
        for section in filter(lambda x: x.module in used_secs, self.sections):
            read.append(section.range())
        read.append((self.rel_offset, self.imp_offset + self.imp_size))
        return sorted(read)

    def compile(self) -> bytes:
        out = b''
        out += bytes([0, self.id])  # Add ID
        out += b'\0\0\0\0'  # Add empty next link
        out += b'\0\0\0\0'  # Add empty prev link
        out += bytes([0, self.num_sections])  # Add section count
        out += bytes([self.section_offset])  # Add section offset
        return out

    def dump_header(self):
        out = "REL Header:\n"
        out += "  ID: " + str(self.id) + "\n"
        out += "  Version: " + str(self.version) + "\n"
        out += "  Prev Module: " + hconv(self.prev_module) + "\n"
        out += "  Next Module: " + hconv(self.next_module) + "\n"
        out += "  Name Offset: " + hconv(self.name_offset) + "\n"
        out += "  Name Size: " + hconv(self.name_size) + "\n"
        out += "  .bss Size: " + hconv(self.bss_size) + "\n"
        out += "  Num Sections: " + str(self.num_sections) + "\n"
        out += "  Sections Start: " + hconv(self.section_offset) + "\n"
        out += "  Sections Size: " + hconv(0x8 * self.num_sections) + "\n"
        out += "  REL Offset: " + hconv(self.rel_offset) + "\n"
        out += "  REL Size: " + hconv(self.imp_offset - self.rel_offset) + "\n"
        out += "  IMP Offset: " + hconv(self.imp_offset) + "\n"
        out += "  IMP Size: " + hconv(self.imp_size) + "\n"
        out += "  Prolog Index: " + str(self.prolog_rel) + "\n"
        out += "  Epilog Index: " + str(self.epilog_rel) + "\n"
        out += "  Unresolved Index: " + str(self.unresolved_rel) + "\n"
        out += "  Prolog Offset: " + hconv(self.prolog) + "\n"
        out += "  Epilog Offset: " + hconv(self.epilog) + "\n"
        out += "  Unresolved Offset: " + hconv(self.unresolved) + "\n"
        if self.version >= 2:
            out += "  Align: " + str(self.align) + "\n"
            out += "  .bss Align: " + str(self.bss_align) + "\n"
        if self.version >= 3:
            out += "  Fix Size: " + hconv(self.fix_size) + "\n"
        return out

    def dump_sections(self):
        out = "Section Table:\n"
        for section in self.sections:
            out += f"  Section {section.id}:\n"
            out += "    Offset: " + hconv(section.offset) + "\n"
            out += "    Length: " + hconv(section.length) + "\n"
            range = section.range()
            if range == (-1, -1):
                range = (0, 0)
            out += "    Range: " + hconv(range[0]) + " - " + hconv(range[1]) + "\n"
            out += "    Executable: " + hconv(section.exec) + "\n"
        return out

    def dump_imports(self):
        out = "Import Table:\n"
        for imp in self.imps:
            out += f"  Import:\n"
            out += "    Module: " + str(imp.module) + "\n"
            out += "    Offset: " + hconv(imp.offset) + "\n"
            out += "    Relocation Table:\n"
            for rel in imp.instructions:
                out += "      Relocation:\n"
                out += "        Position: " + hconv(rel.position) + "\n"
                out += "        Type: " + hconv(rel.type.name) + "\n"
                if rel.type == RelType.R_RVL_STOP:
                    continue
                elif rel.type == RelType.R_RVL_SECT:
                    out += "        Destination Section: " + str(rel.dest_section.id) + "\n"
                    continue
                out += "        Offset from Prev: " + hconv(rel.prev_offset) + "\n"
                out += "        Source: " + str(rel.src_section.id) + " " + hconv(rel.src_offset) + "\n"
                if rel.type == RelType.R_RVL_NONE:
                    continue
                out += "        Destination: " + str(rel.dest_section.id) + " " + hconv(rel.dest_offset) + "\n"
        return out

    def dump_all(self):
        # Build the file header data
        out = self.dump_header()
        out += "\n"
        # Build Section Table Data
        out += self.dump_sections()
        out += "\n"
        # Build Imp data and Rel Operations
        out += self.dump_imports()
        out += "\n"
        # Some notes about how to read the data
        out += "A pointer to -0x1 means that the real pointer is unknown"
        out += "Sections with non-zero length but zero offset have offset initialized at runtime.\n"
        return out


class Section:

    id: int
    offset: int
    exec: bool
    length: int

    def __init__(self, id, offset, exec, length):
        self.id = id
        self.offset = offset
        self.exec = bool(exec)
        self.length = length

    def __str__(self):
        return f"Section(id: {self.id}, offset: {self.offset}, exec: {self.exec}, len: {self.length})"

    def __repr__(self):
        return str(self)

    def __hconv__(self):
        return f"Section(id: {hconv(self.id)}, offset: {hconv(self.offset)}, exec: {hconv(self.exec)}, len: {hconv(self.length)})"

    @property
    def start(self) -> int:
        return self.offset

    @property
    def end(self) -> int:
        return self.offset + self.length

    def range(self) -> Tuple[int, int]:
        if self.offset == 0:
            return -1, -1
        return self.offset, self.offset + self.length


class Imp:

    __slots__ = ("module", "offset", "instructions", "_pointer", "_section")

    module: int
    offset: int
    instructions: List['Reloc']
    _pointer: int
    _section: Section

    def __init__(self, module, offset):
        self.module = module
        self.offset = offset
        self.instructions = []
        self._pointer = 0
        self._section = None

    def __str__(self):
        return f"Imp(module: {self.module}, offset: {self.offset})"

    def __hconv__(self):
        return f"Imp(module: {hconv(self.module)}, offset: {hconv(self.offset)})"

    def add_reloc(self, reloc):
        if reloc.type == RelType.R_RVL_SECT:
            self._pointer = reloc.src_section.offset
            self._section = reloc.src_section
        self._pointer += reloc.prev_offset
        reloc.dest_offset = self._pointer
        reloc.dest_section = self._section
        self.instructions.append(reloc)


class Reloc:

    imp: Imp
    position: int
    prev_offset: int
    type: RelType
    src_section: Section
    dest_section: Section
    dest_offset: int

    def __init__(self, imp, position, prev_offset, type, section, offset):
        self.imp = imp
        self.position = position  # Absolute position in file
        self.prev_offset = prev_offset  # Offset to previous operation
        self.relative_offset = offset  # Offset of source relative to start of section
        self.type = type
        self.dest_section = None
        self.dest_offset = -1  # absolute offset
        self.src_section = section

    def __str__(self):
        return f"Reloc(type: {self.type.name}, prev: {self.prev_offset}, section: {self.dest_section.id}, offset: {self.dest_offset})"

    def __repr__(self):
        return str(self)

    def __hconv__(self):
        return f"Reloc(prev: {hconv(self.prev_offset)}, type: {hconv(self.type.name)}, "\
               f"section: {hconv(self.dest_section.id)}, offset: {hconv(self.dest_offset)})"

    @property
    def src_offset(self) -> int:
        if self.imp.module == 0:
            return self.relative_offset
        if self.src_section.offset == 0:
            return -1
        return self.relative_offset + self.src_section.offset

    @src_offset.setter
    def src_offset(self, value) -> None:
        self.relative_offset = value - self.src_section.offset


def b2d(byte: bytes) -> int:
    return int.from_bytes(byte, "big")


def bits(bytes: bytes) -> Iterator[int]:
    for byte in reversed(bytes):
        for i in range(8):
            yield (byte >> i) & 1


def get_rel_names(root):
    rel_names = []
    for dir_name, dir_list, file_list in os.walk(root):
        for filename in file_list:
            if filename.endswith(".rel"):
                rel_names.append(dir_name + "/" + filename)
    return rel_names


def dump():

    rel_names = get_rel_names("root")

    pathlib.Path("dump").mkdir(parents=True, exist_ok=True)
    with open("dump/README", "w+") as file:
        out = "Author: CraftSpider\n\n"
        out += "Relocation source and destination are in the form '<SECTION> <POINTER>' where the pointer is relative "
        out += "to the beginning of the file.\n"
        out += "A pointer to -0x1 means that the real pointer is unknown\n"
        out += "Sections with non-zero length but zero offset have offset initialized at runtime.\n"
        file.write(out)
    with open("dump/DOL.dump", "w+") as file:
        dol = DOL("root/&&systemdata/Start.dol")
        file.write(dol.dump_all())

    for rel_name in rel_names:
        rel = REL(rel_name)
        human_name = rel_name.split(".")[1]
        pathlib.Path(f"dump/{human_name}").mkdir(parents=True, exist_ok=True)
        for part in ["header", "sections", "imports"]:
            with open(f"dump/{human_name}/{part}.dump", "w+") as file:
                file.write(getattr(rel, f"dump_{part}")())


def alter():
    root = input("Root Folder: ") or "."
    rel_names = get_rel_names(root)

    module = int(input("Module: ") or 2)
    offset = int(input("Offset: ") or "0x22BE0", 16)
    shift = int(input("Shift: ") or 1)

    rels = []
    for rel_name in rel_names:
        rel = REL(rel_name)
        rels.append(rel)

    for rel in rels:
        for imp in rel.imps:
            if imp.module == module:
                for reloc in imp.instructions:
                    if reloc.dest_offset > offset:
                        reloc.dest_offset += shift
                    if reloc.src_offset > offset:
                        reloc.src_offset += shift
        for section in rel.sections:
            if section.offset > 0 and (section.start <= offset <= section.end):
                section.length += shift

    for rel in rels:
        with open(rel.filename, "ba+") as file:
            data = rel.compile()
            # file.write(data)


if __name__ == "__main__":
    alter()

# So. The file is split into pieces. We have:
# File Start
# 0x000000 - 0x000048: Header
# ------
# 0x000048 - 0x0000D8: Section Table
# ------
# 0x0000D8 - 0x25471C: Section Data.
#  1: 0xD8 - 0x16D500
#  2: 0x16D500 - 0x16D504
#  3: 0x16D504 - 0x16D508
#  4: 0x16D508 - 0x1D4050
#  5: 0x1D4060 - 0x25471C
# 0x16E738: Music IDs start
# 0x1E5298: Lighting data start
# 0x204E48: Theme IDs start
# 0x2075B0: Challenge Mode start
# 0x20B448: Story Mode and Difficulties start
# ------
# 0x25471C - 0x2DC774: Rel_Data/Rel_Table [List of Relocation operations]
# ------
# 0x2DC774 - 0x2DC7CC: Imp_Table
# File End

# REL instruction writes to id/offset destination, reads from current pointer.

# Debug controls:
# L+Start: open debug in-game
# L+B: Change whether on top or behind other windows
# L+A: Cycle Focus
