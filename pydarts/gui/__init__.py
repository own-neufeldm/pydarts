import tkinter as tk
from typing import Optional

import customtkinter as ctk


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
