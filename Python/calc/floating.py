"""
    Floating point operations for the PPC.

    Author: CraftSpider
"""


def add_float(nums):
    n1 = nums.pop()
    try:
        n2 = nums.pop()
    except IndexError:
        n2 = 0
    nums.push(n1 + n2)


FUNCTIONS = {
    '&': add_float
}

order_of_ops = {
    '&': 5
}
