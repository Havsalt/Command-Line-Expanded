import sys as _sys
import msvcrt as _msvcrt
import string as _string
from typing import Iterable as _Iterable

from levenshtein import (
    get_closest_match as _get_closest_match,
    Budget as _Budget
)


_SPACE = " "
_ENTER = "\r"
_TAB = "\t"
_DELETE = "\x08"
_WHITELISTED: tuple[str, ...] = (
    _SPACE,
    _TAB,
    _DELETE,
    *_string.ascii_letters,
    *_string.punctuation,
    *_string.digits
)
_BUDGET = _Budget(
    insertion_cost=0.2,
    substitution_cost=0.8,
    equality_bonus=2
)


def get_live_input(
    prompt: str = "",
    /,
    options: _Iterable[str] = ("",),
    *,
    end: str = "\n"
) -> str:
    _sys.stdout.write(prompt)
    _sys.stdout.flush()
    written = ""
    predicted = ""
    while (key := chr(int.from_bytes(_msvcrt.getch(), "big"))) != _ENTER:
        if key not in _WHITELISTED:
            continue
        if key not in (_TAB, _DELETE): # ENTER pressed
            if written:
                remove_code = f"\u001b[{len(written)}D"
                _sys.stdout.write(remove_code)
            written += key
            _sys.stdout.write(written)
            _sys.stdout.flush()
        if key == _DELETE:
            if written:
                remove_code = f"\u001b[{len(written)}D"
                written = written[:-1] # pop last char in string
                fill_code = written.ljust(len(written) + 1)
                move_code = "\u001b[D"
                _sys.stdout.write(remove_code)
                _sys.stdout.write(fill_code)
                _sys.stdout.write(move_code)
                _sys.stdout.flush()
        if key == _TAB and written:
            pattern = written.split()[0] # TODO: move upward, for live recommendations
            predicted = _get_closest_match(pattern, options, budget=_BUDGET)
            remove_code = f"\u001b[{len(written)}D"
            fill_code = predicted.ljust(len(written), " ")
            move_code = (f"\u001b[{len(written) - len(predicted)}D"
                         if written and (len(written) - len(predicted) > 0)
                         else "")
            written = predicted
            _sys.stdout.write(remove_code)
            _sys.stdout.write(fill_code)
            _sys.stdout.write(move_code)
            _sys.stdout.flush()
        # TODO: write and flush
        # _sys.stdout.write("\n---")
        # _sys.stdout.write("\n" + written)
        # _sys.stdout.write("\n" + predicted)
        # _sys.stdout.write("\n===\n")
    _sys.stdout.write(end)
    _sys.stdout.flush()
    return written


if __name__ == "__main__":
    import win_commands as _win_commands
    print(get_live_input("Hello world: ", options=_win_commands.collect()))
