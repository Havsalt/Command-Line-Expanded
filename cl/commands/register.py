from __future__ import annotations as _annotations

import pathlib as _pathlib
from typing import TYPE_CHECKING as _TYPE_CHECKING

from actus import (
    info as _info,
    error as _error
)

# from .. import environment as _environment
from ._command import Command as _Command

if _TYPE_CHECKING:
    from ..parser_args import ParserArguments as _ParserArguments


class Register(_Command):
    def setup(self) -> None:
        self.command_parser.add_argument("command_directory")

    def process(self, args: _ParserArguments) -> None:
        path = _pathlib.Path(args.command_directory).resolve()
        if path.exists() and path.is_dir():
            _info(f'Registered to PATH: "{path}"')
            # DEV - disabled
            # _environment.add_to_path(path)
        elif not path.is_dir():
            _error(f'Path given has to point to a directory: "{path}"')
        else:
            _error(f'Path not found while registering: "{path}"')
