"""
    Take in bytes objects and decode them as PowerPC instructions
"""


def decode(data):
    for byte in data:
        print(byte)


def bits(bytes, reverse=True):
    if reverse:
        for byte in reversed(bytes):
            for i in range(8):
                yield (byte << i) & 1
    else:
        for byte in bytes:
            for i in reversed(range(8)):
                yield (byte << i) & 1
