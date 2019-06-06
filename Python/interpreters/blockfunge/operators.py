
from .enums import Direction
import inspect


def eval_token(token):
    pass


def up_arrow():
    return Direction.UP


def down_arrow():
    return Direction.DOWN


def left_arrow():
    return Direction.LEFT


def right_arrow():
    return Direction.RIGHT


def open_gate(frame):
    top = frame.stack.pop()
    result = frame.eval_token(top)
    if result is True:
        return frame.direction
    else:
        return frame.direction.reverse()


def close_gate(frame):
    top = frame.stack.pop()
    result = frame.eval_token(top)
    if result is True:
        return frame.direction.reverse()
    else:
        return frame.direction


def reverse(frame):
    return frame.direction.reverse()


FLOW_CONTROL = {
    '^': up_arrow,
    'v': down_arrow,
    '<': left_arrow,
    '>': right_arrow,
    '[': open_gate,
    ']': close_gate,
    ':': reverse
}


def add(frame):
    a = frame.stack.pop()
    b = frame.stack.pop()
    return frame.eval_token(a) + frame.eval_token(b)


def subtract(frame):
    a = frame.stack.pop()
    b = frame.stack.pop()
    return frame.eval_token(a) - frame.eval_token(b)


def multiply(frame):
    a = frame.stack.pop()
    b = frame.stack.pop()
    return frame.eval_token(a) * frame.eval_token(b)


def divide(frame):
    a = frame.stack.pop()
    b = frame.stack.pop()
    return frame.eval_token(a) / frame.eval_token(b)


def call(frame):
    func = frame.eval_token(frame.stack.pop())
    num_args = func.arguments
    args = []
    for arg in range(num_args):
        args.append(frame.eval_token(frame.stack.pop()))
    return func.invoke(*args)


ACTIONS = {
    '+': add,
    '-': subtract,
    '*': multiply,
    '/': divide,
    '(': call
}

REFLECTION = {

}


ALL_OPS = FLOW_CONTROL.copy()
ALL_OPS.update(ACTIONS)
ALL_OPS.update(REFLECTION)


def invoke_operator(op, frame):
    func = ALL_OPS[op]
    sig = inspect.signature(func)
    if len(sig.parameters) > 0:
        return func(frame)
    else:
        return func()
