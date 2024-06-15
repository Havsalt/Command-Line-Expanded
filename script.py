
__version__ = "0.2.0"

import argparse

import shell
from constants import PROGRAM_NAME
from parser_args import ParserArguments
# annotation
from commands._command import Command
# commands
# from commands.install import Install
from commands.gather import Gather
from commands.list import List
from commands.register import Register
from commands.set import Set
from commands.get import Get


parser = argparse.ArgumentParser(
    prog="Flavoured Command Line",
    usage=PROGRAM_NAME
)
subparsers = parser.add_subparsers(required=False, dest="command")
# TODO: add this, and a 'scripts' directory

commands: dict[str, Command] = {
    # "install": Install(parser, subparsers),
    "gather": Gather(parser, subparsers),
    "list": List(parser, subparsers),
    "get": Get(parser, subparsers),
    "set": Set(parser, subparsers),
    "register": Register(parser, subparsers)
}

args = ParserArguments()
parser.parse_args(namespace=args)


if args.command is not None:
    command = commands[args.command]
    command.process(args)
    exit(0)

shell.enter_session(context=parser)
