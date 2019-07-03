

class InterpreterError(Exception):
    pass


class ParsingError(InterpreterError):
    pass


class CommandError(InterpreterError):
    pass


class NotEnoughArguments(CommandError):
    pass


class UnknownConversion(CommandError):
    pass


class ConversionError(CommandError):
    pass
