import random
import string


old_faithful = (2, 2, 3, 4, 5, 5)
commands = {}


def command(name=None):

    def pred(func):
        cname = name or func.__name__
        commands[cname] = func
        return func
    return pred


@command()
def roll(*order):
    order = "".join(order)
    dice = []
    flat = []
    die = False
    operator = ""
    times = 1
    temp = ""
    for char in order:
        if char == " ":
            continue
        elif char in string.digits:
            temp += char
        elif char == "d":
            if temp != "":
                times = int(temp)
                temp = ""
            die = True
        else:
            if die:
                if temp:
                    dice += [-int(temp) if operator == "-" else int(temp) for _ in range(times)]
                temp = ""
                die = False
            else:
                if temp:
                    flat += [-int(temp) if operator == "-" else int(temp)]
                temp = ""
            operator = char
    if temp:
        if die:
            dice += [-int(temp) if operator == "-" else int(temp) for _ in range(times)]
        else:
            flat += [-int(temp) if operator == "-" else int(temp)]
    result = 0
    print(flat, dice)
    for i in flat:
        result += i
    for i in dice:
        if i < 0:
            result += -random.randint(1, abs(i))
        else:
            result += random.randint(1, i)
    print(result)
    return result


def main():
    print("DND Roll System")
    order = input("> ")
    while order != "exit":
        args = order.split(" ")
        invoker = args[0]
        args = args[1:]
        if invoker in commands:
            commands[invoker](*args)
        else:
            print("Unknown Command")
        order = input("> ")


if __name__ == "__main__":
    main()
