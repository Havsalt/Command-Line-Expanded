import pathlib as _pathlib
import winreg as _winreg
import os as _os


def add_to_path(directory_path: str | _pathlib.Path) -> None:
    resolved_path = _pathlib.Path(directory_path).resolve()
    if not resolved_path.exists():
        raise ValueError(f"cannot add {directory_path} to PATH, as it does not exist")
    key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER,
                         sub_key="Environment",
                         reserved=int(False),
                         access=_winreg.KEY_ALL_ACCESS)
    path_value, _ = _winreg.QueryValueEx(key, "PATH")
    if str(directory_path) not in path_value.split(_os.pathsep):
        new_path_value = ((path_value + _os.pathsep + str(directory_path))
                        .replace(_os.pathsep*2, _os.pathsep)
                        .replace(_os.pathsep*2, _os.pathsep))
        _winreg.SetValueEx(key,
                          "PATH",
                          int(False),
                          _winreg.REG_EXPAND_SZ,
                          new_path_value)
