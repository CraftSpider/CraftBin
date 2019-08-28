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
                    return False
            else:
                return False
        elif not char.isnumeric():
            return False
    return True


def is_year(string):
    at_letter = False
    num_nums = 0
    for char in string:
        if not at_letter:
            if char.isnumeric():
                num_nums += 1
            elif char.isalpha():
                if num_nums != 4:
                    return False
                at_letter = True
        else:
            if not char.isalpha():
                return False
    return num_nums == 4


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


def _compare(a, b):
    """
        Compare sub-topics or cutters with each other, returning an integer in [-1,1] to indicate
        less than, equal to, or greater than.
    :param a: First topic
    :param b: Second topic
    :return: Result of comparing the two
    """
    a = _split(a)
    b = _split(b)
    if a[0] != b[0]:
        if a[0] > b[0]:
            return 1
        else:
            return -1
    max_len = max(len(a[1]), len(b[1]))
    for i in range(max_len):
        if i > len(b[1]):
            return 1
        elif i > len(a[1]):
            return -1
        schar = a[1][i]
        ochar = b[1][i]
        if schar > ochar:
            return 1
        elif schar < ochar:
            return -1


def _split_year(string):
    return int(string[:4]), string[4:]


class LOC:

    __slots__ = ("orig_code", "section", "topic", "sub_topic", "cutter", "version", "_year", "work_letter", "copy",
                 "other")

    def __init__(self, code):
        """
            Builds a Library of Congress code from an input string or set of args
        :param code: Code should be in one of the supported formats.
                     Version, Year, and Copy can be in any order, however they will always be evaluated in V-Y-C
                     precedence.
        """
        if isinstance(code, str):
            if not self._iscode(code):
                raise ValueError("String is not a valid LoC code")

            self.orig_code = ""
            self.section = ""
            self.topic = ""
            self.sub_topic = ""
            self.cutter = ""
            self.version = 0
            self._year = 0
            self.work_letter = ""
            self.copy = 0
            self.other = ""

            self.orig_code = code
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

            # Now, pull out the cutter if it exists separately.
            if len(code) and is_topic_or_cutter(code[0]):
                self.cutter = code.pop(0)

            # Remainder can come in any order. We'll figure out which it is each iteration.
            for item in code:
                if item.startswith("v."):
                    self.version = int(item[2:])
                elif item.startswith("c."):
                    self.copy = int(item[2:])
                elif is_year(item):
                    self._year, self.work_letter = _split_year(item)
                elif self.section != "" and item.isalpha():
                    self.section = item
                else:
                    if self.other:
                        self.other += " "
                    self.other += item
        elif isinstance(code, LOC):
            self.orig_code = code.orig_code
            self.section = code.section
            self.topic = code.topic
            self.sub_topic = code.sub_topic
            self.cutter = code.cutter
            self.version = code.version
            self._year = code._year
            self.work_letter = code.work_letter
            self.copy = code.copy
            self.other = code.other
        else:
            raise TypeError("Input must be a string LoC code or LoC object")

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
            out += f"{self.section} "
        out += self.topic
        if self.sub_topic != "":
            out += f".{self.sub_topic}"
        if self.cutter != "":
            out += f" {self.cutter}"
        if self.version:
            out += f" v.{self.version}"
        if self.year:
            out += f" {self.year}{self.work_letter}"
        if self.other != "":
            out += f" {self.other}"
        if self.copy:
            out += f" c.{self.copy}"
        return out

    def __repr__(self):
        return self.orig_code

    @property
    def year(self):
        return self._year

    @year.setter
    def year(self, val):
        if not is_year(val):
            raise AttributeError("Cannot set year to a number that isn't a valid year")
        self._year, self.work_letter = val

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
            out.append(self.section)
        out.append(self.topic)
        if self.sub_topic != "":
            out.append(self.sub_topic)
        if self.cutter != "":
            out.append(self.cutter)
        if self.version != 0:
            out.append("v." + str(self.version))
        if self.year != 0:
            out.append(str(self.year) + self.work_letter)
        if self.other != "":
            out.append(self.other)
        if self.copy != 0:
            out.append("c." + str(self.copy))
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
            result = _compare(self.sub_topic, other.sub_topic)
            if result != 0:
                return result

        # Then cutters
        if self.cutter != other.cutter:
            result = _compare(self.cutter, other.cutter)
            if result != 0:
                return result

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
