"""
    A program to convert between decimal and floating point input.

    Author: CraftSpider
"""

import math


def dec_to_bin(decimal, precision=0):
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
            if precision != 0:
                precision += 1
            start = -1
            while decimal > 0:
                if decimal - 2 ** start >= 0:
                    out += "1"
                    decimal -= 2 ** start
                else:
                    out += "0"
                start -= 1

        if len(out) < precision != 0:
            out = "0"*(precision-len(out)) + out
        elif len(out) > precision != 0:
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


def invert(binary):
    """
        Given a binary input string, returns its inversion.
    :param binary: Binary input. Type: String
    :return: Binary inversion of input. Type: String
    """
    out = ""
    for i in binary:
        if i == "1":
            out += "0"
        elif i == "0":
            out += "1"
    return out


def dec_to_float(decimal):
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
            power = "1" + dec_to_bin(log - 1, 7)
        else:
            power = "0" + invert(dec_to_bin(log, 7))

        remainder = dec_to_bin(decimal - 2 ** log)
        if log < 0:
            remainder = remainder[-log+1:24-log]
        else:
            remainder = remainder[:24]
        front_rem = len(remainder)
        for i, x in enumerate(remainder):
            if x == ".":
                remainder = remainder[0:i] + remainder[i+1:]
                front_rem = i
                break
        front = log-front_rem
        if front < 0:
            front = 0
        end = (23-(front+len(remainder)))
        mantissa = "0"*front + remainder + "0"*end

        out = negative + power + mantissa
        return out
    except TypeError:
        print("Bad Input, can't convert.")
        return ""
    except ValueError:
        return "0"*32


def bin_to_dec(binary):
    """
        Converts a binary number to its decimal representation.
    :param binary: Binary number to convert. Type: Numeric
    :return: Decimal form of number. Type: Float
    """
    try:
        out = 0
        decimal = [False]
        binary = str(binary)
        length = -1
        for i in binary:
            if i != ".":
                length += 1
            else:
                break
        for i in range(len(binary)):
            char = binary[i]
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


def float_to_dec(float_str):
    """
        Takes in a float represented in binary, and returns the decimal form.
    :param float_str: A floating point number represented in binary. Type: String
    :return: Decimal conversion of float. Type: Float
    """
    try:
        float_str = str(float_str)
        float_str = "".join(float_str.split())
        neg = float_str[0]
        power = float_str[1:9]
        mantissa = float_str[9:]
        out = (1 if neg == "0" else -1)
        out *= 2**(-127 + bin_to_dec(power))
        out *= bin_to_dec("1." + mantissa)
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
    user_in = input("FPC> ").capitalize()
    while user_in != "":
        if user_in == "A":
            print("Enter decimal number to convert.")
            user_in = input("FPC> ")
            floating = dec_to_float(user_in)
            print("Float:", floating[0] + " " + floating[1:9] + " " + floating[9:])
        elif user_in == "B":
            print("Enter floating-point number to convert.")
            user_in = input("FPC> ")
            decimal = float_to_dec(user_in)
            print("Decimal:", decimal)
        else:
            print("Sorry, I don't understand that. Press <ENTER> to exit.")
        user_in = input("FPC> ").capitalize()


def test():
    print(bin_to_dec("0"))
    print(bin_to_dec("1"))
    print(bin_to_dec("10"))
    print(bin_to_dec("101"))
    print(bin_to_dec("100"))
    print(bin_to_dec(".1"))
    print(bin_to_dec(".011"))
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
