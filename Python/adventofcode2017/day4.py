
with open("input.txt") as file:
    phrases = [line for line in file]

valid = list(filter(lambda x: len(set(x.split())) == len(list(x.split())), phrases))

print(len(valid))
