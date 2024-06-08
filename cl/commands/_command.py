from __future__ import annotations as _annotations

from argparse import ArgumentParser as _ArgumentParser, _SubParsersAction

from parser_args import ParserArguments as _ParserArguments


class Command:
    def __init__(
        self,
        parser: _ArgumentParser,
        subparsers: _SubParsersAction[_ArgumentParser]
    ) -> None:
        self.parser = parser
        self.subparsers = subparsers
        command_name = self.__class__.__name__.lower()
        self.command_parser = subparsers.add_parser(command_name)
        self.setup()
    
    def setup(self) -> None:
        ...
    
    def process(self, args: _ParserArguments) -> None:
        ...
