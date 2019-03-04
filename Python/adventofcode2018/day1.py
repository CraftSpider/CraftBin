

# part 1
def one():
    result = 0
    with open("input.txt", "r") as file:
        for line in file:
            result += int(line)
    print(result)


# part 2
def two():
    data = []
    with open("input.txt", "r") as file:
        for line in file:
            data.append(int(line))

    found = set()
    result = 0
    cont = True
    while cont:
        for num in data:
            result += num
            if result in found:
                cont = False
                break
            found.add(result)
    print(result)


two()
