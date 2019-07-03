
from .errors import ParsingError


QUOTE_CHARS = {"\"", "\'"}


class InputParser:

    __slots__ = ("raw", "pointer", "args", "end", "arg_pos")

    def __init__(self, data):
        self.raw = data
        self.pointer = 0
        self.args = []
        self.arg_pos = 0

        if data == "":
            self.end = True
        else:
            self.end = False

    def all_raw(self):
        return self.raw

    def all_args(self):
        if self.end:
            return [x[2] for x in self.args]
        else:
            point, pos = self.pointer, self.arg_pos
            while self.next_arg() is not None:
                pass
            self.pointer, self.arg_pos = point, pos
            self.end = False
            return [x[2] for x in self.args]

    def next_arg(self):
        if self.end:
            return None
        if self.arg_pos < len(self.args):
            out = self.args[self.arg_pos]
            self.pointer = out[0]
            self.arg_pos += 1
            return out[2]

        in_str = False
        arg = ""
        start = self.pointer
        while True:
            if self.pointer == len(self.raw):
                if in_str:
                    raise ParsingError("Missing end of quote")
                self.end = True
                break
            char = self.raw[self.pointer]
            if char == " " and not in_str:
                break
            elif char in QUOTE_CHARS:
                in_str = not in_str
            else:
                arg += char
            self.pointer += 1
        self.args.append((start, self.pointer, arg))
        self.arg_pos += 1
        while not self.end:
            char = self.raw[self.pointer]
            if char == " ":
                self.pointer += 1
            elif char != " ":
                break
            elif self.pointer == len(self.raw):
                self.end = True
                break
        return arg

    def remaining_args(self):
        out = []
        arg = self.next_arg()
        while arg is not None:
            out.append(arg)
            arg = self.next_arg()
        return out

    def remaining_raw(self):
        if self.end:
            return None
        out = self.raw[self.pointer:]
        return out

    def rewind(self, num=1):
        if num < 1:
            raise AttributeError("Can only rewind a positive number of steps")
        elif num > self.arg_pos:
            raise AttributeError("Can't rewind past 0'th arg")
        if self.end:
            self.end = False
        self.arg_pos -= num
        self.pointer = self.args[self.arg_pos][0]


if __name__ == "__main__":
    test_input = "Input1 \"Input 2\" Input3"
    parser = InputParser(test_input)
    print(parser.next_arg())
    print(parser.remaining_args())
    print(parser.args)
    parser.rewind()
    print(parser.arg_pos)
    print(parser.next_arg())
    print(parser.args)
