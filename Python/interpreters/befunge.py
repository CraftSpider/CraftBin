import random
from collections import defaultdict


class Point:

    __slots__ = ("x", "y")

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"


def noop():
    return " "


def dict_maker():
    return defaultdict(noop)


def interpret(data):
    data = data.strip()
    data = list(reversed(data.split("\n")))
    code = defaultdict(dict_maker)
    for i in range(len(data)):
        for j in range(len(data[i])):
            code[i][j] = data[i][j]

    stack = []
    pos = Point(0, len(code) - 1)
    direction = "R"
    ascii_mode = False
    skip = False

    out = ""

    while True:
        char = code[pos.y][pos.x]

        # Do character processing
        if skip:
            skip = False
        elif ascii_mode:
            if char != "\"":
                stack.append(ord(char))
            else:
                ascii_mode = False
        elif char == ">":
            direction = "R"
        elif char == "<":
            direction = "L"
        elif char == "^":
            direction = "U"
        elif char == "v":
            direction = "D"
        elif char == "?":
            direction = random.choice(["R", "L", "U", "D"])
        elif "0" <= char <= "9":
            stack.append(int(char))
        elif char == "+":
            a = stack.pop()
            b = stack.pop()
            stack.append(b + a)
        elif char == "-":
            a = stack.pop()
            b = stack.pop()
            stack.append(b - a)
        elif char == "*":
            a = stack.pop()
            b = stack.pop()
            stack.append(b * a)
        elif char == "/":
            a = stack.pop()
            b = stack.pop()
            if a == 0:
                stack.append(0)
            else:
                stack.append(b // a)
        elif char == "%":
            a = stack.pop()
            b = stack.pop()
            if a == 0:
                stack.append(0)
            else:
                stack.append(b % a)
        elif char == "!":
            a = stack.pop()
            if a:
                stack.append(0)
            else:
                stack.append(1)
        elif char == "`":
            a = stack.pop()
            b = stack.pop()
            if b > a:
                stack.append(1)
            else:
                stack.append(0)
        elif char == "_":
            a = stack.pop()
            if a == 0:
                direction = "R"
            else:
                direction = "L"
        elif char == "|":
            a = stack.pop()
            if a == 0:
                direction = "D"
            else:
                direction = "U"
        elif char == "\"":
            ascii_mode = True
        elif char == ":":
            if not len(stack):
                stack.append(0)
                stack.append(0)
            else:
                stack.append(stack[-1])
        elif char == "\\":
            a = stack.pop()
            if len(stack):
                b = stack.pop()
            else:
                b = 0
            stack.append(a)
            stack.append(b)
        elif char == "$":
            stack.pop()
        elif char == ".":
            out += str(stack.pop())
        elif char == ",":
            out += chr(stack.pop())
        elif char == "#":
            skip = True
        elif char == "p":
            y = stack.pop()
            x = stack.pop()
            v = stack.pop()
            code[y][x] = chr(v)
        elif char == "g":
            y = stack.pop()
            x = stack.pop()
            stack.append(ord(code[y][x]))
        elif char == "&":
            stack.append(int(input()))
        elif char == "~":
            stack.append(ord(input()))
        elif char == "@":
            break
        elif char == " ":
            pass
        else:
            raise SyntaxError(f"Unknown Befunge-93 Code: {char}")

        if direction == "R":
            pos.x += 1
        elif direction == "L":
            pos.x -= 1
        elif direction == "U":
            pos.y += 1
        elif direction == "D":
            pos.y -= 1

        # Do a check for wraparound
        if pos.y >= len(code):
            pos.y -= len(code)
        elif pos.y < 0:
            pos.y += len(code)

        if pos.x >= len(code[pos.y]):
            pos.x -= len(code[pos.y])
        elif pos.x < 0:
            pos.x += len(code[pos.y])

    return out


print(interpret("""
:0g,:"~"`#@_1+0"Quines are Fun">_
 """))
