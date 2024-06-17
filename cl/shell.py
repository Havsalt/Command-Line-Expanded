from __future__ import annotations

import subprocess
import pathlib
import shlex
import json
import re
import os
from argparse import ArgumentParser
from typing import TypeVar, TypeAlias, Generic

import strox
import colex
from actus import warn, LogSection

from .intake import get_live_input

T = TypeVar("T")
class Stack(list[T], Generic[T]): ...
Command: TypeAlias = list[str]


KEYWORD_PREFIX = "!"
KEYWORD_INSERT_PATTERN = re.compile(
    r"(![-\w]+)[\s\\]?$",
    flags=re.RegexFlag.ASCII
)
KEYWORD_UNMATCHED_PATTERN = re.compile(
    r"(![-\w]+)[\s\\]?$",
    flags=re.RegexFlag.ASCII
)
dev = LogSection("Dev", supress_output=True)


def expand_keywords(string: str) -> str:
    fd = (
        pathlib.Path(__file__)
        .parent
        .joinpath("substitutions.json")
        .open()
    )
    substitutions: dict[str, str] = json.load(fd)
    fd.close()

    def replace(match: re.Match[str]) -> str:
        keyword = match.group()[1:]
        if keyword not in substitutions:
            return match.group()
        return substitutions[keyword]
    
    # substitue keywords with their replacements if possible
    for keyword in sorted(substitutions.keys(), key=len, reverse=True):
        string = re.sub(KEYWORD_INSERT_PATTERN, replace, string)
    # warn non-expanded keywords
    for unmatched in re.finditer(KEYWORD_UNMATCHED_PATTERN, string):
        keyword = unmatched.group()[1:]
        closest = strox.get_closest_match(
            keyword,
            substitutions.keys()
        )
        with warn(f"No keyword replacement found for $[{keyword}]"):
            warn(f"Closest match was $[{closest}]")
    return string


def parse_command(string: str) -> Stack[Command]:
    # NOTE: Stack implementation with only decending layers
    # TODO: make a Tree implementation for layer contiunation
    parts = shlex.split(string, posix=False)
    dev(f"Parts: {parts}")
    if not parts:
        warn("Command has no segments")
    elif parts[0] == "|":
        warn('Command started with $["|"]')
    stack: Stack[Command] = Stack()
    command = []
    for part in parts:
        if part == "|":
            stack.append(command)
            command = []
            continue
        command.append(part)
    if command:
        stack.append(command)
    dev(f"Sub: {stack}")
    # TODO: structure for tree iterations
    # initial command (caller ish)
    # arg - "|" is result of subcommand, layer down
    # (in "|") - "<|" is layer up subcommand
    return stack


def execute_stack(stack: Stack[Command]) -> str | None:
    result: str | None = None
    while stack:
        command = stack.pop(-1)
        if result is not None:
            command.append(result)
        dev(f"Command: {command}")
        process = subprocess.run(command, text=True, shell=True, capture_output=True)
        result = process.stdout.rstrip("\n")
        dev(f"Stdout: {result}")
    dev(f"Result: {result}")
    return result


def enter_session(context: ArgumentParser, dev_mode: bool = False) -> None:
    if dev_mode:
        dev.enable_output()
    while True:
        prompt = (
            colex.colorize("Enter command", colex.SALMON)
            + colex.colorize(":", colex.WHITE)
            + " "
        )
        raw_command = get_live_input(prompt).lstrip()
        dev(f"Raw: {raw_command}")
        if raw_command in ("exit", "."):
            return
        elif raw_command == "cls":
            os.system("cls")
            continue

        expanded = expand_keywords(raw_command)
        command_stack = parse_command(expanded)
        result = execute_stack(command_stack)
        print(result)
