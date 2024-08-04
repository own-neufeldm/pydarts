import tkinter as tk

import customtkinter as ctk

import pydarts
import pydarts.core
import pydarts.gui


class GameStage(pydarts.gui.BaseStage):
    width, height = 2100, 1200

    def __init__(
        self,
        master: ctk.CTk,
        mode: pydarts.core.modes.BaseMode,
        players: list[str],
        *args,
        **kwargs
    ) -> None:
        super().__init__(master, *args, **kwargs)
        return None
