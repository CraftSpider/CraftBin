
import traceback
import threading
import inspect
import builtins

from . import commands

__print__ = builtins.print


class Context:

    def __init__(self, interp, command, data):
        self.interpreter = interp
        self.command = command
        self.raw_data = data


class OutputContext:

    __slots__ = ("name", "module", "qualname", "cur_line", "first_line", "file")

    def __init__(self, frame):
        import types
        frame: types.FrameType
        self.first_line = frame.f_code.co_firstlineno
        self.file = frame.f_code.co_filename
        self.name = frame.f_code.co_name
        self.module = frame.f_globals['__name__']
        self.qualname = self.module + "." + self.name
        self.cur_line = frame.f_lineno


class Interpreter(commands.GroupMixin):

    def __init__(self, name, **kwargs):
        super().__init__(kwargs)
        self.name = name
        self.opening = kwargs.get("opening", None)
        self.prompt = kwargs.get("prompt", "> ")
        self.threaded = kwargs.get("threaded", False)
        self.ctx_class = kwargs.get("ctx_class", Context)

    def _loop(self):
        __print__(self.prompt, end="")
        data = input()
        self.dispatch("input", data)

    def __print_replace(self, *args, **kwargs):
        frame = inspect.currentframe().f_back
        ctx = OutputContext(frame)
        del frame
        self.dispatch("output", ctx, *args, **kwargs)

    def run(self):
        builtins.print = self.__print_replace
        if self.opening:
            __print__(self.opening)
        self.dispatch("start")
        while True:
            try:
                self._loop()
            except (KeyboardInterrupt, EOFError):
                break
            except Exception:
                __print__(f"Ignoring exception in main loop:\n{traceback.format_exc()}")
        self.dispatch("stop")
        builtins.print = __print__

    def dispatch(self, event, *args, **kwargs):
        handler = getattr(self, f"on_{event}", None)
        if handler is not None:
            if self.threaded:
                thread = threading.Thread(target=handler, args=args, kwargs=kwargs)
                thread.start()
            else:
                handler(*args, **kwargs)

    def add_cog(self, cog):
        for name, attr in inspect.getmembers(cog):
            if isinstance(attr, commands.Command):
                self.add_command(attr)
            else:
                __print__(name, attr)

    # Default command handling

    def print(self, *args, **kwargs):
        __print__(*args, **kwargs)

    def process_command(self, data_in):
        split = data_in.split(" ", 1)
        if len(split) == 1:
            split.append("")
        name, data = split
        command = self.get_command(name)
        if command is None:
            self.dispatch("command_not_found", name, data)
        else:
            ctx = self.ctx_class(self, command, data)

            self.dispatch("before_command", name)
            try:
                command.invoke(ctx, data)
            except Exception as e:
                self.dispatch("command_error", command, e)
            self.dispatch("after_command", name)

    def process_filters(self, ctx, *output, **kwargs):
        self.print(ctx.qualname)
        return True  # TODO

    # Default handlers:

    def on_input(self, data):
        self.process_command(data)

    def on_output(self, ctx, *args, **kwargs):
        result = self.process_filters(ctx, *args, **kwargs)
        if result:
            __print__(*args, **kwargs)

    def on_command_not_found(self, name, data):
        print(f"Unrecognized command {name}")

    def on_command_error(self, command, error):
        errmsg = "".join(traceback.format_exception(type(error), error, error.__traceback__))
        print(f"Ignoring exception in command {command.name}:\n{errmsg}")
