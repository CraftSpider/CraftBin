
import random
import cmath


def generate_quad(integer=False, real=True):

    if integer:
        root1 = random.randint(-10, 10)
        root2 = random.randint(-10, 10)

        b = root1 + root2
        c = root1 * root2

        return f"x^2 + {b}x + {c}"

    while True:
        b = random.randint(-25, 25)
        c = random.randint(-100, 100)

        root1 = (-b + cmath.sqrt(b**2 - 4*c)) / 2
        root2 = (-b - cmath.sqrt(b**2 - 4*c)) / 2

        if real and (root1.imag != 0 or root2.imag != 0):
            continue

        root1 = root1.real
        root2 = root2.real

        if abs(int(root1) - root1) < .01 or abs(int(root2) - root2) < .01:
            continue
        else:
            return f"x^2 + {b}x + {c}"


if __name__ == "__main__":
    print(generate_quad())
