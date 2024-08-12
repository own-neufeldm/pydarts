import tkinter as tk

import customtkinter as ctk

import pydarts
import pydarts.core
import pydarts.gui
from pydarts.gui import BaseStage
from pydarts.gui.game import GameStage
from pydarts.gui.pregame import Root


class App(ctk.CTk):
    def __init__(self, enable_debug: bool) -> None:
        super().__init__()
        self.enable_debug = enable_debug
        self.title("PyDarts")
        self.iconbitmap(pydarts.assets_dir / "icon.ico")
        self.grid_columnconfigure(index=0, weight=1)
        self.grid_rowconfigure(index=0, weight=1)
        ctk.set_widget_scaling(2)

        self.active_stage: BaseStage
        self._load_stage(Root)
        return None

    def _load_stage(self, stage_type: type[BaseStage], **kwargs) -> None:
        if stage_type is Root:
            self.active_stage = Root(self, **kwargs)
            width, height = Root.width, Root.height
            self.active_stage.start_btn.configure(command=self._start_game_cmd)
        if stage_type is GameStage:
            self.active_stage.destroy()
            self.active_stage = GameStage(self, **kwargs)
            width, height = GameStage.width, GameStage.height
        self.active_stage.grid(column=0, row=0, sticky="NSWE")
        self.minsize(width, height)
        self.maxsize(width, height)
        x, y = (self.winfo_screenwidth() - width) // 2, (self.winfo_screenheight() - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")
        if self.enable_debug:
            self._enable_debug()
        return None

    def _enable_debug(self):
        pydarts.gui.highlight_children(self)
        sequences = []
        for sequence in sequences:
            self.bind_all(sequence, self._handle_event)

    def _handle_event(self, event: tk.Event):
        pydarts.logger.debug(
            f"application caught event:\n"
            f"  event: {event!r}\n"
            f"  widget: {event.widget!r}"
        )

    def _start_game_cmd(self) -> None:
        stage: Root = self.active_stage  # type: ignore
        mode = pydarts.core.get_mode_by_name(stage.state.mode_name.get())
        players = [
            pydarts.core.players.Player(player, mode.get_initial_score())
            for player in stage.state.player_names.get()
        ]
        self._load_stage(GameStage, mode=mode, players=players)
        return None
