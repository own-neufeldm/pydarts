import customtkinter as ctk

import pydarts
import pydarts.core
import pydarts.core.modes
import pydarts.core.players
import pydarts.gui
import pydarts.gui.game
import pydarts.gui.postgame
import pydarts.gui.pregame


class App(ctk.CTk):
    class State(pydarts.gui.State):
        def __init__(self) -> None:
            super().__init__()  # only allowed usage of this method is here
            return None

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.readonly_state = self.State()  # name 'state' is reserved
        self.title("PyDarts")
        self.iconbitmap(pydarts.assets_dir / "icon.ico")
        self.grid_columnconfigure(index=0, weight=1)
        self.grid_rowconfigure(index=0, weight=1)

        ctk.deactivate_automatic_dpi_awareness()
        self.readonly_state.widget_scaling.trace_add("write", self._widget_scaling_changed_cmd)
        self.readonly_state.widget_scaling.set(2.5)
        self.readonly_state.appearance_mode.trace_add("write", self._appearance_mode_changed_cmd)
        self.readonly_state.appearance_mode.set("dark")

        self.pregame_frm: pydarts.gui.pregame.RootFrm
        self.game_frm: pydarts.gui.game.RootFrm
        self.postgame_frm: pydarts.gui.postgame.RootFrm

        self.pregame_frm = pydarts.gui.pregame.RootFrm(self)
        self.pregame_frm.state.start_game.trace_add("write", self._start_game_cmd)
        self._load_stage(self.pregame_frm)
        return None

    def _widget_scaling_changed_cmd(self, *args) -> None:
        value = self.readonly_state.widget_scaling.get()
        ctk.set_widget_scaling(value)
        return None

    def _appearance_mode_changed_cmd(self, *args) -> None:
        value = self.readonly_state.appearance_mode.get()
        ctk.set_appearance_mode(value)
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
        if not self.pregame_frm.state.start_game.get():
            return None
        mode = pydarts.core.modes.get_mode_by_name(self.pregame_frm.state.mode_name.get())
        players = [
            pydarts.core.players.Player(player, mode.get_initial_score())
            for player in self.pregame_frm.state.player_names.get()
        ]
        self.pregame_frm.destroy()
        self.game_frm = pydarts.gui.game.RootFrm(self, mode=mode(), players=players)
        self._load_stage(self.game_frm)
        return None
