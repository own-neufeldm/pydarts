import tkinter as tk

import customtkinter as ctk

import pydarts
import pydarts.core
import pydarts.gui


class PregameStage(pydarts.gui.BaseStage):
    width, height = 640, 400

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.grid_columnconfigure(index=0, weight=1, minsize=PregameStage.width // 2)
        self.grid_columnconfigure(index=1, weight=1, minsize=PregameStage.width // 2)
        self.grid_rowconfigure(index=0, weight=1)

        self.mode_selection = ModeSelection(self)
        self.mode_selection.grid(column=0, row=0, sticky="NSWE", padx=10, pady=10)

        self.player_selection = PlayerSelection(self)
        self.player_selection.grid(column=1, row=0, sticky="NSWE", padx=10, pady=10)
        return None


class ModeSelection(ctk.CTkFrame):
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
            wraplength=280,
        )
        self.description_lbl.grid(column=0, row=1, sticky="NSWE", padx=10, pady=(5, 10))
        return None

    def _mode_selected_cmd(self, selection: str) -> None:
        mode = pydarts.core.get_mode_by_name(selection)
        self.description_lbl.configure(text=mode.get_description())
        return None


class PlayerSelection(ctk.CTkFrame):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.grid_columnconfigure(index=0, weight=1)
        self.grid_rowconfigure(index=1, weight=1)
        self.players: list[str] = []
        self.selected_player = ""

        self.player_selection_entry = PlayerSelectionEntry(self, fg_color="transparent")
        self.player_selection_entry.grid(column=0, row=0, sticky="NSWE", padx=10, pady=(10, 5))
        self.player_selection_entry.entry_ntr.bind(
            "<Return>",
            lambda *_: self.player_selection_entry.add_btn.invoke()
        )
        self.player_selection_entry.add_btn.configure(command=self._add_player_cmd)

        self.player_selection_overview = PlayerSelectionOverview(self)
        self.player_selection_overview.grid(column=0, row=1, sticky="NSWE", padx=10, pady=5)

        self.player_selection_controls = PlayerSelectionControls(self, fg_color="transparent")
        self.player_selection_controls.grid(column=0, row=2, sticky="NSWE", padx=10, pady=(5, 10))
        self.player_selection_controls.remove_btn.configure(command=self._remove_player_cmd)
        return None

    def _select_player_cmd(self, event: tk.Event) -> None:
        selected_player = event.widget.master.cget("text")[3:]
        for child in self.player_selection_overview.winfo_children():
            if child.cget("text")[3:] != selected_player:
                child.configure(fg_color="gray30")  # type: ignore
                continue
            self.selected_player = selected_player
            child.configure(fg_color="black")  # type: ignore
        return None

    def _draw_players(self) -> None:
        for child in self.player_selection_overview.winfo_children():
            child.destroy()
        for row, player in enumerate(self.players):
            text = f"{row + 1}. {player}"
            label = ctk.CTkLabel(
                self.player_selection_overview,
                text=text,
                anchor="w",
                fg_color="gray30",
                corner_radius=7,
            )
            label.grid(column=0, row=row, sticky="NSWE", padx=3, pady=3)
            label.bind("<ButtonRelease-1>", self._select_player_cmd)
        return None

    def _add_player_cmd(self) -> None:
        name = self.player_selection_entry.entry_var.get().strip()
        if name and name not in self.players and len(self.players) < 8:
            self.players.append(name)
        self.player_selection_entry.entry_var.set("")
        self._draw_players()
        return None

    def _remove_player_cmd(self) -> None:
        return None


class PlayerSelectionEntry(ctk.CTkFrame):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.grid_columnconfigure(index=1, weight=1)
        self.grid_columnconfigure(index=2, weight=1)

        self.entry_lbl = ctk.CTkLabel(self, text="Players: ")
        self.entry_lbl.grid(column=0, row=0, sticky="NSWE", padx=(0, 5))

        self.entry_var = tk.StringVar()
        self.entry_ntr = ctk.CTkEntry(self, textvariable=self.entry_var)
        self.entry_ntr.grid(column=1, row=0, sticky="NSWE", padx=5)

        self.add_btn = ctk.CTkButton(self, text="+", width=10)
        self.add_btn.grid(column=2, row=0, sticky="NSWE", padx=(5, 0))
        return None


class PlayerSelectionOverview(ctk.CTkScrollableFrame):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.grid_columnconfigure(index=0, weight=1)
        return None


class PlayerSelectionControls(ctk.CTkFrame):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.grid_columnconfigure(index=0, weight=1)
        self.grid_columnconfigure(index=1, weight=1)
        self.grid_columnconfigure(index=2, weight=1)
        self.grid_rowconfigure(index=0, weight=1)

        self.remove_btn = ctk.CTkButton(self, text="-")
        self.remove_btn.grid(column=0, row=0, sticky="NSWE", padx=(0, 5))

        self.move_up_btn = ctk.CTkButton(self, text="∧")
        self.move_up_btn.grid(column=1, row=0, sticky="NSWE", padx=(5, 5))

        self.move_down_btn = ctk.CTkButton(self, text="∨")
        self.move_down_btn.grid(column=2, row=0, sticky="NSWE", padx=(5, 0))
        return None
