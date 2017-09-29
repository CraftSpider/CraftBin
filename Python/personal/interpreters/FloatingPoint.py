"""
    A program to convert between decimal and floating point input.

    Author: CraftSpider
"""

import math


def decToBin(decimal, precision=0):
    """
        Takes in a decimal number, and returns its binary representation as a string.
    :param decimal: Base 10 number. Type: Numeric
    :param precision: How many digits to include in the result. Type: Int
    :return: Base 2 conversion of input value. Type: String
    """
    try:
        out = ""
        neg = False
        decimal = float(decimal)

        if decimal < 0:
            decimal = -decimal
            neg = True
        elif decimal == 0:
            return "0"*(1 if precision == 0 else precision)

        bit = math.floor(math.log2(decimal))
        while bit >= 0:
            if decimal - 2**bit >= 0:
                out += "1"
                decimal -= 2**bit
            else:
                out += "0"
            bit -= 1

        if decimal > 0:
            out += "."
            if precision != 0: precision += 1
            start = -1
            while decimal > 0:
                if decimal - 2 ** start >= 0:
                    out += "1"
                    decimal -= 2 ** start
                else:
                    out += "0"
                start -= 1

        if len(out) < precision and precision != 0:
            out = "0"*(precision-len(out)) + out
        elif len(out) > precision and precision != 0:
            if "." in out:
                out = out[0:precision]
            else:
                out = out[0:precision] + "B" + str(len(out[precision:]))
        if neg:
            return "-" + out
        return out
    except TypeError:
       print("Bad Input, can't convert.")
       return ""


def invert(bin):
    """
        Given a binary input string, returns its inversion.
    :param bin: Binary input. Type: String
    :return: Binary inversion of input. Type: String
    """
    out = ""
    for i in bin:
        if i == "1":
            out += "0"
        elif i == "0":
            out += "1"
    return out


def decToFloat(decimal):
    """
        Takes in a decimal number, and returns the binary representation of its floating point value.
    :param decimal: Base 10 number. Type: Numeric
    :return: Binary representation of input value. Type: String
    """
    try:
        decimal = float(decimal)
        if decimal < 0:
            negative = "1"
            decimal = -decimal
        else:
            negative = "0"

        log = math.floor(math.log2(decimal))

        if log > 0:
            power = "1" + decToBin(log - 1, 7)
        else:
            power = "0" + invert(decToBin(log, 7))

        remainder = decToBin(decimal - 2 ** log)
        if log < 0:
            remainder = remainder[-log+1:24-log]
        else:
            remainder = remainder[:24]
        frontRem = len(remainder)
        for i, x in enumerate(remainder):
            if x == ".":
                remainder = remainder[0:i] + remainder[i+1:]
                frontRem = i
                break
        front = log-frontRem
        if front < 0: front = 0
        end = (23-(front+len(remainder)))
        mantissa = "0"*front + remainder + "0"*end

        out = negative + power + mantissa
        return out
    except TypeError:
        print("Bad Input, can't convert.")
        return ""
    except ValueError:
        return "0"*32


def binToDec(bin):
    """
        Converts a binary number to its decimal representation.
    :param bin: Binary number to convert. Type: Numeric
    :return: Decimal form of number. Type: Float
    """
    try:
        out = 0
        decimal = [False]
        bin = str(bin)
        length = -1
        for i in bin:
            if i != ".":
                length += 1
            else:
                break
        for i in range(len(bin)):
            char = bin[i]
            if decimal[0]:
                if char == "1":
                    decimal[1] += 2**-decimal[2]
                decimal[2] += 1
            elif char == "1":
                out += 2**length
                length -= 1
            elif char == "0":
                length -= 1
            elif char == ".":
                decimal = [True, 0, 1]
        if decimal[0]:
            out += decimal[1]
        return out
    except TypeError:
        print("Bad Input, can't convert.")
        return 0


def floatToDec(float):
    """
        Takes in a float represented in binary, and returns the decimal form.
    :param float: A floating point number represented in binary. Type: String
    :return: Decimal conversion of float. Type: Float
    """
    try:
        float = str(float)
        float = "".join(float.split())
        neg = float[0]
        power = float[1:9]
        mantissa = float[9:]
        out = (1 if neg == "0" else -1)
        out *= 2**(-127+binToDec(power))
        out *= binToDec("1."+mantissa)
        return out
    except TypeError:
        print("Bad Input, can't convert.")
        return 0


def main():
    """
        Main function. Takes user input and runs other stuff.
    """
    print("Welcome to the python floating point converter.")
    print("Enter A to convert decimal to binary, or B to convert binary to decimal")
    userIn = input("FPC> ").capitalize()
    while userIn != "":
        if userIn == "A":
            print("Enter decimal number to convert.")
            userIn = input("FPC> ")
            floating = decToFloat(userIn)
            print("Float:", floating[0] + " " + floating[1:9] + " " + floating[9:])
        elif userIn == "B":
            print("Enter floating-point number to convert.")
            userIn = input("FPC> ")
            decimal = floatToDec(userIn)
            print("Decimal:", decimal)
        else:
            print("Sorry, I don't understand that. Press <ENTER> to exit.")
        userIn = input("FPC> ").capitalize()


def test():
    print(binToDec("0"))
    print(binToDec("1"))
    print(binToDec("10"))
    print(binToDec("101"))
    print(binToDec("100"))
    print(binToDec(".1"))
    print(binToDec(".011"))
    # print("Enter decimal number to convert.")
    # userIn = input("FPC> ")
    # while userIn != "":
    #     floating = decToFloat(userIn)
    #     print("Float:", floating[0] + " " + floating[1:9] + " " + floating[9:])
    #     print("Enter decimal number to convert.")
    #     userIn = input("FPC> ")


if __name__ == "__main__":
    main()
    # test()
