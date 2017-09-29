"""
    Holds functions for the PPC

    Author: CraftSpider
"""


def add(nums):
    N1 = nums.pop()
    try:
        N2 = nums.pop()
    except IndexError:
        N2 = 0
    nums.push(N1 + N2)


def subtract(nums):
    N1 = nums.pop()
    try:
        N2 = nums.pop()
    except IndexError:
        N2 = 0
    nums.push(N2 - N1)


def multiply(nums):
    N1 = nums.pop()
    try:
        N2 = nums.pop()
    except IndexError:
        N2 = 1
    nums.push(N1 * N2)


def divide(nums):
    N1 = nums.pop()
    try:
        N2 = nums.pop()
    except IndexError:
        N2 = 1
    nums.push(N2 / N1)


def exponent(nums):
    N1 = nums.pop()
    try:
        N2 = nums.pop()
    except IndexError:
        N2 = 1
    nums.push(N1 ** N2)


def equals(nums):
    N1 = nums.pop()
    try:
        N2 = nums.pop()
    except IndexError:
        N2 = None
    nums.push(N1 == N2)

FUNCTIONS = {
    '+': add,
    '-': subtract,
    '*': multiply,
    '/': divide,
    '^': exponent,
    '=': equals,
    '(': True,
}

orderOfOps = {
    '=': 0,
    '+': 1,
    '-': 1,
    '*': 2,
    '/': 2,
    '^': 3,
    '(': 100
}  # ['^', ['*', '/'], ['+', '-'], '=']
