"""
    Loads functions into the calculator. Any file in the same folder as the loader is checked,
    and if it contains a valid function library, is added to the list passed on to the calculator.

    Author: CraftSpider
"""

import importlib
import os

Modes = []
FUNCTIONS = {}
order_of_ops = {}
dir_path = os.path.dirname(os.path.realpath(__file__))


def init():
    for file in os.listdir(dir_path):
        file = file.split('.')
        if file[-1].lower() == 'py':
            if os.getcwd() == dir_path:
                Modes.append(importlib.import_module(file[0]))
            else:
                Modes.append(importlib.import_module("calc."+str(file[0])))

    for item in Modes:
        for key in item.FUNCTIONS:
            FUNCTIONS[key] = item.FUNCTIONS[key]
        for key in item.order_of_ops:
            order_of_ops[key] = item.order_of_ops[key]


if __name__ == "__main__":
    init()
    print(Modes)
    print(FUNCTIONS)
    print(order_of_ops)
