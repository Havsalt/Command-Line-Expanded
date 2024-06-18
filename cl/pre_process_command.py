from __future__ import annotations as _annotations

import subprocess as _subprocess
import pathlib as _pathlib
import shlex as _shlex
import json as _json
import re as _re
from typing import (
    TypeVar as _TypeVar,
    TypeAlias as _TypeAlias,
    Generic as _Generic
)

import strox as _strox
from actus import warn as _warn

from .dev_utils import dev as _dev


_T = _TypeVar("_T")
class _Stack(list[_T], _Generic[_T]): ...
_Command: _TypeAlias = list[str]


_KEYWORD_PREFIX = "!"
_KEYWORD_INSERT_PATTERN = _re.compile(
    r"(![-\w]+)[\s\\]?$",
    flags=_re.RegexFlag.ASCII
)
_KEYWORD_UNMATCHED_PATTERN = _re.compile(
    r"(![-\w]+)[\s\\]?$",
    flags=_re.RegexFlag.ASCII
)


def expand_keywords(string: str) -> str:
    fd = (
        _pathlib.Path(__file__)
        .parent
        .joinpath("substitutions.json")
        .open()
    )
    substitutions: dict[str, str] = _json.load(fd)
    fd.close()

    def replace(match: _re.Match[str]) -> str:
        keyword = match.group()[1:]
        if keyword not in substitutions:
            return match.group()
        return substitutions[keyword]
    
    # substitue keywords with their replacements if possible
    for keyword in sorted(substitutions.keys(), key=len, reverse=True):
        string = _re.sub(_KEYWORD_INSERT_PATTERN, replace, string)
    # _warn non-expanded keywords
    for unmatched in _re.finditer(_KEYWORD_UNMATCHED_PATTERN, string):
        keyword = unmatched.group()[1:]
        closest = _strox.get_closest_match(
            keyword,
            substitutions.keys()
        )
        with _warn(f"No keyword replacement found for $[{keyword}]"):
            _warn(f"Closest match was $[{closest}]")
    return string


def parse_command(string: str) -> _Stack[_Command]:
    # NOTE: _Stack implementation with only decending layers
    # TODO: make a Tree implementation for layer contiunation
    parts = _shlex.split(string, posix=False)
    _dev(f"Parts: {parts}")
    if not parts:
        _warn("Command has no segments")
    elif parts[0] == "|":
        _warn('Command started with $["|"]')
    stack: _Stack[_Command] = _Stack()
    command = []
    for part in parts:
        if part == "|":
            stack.append(command)
            command = []
            continue
        command.append(part)
    if command:
        stack.append(command)
    _dev(f"Sub: {stack}")
    # TODO: structure for tree iterations
    # initial command (caller ish)
    # arg - "|" is result of subcommand, layer down
    # (in "|") - "<|" is layer up subcommand
    return stack


def execute_stack(stack: _Stack[_Command]) -> str | None:
    result: str | None = None
    while stack:
        command = stack.pop(-1)
        if result is not None:
            command.append(result)
        _dev(f"Command: {command}")
        process = _subprocess.run(command, text=True, shell=True, capture_output=True)
        result = process.stdout.rstrip("\n")
        _dev(f"Stdout: {result}")
    _dev(f"Result: {result}")
    return result
