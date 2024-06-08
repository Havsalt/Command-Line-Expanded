from __future__ import annotations as _annotations

from typing import TYPE_CHECKING as _TYPE_CHECKING

from ._command import Command as _Command
import config as _config
import logger as _logger

if _TYPE_CHECKING:
    from ..parser_args import ParserArguments as _ParserArguments


class Set(_Command):
    def setup(self) -> None:
        self.command_parser.add_argument("section")
        self.command_parser.add_argument("key")
        self.command_parser.add_argument("value")

    def process(self, args: _ParserArguments) -> None:
        _config.get().setdefault(args.section, dict())
        _config.get()[args.section][args.key] = args.value
        _config.save()
        _logger.info(f"Set {args.key}={args.value} in section {args.section}")
