import inspect

from . import modes, players


def get_modes() -> list[type[modes.BaseMode]]:
    return [
        member for _, member in
        inspect.getmembers(
            modes,
            lambda m: (
                inspect.isclass(m)
                and m is not modes.BaseMode
                and issubclass(m, modes.BaseMode)
            ),
        )
    ]


def get_mode_names() -> list[str]:
    return [mode.get_name() for mode in get_modes()]


def get_mode_by_name(name: str) -> type[modes.BaseMode]:
    for mode in get_modes():
        if mode.get_name() == name:
            return mode
    raise ValueError(f"No mode named {name!r}.")
