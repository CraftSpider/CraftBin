
from . import parse
from . import interpreter as interp


def main():
    name = "blockfunge/test.hd"  # input("Filename: ")
    with open(name) as file:
        blocks = parse.parse_file(file, True)
    main = interp.Module(*blocks)
    main.run()


if __name__ == "__main__":
    main()
