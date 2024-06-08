from __future__ import annotations as _annotations

from commands._command import Command as _Command


class Install(_Command):
    def setup(self) -> None:
        self.command_parser.add_argument("location")
        raise NotImplementedError
