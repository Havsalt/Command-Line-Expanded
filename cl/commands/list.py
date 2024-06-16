from __future__ import annotations as _annotations

from typing import TYPE_CHECKING as _TYPE_CHECKING

from strox import (
    get_similarity_score as _get_similarity_score,
    Budget as _Budget
)

import colex as _colex
from actus import (
    info as _info,
    LogSection as _LogSection
)

from ._command import Command as _Command
from .. import win_commands as _win_commands
from rich.pretty import pprint as _pprint

if _TYPE_CHECKING:
    from ..parser_args import ParserArguments as _ParserArguments


_list_command = _LogSection("Commands")

_COMMAND_SORT_BUDGET = _Budget(
    substitution_cost=10,
    insertion_cost=0.1,
    deletion_cost=10,
    equality_bonus=20
)


class List(_Command):
    listing_choices: set[str] = {
        "config",
        "scripts",
        "commands"
    }
    
    def setup(self) -> None:
        self.command_parser.add_argument("what", choices=self.listing_choices)
        self.command_parser.add_argument("search", nargs="?")

    def process(self, args: _ParserArguments) -> None:
        _info(f"Listing registered {args.what}:")
        if args.what == "config":
            # top_level_keys = _config.get().keys() # iterator will be exhausted, only use once
            # longest_top_level_length = len(max(top_level_keys, key=len))
            for key, value in _config.get().items():
                painted_key = _colex.colorize(key, _colex.RED)
                print(painted_key, end=" ")
                _pprint(value, expand_all=True)
            print()
            return
        elif args.what == "commands":
            commands = set((
                *_win_commands.collect(),
                *_config.get()["scripts"].keys()
            ))
            if args.search is not None:
                def sort_function(command_name: str) -> float:
                    return _get_similarity_score(command_name, args.search, budget=_COMMAND_SORT_BUDGET)
                sorted_commands = sorted(commands, key=sort_function)
            else:
                sorted_commands = sorted(commands)
            for command in sorted_commands:
                print("-", command)
            return
        # actual sections present in the config file
        field_keys = _config.get()[args.what].keys() # iterator will be exhausted, only use once
        longest_field_length = len(max(field_keys, key=len))
        for key, value in _config.get()[args.what].items():
            padded_key = key.ljust(longest_field_length)
            painted_key = _colex.colorize(padded_key, _colex.RED)
            print(painted_key, end=" ")
            _pprint(value, expand_all=True)
        print()
