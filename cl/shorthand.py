import pathlib as _pathlib
import re as _re
from functools import wraps as _wraps
from typing import (
    TypeAlias as _TypeAlias,
    Callable as _Callable
)

import config as _config

_ConverterFunction: _TypeAlias = _Callable[..., str]


_registry: dict[str, _ConverterFunction] = {}
def _register(pattern: str) -> _Callable[[_ConverterFunction], _ConverterFunction]:
    def decorator(function: _ConverterFunction) -> _ConverterFunction:
        @_wraps(function)
        def wrapper(*args: str) -> str:
            result = function(*args)
            return result
        _registry[function.__name__.removeprefix("_")] = wrapper
        return wrapper
    return decorator


@_register("{prefix}/{path}/?")
def _pycli(*, prefix: str, path: str) -> str:
    location = _config.get()["shorthand"]["pycli"]
    return str(_pathlib.Path(location) / path)


def substitute(arguments: list[str], /) -> list[str]:
    final: list[str] = []
    prefix = _config.get()["shorthand"]["prefix"]["symbol"]
    for argument in arguments:
        if argument.startswith(prefix):
            shortcut = argument.removeprefix(prefix)
            if shortcut == "prefix":
                continue
            for known_shortcut, full_path in _config.get()["shorthand"].items():
                if known_shortcut == shortcut:
                    final.append(full_path)
        else:
            final.append(argument)
    return final
