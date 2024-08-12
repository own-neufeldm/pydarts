import customtkinter as ctk

import pydarts
import pydarts.core
import pydarts.gui


class RootFrm(ctk.CTkFrame):
    width, height = 1200, 750

    class State():
        def __init__(self) -> None:
            return None

    def __init__(self, master: ctk.CTk, *args, **kwargs) -> None:
        super().__init__(master, *args, **kwargs)
        self.state = self.State()
        return None
