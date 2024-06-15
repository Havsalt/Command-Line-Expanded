import pathlib
import shlex
import os
from argparse import ArgumentParser

from actus import info, warn
import colex

from . import (
    shorthand,
    win_commands,
    intake
)


def enter_session(context: ArgumentParser) -> None:
    parser = context # alias
    # main loop
    info("Started 'cl' session")
    options = win_commands.collect()
    while True:
        # raw_command = input("Enter command: ")
        prompt = f"{colex.colorize('(Cl)', colex.SEA_GREEN)} {pathlib.Path.cwd().stem}: "
        raw_command = intake.get_live_input(prompt, options=options)
        command_parts = shlex.split(raw_command)
        match command_parts:
            case ["exit", *_]:
                info(f"Exited '{parser.usage}' session")
                exit(0)
            case [parser.usage]: # "cl"
                warn(f"Cannot run command '{parser.usage}' from '{parser.usage}' session")
                continue
            case [command, *arguments]:
                substituted_arguments = shorthand.substitute(arguments)
                final_command = command + " " + " ".join(substituted_arguments)
                os.system(final_command)
            case [command]:
                os.system(raw_command)