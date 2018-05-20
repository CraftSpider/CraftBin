"""
    Program to generate an ASCII chart from input

    Author: CraftSpider
"""

from utils import file_readers as fr


def make_chart(data, title="Data Table", bord="#"):
    """
        Generates and returns an ASCII list
    :param title:
    :param bord:
    :param data:
    :return:
    """
    out = ""

    # Determine the maximum width of the chart and the maximum length in each data field
    maxWidth = len(title) + 4
    maxVars = [0 for i in range(maxLen(data))]
    maxCols = len(maxVars)
    maxRows = len(data)
    for i in data:
        for j in range(len(i)):
            if len(i[j]) > maxVars[j]:
                maxVars[j] = len(i[j])
        i = "   ".join(i)
        if len(i) + 2 > maxWidth:
            maxWidth = len(i) + 4

    # First line
    out += bord*maxWidth + "\n"

    # Title Line
    titleGap = int((maxWidth - (len(title) + 2)) / 2)
    if titleGap*2 + len(title) + 2 != maxWidth:
        out += bord + " "*titleGap + title + " "*(titleGap+1) + bord + "\n"
    else:
        out += bord + " "*titleGap + title + " "*titleGap + bord + "\n"

    # Second Line
    out += bord*maxWidth + "\n"

    # Gaps
    gaps = [[0 for _ in range(maxCols)] for _ in range(maxRows)]
    for i in range(len(data)):
        out += bord
        for j in range(len(data[i])):
            minPad = (maxWidth - (len(data[i]))) / len(data[i]) - len(data[i][j])
            varGap = ((maxVars[j] + minPad) - len(data[i][j])) / 2
            if int(varGap) == varGap:
                gaps[i][j] = varGap
            else:
                gaps[i][j] = int(varGap) + .5

    print(maxWidth)
    print(gaps)
    for i in gaps:
        curGap = sum(i)*2+sum(maxVars)+maxCols+1
        if curGap > maxWidth:
            temp = (int(sum(i)*2+sum(maxVars)+maxCols+1) - maxWidth) % maxCols
            if maxCols == 1:
                temp = 1
            for j in range(1,temp+1):
                print(j)
                if i[-j] == int(i[-j]):
                    i[-j] -= .5
                else:
                    i[-j] = round(i[-j]-.5)
        elif curGap < maxWidth:
            temp = (maxWidth - int(sum(i) * 2 + sum(maxVars) + maxCols + 1)) % maxCols
            if maxCols == 1:
                temp = 1
            for j in range(temp):
                if i[j] == int(i[j]):
                    i[j] += .5
                else:
                    i[j] = round(i[j]+.5)
    print(gaps)

    for i in range(len(gaps)):
        gapList = gaps[i]
        for j in range(len(gapList)):
            gap = gapList[j]
            if gap == int(gap):
                gap = int(gap)
                out += " "*gap + data[i][j] + " "*gap + bord
            else:
                gap = int(gap)
                out += " " * gap + data[i][j] + " " * (gap+1) + bord
        out += "\n"

    # Final Line
    out += bord*maxWidth

    return out


def maxLen(list):
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

    border = "#"  # input("What border style would you like? ")
    title = "Test test test test test test"  # input("What title would you like? ")
    dataFile = "singleData.txt"  # input("What filename do you wish to read your values from? ")
    data = fr.parse_file("../" + dataFile, ";")
    chart = make_chart([['','','','','','','','','','','','']], title, border)
    print(chart)


if __name__ == "__main__":
    main()
