"""
    Generates wonderful names for a fictional hacking group

    Author: CraftSpider
"""

import random

animals = ["lizard", "poodle", "crocodile", "snake", "spider", "cat", "tiger", "lion", "dog", "polar bear", "bird",
           "condor", "eagle", "mouse", "gerbil", "hamster", "dragon", "unicorn", "gryphon", "prairie dog", "shark",
           "fish", "tuna", "dolphin", "llama", "bunny", "rabbit", "alpaca", "frog", "toad", "arachno"]
corporate = ["corp", "inc", "squad", "force", "company", "LLC", "crew", "team", "nation", "crackers", "booters",
             "wreckers", "destroyers", "builders", "breakers", "saur"]


def randomHackName(times=1):
    """
        Generates a name of format a-s-c, random animal, maybe a space, random corporate title.
    :return: New company name. Type: String.
    """
    out = []
    while times > 0:
        name = ""
        name += animals[random.randint(0, len(animals)-1)]
        if random.randint(0, 1) == 1:
            name += " "
        name += corporate[random.randint(0, len(corporate)-1)]
        out += [name]
        times -= 1
    if len(out) == 1:
        out = out[0]
    return out


print(randomHackName(10))
