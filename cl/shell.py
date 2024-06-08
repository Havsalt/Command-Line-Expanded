import pathlib
import os
from argparse import ArgumentParser

import shorthand
import win_commands
import logger
import intake
import shlex
import color
from color import paint


def enter_session(context: ArgumentParser) -> None:
    parser = context # alias
    # main loop
    logger.info("Started 'cl' session")
    options = win_commands.collect()
    while True:
        # raw_command = input("Enter command: ")
        prompt = f"{paint('(Cl)', color.SEA_GREEN)} {pathlib.Path.cwd().stem}: "
        raw_command = intake.get_live_input(prompt, options=options)
        command_parts = shlex.split(raw_command)
        match command_parts:
            case ["exit", *_]:
                logger.info(f"Exited '{parser.usage}' session")
                exit(0)
            case [parser.usage]: # "cl"
                logger.warn(f"Cannot run command '{parser.usage}' from '{parser.usage}' session")
                continue
            case [command, *arguments]:
                substituted_arguments = shorthand.substitute(arguments)
                final_command = command + " " + " ".join(substituted_arguments)
                os.system(final_command)
            case [command]:
                os.system(raw_command)