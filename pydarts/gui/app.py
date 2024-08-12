import customtkinter as ctk

import pydarts
import pydarts.core
import pydarts.gui
import pydarts.gui.game
import pydarts.gui.postgame
import pydarts.gui.pregame


class App(ctk.CTk):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.title("PyDarts")
        self.iconbitmap(pydarts.assets_dir / "icon.ico")
        self.grid_columnconfigure(index=0, weight=1)
        self.grid_rowconfigure(index=0, weight=1)
        ctk.set_widget_scaling(2)

        self.pregame_frm: pydarts.gui.pregame.RootFrm
        self.game_frm: pydarts.gui.game.RootFrm
        self.postgame_frm: pydarts.gui.postgame.RootFrm

        self.pregame_frm = pydarts.gui.pregame.RootFrm(self)
        self.pregame_frm.state.start_game.trace_add("write", self._start_game_cmd)
        self._load_stage(self.pregame_frm)
        return None

    def _load_stage(
        self,
        stage: (
            pydarts.gui.pregame.RootFrm |
            pydarts.gui.game.RootFrm |
            pydarts.gui.postgame.RootFrm
        ),
    ) -> None:
        width, height = stage.width, stage.height
        stage.grid(column=0, row=0, sticky="NSWE")
        self.minsize(width, height)
        self.maxsize(width, height)
        x, y = (self.winfo_screenwidth() - width) // 2, (self.winfo_screenheight() - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")
        return None

    def _start_game_cmd(self, *args) -> None:
        mode = pydarts.core.get_mode_by_name(self.pregame_frm.state.mode_name.get())
        players = [
            pydarts.core.players.Player(player, mode.get_initial_score())
            for player in self.pregame_frm.state.player_names.get()
        ]
        self.pregame_frm.destroy()
        self.game_frm = pydarts.gui.game.RootFrm(self, mode=mode(), players=players)
        self._load_stage(self.game_frm)
        return None
