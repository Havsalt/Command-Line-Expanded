import sys as _sys
import msvcrt as _msvcrt
import string as _string
from typing import Iterable as _Iterable

from strox import (
    get_closest_match as _get_closest_match,
    Budget as _Budget
)


_SPACE = " "
_ENTER = b"\r"
_TAB = b"\t"
_DELETE = b"\x08"
_DELETE_WORD = (b"\x17", b"\x7f")
_CONTROL_C = b"\x03"

_ARROW_MODIFIER = b"\xe0"
_ARROW_LEFT = b"K"
_ARROW_RIGHT = b"M"
# _ARROW_UP = b"H"
# _ARROW_DOWN = b"P"
_ARROW_JUMP_LEFT = b"s"
_ARROW_JUMP_RIGHT = b"t"

_WHITELISTED: tuple[str, ...] = (
    _SPACE,
    *_string.ascii_letters,
    *_string.punctuation,
    *_string.digits
)
_BUDGET = _Budget(
    insertion_cost=0.2,
    substitution_cost=0.8,
    equality_bonus=2
)


def get_live_input( # TODO: add History param
    prompt: str = "",
    /,
    options: _Iterable[str] = ("",),
    *,
    end: str = "\n"
) -> str:
    _sys.stdout.write(prompt)
    _sys.stdout.flush()
    cursor = 0
    written = ""
    predicted = ""
    while (key_code := _msvcrt.getch()) != _ENTER:
        if key_code == _CONTROL_C:
            raise KeyboardInterrupt # TODO: make this a silent error
        
        elif key_code == _ARROW_MODIFIER:
            arrow_code = _msvcrt.getch()
            if arrow_code == _ARROW_LEFT and cursor > 0:
                cursor -= 1
                _sys.stdout.write("\u001b[D")
            elif arrow_code == _ARROW_RIGHT and cursor < len(written):
                cursor += 1
                _sys.stdout.write("\u001b[C")
            _sys.stdout.flush()
            # print(arrow_code)
            continue
        
        elif key_code == _DELETE:
            if written:
                remove_code = f"\u001b[{len(written)}D"
                written = written[:-1] # pop last char in string
                fill_code = written.ljust(len(written) + 1)
                move_code = "\u001b[D"
                _sys.stdout.write(remove_code)
                _sys.stdout.write(fill_code)
                _sys.stdout.write(move_code)
                _sys.stdout.flush()
        
        elif key_code in _DELETE_WORD:
            ignore_first = bool(written) and written[-1] == _SPACE
            while written and (written[-1] != _SPACE or ignore_first):
                if ignore_first:
                    ignore_first = False
                remove_code = f"\u001b[{len(written)}D"
                written = written[:-1] # pop last char in string
                fill_code = written.ljust(len(written) + 1)
                move_code = "\u001b[D"
                _sys.stdout.write(remove_code)
                _sys.stdout.write(fill_code)
                _sys.stdout.write(move_code)
            _sys.stdout.flush()
        
        key = key_code.decode()
        if key not in _WHITELISTED:
            continue
        
        if key not in (_TAB, _DELETE): # ENTER pressed
            if written:
                remove_code = f"\u001b[{len(written)}D"
                _sys.stdout.write(remove_code)
            written += key
            cursor += 1
            _sys.stdout.write(written)
            _sys.stdout.flush()
        
        if key == _TAB and written:
            pattern = written.split()[0] # TODO: move upward, for live recommendations
            predicted = _get_closest_match(pattern, options, budget=_BUDGET)
            remove_code = f"\u001b[{len(written)}D"
            fill_code = predicted.ljust(len(written), " ")
            move_code = (
                f"\u001b[{len(written) - len(predicted)}D"
                if written and (len(written) - len(predicted) > 0)
                else ""
            )
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
    import cl.win_commands as _win_commands
    print(get_live_input("Hello world: ", options=_win_commands.collect()))
