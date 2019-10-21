"""
    Holds functions for the PPC

    Author: CraftSpider
"""


FUNCTIONS = {'(': lambda x: 0}
order_of_ops = {'(': 100}


def func(symbol, priority):

    def pred(func_in):
        FUNCTIONS[symbol] = func_in
        order_of_ops[symbol] = priority
        return func
    return pred


@func("+", 10)
def add(nums):
    n1 = nums.pop()
    try:
        n2 = nums.pop()
    except IndexError:
        n2 = 0
    nums.append(n1 + n2)


@func("-", 10)
def subtract(nums):
    n1 = nums.pop()
    try:
        n2 = nums.pop()
    except IndexError:
        n2 = 0
    nums.append(n2 - n1)


@func("*", 20)
def multiply(nums):
    n1 = nums.pop()
    try:
        n2 = nums.pop()
    except IndexError:
        n2 = 1
    nums.append(n1 * n2)


@func("/", 20)
def divide(nums):
    n1 = nums.pop()
    try:
        n2 = nums.pop()
    except IndexError:
        n2 = 1
    nums.append((n2 / n1))


@func("^", 30)
def exponent(nums):
    n1 = nums.pop()
    try:
        n2 = nums.pop()
    except IndexError:
        n2 = 1
    nums.append(n1 ** n2)


@func("=", 0)
def equals(nums):
    n1 = nums.pop()
    try:
        n2 = nums.pop()
    except IndexError:
        n2 = None
    nums.append(n1 == n2)
