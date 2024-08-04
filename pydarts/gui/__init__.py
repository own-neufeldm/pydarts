import tkinter as tk
from typing import Iterable

import customtkinter as ctk


class BaseStage(ctk.CTkFrame):
    def __init__(self, master: ctk.CTk, *args, **kwargs) -> None:
        super().__init__(master, *args, **kwargs)
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
