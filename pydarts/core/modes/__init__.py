import functools
import importlib
import inspect
from pathlib import Path

import pydarts.core._modes
from pydarts.core._modes import BaseMode


class ModeNotFoundError(Exception):
    """
    Mode with the given name not found.
    """

    def __init__(self, mode_name: str, *args: object) -> None:
        super().__init__(*args)
        self.mode_name = mode_name
        return None

    def __str__(self) -> str:
        return f"Mode {self.mode_name} not found."


@functools.cache
def get_modes() -> list[type[BaseMode]]:
    modes: list[type[BaseMode]] = []
    for file in Path(pydarts.core._modes.__file__).parent.glob("*.py"):
        if file.stem in ["__init__"]:
            continue
        module_name = f"{pydarts.core._modes.__name__}.{file.stem}"
        module = importlib.import_module(module_name)
        _, mode = inspect.getmembers(
            module,
            lambda m: (
                inspect.isclass(m)
                and m is not BaseMode
                and issubclass(m, BaseMode)
                and m.__name__ == "Mode"
            )
        )[0]
        modes.append(mode)
    return modes


@functools.cache
def get_mode_names() -> list[str]:
    return [mode.get_name() for mode in get_modes()]


def get_mode_by_name(name: str) -> type[BaseMode]:
    for mode in get_modes():
        if mode.get_name() == name:
            return mode
    raise ModeNotFoundError(name)
