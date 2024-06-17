from argparse import Namespace as _Namespace
from typing import Literal as _Literal


class ParserArguments(_Namespace):
    command: (
        _Literal["install"] |
        _Literal["register"] |
        _Literal["gather"] |
        _Literal["list"] |
        _Literal["set"] |
        None
    )
    command_name: str
    command_directory: str
    what: _Literal["config", "scripts"]
    search: str
    section: str
    key: str
    value: str
    dev_mode: bool
