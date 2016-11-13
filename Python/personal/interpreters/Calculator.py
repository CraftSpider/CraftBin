"""
    Act like a regular calculator... Except that it can't have any two digit numbers

    Author: CraftSpider
"""

from Calc.functions import *

variables = {
    'pi': '3.14159265',
    'e': '2.71828182',
}


def help(a=""):
    print("List of valid functions:")
    print("+, performs basic addition")
    print("-, performs basic subtraction")
    print("*, performs basic multiplication")
    print("/, performs basic division")


def clear(var):
    if var in variables.keys():
        del variables[var]
    else:
        print("Variable", var, "doesn't exist")


def variable(a=""):
    print("Variable table:")
    for i in variables:
        print("Variable:", i, "Value:", variables[i])

commands = {
    "help": help,
    "clear": clear,
    "variables": variable,
}


def setVar(line):
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
    # result = parseLine(line[i+1:])
    # result = execute(result)
    # result = verifyRound(result)
    variables[word] = line[i+1:]
    return word, line[i+1:]


def execute(orders):
    if isinstance(orders, str):
        raise TypeError("invalid input, expected list got string")
    if len(orders) == 0:
        return None

    for i in range(len(orders)):
        item = orders[i]
        if isinstance(item, list):
            orders[i] = execute(item)

    for item in orderOfOps:
        index = 0
        while index < len(orders):
            if isinstance(item, list):
                for i in item:
                    if orders[index] == FUNCTIONS[i]:
                        try:
                            orders = FUNCTIONS[i](orders, index)
                        except TypeError:
                            return None
                        index = 0
            else:
                if orders[index] == FUNCTIONS[item]:
                    try:
                        orders = FUNCTIONS[i](orders, index)
                    except TypeError:
                        return None
                    index = 0
            index += 1
    return orders[0]


def verifyRound(num):
    if num == None:
        return None
    if num == int(num):
        return int(num)
    num = str(num)
    curChar = num[0]
    maxStreak = 0
    start = 0
    streak = 0
    for index in range(len(num)):
        char = num[index]
        if char == curChar:
            streak += 1
        else:
            curChar = char
            if streak > maxStreak:
                maxStreak = streak
                start = index - streak
            streak = 0
    if maxStreak > 10:
        num = round(float(num), start)
    return num


def isNumber(word):
    if word == "":
        return False
    for char in word:
        if not (char.isdigit() or char == "-" or char == "."):
            return False
    return True


def parseWord(word):
    word = word[:len(word) - 1]
    if word == "":
        return []
    elif isNumber(word):
        return [float(word)]
    elif word in variables:
        result = parseLine(variables[word])
        try:
            execute(result)
        except (TypeError, ValueError):
            return None
        return result
    else:
        return None


def parseLine(line):
    out = []
    word = ""
    skip = 0
    for index in range(len(line) + 1):
        if skip > 0:
            skip -= 1
            continue

        if index < len(line):
            char = line[index]
        else:
            char = " "
        word += char

        if word in FUNCTIONS:
            out += [FUNCTIONS[word]]
            word = ""
        elif char in FUNCTIONS:
            result = parseWord(word)
            if result == None:
                return word
            out += result
            out += [FUNCTIONS[char]]
            word = ""
        elif char == " ":
            result = parseWord(word)
            if result == None:
                return word
            out += result
            word = ""
        elif char == "(" or char == "[":
            result = parseLine(line[index+1:])
            out += [result[0]]
            skip = result[1]
            word = ""
        elif char == ")" or char == "]":
            result = parseWord(word)
            if result == None:
                return word
            out += result
            return out, index+1

    return out


def firstWord(str):
    word = ""
    for i in str:
        if i != " " and i not in FUNCTIONS:
            word += i
        else:
            break
    return word


def firstFunction(str):
    word = ""
    for i in str:
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
    print("Welcome to the python programmable calculator!")
    line = input("PPC> ")
    while line != "":
        first = firstWord(line)
        if first in commands:
            commands[first](line[len(first)+1:])
        elif first in variables and firstFunction(line) == '=':
            result = setVar(line)
            if result == None:
                print("Variable can not contain itself in its definition!")
            else:
                print("Variable", result[0], "set to", result[1])
        else:
            orders = parseLine(line)
            if isinstance(orders, list) and len(orders) != 0:
                result = execute(orders)
                result = verifyRound(result)
                if result == None:
                    print("Statement syntax unreadable")
                else:
                    print(result)
            elif '=' in line:
                result = setVar(line)
                if result == None:
                    print("Variable can not contain itself in its definition!")
                else:
                    print("Variable", result[0], "set to", result[1])
            else:
                print(orders + "is not a known function, variable, or command")
        line = input("PPC> ")
    print("Shutting down, goodnight!")


if __name__ == "__main__":
    main()
