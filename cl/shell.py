from __future__ import annotations

import os

import colex
from actus import warn

from .intake import get_live_input
from .process_command import expand_keywords, parse_command, execute_stack
from .dev_utils import dev


def run(dev_mode: bool = False) -> int:
    if dev_mode:
        dev.enable_output()
    while True:
        prompt = (
            colex.colorize("Enter command", colex.CYAN + colex.BLINK)
            + colex.colorize(":", colex.WHITE)
            + " "
        )
        raw_command = get_live_input(prompt).lstrip()
        dev(f"Raw: {raw_command}")
        if raw_command in ("exit", "."):
            break # quit main loop of shell
        elif raw_command == "cls":
            os.system("cls")
            continue

        expanded = expand_keywords(raw_command)
        try:
            command_stack = parse_command(expanded)
        except ValueError:
            with warn(f"Could not parse command string: $['{raw_command}']"):
                warn(f"Expanded command: $['{expanded}']")
            with dev:
                dev(f"Stack: {command_stack}")

            continue # failed to parse command string
        result = execute_stack(command_stack)
        print(result)
    return 0
