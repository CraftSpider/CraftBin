"""
    Day 3
    Author: Rune Tynan
"""
import math


def _make_origins(square, ring):
    even = square - 1
    first_orig = (square - 2)**2 + ring
    return tuple(first_orig + even*i for i in range(4))


def _make_corners(square, ring):
    even = square - 1
    first_corner = (square - 2)**2 + ring*2
    return tuple(first_corner + even*i for i in range(4))


# Each full square is an odd power of 2

def get_steps():
    num = int(input("> "))

    square = math.ceil(num**.5)  # Squared, the max of the ring
    if square % 2 == 0:
        square += 1
    ring = (square - 1) // 2  # How far out from the center

    origs = _make_origins(square, ring)

    closest = None
    min_dist = None
    for item in origs:
        if min_dist is None or abs(item - num) < min_dist:
            min_dist = abs(item - num)
            closest = item

    print(f"Minimum Steps: {min_dist + ring}")
