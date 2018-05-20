"""
    Day 1
    Author: Rune Tynan
"""

result = 0
prev = ""
instr = input("> ")
for i in instr:
    if i == prev:
        result += int(i)
    prev = i
if instr[0] == instr[-1]:
    result += int(instr[0])
print("Result: " + str(result))
