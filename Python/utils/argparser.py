
class ArgParser:

    def __init__(self, args):
        self.source = args[0]
        args = args[1:]

        self.args = []
        self.flags = []
        self.options = {}

        for arg in args:
            if arg.startswith("--"):
                if "=" in arg:
                    arg = arg[2:]
                    pair = arg.split("=")
                    self.options[pair[0]] = pair[1]
                else:
                    self.flags.append(arg[2:])
            elif arg.startswith("-"):
                for char in arg[1:]:
                    self.flags.append(char)
            else:
                self.args.append(arg)

    def get_arg(self, pos):
        return self.args[pos]

    def has_flag(self, *, short=None, long=None):
        return (short in self.flags) or (long in self.flags)

    def has_option(self, name):
        return name in self.options

    def get_option(self, name, default=None):
        return self.options.get(name, default)
