from __future__ import annotations as _annotations

from typing import TYPE_CHECKING as _TYPE_CHECKING

from ._command import Command as _Command

from actus import info

if _TYPE_CHECKING:
    from ..parser_args import ParserArguments as _ParserArguments


class Get(_Command):
    def setup(self) -> None:
        self.command_parser.add_argument("section")
        self.command_parser.add_argument("key")

    def process(self, args: _ParserArguments) -> None:
        found = False
        if (config := _config.get(args.section)) is not None:
            if (value := _config.get(args.key)) is not None:
                info(f"Get $[{args.key}]=$[{value}] in section $[{args.section}]")
                found = True
        if not found:
            info(f"Could not find key $[{args.key}] in section $[{args.section}]")
