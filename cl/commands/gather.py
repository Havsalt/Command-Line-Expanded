import contextlib as _contextlib
import subprocess as _subprocess
import pathlib as _pathlib

from actus import error as _error

from ..commands._command import Command as _Command
from ..parser_args import ParserArguments as _ParserArguments


class Gather(_Command):
    def process(self, args: _ParserArguments) -> None:
        with _contextlib.redirect_stdout(None):
            result = _subprocess.run(["where", args.command_name],
                                     capture_output=True,
                                     text=True)
            if not result.stdout:
                _error(f"Could not gather command '{args.command_name}', as it was not found in PATH")
                self.parser.exit(1)
        raw_path = result.stdout.rstrip("\n")
        path = _pathlib.Path(raw_path).resolve()
        script_name = path.stem
        # _config.get()["scripts"][script_name] = str(path)
        # _config.save()
