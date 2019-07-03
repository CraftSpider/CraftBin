"""
    An API for registering interactive command line tools, with argument parsing
    and event handling
"""

from .commands import Command, GroupMixin, command
from .interpreter import Interpreter, Context
