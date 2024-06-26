"""
Command Line Expanded
---------------------

Custom command line shell

Features:
- Can pipe commands
- Inject substitutions for keywords
- History # TODO
- Adaptive autocompleation # TODO
"""

__version__ = "0.6.3"

import argparse

from cl import shell
from cl.parser_args import ParserArguments
# annotation
from cl.commands._command import Command
# commands
# from cl.commands.install import Install
from cl.commands.gather import Gather
from cl.commands.list import List
from cl.commands.register import Register
from cl.commands.set import Set
from cl.commands.get import Get


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="cl"
    )
    parser.add_argument("-d", "--dev",
                        action="store_true",
                        dest="dev_mode",
                        help="Enable dev mode")
    subparsers = parser.add_subparsers(required=False, dest="command")
    # TODO: add this, and a 'scripts' directory

    commands: dict[str, Command] = { # FIXME: temporary disabled
        # "install": Install(parser, subparsers),
        # "gather": Gather(parser, subparsers),
        # "list": List(parser, subparsers),
        # "get": Get(parser, subparsers),
        # "set": Set(parser, subparsers),
        # "register": Register(parser, subparsers)
    }

    args = ParserArguments()
    parser.parse_args(namespace=args)

    if args.command is not None:
        command = commands[args.command]
        command.process(args)
        return 0

    exit_code = shell.run(dev_mode=args.dev_mode)
    return exit_code
