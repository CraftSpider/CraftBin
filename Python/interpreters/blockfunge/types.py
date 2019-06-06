
from . import operators
from .enums import Direction, TokenType


def make_token(arg):
    if isinstance(arg, Token):
        return arg
    elif isinstance(arg, (int, float)):
        return Token(TokenType.NUM, arg)
    elif isinstance(arg, str):
        return Token(TokenType.STRING, arg)
    else:
        return Token(TokenType.REF, arg)


class Graph:

    def __init__(self, height=0, width=0):
        self.buffer = []
        self.height = height
        self.width = width

    def __len__(self):
        return len(self.buffer)

    def __repr__(self):
        return f"Graph(height={self.height}, width={self.width})"

    def __getitem__(self, item):
        if isinstance(item, (tuple, list)):
            if item[0] > self.height or item[1] > self.width:
                raise IndexError("Access outside graph size")
            try:
                return self.buffer[item[0]][item[1]]
            except IndexError:
                return None
        else:
            return self.buffer[item]

    def __setitem__(self, key, value):
        if isinstance(key, (tuple, list)):
            if key[0] > self.height or key[1] > self.width:
                raise IndexError("Access outside graph size")
            try:
                self.buffer[key[0]][key[1]] = value
            except IndexError:
                print("TODO: Key outside range")
        else:
            self.buffer[key] = value

    def is_within(self, point):
        return 0 <= point[0] < self.height and 0 <= point[1] < self.width

    def append(self, line):
        if len(line) > self.width:
            self.width = len(line)
        if len(self.buffer) + 1 > self.height:
            self.height += 1
        self.buffer.append(line)


class Block:

    __slots__ = ("name", "graph", "arguments", "module")

    def __init__(self, name, graph):
        arg_pos = name.find('[')
        self.arguments = 0
        if arg_pos > 0:
            self.arguments = int(name[arg_pos+1:len(name)-1])
            name = name[:arg_pos]
        self.name = name
        self.graph = graph

    def __repr__(self):
        return f"Block(name={self.name}, arguments={self.arguments}, graph={self.graph})"


class Function(Block):

    __slots__ = ()

    def __init__(self, name, code):
        super().__init__(name, code)

    def invoke(self, *args):
        tokens = []
        for arg in args:
            tokens.append(make_token(arg))
        print(f"Invoking {self.name}")
        frame = Frame(self, tokens)
        return self.module.add_frame(frame)


class Type(Block):

    __slots__ = ("methods",)


class Extern(Block):
    pass


class Token:

    __slots__ = ("type", "value")

    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return str(self.value)


class Frame:

    __slots__ = ("func", "stack", "ptr", "direction", "register", "locals")

    def __init__(self, func, args):
        self.func = func
        self.register = ""
        self.stack = [*args]
        self.ptr = [0, 0]
        self.direction = Direction.RIGHT
        self.locals = {}

    def eval_token(self, token):
        if token.type == TokenType.NUM:
            return int(token.value)
        elif str(token) in self.locals:
            return self.locals[str(token)]
        else:
            return self.func.module.eval_token(token)

    def _shift_pointer(self):
        if self.direction == Direction.RIGHT:
            self.ptr[1] += 1
        elif self.direction == Direction.LEFT:
            self.ptr[1] -= 1
        elif self.direction == Direction.DOWN:
            self.ptr[0] += 1
        elif self.direction == Direction.UP:
            self.ptr[0] -= 1

    def _push(self):
        if self.register == "":
            return
        if self.register.isnumeric():
            ttype = TokenType.NUM
        else:
            ttype = TokenType.VAR
        self.stack.append(Token(ttype, self.register))
        self.register = ""

    def run(self):

        while self.func.graph.is_within(self.ptr):
            char = self.func.graph[self.ptr]

            if char in operators.FLOW_CONTROL:
                if self.register != "":
                    self._push()
                self.direction = operators.invoke_operator(char, self)
            elif char in operators.ACTIONS:
                self._push()
                result = operators.invoke_operator(char, self)
                if result is not None:
                    self.stack.append(make_token(result))
            elif char == '"':
                pass
                # TODO: String mode
            elif char == ' ':
                self._push()
            else:
                self.register += char

            self._shift_pointer()

        if len(self.stack):
            return self.stack.pop()
        return None

