"""
    Holds functions for the PPC

    Author: CraftSpider
"""


FUNCTIONS = {'(': True}
order_of_ops = {'(': 100}


def func(symbol, priority):

    def pred(func_in):
        FUNCTIONS[symbol] = func_in
        order_of_ops[symbol] = priority
        return func
    return pred


@func("+", 1)
def add(nums):
    n1 = nums.pop()
    try:
        n2 = nums.pop()
    except IndexError:
        n2 = 0
    nums.push(n1 + n2)


@func("-", 1)
def subtract(nums):
    n1 = nums.pop()
    try:
        n2 = nums.pop()
    except IndexError:
        n2 = 0
    nums.push(n2 - n1)


@func("*", 2)
def multiply(nums):
    n1 = nums.pop()
    try:
        n2 = nums.pop()
    except IndexError:
        n2 = 1
    nums.push(n1 * n2)


@func("/", 2)
def divide(nums):
    n1 = nums.pop()
    try:
        n2 = nums.pop()
    except IndexError:
        n2 = 1
    nums.push(n2 / n1)


@func("^", 3)
def exponent(nums):
    n1 = nums.pop()
    try:
        n2 = nums.pop()
    except IndexError:
        n2 = 1
    nums.push(n1 ** n2)


@func("=", 0)
def equals(nums):
    n1 = nums.pop()
    try:
        n2 = nums.pop()
    except IndexError:
        n2 = None
    nums.push(n1 == n2)
