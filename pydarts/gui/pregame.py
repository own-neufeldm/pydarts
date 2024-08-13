import re

import customtkinter as ctk

import pydarts
import pydarts.core
import pydarts.gui


class RootFrm(ctk.CTkFrame):
    width, height = 1200, 750

    class State():
        def __init__(self) -> None:
            self.mode_name = ctk.StringVar()  # use mode_type to check if mode changed
            self.mode_type = pydarts.gui.TypedVar(value_type=type[pydarts.core.modes.BaseMode])
            self.max_players = ctk.IntVar()
            self.player_names = pydarts.gui.TypedVar(value_type=list[str])
            self.start_game = ctk.BooleanVar()
            return None

    def __init__(self, master: ctk.CTk, *args, **kwargs) -> None:
        super().__init__(master, *args, **kwargs)
        self.state = self.State()
        self.grid_columnconfigure(index=0, weight=1, minsize=self.width // 2)
        self.grid_columnconfigure(index=1, weight=1, minsize=self.width // 2)
        self.grid_rowconfigure(index=0, weight=1)

        self.mode_frm = ModeFrm(self)
        self.mode_frm.grid(column=0, row=0, sticky="NSWE", padx=10, pady=10)

        self.players_frm = PlayersFrm(self)
        self.players_frm.grid(column=1, row=0, sticky="NSWE", padx=10, pady=10)
        self.state.player_names.trace_add("write", self._player_names_changed_cmd)

        self.start_btn = ctk.CTkButton(self, text="Start", command=self._game_started_cmd)
        self.start_btn.grid(column=0, row=1, columnspan=2, sticky="NSWE", padx=10, pady=(0, 10))
        self.start_btn.configure(state="disabled")

        self.state.mode_name.set(pydarts.core.get_modes()[0].get_name())
        self.state.max_players.set(8)
        self.player_names = self.state.player_names.set([])
        return None

    def _player_names_changed_cmd(self, *args) -> None:
        player_names = self.state.player_names.get()
        if player_names:
            self.start_btn.configure(state="enabled")
        else:
            self.start_btn.configure(state="disabled")
        return None

    def _game_started_cmd(self, *args) -> None:
        self.state.start_game.set(True)
        return None


class ModeFrm(ctk.CTkFrame):
    class State():
        def __init__(self, state: RootFrm.State) -> None:
            self.mode_name = state.mode_name
            self.mode_type = state.mode_type
            self.max_players = state.max_players
            self.player_names = state.player_names
            self.start_game = state.start_game
            return None

    def __init__(self, master: RootFrm, *args, **kwargs) -> None:
        super().__init__(master, *args, **kwargs)
        self.state = self.State(master.state)
        self.grid_columnconfigure(index=0, weight=1)
        self.grid_rowconfigure(index=3, weight=1)

        self.title_lbl = ctk.CTkLabel(self, text="Game mode", fg_color="gray30", corner_radius=6)
        self.title_lbl.grid(column=0, row=0, sticky="NSWE", padx=10, pady=(10, 5))

        # only allowed bind for mode_name, use mode_type everywhere else
        self.state.mode_name.trace_add("write", self._mode_name_changed_cmd)
        self.state.mode_type.trace_add("write", self._mode_type_changed_cmd)

        self.selection_cmbbox = ctk.CTkComboBox(
            self,
            variable=self.state.mode_name,
            values=pydarts.core.get_mode_names(),
            state="readonly",
        )
        self.selection_cmbbox.grid(column=0, row=1, sticky="NSWE", padx=10, pady=(5, 5))

        self.description_lbl = ctk.CTkLabel(
            self,
            text="Please select a game mode.",
            anchor="nw",
            justify="left",
            wraplength=250,
        )
        self.description_lbl.grid(column=0, row=2, sticky="NSWE", padx=10, pady=(5, 5))

        self.options_sfrm = OptionsFrm(self)
        self.options_sfrm.grid(column=0, row=3, sticky="NSWE", padx=10, pady=(5, 10))
        return None

    def _mode_name_changed_cmd(self, *args) -> None:
        # somehow 'write' is triggered twice, but only the second event has a value
        if not (selection := self.state.mode_name.get()):
            return None
        new_mode_type = pydarts.core.get_mode_by_name(selection)
        try:
            current_mode_type = self.state.mode_type.get()
        except AttributeError:
            current_mode_type = None
        if new_mode_type is current_mode_type:
            return None
        self.state.mode_type.set(new_mode_type)
        return None

    def _mode_type_changed_cmd(self, *args) -> None:
        text = self.state.mode_type.get().get_description()
        self.description_lbl.configure(text=text)
        return None


class OptionsFrm(ctk.CTkFrame):
    class State():
        def __init__(self, state: ModeFrm.State) -> None:
            self.mode_name = state.mode_name
            self.mode_type = state.mode_type
            self.max_players = state.max_players
            self.player_names = state.player_names
            self.start_game = state.start_game
            return None

    def __init__(self, master: ModeFrm, *args, **kwargs) -> None:
        super().__init__(master, *args, **kwargs)
        self.state = self.State(master.state)
        self.grid_columnconfigure(index=0, weight=1)
        self.grid_rowconfigure(index=1, weight=1)

        self.title_lbl = ctk.CTkLabel(self, text="Options", fg_color="gray30", corner_radius=6)
        self.title_lbl.grid(column=0, row=0, sticky="NSWE", padx=10, pady=(10, 5))

        self.options_sfrm = OptionsSfrm(self)
        self.options_sfrm.grid(column=0, row=1, sticky="NSWE", padx=10, pady=(5, 10))
        return None


class OptionsSfrm(ctk.CTkScrollableFrame):
    class State():
        def __init__(self, state: OptionsFrm.State) -> None:
            self.mode_name = state.mode_name
            self.mode_type = state.mode_type
            self.max_players = state.max_players
            self.player_names = state.player_names
            self.start_game = state.start_game
            return None

    def __init__(self, master: OptionsFrm, *args, **kwargs) -> None:
        super().__init__(master, *args, **kwargs)
        self.state = self.State(master.state)
        self.grid_columnconfigure(index=0, weight=1)

        self.option_chkbox_s: list[ctk.CTkCheckBox] = []
        self.state.mode_type.trace_add("write", self._mode_type_changed_cmd)
        return None

    def _mode_type_changed_cmd(self, *args) -> None:
        for option_chkbox in self.option_chkbox_s:
            option_chkbox.destroy()
        self.option_chkbox_s.clear()
        for row, option in enumerate(self.state.mode_type.get().get_options()):
            option_chkbox = ctk.CTkCheckBox(self, text=option)
            option_chkbox.grid(column=0, row=row, sticky="NSWE", padx=5, pady=10)
            self.option_chkbox_s.append(option_chkbox)
        return None


class PlayersFrm(ctk.CTkFrame):
    class State():
        def __init__(self, state: RootFrm.State) -> None:
            self.mode_name = state.mode_name
            self.mode_type = state.mode_type
            self.max_players = state.max_players
            self.player_names = state.player_names
            self.start_game = state.start_game
            return None

    def __init__(self, master: RootFrm, *args, **kwargs) -> None:
        super().__init__(master, *args, **kwargs)
        self.state = self.State(master.state)
        self.grid_columnconfigure(index=0, weight=1)
        self.grid_rowconfigure(index=2, weight=1)

        self.title_lbl = ctk.CTkLabel(self, text="Players", fg_color="gray30", corner_radius=6)
        self.title_lbl.grid(row=0, column=0, sticky="NSWE", padx=10, pady=(10, 5))

        self.entry_frm = EntryFrm(self, fg_color="transparent")
        self.entry_frm.grid(column=0, row=1, sticky="NSWE", padx=10, pady=(5, 5))

        self.players_sfrm = PlayersSfrm(self)
        self.players_sfrm.grid(column=0, row=2, sticky="NSWE", padx=10, pady=(5, 10))
        return None


class EntryFrm(ctk.CTkFrame):
    class State():
        def __init__(self, state: PlayersFrm.State) -> None:
            self.mode_name = state.mode_name
            self.mode_type = state.mode_type
            self.max_players = state.max_players
            self.player_names = state.player_names
            self.start_game = state.start_game
            self.player_name = ctk.StringVar()
            return None

    def __init__(self, master: PlayersFrm, *args, **kwargs) -> None:
        super().__init__(master, *args, **kwargs)
        self.state = self.State(master.state)
        self.grid_columnconfigure(index=1, weight=1)

        self.name_lbl = ctk.CTkLabel(self, text=f"Name:")
        self.name_lbl.grid(column=0, row=0, sticky="NSWE", padx=3)

        self.name_ntr = ctk.CTkEntry(
            self,
            validate="key",
            textvariable=self.state.player_name,
            validatecommand=(self.register(self._validate_player_entry_cmd), "%P")
        )
        self.name_ntr.grid(column=1, row=0, sticky="NSWE", padx=3)
        self.name_ntr.bind("<Return>", lambda *_: self.add_btn.invoke())

        self.add_btn = ctk.CTkButton(
            self,
            text="+",
            width=0,
            command=self._player_name_entered_cmd,
        )
        self.add_btn.grid(column=2, row=0, sticky="NSWE", padx=3)

        self.state.player_names.trace_add("write", self._player_names_changed_cmd)
        return None

    def _validate_player_entry_cmd(self, string: str) -> bool:
        pattern = r"^[a-zA-Z0-9_ .-]{0,12}$"
        return re.match(pattern, string) is not None

    def _player_name_entered_cmd(self, *args) -> None:
        name = self.state.player_name.get().strip()
        self.state.player_name.set("")
        if not name:
            return None
        player_names = self.state.player_names.get()
        player_names.append(name)
        self.state.player_names.set(player_names)
        return None

    def _player_names_changed_cmd(self, *args) -> None:
        if len(self.state.player_names.get()) == self.state.max_players.get():
            self.name_ntr.configure(state="readonly")
            self.add_btn.configure(state="disabled")
        else:
            self.name_ntr.configure(state="normal")
            self.add_btn.configure(state="enabled")
        return None


class PlayersSfrm(ctk.CTkScrollableFrame):
    class State():
        def __init__(self, state: PlayersFrm.State) -> None:
            self.mode_name = state.mode_name
            self.mode_type = state.mode_type
            self.max_players = state.max_players
            self.player_names = state.player_names
            self.start_game = state.start_game
            return None

    def __init__(self, master: PlayersFrm, *args, **kwargs) -> None:
        super().__init__(master, *args, **kwargs)
        self.state = self.State(master.state)
        self.grid_columnconfigure(index=0, weight=1)

        self.player_frm_s: list["PlayerFrm"] = []
        self.state.max_players.trace_add("write", self._max_players_changed_cmd)

        self.state.player_names.trace_add("write", self._player_names_changed_cmd)
        return None

    def _max_players_changed_cmd(self, *args) -> None:
        for player_frm in self.player_frm_s:
            player_frm.destroy()
        self.player_frm_s.clear()
        for row in range(self.state.max_players.get()):
            player_frm = PlayerFrm(self, position=row+1)
            player_frm.grid(column=0, row=row, sticky="NSWE", padx=5, pady=10)
            self.player_frm_s.append(player_frm)
        return None

    def _player_names_changed_cmd(self, *args) -> None:
        player_names = self.state.player_names.get()
        for index, player_frm in enumerate(self.player_frm_s):
            try:
                player_name = player_names[index]
            except IndexError:
                player_name = ""
            player_frm.state.player_name.set(player_name)
        return None


class PlayerFrm(ctk.CTkFrame):
    class State():
        def __init__(self, state: PlayersSfrm.State) -> None:
            self.mode_name = state.mode_name
            self.mode_type = state.mode_type
            self.max_players = state.max_players
            self.player_names = state.player_names
            self.start_game = state.start_game
            self.player_name = ctk.StringVar()
            return None

    def __init__(self, master: PlayersSfrm, *args, position: int, **kwargs) -> None:
        super().__init__(master, *args, **kwargs)
        self.state = self.State(master.state)
        self.grid_columnconfigure(index=1, weight=1)
        self.grid_rowconfigure(index=0, weight=1)
        self.configure(fg_color="transparent", corner_radius=6)

        self.position = position
        self.position_lbl = ctk.CTkLabel(self, text=f"{self.position}.")
        self.position_lbl.grid(column=0, row=0, sticky="NSWE", padx=3)

        self.name_ntr = ctk.CTkEntry(self, state="readonly", textvariable=self.state.player_name)
        self.name_ntr.grid(column=1, row=0, sticky="NSWE", padx=3)

        self.remove_btn = ctk.CTkButton(
            self,
            text="―",
            width=0,
            command=self._player_name_removed_cmd,
        )
        self.remove_btn.grid(column=2, row=0, sticky="NSWE", padx=3)
        return None

    def _player_name_removed_cmd(self, *args) -> None:
        name = self.state.player_name.get().strip()
        if not name:
            return None
        self.state.player_name.set("")
        player_names = self.state.player_names.get()
        player_names.remove(name)
        self.state.player_names.set(player_names)
        return None
