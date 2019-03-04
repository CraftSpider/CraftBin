
import string


def one():
    two = 0
    three = 0
    with open("input.txt", "r") as file:
        for id in file:
            found = 0
            for char in string.ascii_letters:
                result = id.count(char)
                if result == 2 and not (found & 1):
                    two += 1
                    found |= 1
                elif result == 3 and not (found & 2):
                    three += 1
                    found |= 2
    print(two * three)


def two():
    ids = []
    with open("input.txt", "r") as file:
        for id in file:
            ids.append(id)

    for id in ids:
        for oid in ids:
            if id == oid:
                continue
            pass


one()
