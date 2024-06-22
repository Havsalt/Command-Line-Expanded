import pathlib
import os


def collapse_path(path: str | pathlib.Path, /) -> str:
    true_path = (
        pathlib.Path(path)
        if isinstance(path, str)
        else path.resolve()
    )
    firsts = map(lambda segment: segment[0], true_path.parts[1:-1])
    return os.sep.join([true_path.drive, *firsts, true_path.name])
