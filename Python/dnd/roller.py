import random
import string

import utils.interp as interp


old_faithful = (2, 2, 3, 4, 5, 5)


roller = interp.Interpreter("DND Roller", opening="DND Roll System")


@roller.command()
def roll(*, order):
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
    roller.run()


if __name__ == "__main__":
    main()
