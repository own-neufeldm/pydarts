import tkinter as tk
from typing import Iterable, Optional

import customtkinter as ctk


class BaseStage(ctk.CTkFrame):
    def __init__(self, master: ctk.CTk, *args, **kwargs) -> None:
        super().__init__(master, *args, **kwargs)
        return None


class StrListVar(ctk.StringVar):
    def __init__(
        self,
        master: Optional[tk.Misc] = None,
        value: Optional[list[str]] = None,
        name: Optional[str] = None,
        separator: str = ",",
    ) -> None:
        str_value = separator.join(value) if value is not None else ""
        super().__init__(master, str_value, name)
        self.separator = separator
        return None

    def get(self) -> list[str]:
        value = super().get()
        return value.split(self.separator) if value else []

    def set(self, value: list[str]) -> None:
        super().set(self.separator.join(value))
        return None


def highlight_children(parent: tk.Misc):
    for widget in walk_children(parent):
        try:
            widget.configure(borderwidth=1, relief="solid")  # type: ignore
        except (tk.TclError, ValueError):
            # widget does not support borders, fine
            pass


def walk_children(parent: tk.Misc, max_depth: int = -1) -> Iterable[tk.Misc]:
    children = [(child, max_depth) for child in reversed(parent.winfo_children())]
    while children:
        child, max_depth = children.pop()
        yield child
        if max_depth == 0:
            continue
        for grandchild in reversed(child.winfo_children()):
            children.append((grandchild, max_depth - 1))
