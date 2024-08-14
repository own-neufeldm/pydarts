import functools

import customtkinter as ctk

import pydarts
import pydarts.core
import pydarts.core.modes
import pydarts.core.players
import pydarts.gui


class RootFrm(ctk.CTkFrame):
    class State(pydarts.gui.State):
        def __init__(self, master_state: pydarts.gui.State) -> None:
            for name, var in vars(master_state).items():
                setattr(self, name, var)
            self.mode = pydarts.gui.TypedVar(value_type=type[pydarts.core.modes.BaseMode])
            self.players = pydarts.gui.TypedVar(value_type=list[pydarts.core.players.Player])
            return None

    def __init__(
        self,
        master: ctk.CTk,
        *args,
        mode: type[pydarts.core.modes.BaseMode],
        players: list[pydarts.core.players.Player],
        **kwargs
    ) -> None:
        super().__init__(master, *args, **kwargs)
        self.state = self.State(master.readonly_state)  # type: ignore
        self.grid_columnconfigure(index=0, weight=1, minsize=(self.width // 3) * 2)
        self.grid_columnconfigure(index=1, weight=1, minsize=(self.width // 3))
        self.grid_rowconfigure(index=0, weight=1)

        self.input_frm = InputFrm(self)
        self.input_frm.grid(column=0, row=0, sticky="NSWE", padx=10, pady=10)

        self.turn_frm = TurnFrm(self)
        self.turn_frm.grid(column=1, row=0, sticky="NSWE", padx=10, pady=10)

        self.state.mode.set(mode)
        self.state.players.set(players)
        return None

    @property
    def width(self) -> int:
        return self.winfo_screenwidth() // 5 * 4

    @property
    def height(self) -> int:
        return self.winfo_screenheight() // 5 * 4


class InputFrm(ctk.CTkFrame):
    class State(RootFrm.State):
        def __init__(self, master_state: RootFrm.State) -> None:
            for name, var in vars(master_state).items():
                setattr(self, name, var)
            self.mulitplier = ctk.IntVar()
            return None

    def __init__(self, master: RootFrm, *args, **kwargs) -> None:
        super().__init__(master, *args, **kwargs)
        self.state = self.State(master.state)
        for column in range(4):
            self.grid_columnconfigure(index=column, weight=1)
        for row in range(7):
            self.grid_rowconfigure(index=row, weight=1)

        font = ctk.CTkFont(family="Roboto", size=18, weight="normal")
        self.single_radbtn = ctk.CTkRadioButton(
            self,
            text="Single",
            command=self._multiplier_selected_cmd,
            variable=self.state.mulitplier,
            value=1,
            font=font,
        )
        self.single_radbtn.grid(column=0, row=0, sticky="NS", padx=10, pady=10)

        self.double_radbtn = ctk.CTkRadioButton(
            self,
            text="Double",
            command=self._multiplier_selected_cmd,
            variable=self.state.mulitplier,
            value=2,
            font=font,
        )
        self.double_radbtn.grid(column=1, row=0, sticky="NS", padx=10, pady=10)

        self.triple_radbtn = ctk.CTkRadioButton(
            self,
            text="Triple",
            command=self._multiplier_selected_cmd,
            variable=self.state.mulitplier,
            value=3,
            font=font,
        )
        self.triple_radbtn.grid(column=2, row=0, sticky="NS", padx=10, pady=10)

        self.input_btn_s: list[ctk.CTkButton] = []

        miss_btn = ctk.CTkButton(
            self,
            text="Miss",
            command=lambda: self._input_provided_cmd(0),
            font=font,
        )
        miss_btn.grid(column=3, row=0, sticky="NSWE", padx=10, pady=10)
        self.input_btn_s.append(miss_btn)

        for row in range(1, 6):
            for column in range(0, 4):
                value = (row-1)*4 + (column+1)
                input_btn = ctk.CTkButton(
                    self,
                    text=str(value),
                    command=functools.partial(self._input_provided_cmd, value),
                    font=font,
                )
                input_btn.grid(column=column, row=row, sticky="NSWE", padx=10, pady=10)
                self.input_btn_s.append(input_btn)

        input_btn = ctk.CTkButton(
            self,
            text="25",
            command=lambda: self._input_provided_cmd(25),
            font=font,
        )
        input_btn.grid(column=0, row=6, columnspan=4, sticky="NSWE", padx=10, pady=10)
        self.input_btn_s.append(input_btn)
        return None

    def _multiplier_selected_cmd(self, *args) -> None:
        pydarts.logger.info(f"Multiplier selected: {self.state.mulitplier.get()}")
        return None

    def _input_provided_cmd(self, value: int) -> None:
        pydarts.logger.info(f"Value provided: {value}")
        return None


class TurnFrm(ctk.CTkFrame):
    class State(RootFrm.State):
        def __init__(self, master_state: RootFrm.State) -> None:
            for name, var in vars(master_state).items():
                setattr(self, name, var)
            return None

    def __init__(self, master: RootFrm, *args, **kwargs) -> None:
        super().__init__(master, *args, **kwargs)
        self.state = self.State(master.state)
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
    class State(TurnFrm.State):
        def __init__(self, master_state: TurnFrm.State) -> None:
            for name, var in vars(master_state).items():
                setattr(self, name, var)
            return None

    def __init__(self, master: TurnFrm, *args, **kwargs) -> None:
        super().__init__(master, *args, **kwargs)
        self.state = self.State(master.state)
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
        for position, player in enumerate(self.state.players.get(), start=1):
            child: ctk.CTkLabel = self.winfo_children()[position-1]
            child.configure(text=f"{position}. {player.name} ({player.score})")
        return None


class ActiveTurnFrm(ctk.CTkFrame):
    class State(TurnFrm.State):
        def __init__(self, master_state: TurnFrm.State) -> None:
            for name, var in vars(master_state).items():
                setattr(self, name, var)
            return None

    def __init__(self, master: TurnFrm, *args, **kwargs) -> None:
        super().__init__(master, *args, **kwargs)
        self.state = self.State(master.state)
        self.grid_columnconfigure(index=0, weight=1)

        self.active_turn_input_frm = ActiveTurnInputFrm(self, fg_color="transparent")
        self.active_turn_input_frm.grid(column=0, row=0, sticky="NSWE", padx=10, pady=(10, 5))

        self.active_turn_controls_frm = ActiveTurnControlsFrm(self, fg_color="transparent")
        self.active_turn_controls_frm.grid(column=0, row=1, sticky="NSWE", padx=10, pady=(5, 10))
        return None


class ActiveTurnInputFrm(ctk.CTkFrame):
    class State(ActiveTurnFrm.State):
        def __init__(self, master_state: ActiveTurnFrm.State) -> None:
            for name, var in vars(master_state).items():
                setattr(self, name, var)
            return None

    def __init__(self, master: ActiveTurnFrm, *args, **kwargs) -> None:
        super().__init__(master, *args, **kwargs)
        self.state = self.State(master.state)
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
    class State(ActiveTurnFrm.State):
        def __init__(self, master_state: ActiveTurnFrm.State) -> None:
            for name, var in vars(master_state).items():
                setattr(self, name, var)
            return None

    def __init__(self, master: ActiveTurnFrm, *args, **kwargs) -> None:
        super().__init__(master, *args, **kwargs)
        self.state = self.State(master.state)
        self.grid_columnconfigure(index=0, weight=1)
        self.grid_columnconfigure(index=1, weight=1)

        self.undo_btn = ctk.CTkButton(self, text="Undo")
        self.undo_btn.grid(column=0, row=0, sticky="NSWE", padx=(0, 5))

        self.next_player_btn = ctk.CTkButton(self, text="Next player")
        self.next_player_btn.grid(column=1, row=0, sticky="NSWE", padx=(5, 0))
        return None
