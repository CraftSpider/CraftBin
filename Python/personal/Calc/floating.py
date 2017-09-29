"""
    Floating point operations for the PPC.

    Author: CraftSpider
"""

def addFloat(nums):
    N1 = nums.pop()
    try:
        N2 = nums.pop()
    except IndexError:
        N2 = 0
    nums.push(N1 + N2)

FUNCTIONS = {
    '&': addFloat
}

orderOfOps = {
    '&': 5
}
