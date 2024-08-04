import functools
import tkinter as tk

import customtkinter as ctk

import pydarts
import pydarts.core
import pydarts.gui


class PregameStage(pydarts.gui.BaseStage):
    width, height = 1200, 750

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.grid_columnconfigure(index=0, weight=1, minsize=PregameStage.width // 2)
        self.grid_columnconfigure(index=1, weight=1, minsize=PregameStage.width // 2)
        self.grid_rowconfigure(index=0, weight=1)

        self.mode_selection_frm = ModeSelectionFrm(self)
        self.mode_selection_frm.grid(column=0, row=0, sticky="NSWE", padx=10, pady=10)

        self.player_selection_frm = PlayerSelectionFrm(self)
        self.player_selection_frm.grid(column=1, row=0, sticky="NSWE", padx=10, pady=10)

        self.start_btn = ctk.CTkButton(self, text="Start", command=self._start_cmd)
        self.start_btn.grid(column=0, row=1, columnspan=2, sticky="NSWE", padx=10, pady=(0, 10))
        return None

    def _start_cmd(self) -> None:
        # TODO: raise event or some like dat
        print(f"Mode: {self.mode_selection_frm.mode.get_name()}")
        print(f"Players: {self.player_selection_frm.players}")
        return None


class ModeSelectionFrm(ctk.CTkFrame):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.grid_columnconfigure(index=0, weight=1)
        self.grid_rowconfigure(index=1, weight=1)
        self.mode: type[pydarts.core.modes.BaseMode]

        self.selection_var = ctk.StringVar()
        self.selection_var.trace_add("write", lambda *_: self._mode_selected_cmd())
        self.seletion_cbx = ctk.CTkComboBox(
            self,
            variable=self.selection_var,
            values=pydarts.core.get_mode_names(),
        )
        self.seletion_cbx.grid(column=0, row=0, sticky="NSWE", padx=10, pady=(10, 5))

        self.description_lbl = ctk.CTkLabel(
            self,
            text="Please select a game mode.",
            anchor="nw",
            justify="left",
            wraplength=250,
        )
        self.description_lbl.grid(column=0, row=1, sticky="NSWE", padx=10, pady=(5, 10))

        self.selection_var.set(pydarts.core.get_mode_names()[0])
        return None

    def _mode_selected_cmd(self) -> None:
        # somehow 'write' is triggered twice, but only the second event has a value
        if not (selection := self.selection_var.get()):
            return None
        self.mode = pydarts.core.get_mode_by_name(selection)
        self.description_lbl.configure(text=self.mode.get_description())
        return None


class PlayerSelectionFrm(ctk.CTkFrame):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.grid_columnconfigure(index=0, weight=1)
        self.grid_rowconfigure(index=1, weight=1)
        self.players: list[str] = []
        self.max_players = 8

        self.player_entry_frm = PlayerEntryFrm(self, fg_color="transparent")
        self.player_entry_frm.grid(column=0, row=0, sticky="NSWE", padx=10, pady=(10, 5))
        self.player_entry_frm.entry_ntr.bind(
            "<Return>",
            lambda *_: self.player_entry_frm.add_btn.invoke()
        )
        self.player_entry_frm.add_btn.configure(command=self._add_player_cmd)

        self.player_overview_sfrm = PlayerOverviewSfrm(self)
        self.player_overview_sfrm.grid(column=0, row=1, sticky="NSWE", padx=10, pady=5)
        return None

    def _draw_players(self) -> None:
        for child in self.player_overview_sfrm.winfo_children():
            child.destroy()
        for row, player in enumerate(self.players):
            player_frm = PlayerFrm(
                self.player_overview_sfrm,
                position=row+1,
                name=player,
            )
            player_frm.grid(column=0, row=row, sticky="NSWE", padx=3, pady=3)
            player_frm.move_up_btn.configure(command=functools.partial(self._move_player_up_cmd, row))
            player_frm.move_down_btn.configure(command=functools.partial(self._move_player_down_cmd, row))
            player_frm.remove_btn.configure(command=functools.partial(self._remove_player_cmd, row))
            if row == 0:
                player_frm.move_up_btn.configure(state="disabled")
            if row == len(self.players) - 1:
                player_frm.move_down_btn.configure(state="disabled")
        return None

    def _add_player_cmd(self) -> None:
        name = self.player_entry_frm.entry_var.get().strip()
        if name and name not in self.players and len(self.players) < self.max_players:
            self.players.append(name)
        self.player_entry_frm.entry_var.set("")
        self._draw_players()
        return None

    def _move_player_up_cmd(self, row: int) -> None:
        player = self.players.pop(row)
        self.players.insert(row-1, player)
        self._draw_players()
        return None

    def _move_player_down_cmd(self, row: int) -> None:
        player = self.players.pop(row)
        self.players.insert(row+1, player)
        self._draw_players()
        return None

    def _remove_player_cmd(self, row: int) -> None:
        self.players.pop(row)
        self._draw_players()
        return None


class PlayerEntryFrm(ctk.CTkFrame):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.grid_columnconfigure(index=1, weight=1)
        self.grid_columnconfigure(index=2, weight=1)

        self.entry_lbl = ctk.CTkLabel(self, text="Players: ")
        self.entry_lbl.grid(column=0, row=0, sticky="NSWE")

        self.entry_var = tk.StringVar()
        self.entry_ntr = ctk.CTkEntry(self, textvariable=self.entry_var)
        self.entry_ntr.grid(column=1, row=0, sticky="NSWE", padx=5)

        self.add_btn = ctk.CTkButton(self, text="+", width=10)
        self.add_btn.grid(column=2, row=0, sticky="NSWE")
        return None


class PlayerOverviewSfrm(ctk.CTkScrollableFrame):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.grid_columnconfigure(index=0, weight=1)
        return None


class PlayerFrm(ctk.CTkFrame):
    def __init__(
        self,
        master: PlayerOverviewSfrm,
        position: int,
        name: str,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(master, *args, **kwargs)
        self.position = position
        self.name = name
        self.grid_columnconfigure(index=1, weight=1)
        self.configure(fg_color="transparent", corner_radius=7)

        self.move_up_btn = ctk.CTkButton(self, text="∧", width=0)
        self.move_up_btn.grid(column=0, row=0, sticky="NSWE", pady=(0, 1))

        self.move_down_btn = ctk.CTkButton(self, text="∨", width=0)
        self.move_down_btn.grid(column=0, row=1, sticky="NSWE", pady=(1, 0))

        self.player_lbl = ctk.CTkLabel(
            self,
            text=f"{self.position}. {self.name}",
            anchor="w",
            fg_color="gray30",
            corner_radius=5,
        )
        self.player_lbl.grid(column=1, row=0, rowspan=2, sticky="NSWE", padx=5)

        self.remove_btn = ctk.CTkButton(self, text="―", width=0)
        self.remove_btn.grid(column=2, row=0, rowspan=2, sticky="NSWE")
        return None
