"""
    Program to generate an ASCII chart from input

    Author: CraftSpider
"""


def fix_data(data, meta):
    """
        Fixes input data in place for the chart function
    :param data: list of lists of anything, no special guarantees
    :param meta: calculated metadata to help with fixing
    """
    for row in data:
        for index in range(len(row)):
            if not isinstance(row[index], str):
                row[index] = str(row[index])
        if len(row) < meta["cols"]:
            row += ["" for _ in range(meta["cols"] - len(row))]


def build_meta(data, title):
    """
        Generate the number of rows and columns, minimum chart width, and minimum width of each column
    :param data: input chart data, in list of lists form
    :param title: title of the chart
    :return: Dictionary of chart metadata
    """
    if title is None:
        title = ""
    out = dict()
    out["cols"] = max_len(data)
    out["rows"] = len(data)
    out["width"] = len(title) + 4
    out["col_maxes"] = [0 for _ in range(out["cols"])]

    # determine real column maxes
    for row in data:
        for index in range(len(row)):
            if len(row[index]) > out["col_maxes"][index]:
                out["col_maxes"][index] = len(row[index])
    out["col_maxes"] = [x + 2 for x in out["col_maxes"]]  # add padding to each column

    # determine real table minimum width
    data_width = sum(out["col_maxes"]) + out["cols"] + 1
    if data_width > out["width"]:
        out["width"] = data_width

    print(out["col_maxes"])
    return out


def make_chart(data, title=None, bord="#"):  # TODO: add min_padding variable
    """
        Generates and returns an ASCII chart
    :param title: Title of the chart, or None for no title
    :param bord: Border character for the chart. Defaults to '#'
    :param data: List of lists of strings for the chart data.
    :return: Built ASCII chart
    """
    out = ""

    meta = build_meta(data, title)

    fix_data(data, meta)

    if title:
        # Title Header:
        #  First line
        out += bord*meta["width"] + "\n"
        #  Title Line
        title_gap = int((meta["width"] - (len(title) + 2)) / 2)
        out += bord + " "*title_gap + title + " "*(title_gap if meta["width"] % 2 else title_gap + 1) + bord + "\n"
        #  Second Line
        out += bord*meta["width"] + "\n"
    else:
        out += bord*meta["width"] + "\n"

    # Gaps
    gaps = [[0 for _ in range(meta["cols"])] for _ in range(meta["rows"])]
    for row_index in range(len(data)):
        for col_index in range(len(meta["col_maxes"])):
            col_max = meta["col_maxes"][col_index]
            gaps[row_index][col_index] = (col_max - len(data[row_index][col_index])) / 2

    for i in range(len(gaps)):
        out += bord
        gap_list = gaps[i]
        for j in range(len(gap_list)):
            gap = gap_list[j]
            if gap == int(gap):
                gap = int(gap)
                out += " "*gap + data[i][j] + " "*gap + bord
            else:
                gap = int(gap)
                out += " " * gap + data[i][j] + " " * (gap+1) + bord
        out += "\n"
        out += bord*meta["width"]
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

    border = input("What border style would you like? ") or "#"
    title = input("What title would you like? ") or None
    data_file = input("What file do you wish to read your values from? ") or "test.dat"
    with open(data_file) as file:
        data = [line.strip().split(";") for line in file]
        if len(data) and data[-1][-1] == "":
            del data[-1]
    chart = make_chart(data, title, border)
    print(chart)


if __name__ == "__main__":
    main()
