"""
    Acts like a normal calculator, just much less efficient.
    An excuse to practice stack execution and interpreting input.

    Author: CraftSpider
"""

from utils.stack import *
from calc.loader import *

variables = {
    'pi': '3.14159265',
    'e': '2.71828182',
}
commands = {}


def command(name=None):

    def pred(func):
        cname = name or func.__name__
        commands[cname] = func
        return func
    return pred


@command(name="help")
def help_command(a=""):
    print("List of valid functions:")
    print("+, performs basic addition")
    print("-, performs basic subtraction/negation")
    print("*, performs basic multiplication")
    print("/, performs basic division")
    print("^, performs exponentiation")
    print("=, set variables or checks equality")


@command()
def clear(var):
    if var in variables.keys():
        del variables[var]
    else:
        print("Variable", var, "doesn't exist")


@command()
def variables(a=""):
    print("Variable table:")
    for i in variables:
        print("Variable:", i, "Value:", variables[i])


def set_var(line):
    """
        From a given input line, set whatever variable it starts with to the equation after the equals sign
        Returns None instead of declared output if variable name is part of its definition.
    :param line: Command input line to interpret. Type: String
    :return: Tuple containing variable name and value it was set to. Type: (String, String)
    """
    word = ""
    i = 0
    while line[i] != '=' and line[i] != " ":
        word += line[i]
        i += 1
    while line[i] != '=':
        i += 1
    while line[i+1] == ' ':
        i += 1
    if word in line[i:]:
        return None
    variables[word] = line[i+1:]
    return word, line[i+1:]


def execute(orders):
    """
        Given a list of valid orders, will execute them and return the result.
        returns None if input cannot be interpreted into a valid numeric output
    :param orders: List of valid functions and values to execute. Type: List
    :return: Result of running input orders. Type: Float
    """
    if isinstance(orders, str):
        raise TypeError("invalid input, expected list got string")
    if len(orders) == 0:
        return None
    numbers = create_stack()
    functions = create_stack()

    for item in orders:
        if FUNCTIONS.get(item):
            try:
                top_func = functions.top()
                if order_of_ops[top_func] > order_of_ops[item] and top_func != '(':
                    FUNCTIONS[top_func](numbers)
                functions.push(item)
            except IndexError:
                functions.push(item)
        elif item == ")":
            try:
                while functions.top() != "(":
                    calc_func = functions.pop()
                    FUNCTIONS[calc_func](numbers)
                functions.pop()
            except IndexError:
                pass
        else:
            numbers.push(item)

    try:
        while functions.top():
            calc_func = functions.pop()
            if calc_func == '(':
                continue
            FUNCTIONS[calc_func](numbers)
    except IndexError:
        try:
            return numbers.top()
        except IndexError:
            return None


def verify_round(num):
    if num is None:
        return None
    if num == int(num):
        return int(num)
    num = str(num)
    cur_char = num[0]
    max_streak = 0
    start = 0
    streak = 0
    for index in range(len(num)):
        char = num[index]
        if char == cur_char:
            streak += 1
        else:
            cur_char = char
            if streak > max_streak:
                max_streak = streak
                start = index - streak
            streak = 0
    if max_streak > 10:
        num = round(float(num), start)
    return num


def is_number(word):
    """
        Determines whether the input word is a number.
    :param word: Word to check. Type: String
    :return: Whether word is numeric. Type: Boolean
    """
    if word == "":
        return False
    for char in word:
        if not (char.isdigit() or char == "-" or char == "."):
            return False
    return True


def parse_word(word):
    word = word[:len(word) - 1]
    if word == "":
        return []
    elif is_number(word):
        return [float(word)]
    elif word in variables:
        result = parse_line(variables[word])
        try:
            execute(result)
        except (TypeError, ValueError):
            return None
        return result
    else:
        return None


def parse_line(line):
    out = []
    word = ""
    for index in range(len(line) + 1):
        if index < len(line):
            char = line[index]
        else:
            char = " "
        word += char

        if word in FUNCTIONS:
            if word == '-':
                continue
            out += [word]
            word = ""
        elif char in FUNCTIONS:
            result = parse_word(word)
            if result is None:
                return word
            out += result
            out += [char]
            word = ""
        elif char == " ":
            if word[0] == "-":
                try:
                    out += parse_word(word)
                    word = ""
                except ValueError:
                    out += [word[0]]
                    if word[1:] != "":
                        out += parse_word(word[1:])
                    word = ""
                continue
            result = parse_word(word)
            if result is None:
                return word
            out += result
            word = ""
        elif char == "(" or char == "[":
            result = '('
            out += [result]
            word = ""
        elif char == ")" or char == "]":
            result = parse_word(word)
            out += result
            out += [")"]
            word = ""

    return out


def first_word(string):
    word = ""
    for i in string:
        if i != " " and i not in FUNCTIONS:
            word += i
        else:
            break
    return word


def first_function(string):
    """
        Determines the first function in a string. (Checks the calculator's function library to determine)
    :param string: Text to look through. Type: String
    :return: The first function in the string. Type: String
    """
    word = ""
    for i in string:
        word += i
        if word in FUNCTIONS:
            return word
        elif i in FUNCTIONS:
            return i
        elif i == " ":
            word = ""
    return None


def main():
    """
        Runs the primary function loop
    """
    init()
    print("Welcome to the python programmable calculator!")
    line = input("PPC> ")
    exits = ["QUIT", "EXIT", "SHUTDOWN"]
    while line not in exits:
        first = first_word(line)
        if first in commands:
            commands[first](line[len(first)+1:])
        elif first in variables and first_function(line) == '=':
            result = set_var(line)
            if result is None:
                print("Variable can not contain itself in its definition!")
            else:
                print("Variable", result[0], "set to", result[1])
        else:
            orders = parse_line(line)
            if isinstance(orders, list) and len(orders) != 0:
                result = execute(orders)
                result = verify_round(result)
                if result is None:
                    print("Statement syntax unreadable")
                else:
                    print(result)
            elif '=' in line:
                result = set_var(line)
                if result is None:
                    print("Variable can not contain itself in its definition!")
                else:
                    print("Variable", result[0], "set to", result[1])
            elif not isinstance(orders, list):
                print(str(orders) + "is not a known function, variable, or command")
        line = input("PPC> ")
    print("Shutting down, goodnight!")


if __name__ == "__main__":
    main()