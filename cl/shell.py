from __future__ import annotations

import os

import colex

from .intake import get_live_input
from .pre_process_command import expand_keywords, parse_command, execute_stack
from .dev_utils import dev


def enter_session(dev_mode: bool = False) -> None:
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
            return
        elif raw_command == "cls":
            os.system("cls")
            continue

        expanded = expand_keywords(raw_command)
        command_stack = parse_command(expanded)
        result = execute_stack(command_stack)
        print(result)
