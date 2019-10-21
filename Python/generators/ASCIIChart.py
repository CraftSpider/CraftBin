"""
    Program to generate an ASCII chart from input

    Author: CraftSpider
"""


class Border:

    _REGISTRY = {}

    def __init__(self, base=None, horizontal=None, vertical=None, four_way=None, tl_corner=None, tr_corner=None,
                 bl_corner=None, br_corner=None, t_left=None, t_right=None, t_up=None, t_down=None):
        if base is None and (horizontal is None or vertical is None or four_way is None or tl_corner is None or
                             tr_corner is None or bl_corner is None or br_corner is None or t_left is None or
                             t_right is None or t_up is None or t_down is None):
            raise AttributeError("Base must be provided if not all element types are defined")
        self._base = base
        self._horizontal = horizontal
        self._vertical = vertical
        self._four_way = four_way
        self._tl_corner = tl_corner
        self._tr_corner = tr_corner
        self._bl_corner = bl_corner
        self._br_corner = br_corner
        self._t_up = t_up
        self._t_down = t_down
        self._t_left = t_left
        self._t_right = t_right

    @property
    def horizontal(self):
        return self._horizontal or self._base

    @property
    def vertical(self):
        return self._vertical or self._base

    @property
    def four_way(self):
        return self._four_way or self._base

    @property
    def tl_corner(self):
        return self._tl_corner or self._base

    @property
    def tr_corner(self):
        return self._tr_corner or self._base

    @property
    def bl_corner(self):
        return self._bl_corner or self._base

    @property
    def br_corner(self):
        return self._br_corner or self._base

    @property
    def t_up(self):
        return self._t_up or self._base

    @property
    def t_down(self):
        return self._t_down or self._base

    @property
    def t_left(self):
        return self._t_left or self._base

    @property
    def t_right(self):
        return self._t_right or self._base

    @classmethod
    def register(cls, name, **kwargs):
        if name in cls._REGISTRY:
            raise ValueError("Border type already registered")
        cls._REGISTRY[name] = Border(**kwargs)

    @classmethod
    def get_border(cls, name):
        if name not in cls._REGISTRY:
            raise ValueError("Invalid Border type")
        return cls._REGISTRY[name]


Border.register("pipes", horizontal="─", vertical="│", tl_corner="┌", tr_corner="┐", bl_corner="└", br_corner="┘",
                t_left="┤", t_right="├", t_up="┴", t_down="┬", four_way="┼")
Border.register("double-pipes", horizontal="═", vertical="║", tl_corner="╔", tr_corner="╗", bl_corner="╚",
                br_corner="╝", t_left="╣", t_right="╠", t_up="╩", t_down="╦", four_way="╬")
Border.register("simple", base="#", horizontal="-", vertical="|", tl_corner="/", tr_corner="\\", bl_corner="\\",
                br_corner="/", four_way="+")


def fix_data(data, meta):
    """
        Fixes input data in place for the chart function. Stringifies all data and makes sure all rows are of the
        same length.
    :param data: list of lists of anything, no special guarantees
    :param meta: calculated metadata to help with fixing
    """
    for row in data:
        for index, val in enumerate(row):
            if not isinstance(val, str):
                row[index] = str(val)
        if len(row) < meta["cols"]:
            row += ["" for _ in range(meta["cols"] - len(row))]


def build_meta(data, title, padding):
    """
        Generate the number of rows and columns, minimum chart width, and minimum width of each column
    :param data: input chart data, in list of lists form
    :param title: title of the chart
    :return: Dictionary of chart metadata
    """
    if title is None:
        title = ""
    out = dict()
    out["padding"] = padding
    out["cols"] = max_len(data)
    out["rows"] = len(data)
    out["width"] = len(title) + 4
    out["row_maxes"] = [0 for _ in range(out["rows"])]
    out["col_maxes"] = [0 for _ in range(out["cols"])]

    # determine real maxes
    for row in data:
        for index, value in enumerate(row):
            if value.count("\n") + 1 > out["row_maxes"][index]:
                out["row_maxes"][index] = value.count("\n") + 1
            if len(value) > out["col_maxes"][index]:
                out["col_maxes"][index] = len(value)
    out["col_maxes"] = [x + padding*2 for x in out["col_maxes"]]  # add padding to each column

    # determine real table minimum width
    data_width = sum(out["col_maxes"]) + out["cols"] + 1
    if data_width > out["width"]:
        out["width"] = data_width

    print(out)

    return out


def make_row(meta, bord, char):
    out = ""
    for item in meta["col_maxes"]:
        out += bord.horizontal*item
        out += char
    return out[:-1]


def make_chart(data, title=None, bord="#", padding=1):
    """
        Generates and returns an ASCII chart
    :param title: Title of the chart, or None for no title
    :param bord: Border character for the chart. Defaults to '#'
    :param data: List of lists of strings for the chart data.
    :param padding: How much padding to put around data values, at minimum
    :return: Built ASCII chart
    """
    if isinstance(bord, str):
        if len(bord) == 1:
            bord = Border(bord)
        else:
            bord = Border.get_border(bord)

    out = ""

    meta = build_meta(data, title, padding)

    fix_data(data, meta)

    if title:
        # Title Header:
        #  First line
        out += bord.tl_corner + bord.horizontal*(meta["width"]-2) + bord.tr_corner + "\n"
        #  Title Line
        title_gap = int((meta["width"] - (len(title) + 2)) / 2)
        out += bord.vertical + " "*title_gap + title + " "*(title_gap if meta["width"] % 2 else title_gap + 1) + bord.vertical + "\n"
        #  Second Line
        out += bord.t_right + make_row(meta, bord, bord.t_down) + bord.t_left + "\n"
    else:
        out += bord.tl_corner + make_row(meta, bord, bord.t_down) + bord.tr_corner + "\n"

    # Gaps
    gaps = [[0 for _ in range(meta["cols"])] for _ in range(meta["rows"])]
    for row_index in range(len(data)):
        for col_index in range(len(meta["col_maxes"])):
            col_max = meta["col_maxes"][col_index]
            gaps[row_index][col_index] = (col_max - len(data[row_index][col_index])) / 2

    for i, gap_list in enumerate(gaps):
        out += bord.vertical
        for j in range(len(gap_list)):
            gap = gap_list[j]
            if gap == int(gap):
                gap = int(gap)
                out += " "*gap + data[i][j] + " "*gap + bord.vertical
            else:
                gap = int(gap)
                out += " " * gap + data[i][j] + " " * (gap+1) + bord.vertical
        out += "\n"
        if i == meta["cols"] - 1:
            out += bord.bl_corner + make_row(meta, bord, bord.t_up) + bord.br_corner
        else:
            out += bord.t_right + make_row(meta, bord, bord.four_way) + bord.t_left
        out += "\n"

    return out


def max_len(list):
    """
        For a list of lists, return the length of the longest list.
    :param list: List to find max of. Type: List
    :return: Maximum length. Type: Int
    """
    out = 0
    for i in list:
        if len(i) > out:
            out = len(i)
    return out


def main():
    """
        Takes user input to generate the chart from.
    """

    border = input("What border style would you like? ") or "pipes"
    padding = input("How much padding would you like?") or 1
    title = input("What title would you like? ") or None
    data_file = input("What file do you wish to read your values from? ") or "test.dat"
    with open(data_file) as file:
        data = [line.strip().split(",") for line in file.read().split(";")]
        if len(data) and data[-1][-1] == "":
            del data[-1]
    chart = make_chart(data, title, border, padding)
    print(chart)


if __name__ == "__main__":
    main()
