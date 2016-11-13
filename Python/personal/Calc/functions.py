"""
    Holds functions for the PPC

    Author: CraftSpider
"""


def add(orders, index):
    result = orders[index - 1] + orders[index + 1]
    orders = orders[:index - 1] + [result] + orders[index + 2:]
    return orders


def subtract(orders, index):
    result = orders[index - 1] - orders[index + 1]
    orders = orders[:index - 1] + [result] + orders[index + 2:]
    return orders


def multiply(orders, index):
    result = orders[index - 1] * orders[index + 1]
    orders = orders[:index - 1] + [result] + orders[index + 2:]
    return orders


def divide(orders, index):
    result = orders[index - 1] / orders[index + 1]
    orders = orders[:index - 1] + [result] + orders[index + 2:]
    return orders


def exponent(orders, index):
    result = orders[index - 1] ** orders[index + 1]
    orders = orders[:index - 1] + [result] + orders[index + 2:]
    return orders


def equals(orders, index):
    result = orders[index - 1] == orders[index + 1]
    orders = orders[:index - 1] + [result] + orders[index + 2:]
    return orders

FUNCTIONS = {
    '+': add,
    '-': subtract,
    '*': multiply,
    '/': divide,
    '^': exponent,
    '=': equals,
}

orderOfOps = ['^', ['*', '/'], ['+', '-'], '=']