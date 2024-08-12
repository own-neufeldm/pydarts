from dataclasses import dataclass

import customtkinter as ctk

import pydarts
import pydarts.core
import pydarts.gui

state: "State"


@dataclass()
class State():
    mode: pydarts.core.modes.BaseMode
    players: list[pydarts.core.players.Player]


class GameStage(pydarts.gui.BaseStage):
    width, height = 2100, 1200

    def __init__(
        self,
        master: ctk.CTk,
        mode: pydarts.core.modes.BaseMode,
        players: list[pydarts.core.players.Player],
        *args,
        **kwargs
    ) -> None:
        super().__init__(master, *args, **kwargs)
        self.grid_columnconfigure(index=0, weight=1, minsize=(GameStage.width // 3) * 2)
        self.grid_columnconfigure(index=1, weight=1, minsize=(GameStage.width // 3))
        self.grid_rowconfigure(index=0, weight=1)

        self.input_frm = InputFrm(self)
        self.input_frm.grid(column=0, row=0, sticky="NSWE", padx=10, pady=10)

        self.turn_frm = TurnFrm(self)
        self.turn_frm.grid(column=1, row=0, sticky="NSWE", padx=10, pady=10)

        global state
        state = State(mode, players)
        return None


class InputFrm(ctk.CTkFrame):
    def __init__(self, master: GameStage, *args, **kwargs) -> None:
        super().__init__(master, *args, **kwargs)
        return None


class TurnFrm(ctk.CTkFrame):
    def __init__(self, master: GameStage, *args, **kwargs) -> None:
        super().__init__(master, *args, **kwargs)
        self.grid_columnconfigure(index=0, weight=1)
        self.grid_rowconfigure(index=1, weight=1)

        self.turn_order_frm = TurnOrderFrm(self)
        self.turn_order_frm.grid(column=0, row=0, sticky="NSWE", padx=10, pady=10)

        self.active_turn_frm = ActiveTurnFrm(self)
        self.active_turn_frm.grid(column=0, row=1, sticky="NSWE", padx=10, pady=10)
        self.active_turn_frm.active_turn_controls_frm.next_player_btn.configure(
            command=self.turn_order_frm._next_player_cmd
        )
        return None


class TurnOrderFrm(ctk.CTkFrame):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.grid_columnconfigure(index=0, weight=1)
        self.grid_columnconfigure(index=1, weight=1)

        self._get_player_label().grid(column=0, row=0, sticky="NSWE", padx=(10, 5), pady=(10, 5))
        self._get_player_label().grid(column=0, row=1, sticky="NSWE", padx=(10, 5), pady=(5, 5))
        self._get_player_label().grid(column=0, row=2, sticky="NSWE", padx=(10, 5), pady=(5, 5))
        self._get_player_label().grid(column=0, row=3, sticky="NSWE", padx=(10, 5), pady=(5, 10))
        self._get_player_label().grid(column=1, row=0, sticky="NSWE", padx=(5, 10), pady=(10, 5))
        self._get_player_label().grid(column=1, row=1, sticky="NSWE", padx=(5, 10), pady=(5, 5))
        self._get_player_label().grid(column=1, row=2, sticky="NSWE", padx=(5, 10), pady=(5, 5))
        self._get_player_label().grid(column=1, row=3, sticky="NSWE", padx=(5, 10), pady=(5, 10))
        return None

    def _get_player_label(self) -> ctk.CTkLabel:
        return ctk.CTkLabel(
            self,
            fg_color="gray30",
            anchor="w",
            corner_radius=7,
        )

    def _next_player_cmd(self) -> None:
        for position, player in enumerate(state.players, start=1):
            child: ctk.CTkLabel = self.winfo_children()[position-1]
            child.configure(text=f"{position}. {player.name} ({player.score})")
        return None


class ActiveTurnFrm(ctk.CTkFrame):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.grid_columnconfigure(index=0, weight=1)

        self.active_turn_input_frm = ActiveTurnInputFrm(self, fg_color="transparent")
        self.active_turn_input_frm.grid(column=0, row=0, sticky="NSWE", padx=10, pady=(10, 5))

        self.active_turn_controls_frm = ActiveTurnControlsFrm(self, fg_color="transparent")
        self.active_turn_controls_frm.grid(column=0, row=1, sticky="NSWE", padx=10, pady=(5, 10))
        return None


class ActiveTurnInputFrm(ctk.CTkFrame):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.grid_columnconfigure(index=0, weight=1)
        self.grid_columnconfigure(index=1, weight=1)
        self.grid_columnconfigure(index=2, weight=1)

        self.input_1_ntr = ctk.CTkEntry(self)
        self.input_1_ntr.grid(column=0, row=0, sticky="NSWE", padx=(0, 5))

        self.input_2_ntr = ctk.CTkEntry(self)
        self.input_2_ntr.grid(column=1, row=0, sticky="NSWE", padx=(5, 5))

        self.input_3_ntr = ctk.CTkEntry(self)
        self.input_3_ntr.grid(column=2, row=0, sticky="NSWE", padx=(5, 0))
        return None


class ActiveTurnControlsFrm(ctk.CTkFrame):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.grid_columnconfigure(index=0, weight=1)
        self.grid_columnconfigure(index=1, weight=1)

        self.undo_btn = ctk.CTkButton(self, text="Undo")
        self.undo_btn.grid(column=0, row=0, sticky="NSWE", padx=(0, 5))

        self.next_player_btn = ctk.CTkButton(self, text="Next player")
        self.next_player_btn.grid(column=1, row=0, sticky="NSWE", padx=(5, 0))
        return None
