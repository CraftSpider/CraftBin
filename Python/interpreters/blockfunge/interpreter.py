

class Module:

    def __init__(self, funcs, types, externs):
        self.funcs = funcs
        self.types = types
        self.externs = externs
        for func in funcs:
            funcs[func].module = self
        for type in types:
            types[type].module = self
        for extern in externs:
            externs[extern].module = self

        self.frames = []

    def eval_token(self, token):
        if str(token) in self.funcs:
            return self.funcs[str(token)]
        elif str(token) in self.types:
            return self.types[str(token)]
        print("Unknown Token")
        exit(1)

    def run(self):
        print(self.funcs["main"].invoke())

    def add_frame(self, frame):
        self.frames.append(frame)
        result = frame.run()
        self.frames.pop()
        return result
