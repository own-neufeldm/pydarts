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
        return None


class ModeSelectionFrm(ctk.CTkFrame):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.grid_columnconfigure(index=0, weight=1)
        self.grid_rowconfigure(index=1, weight=1)

        self.selection_var = ctk.StringVar()
        self.seletion_cbx = ctk.CTkComboBox(
            self,
            variable=self.selection_var,
            command=self._mode_selected_cmd,
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
        return None

    def _mode_selected_cmd(self, selection: str) -> None:
        mode = pydarts.core.get_mode_by_name(selection)
        self.description_lbl.configure(text=mode.get_description())
        return None


class PlayerSelectionFrm(ctk.CTkFrame):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.grid_columnconfigure(index=0, weight=1)
        self.grid_rowconfigure(index=1, weight=1)
        self.players: list[str] = []
        self.selected_player = ""

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
            player_item = PlayerFrm(
                self.player_overview_sfrm,
                position=row+1,
                name=player,
            )
            player_item.grid(column=0, row=row, sticky="NSWE", padx=3, pady=3)
        return None

    def _add_player_cmd(self) -> None:
        name = self.player_entry_frm.entry_var.get().strip()
        if name and name not in self.players and len(self.players) < 8:
            self.players.append(name)
        self.player_entry_frm.entry_var.set("")
        self._draw_players()
        return None

    def _remove_player_cmd(self) -> None:
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
