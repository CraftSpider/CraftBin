"""
    Loads functions into the calculator. Any file in the same folder as the loader is checked,
    and if it contains a valid function library, is added to the list passed on to the calculator.

    Author: CraftSpider
"""

import importlib
import os

Modes = []
FUNCTIONS = {}
orderOfOps = {}
dir_path = os.path.dirname(os.path.realpath(__file__))

def init():
    for file in os.listdir(dir_path):
        file = file.split('.')
        if file[-1].lower() == 'py':
            if os.getcwd() == dir_path:
                Modes.append(importlib.import_module(file[0]))
            else:
                Modes.append(importlib.import_module("Calc."+file[0]))

    for item in Modes:
        for key in item.FUNCTIONS:
            FUNCTIONS[key] = item.FUNCTIONS[key]
        for key in item.orderOfOps:
            orderOfOps[key] = item.orderOfOps[key]

if __name__ == "__main__":
    init()
    print(Modes)
    print(FUNCTIONS)
    print(orderOfOps)