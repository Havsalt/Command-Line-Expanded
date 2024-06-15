from __future__ import annotations as _annotations

import pathlib as _pathlib
from typing import Any as _Any

import toml as _toml

from .constants import CONFIG_FILEPATH as _CONFIG_FILEPATH


_singleton: Config | None = None

class Config(dict[str, _Any]): ...


def _set_defaults(config: Config) -> None:
    config.setdefault("scripts", dict())
    config.setdefault("shorthand", dict())


def load() -> Config:
    # NOTE: config file cannot contain top level fields!
    current_directory = _pathlib.Path(__file__).parent # NOTE: not current WORKING directory
    config_file = current_directory / _CONFIG_FILEPATH
    if not config_file.exists():
        config_file.touch()
    config = Config(_toml.loads(config_file.read_text(encoding="utf-8")))
    _set_defaults(config)
    return config


def get() -> Config:
    global _singleton
    if _singleton is not None:
        return _singleton
    _singleton = load()
    return _singleton


def save() -> None:
    config = get()
    current_directory = _pathlib.Path(__file__).parent # NOTE: not current WORKING directory
    config_file = current_directory / _CONFIG_FILEPATH
    fd = config_file.open(mode="w", encoding="utf-8")
    _toml.dump(config, fd)
    fd.close()
