import re as _re
import toml as _toml
import pathlib as _pathlib
import contextlib as _contextlib
import subprocess as _subprocess


_CONFIG_FILENAME = "config.toml"
_HELP_COMMANDS_PATTERN = r"\b[A-Z]+\b"


def collect() -> list[str]:
    commands: list[str] = []
    file = _pathlib.Path(__file__).parent / _CONFIG_FILENAME
    config = _toml.loads(file.read_text(encoding="utf-8"))
    registered = config["scripts"]
    commands.extend(registered.keys())
    with _contextlib.redirect_stdout(None):
        result = _subprocess.run("help", capture_output=True, text=True)
    matches = _re.findall(_HELP_COMMANDS_PATTERN, result.stdout)
    commands.extend(match.lower() for match in matches)
    return commands
