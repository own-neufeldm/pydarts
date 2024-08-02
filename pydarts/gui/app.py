import tkinter as tk
from typing import Iterable

import customtkinter as ctk

import pydarts
from pydarts.gui import BaseStage
from pydarts.gui.pregame import PregameStage


class App(ctk.CTk):
    def __init__(self, enable_debug: bool) -> None:
        super().__init__()
        self.enable_debug = enable_debug
        self.title("PyDarts")
        self.iconbitmap(pydarts.assets_dir / "icon.ico")
        self.grid_columnconfigure(index=0, weight=1)
        self.grid_rowconfigure(index=0, weight=1)

        ctk.set_widget_scaling(2)
        # ctk.set_window_scaling(1.5)

        self.active_stage: BaseStage
        self._load_stage(PregameStage)
        return None

    def _load_stage(self, stage_type: type[BaseStage], *args, **kwargs) -> None:
        if stage_type is PregameStage:
            self.active_stage = stage_type(self, *args, **kwargs)
            width, height = PregameStage.width, PregameStage.height
        self.active_stage.grid(column=0, row=0, sticky="NSWE")
        self.minsize(width, height)
        self.maxsize(width, height)
        x, y = (self.winfo_screenwidth() - width) // 2, (self.winfo_screenheight() - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")
        if self.enable_debug:
            self._enable_debug()
        return None

    def _enable_debug(self):
        highlight_children(self)
        sequences = []
        for sequence in sequences:
            self.bind_all(sequence, self._handle_event)

    def _handle_event(self, event: tk.Event):
        pydarts.logger.debug(
            f"application caught event:\n"
            f"  event: {event!r}\n"
            f"  widget: {event.widget!r}"
        )


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
