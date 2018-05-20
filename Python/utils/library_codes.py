"""
    A program and a class to deal with LOC codes.

    Author: CraftSpider
"""

"""
    Prefix
        Section          OVER
    Class Number
        Topic            QC123
        Sub-Topic        .B45
    Book Number
        Cutter           H64
    Other
        Version          v.1
        Year-Work Letter 2017b
        Copy             c.1
    
    Sub-Topic is also a Cutter. But makes more sense to call it like this for our purposes.
"""

"""
    Supported Formats:
    [Section] <Topic>.[Sub-Topic] [Cutter] [[Version] [Year] [Copy]]
    [Section] <Topic>.[Sub-Topic].[Cutter] [[Version] [Year] [Copy]]
    <Topic>.[Sub-Topic] [Cutter] [[Section] [Version] [Year] [Copy]]
    <Topic>.[Sub-Topic].[Cutter] [[Section] [Version] [Year] [Copy]]
    <>: required []: optional [<>[]]: any order
"""


def is_topic_or_cutter(string):
    """Checks whether a string fits the form [alpha]+[numeric]+"""
    is_cutter = True
    at_num = False
    found_alpha = False
    for char in string:
        if at_num is False:
            if char.isalpha():
                found_alpha = True
            elif char.isnumeric():
                if found_alpha:
                    at_num = True
                else:
                    is_cutter = False
                    break
            else:
                is_cutter = False
                break
        else:
            if char.isalpha():
                is_cutter = False
                break
            elif char.isnumeric():
                pass
            else:
                is_cutter = False
                break
    return is_cutter


def is_year(string):
    is_year_format = True
    at_letter = False
    num_nums = 0
    for char in string:
        if not at_letter:
            if char.isnumeric():
                num_nums += 1
            elif char.isalpha():
                if num_nums != 4:
                    is_year_format = False
                    break
                at_letter = True
        else:
            if not char.isalpha():
                is_year_format = False
                break
    return is_year_format


def _split(string):
    """
        Splits a part of the code like A45 into ['A', '45']
    :param string: Sub-code to split. Type: String
    :return: List of length 2. Type: List
    """
    out = ["", ""]
    for i in string:
        if i.isalpha():
            out[0] += i
        elif i.isnumeric() or i == ".":
            out[1] += i
    return out


class LOC:

    origCode = ""

    section = ""
    topic = ""
    sub_topic = ""
    cutter = ""
    version = 0
    year = 0
    work_letter = ""
    copy = 0
    other = ""

    def __init__(self, code):
        """
            Builds a Library of Congress code from an input string or set of args
        :param code: Code should be in one of the supported formats.
                     Version, Year, and Copy can be in any order, however they will always be evaluated in V-Y-C
                     precedence.
        """
        if isinstance(code, str):
            if self._iscode(code):
                self.origCode = code
                code = code.split()
                # If there's a section name, pull that out first
                if code[0].isalpha():
                    self.section = code.pop(0)
                # Now, get the topic and sub-topic if they exist. Also cutter if it's dotted.
                whole_topic = code.pop(0)
                whole_topic = whole_topic.split(".")
                self.topic = whole_topic.pop(0) +\
                    (".{}".format(whole_topic.pop(0)) if len(whole_topic) and whole_topic[0].isnumeric() else "")
                if len(whole_topic):
                    self.sub_topic = whole_topic.pop(0)
                if len(whole_topic):
                    self.cutter = whole_topic[0]
                # Now, pull out the cutter if it exists.
                if len(code):
                    if is_topic_or_cutter(code[0]):
                        self.cutter = code.pop(0)
                # Remainder can come in any order. We'll figure out which it is each iteration.
                for item in code:
                    if item.startswith("v."):
                        self.version = int(item[2:])
                    elif item.startswith("c."):
                        self.copy = int(item[2:])
                    elif is_year(item):
                        self.year = int(item[:4])
                        self.work_letter = item[4:]
                    elif self.section != "" and item.isalpha():
                        self.section = item
                    else:
                        self.other += item

            else:
                raise ValueError
        else:
            raise TypeError

    def _iscode(self, code):
        if code.isalpha() or code.isnumeric():
            return False
        for char in code:
            if not char.isalnum() and char != "." and char != " ":
                return False
        return True

    def split(self):
        """
            Splits self into a list, with each portion of the code in order.
            Form:
            ['OVER', 'A14.5', 'B43', 'F3', 'v.1', '2001', 'c.1']
        :return: Code split into a list. Type: List
        """
        out = []
        if self.section != "":
            out += [self.section]
        out += [self.topic]
        if self.sub_topic != "":
            out += [self.sub_topic]
        if self.cutter != "":
            out += [self.cutter]
        if self.version != 0:
            out += ["v." + str(self.version)]
        if self.year != 0:
            out += [str(self.year) + self.work_letter]
        if self.other != "":
            out += [self.other]
        if self.copy != 0:
            out += ["c." + str(self.copy)]
        return out

    def compare(self, other):
        """
            Compare ourselves to another LOC instance, and determine whether we are greater, less than, or equal.
            "Lesser" Means closer to A1, and "Greater" means closer to Z9999
        :param other: LOC class instance to compare to. Type: LOC
        :return: 1 if we're greater, 0 if equal, -1 if we're lesser. Prefixes are greater than not, in alphabet order. Type: Int
        """
        # First, compare sections
        if (self.section != "" or other.section != "") and self.section != other.section:
            if self.section == "" and other.section != "":
                return -1
            elif self.section != "" and other.section == "":
                return 1
            else:
                if self.section > other.section:
                    return 1
                else:
                    return -1

        # Next, compare topics
        if self.topic != other.topic:
            stopic = _split(self.topic)
            otopic = _split(other.topic)
            if stopic[0] != otopic[0]:
                if stopic[0] > otopic[0]:
                    return 1
                else:
                    return -1
            if float(stopic[1]) > float(otopic[1]):
                return 1
            else:
                return -1

        # Then sub-topics
        if self.sub_topic != other.sub_topic:
            stopic = _split(self.sub_topic)
            otopic = _split(other.sub_topic)
            if stopic[0] != otopic[0]:
                if stopic[0] > otopic[0]:
                    return 1
                else:
                    return -1
            if len(stopic[1]) >= len(otopic[1]):
                for i in range(len(stopic[1])):
                    if i > len(otopic[1]):
                        return 1
                    schar = stopic[1][i]
                    ochar = otopic[1][i]
                    if schar > ochar:
                        return 1
                    elif schar < ochar:
                        return -1
            else:
                for i in range(len(otopic[1])):
                    if i > len(stopic[1]):
                        return -1
                    schar = stopic[1][i]
                    ochar = otopic[1][i]
                    if schar > ochar:
                        return 1
                    elif schar < ochar:
                        return -1

        # Then cutters (same as sub-topic)
        if self.cutter != other.cutter:
            scutter = _split(self.cutter)
            ocutter = _split(other.cutter)
            if scutter[0] != ocutter[0]:
                if scutter[0] > ocutter[0]:
                    return 1
                else:
                    return -1
            if len(scutter[1]) >= len(ocutter[1]):
                for i in range(len(scutter[1])):
                    if i > len(ocutter[1]):
                        return 1
                    schar = scutter[1][i]
                    ochar = ocutter[1][i]
                    if schar > ochar:
                        return 1
                    elif schar < ochar:
                        return -1
            else:
                for i in range(len(ocutter[1])):
                    if i > len(scutter[1]):
                        return -1
                    schar = scutter[1][i]
                    ochar = ocutter[1][i]
                    if schar > ochar:
                        return 1
                    elif schar < ochar:
                        return -1

        # Then normal after-effects in V-Y-O-C priority
        if self.version != other.version:
            if self.version > other.version:
                return 1
            return -1

        if self.year != other.year:
            if self.year > other.year:
                return 1
            return -1

        # We must take the work letter into account
        if self.work_letter != other.work_letter:
            if self.work_letter > other.work_letter:
                return 1
            return -1

        # If any unknown additions are present, try to guess at those.
        if self.other != other.other:
            # TODO: Try to guess numbers vs words and such
            if self.other > other.other:
                return 1
            return -1

        # Copy is always evaluated last
        if self.copy != other.copy:
            if self.copy > other.copy:
                return 1
            return -1

        return 0  # All else fails, we must be equal.

    def __eq__(self, other):
        if isinstance(other, LOC):
            return self.compare(other) == 0
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        if isinstance(other, LOC):
            return self.compare(other) == -1
        else:
            raise TypeError

    def __le__(self, other):
        if isinstance(other, LOC):
            return self.compare(other) <= 0
        else:
            raise TypeError

    def __gt__(self, other):
        if isinstance(other, LOC):
            return self.compare(other) == 1
        else:
            raise TypeError

    def __ge__(self, other):
        if isinstance(other, LOC):
            return self.compare(other) >= 0
        else:
            raise TypeError

    def __str__(self):
        out = ""
        if self.section != "":
            out += "{} ".format(self.section)
        out += self.topic
        if self.sub_topic != "":
            out += ".{}".format(self.sub_topic)
        if self.cutter != "":
            out += " {}".format(self.cutter)
        if self.version:
            out += " v.{}".format(self.version)
        if self.year:
            out += " {}{}".format(self.year, self.work_letter)
        if self.other != "":
            out += " {}".format(self.other)
        if self.copy:
            out += " c.{}".format(self.copy)
        return out

    def __repr__(self):
        return self.origCode


def compare_codes(code1="", op="", code2=""):
    if op == "":
        op = input("Operator: ")
    try:
        if code1 == "":
            code1 = input("Code 1: ")
        loc1 = LOC(code1)
        if code2 == "":
            code2 = input("Code 2: ")
        loc2 = LOC(code2)
    except ValueError:
        print("Invalid Code Input!")
    else:
        if op == "=" or op == "==":
            print(loc1 == loc2)
        elif op == "!=":
            print(loc1 != loc2)
        elif op == "<":
            print(loc1 < loc2)
        elif op == "<=":
            print(loc1 <= loc2)
        elif op == ">":
            print(loc1 > loc2)
        elif op == ">=":
            print(loc1 >= loc2)


commands = {
    "compare": compare_codes
}


def main():
    print("LOC Reader V0.1")
    instr = input("> ").split()
    command = instr[0]
    args = instr[1:]
    while command.upper() != "QUIT":
        try:
            if command in commands:
                commands[command](*args)
        except Exception as e:
            print(e)
        instr = input("> ").split()
        command = instr[0]
        args = instr[1:]
        # print("section: " + loc1.section, "topic: " + loc1.topic, "sub: " + loc1.sub_topic, "cutter: " + loc1.cutter, "version: " + str(loc1.version), "copy: " + str(loc1.copy), "year: " + str(loc1.year) + loc1.work_letter, "other: " + loc1.other)


if __name__ == "__main__":
    main()
