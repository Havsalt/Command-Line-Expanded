from __future__ import annotations

import pathlib
import os

import colex
from actus import warn

from .intake import get_live_input
from .path_collapse import collapse_path
from .process_command import expand_keywords, parse_command, execute_stack
from .dev_utils import dev


def run(no_blink: bool = False, dev_mode: bool = False) -> int:
    if dev_mode:
        dev.enable_output()
    while True:
        color = (
            colex.CYAN
            if no_blink
            else colex.CYAN + colex.BLINK
        )
        prompt = collapse_path(os.getcwd())
        styled_prompt = (
            colex.colorize(prompt, color)
            + colex.colorize(">", colex.WHITE)
            + " "
        )
        raw_command = get_live_input(styled_prompt).lstrip()
        dev(f"Raw: {raw_command}")
        if raw_command in ("exit", "."):
            break # quit main loop of shell
        elif raw_command == "cls":
            os.system("cls")
            continue
        elif (
            " " in raw_command
            and len(raw_command.split(" ", maxsplit=1)) == 2
            and raw_command.split(" ")[0] == "cd"
        ):
            new_cwd = pathlib.Path(raw_command.split(" ", maxsplit=1)[1]).resolve()
            if new_cwd.exists() and new_cwd.is_dir():
                dev(f"Valid path: $[{new_cwd}]")
                os.chdir(new_cwd)
            else:
                with warn("Tried $[cd] into invalid directory"):
                    warn(f"Attemped: $[{new_cwd}]")
                    if not new_cwd.is_dir():
                        warn("Failed $[.is_dir()] check")
                    if not new_cwd.exists():
                        warn("Failed $[.exists()] check")
            continue

        expanded = expand_keywords(raw_command)
        try:
            command_stack = parse_command(expanded)
        except ValueError as value_error:
            with warn(f"Could not parse command string: $['{raw_command}']"):
                warn(f"Expanded command: $['{expanded}']")
                warn(f"Reason: $[{value_error}]")
                warn("Skipping command...")
            continue # failed to parse command string
        with dev:
            dev(f"Stack: {command_stack}")

        status, result = execute_stack(command_stack)
        if dev_mode:
            print("Process status:", status)
        if result:
            print(result)
        print() # extra whitespace under result
    return 0
