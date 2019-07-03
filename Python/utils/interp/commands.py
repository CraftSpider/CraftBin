
import inspect

from . import parser, converters
from .errors import NotEnoughArguments


class GroupMixin:

    __slots__ = ("_commands",)

    def __init__(self, *args, **kwargs):
        self._commands = {}

    def add_command(self, command):
        if not isinstance(command, Command):
            raise TypeError("Can only add Command instances to CommandLine tools")
        if command.name in self._commands:
            raise AttributeError("Command already exists with given name")
        self._commands[command.name] = command

    def get_command(self, name):
        return self._commands.get(name, None)

    def remove_command(self, command):
        if not isinstance(command, Command):
            raise TypeError("Can only remove Command instances from CommandLine tools")
        del self._commands[command.name]

    def command(self, **kwargs):
        def callback(func):
            _command = Command(func, **kwargs)
            self.add_command(_command)
            return _command
        return callback


class Command:

    __slots__ = ("_callback", "name", "__wrapped__", "_signature", "description", "documentation", "pass_ctx")

    def __call__(self, *args, **kwargs):
        raise TypeError("Commands should be called indirectly through .invoke() or directly through .callback()")

    def __init__(self, callback, **kwargs):
        self._callback = self.__wrapped__ = callback
        self._signature = inspect.signature(callback)
        self.description = kwargs.get("description", None)
        self.documentation = kwargs.get("documentation", inspect.getdoc(callback))
        self.name = kwargs.get("name", callback.__name__)
        self.pass_ctx = kwargs.get("pass_ctx", False)

    @property
    def callback(self):
        return self._callback

    @callback.setter
    def callback(self, new):
        if not callable(new):
            raise TypeError("Callback must be a callable type")
        self._signature = inspect.signature(new)
        self._callback = new

    @property
    def signature(self):
        return self._signature

    def invoke(self, ctx, data):
        params = self._signature.parameters
        parse = parser.InputParser(data)
        args = []
        kwargs = {}
        if self.pass_ctx:
            args.append(ctx)

        first = True
        for name in params:
            if self.pass_ctx and first:
                first = False
                continue
            param = params[name]
            if param.kind == inspect.Parameter.POSITIONAL_OR_KEYWORD:
                out = parse.next_arg()
                if out is None and param.default is inspect.Parameter.empty:
                    raise NotEnoughArguments()
                if param.annotation is not inspect.Parameter.empty:
                    out = converters.handle_conversion(out, param.annotation)
                args.append(out)
            elif param.kind == inspect.Parameter.VAR_POSITIONAL:
                out = parse.remaining_args()
                if param.annotation is not inspect.Parameter.empty:
                    for i in range(len(out)):
                        out[i] = converters.handle_conversion(out[i], param.annotation)
                args.extend(out)
            elif param.kind == inspect.Parameter.KEYWORD_ONLY:
                out = parse.remaining_raw()
                if out is None and param.default is not inspect.Parameter.empty:
                    out = param.default
                elif out is None:
                    out = ""
                kwargs[name] = out
        self.callback(*args, **kwargs)


def command(**kwargs):
    def callback(func):
        return Command(func, **kwargs)
    return callback


# TODO: Group command
