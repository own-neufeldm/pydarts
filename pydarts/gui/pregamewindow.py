import tkinter as tk
import tkinter.ttk as ttk
from abc import ABC, abstractmethod

import pydarts.gui.tkhelper as tkh
from pydarts.core import games


class Data():
    PLAYER_LIMIT = 8

    def __init__(self):
        self._players = tkh.ListVar()
        self._games_metadata = games.METADATA
        self._mode_id = tk.StringVar()
    
    @property
    def players(self) -> tkh.ListVar:
        return self._players

    @property
    def games_metadata(self) -> games.Metadata:
        return self._games_metadata

    @property
    def mode_id(self) -> tk.StringVar:
        return self._mode_id


class BaseTab(ABC):
    @property
    def parent(self) -> ttk.Notebook: return self._parent
    @parent.setter
    def parent(self, parent: ttk.Notebook): self._parent = parent

    @property
    def root(self) -> ttk.Frame: return self._root
    @root.setter
    def root(self, root: ttk.Frame): self._root = root

    @abstractmethod
    def handle_change_to_self(self, event: tk.Event = None):
        ...

    def is_active(self) -> bool:
        return self.parent.index(self.root) == self.parent.index("current")


class ModesTab(BaseTab):
    """
    tbc
    """

    # Temporary, to be defined somewhere/-how else once I know a better way.
    TEXTS = {
        "title": "Modus wählen",
        "view": {
            "columns": {
                "#0": "Modus",
                "description": "Beschreibung"
            }
        }
    }

    def __init__(self, parent: ttk.Notebook, data: Data):
        self.parent = parent
        self.root = ttk.Frame(master=self.parent)
        self._data = data

        self.view = ttk.Treeview(master=self.root)

    def build(self):
        self.build_root()
        self.build_view()

    def build_root(self):
        text: str = ModesTab.TEXTS["title"]
        widget = self.root
        widget.configure(padding=5, takefocus=0)
        self.parent.add(child=widget, text=text)
        widget.rowconfigure(index=0, weight=1)
        widget.columnconfigure(index=0, weight=1)
    
    # [TODO]: calculate width for '#0' based on longest 'display_name'?
    def build_view(self):
        texts: dict[str, str] = ModesTab.TEXTS["view"]["columns"]
        widget = self.view

        widget.configure(
            columns=list(texts)[1:], selectmode="browse", takefocus=0
        )
        widget.grid(row=0, column=0, sticky="nsew")
        widget.column(column="#0", stretch=tk.NO)
        widget.column(column="description", anchor="w")

        for key, value in texts.items():
            widget.heading(column=key, text=value)

        for game in self._data._games_metadata.games:
            widget.insert(
                parent="", index=tk.END, text=game.display_name,
                values=(game.description,)
            )

    def bind(self):
        self.bind_view()

    def bind_view(self):
        self.view.bind("<<TreeviewSelect>>", self.handle_selection)

    def handle_change_to_self(self, event: tk.Event = None):
        pass

    def handle_selection(self, event: tk.Event = None):
        item = self.view.selection()[0]
        index = self.view.index(item)
        mode_id = self._data.games_metadata.games[index].id
        self._data.mode_id.set(mode_id)


class PlayersTab(BaseTab):
    """
    tbc
    """

    # Temporary, to be defined somewhere/-how else once I know a better way.
    TEXTS = {
        "title": "Spieler hinzufügen",
        "prompt": {
            "label": {
                "title": "Gib einen Namen ein:"
            },
            "entry": {},
            "add": {
                "title": "Hinzufügen"
            }
        },
        "view": {
            "columns": {
                "#0": "Position",
                "player": "Spieler"
            }
        },
        "controls": {
            "move_top": {
                "title": "⊼"
            },
            "move_up": {
                "title": "∧"
            },
            "move_down": {
                "title": "∨"
            },
            "move_bottom": {
                "title": "⊻"
            },
            "remove": {
                "title": "Entfernen"
            }
        }
    }

    def __init__(self, parent: ttk.Notebook, data: Data):
        self.parent = parent
        self.root = ttk.Frame(master=self.parent)
        self._data = data

        self.prompt = ttk.Frame(master=self.root)
        self.label = ttk.Label(master=self.prompt)
        self.entry = ttk.Entry(master=self.prompt)
        self.add = ttk.Button(master=self.prompt)
        self.player_to_add = tk.StringVar()

        self.view = ttk.Treeview(master=self.root)

        self.controls = ttk.Frame(master=self.root)
        self.move_top = ttk.Button(master=self.controls)
        self.move_up = ttk.Button(master=self.controls)
        self.move_down = ttk.Button(master=self.controls)
        self.move_bottom = ttk.Button(master=self.controls)
        self.remove = ttk.Button(master=self.controls)

    def build(self):
        self.build_root()
        self.build_prompt()
        self.build_label()
        self.build_entry()
        self.build_add()
        self.build_view()
        self.build_controls()
        self.build_move_top()
        self.build_move_up()
        self.build_move_down()
        self.build_move_bottom()
        self.build_remove()

    def build_root(self):
        text: str = PlayersTab.TEXTS["title"]
        widget = self.root
        widget.configure(padding=5, takefocus=0)
        self.parent.add(child=widget, text=text)
        widget.rowconfigure(index=1, weight=1)
        widget.columnconfigure(index=0, weight=1)

    def build_prompt(self):
        widget = self.prompt
        widget.configure(padding=5, takefocus=0)
        widget.grid(row=0, column=0, sticky="nsew")
        widget.rowconfigure(index=0, weight=1)
        widget.columnconfigure(index=0, weight=1)
        widget.columnconfigure(index=1, weight=1)
        widget.columnconfigure(index=2, weight=1)

    def build_label(self):
        text: str = PlayersTab.TEXTS["prompt"]["label"]["title"]
        widget = self.label
        widget.configure(text=text, takefocus=0)
        widget.grid(row=0, column=0, sticky="nse")

    def build_entry(self):
        widget = self.entry
        widget.grid(row=0, column=1, sticky="nsew", padx=5)

    def build_add(self):
        text: str = PlayersTab.TEXTS["prompt"]["add"]["title"]
        widget = self.add
        widget.configure(text=text)
        widget.grid(row=0, column=2, sticky="nsw")

    def build_view(self):
        texts: dict[str, str] = PlayersTab.TEXTS["view"]["columns"]
        widget = self.view

        widget.configure(
            columns=list(texts)[1:], selectmode="browse", takefocus=0
        )
        widget.grid(row=1, column=0, sticky="nsew")
        widget.column(column="#0", stretch=tk.NO)
        widget.column(column="player", anchor="w")

        for key, value in texts.items():
            widget.heading(column=key, text=value)
    
    def build_controls(self):
        widget = self.controls
        widget.configure(takefocus=0)
        widget.grid(row=2, column=0, sticky="nsew", pady=(5, 0))
        widget.rowconfigure(index=0, weight=1)
        widget.columnconfigure(index=0, weight=1)
        widget.columnconfigure(index=1, weight=1)
        widget.columnconfigure(index=2, weight=1)
        widget.columnconfigure(index=3, weight=1)
        widget.columnconfigure(index=4, weight=1)

    def build_move_top(self):
        text: str = PlayersTab.TEXTS["controls"]["move_top"]["title"]
        widget = self.move_top
        widget.configure(text=text)
        widget.grid(row=0, column=0, sticky="nsew")

    def build_move_up(self):
        text: str = PlayersTab.TEXTS["controls"]["move_up"]["title"]
        widget = self.move_up
        widget.configure(text=text)
        widget.grid(row=0, column=1, sticky="nsew")

    def build_move_down(self):
        text: str = PlayersTab.TEXTS["controls"]["move_down"]["title"]
        widget = self.move_down
        widget.configure(text=text)
        widget.grid(row=0, column=2, sticky="nsew")

    def build_move_bottom(self):
        text: str = PlayersTab.TEXTS["controls"]["move_bottom"]["title"]
        widget = self.move_bottom
        widget.configure(text=text)
        widget.grid(row=0, column=3, sticky="nsew")

    def build_remove(self):
        text: str = PlayersTab.TEXTS["controls"]["remove"]["title"]
        widget = self.remove
        widget.configure(text=text)
        widget.grid(row=0, column=4, sticky="nsew")

    def bind(self):
        self.bind_entry()
        self.bind_add()
        self.bind_view()
        self.bind_move_top()
        self.bind_move_up()
        self.bind_move_down()
        self.bind_move_bottom()
        self.bind_remove()

    def bind_entry(self):
        self.entry.configure(textvariable=self.player_to_add)
        self.entry.bind(
            "<KeyRelease-Return>", self.handle_key_release_return_in_entry
        )

    def bind_add(self):
        self.add.configure(command=self.handle_add)

    def bind_view(self):
        self._data.players.trace_add("write", self.handle_players_write)

    def bind_move_top(self):
        self.move_top.configure(command=self.handle_move_top)

    def bind_move_up(self):
        self.move_up.configure(command=self.handle_move_up)

    def bind_move_down(self):
        self.move_down.configure(command=self.handle_move_down)

    def bind_move_bottom(self):
        self.move_bottom.configure(command=self.handle_move_bottom)

    def bind_remove(self):
        self.remove.configure(command=self.handle_remove)

    def handle_change_to_self(self, event: tk.Event = None):
        self.toggle_controls()
        self.entry.focus_set()

    def handle_key_release_return_in_entry(self, event: tk.Event = None):
        self.add.invoke()

    def handle_add(self, event: tk.Event = None) -> None:
        self.entry.focus_set()
        player_name = self.player_to_add.get().strip()
        self.player_to_add.set("")

        if not self.is_valid_player_name(player_name):
            # [TODO] notify user somehow
            return None

        players = self._data.players.get()
        players.append(player_name)
        self._data.players.set(players)
        return None

    def handle_move_top(self, event: tk.Event = None):
        selection = self.view.selection()
        if not selection:
            return None

        index = self.view.index(self.view.selection()[0])
        if index == 0:
            return None

        self._swap_player_positions(index, 0)
        return None

    def handle_move_up(self, event: tk.Event = None):
        selection = self.view.selection()
        if not selection:
            return None

        index = self.view.index(self.view.selection()[0])
        if index == 0:
            return None

        self._swap_player_positions(index, index-1)
        return None

    def handle_move_down(self, event: tk.Event = None):
        selection = self.view.selection()
        if not selection:
            return None

        index = self.view.index(self.view.selection()[0])
        if index == len(self.view.get_children())-1:
            return None

        self._swap_player_positions(index, index+1)
        return None

    def handle_move_bottom(self, event: tk.Event = None):
        selection = self.view.selection()
        if not selection:
            return None

        index = self.view.index(self.view.selection()[0])
        last_index = len(self.view.get_children())-1
        if index == last_index:
            return None

        self._swap_player_positions(index, last_index)
        return None

    def handle_remove(self, event: tk.Event = None) -> None:
        selection = self.view.selection()
        if not selection:
            return None

        index = self.view.index(self.view.selection()[0])
        players = self._data.players.get()
        players.pop(index)
        self._data.players.set(players)

        if not self.view.get_children():
            self.entry.focus_set()
            return None
        
        if index == len(self.view.get_children()):
            new_index = index-1
        else:
            new_index = index

        self.view.selection_set(self.view.get_children()[new_index])
        return None

    def handle_players_write(self, *args):
        self.update_view()
        self.toggle_controls()

    def is_valid_player_name(self, player_name: str) -> bool:
        if not player_name:
            return False

        players = self._data.players.get()
        if player_name in players:
            return False

        if len(players) == Data.PLAYER_LIMIT:
            return False
        return True

    def _swap_player_positions(self, current_index: int, new_index: int):
        players = self._data.players.get()
        players.insert(new_index, players.pop(current_index))
        self._data.players.set(players)
        self.view.selection_set(self.view.get_children()[new_index])

    def toggle_controls(self):
        controls = [
            control for control in vars(self).values()
            if
                isinstance(control, ttk.Button)
                and control.master is self.controls
        ]

        if len(self._data.players.get()) == 0:
            for control in controls:
                control.state(["disabled"])
        else:
            for control in controls:
                control.state(["!disabled"])

    def update_view(self):
        for item in self.view.get_children():
            self.view.delete(item)
        for position, player in enumerate(self._data.players.get(), start=1):
            self.view.insert(
                parent="", index=tk.END, text=position, values=(player,)
            )


class OverviewTab(BaseTab):
    """
    tbc
    """

    # Temporary, to be defined somewhere/-how else once I know a better way.
    TEXTS = {
        "title": "Spiel starten",
        "mode": {
            "title": "Modus",
        },
        "players": {
            "title": "Spieler",
            "edit": {
                "title": "Bearbeiten"
            }
        },
        "start": {
            "title": "Start!"
        }
    }

    def __init__(self, parent: ttk.Notebook, data: Data):
        self.parent = parent
        self.root = ttk.Frame(master=self.parent)
        self._data = data

        self.mode = ttk.Labelframe(master=self.root)
        self.mode_name_label = ttk.Label(master=self.mode)
        self.mode_separator = ttk.Separator(master=self.mode)
        self.mode_description_label = ttk.Label(master=self.mode)

        self.players = ttk.Labelframe(master=self.root)
        self.players_view = ttk.Treeview(master=self.players)

        self.start = ttk.Button(master=self.root)

    def build(self):
        self.build_root()
        self.build_mode()
        self.build_mode_name_label()
        self.build_mode_separator()
        self.build_mode_description_label()
        self.build_players()
        self.build_players_view()
        self.build_start()

    def build_root(self):
        text: str = OverviewTab.TEXTS["title"]
        widget = self.root
        widget.configure(padding=5, takefocus=0)
        self.parent.add(child=widget, text=text)
        widget.rowconfigure(index=0, weight=1)
        widget.rowconfigure(index=1, weight=3)
        widget.columnconfigure(index=0, weight=1)

    def build_mode(self):
        text: str = OverviewTab.TEXTS["mode"]["title"]
        widget = self.mode
        widget.configure(padding=5, text=text, takefocus=0)
        widget.grid(row=0, column=0, sticky="nsew", pady=10)
        widget.rowconfigure(index=0, weight=1)
        widget.rowconfigure(index=1, weight=1)
        widget.rowconfigure(index=2, weight=8)
        widget.columnconfigure(index=0, weight=1)

    def build_mode_name_label(self):
        widget = self.mode_name_label
        widget.configure(
            padding=5, anchor="center", justify=tk.CENTER, takefocus=0
        )
        widget.grid(row=0, column=0, sticky="nsew")

    def build_mode_separator(self):
        widget = self.mode_separator
        widget.configure(orient=tk.HORIZONTAL, takefocus=0)
        widget.grid(row=1, column=0, sticky="nsew")

    def build_mode_description_label(self):
        widget = self.mode_description_label
        widget.configure(
            padding=5, anchor="center", justify=tk.CENTER, takefocus=0
        )
        widget.grid(row=2, column=0, sticky="nsew")

    def build_players(self):
        text: str = OverviewTab.TEXTS["players"]["title"]
        widget = self.players
        widget.configure(padding=5, text=text, takefocus=0)
        widget.grid(row=1, column=0, sticky="nsew", pady=10)
        widget.rowconfigure(index=0, weight=1)
        widget.columnconfigure(index=0, weight=1)

    def build_players_view(self):
        texts: dict[str, str] = PlayersTab.TEXTS["view"]["columns"]
        widget = self.players_view

        widget.configure(
            columns=list(texts)[1:], selectmode="none", takefocus=0
        )
        widget.grid(row=0, column=0, sticky="nsew")
        widget.column(column="#0", stretch=tk.NO)
        widget.column(column="player", anchor="w")

        for key, value in texts.items():
            widget.heading(column=key, text=value)

    def build_start(self):
        text: str = OverviewTab.TEXTS["start"]["title"]
        widget = self.start
        widget.configure(padding=5, text=text)
        widget.grid(row=2, column=0, sticky="nsew")

    def bind(self):
        self.bind_mode()
        self.bind_players_view()
        self.bind_start()

    def bind_mode(self):
        self._data.mode_id.trace_add("write", self.handle_mode_id_write)

    def bind_players_view(self):
        self._data.players.trace_add("write", self.handle_players_write)

    def bind_start(self):
        self.start.configure(command=self.handle_start)

    def handle_change_to_self(self, event: tk.Event = None):
        self.toggle_start()
        self.start.focus_set()
        ...
    
    def handle_start(self, event: tk.Event = None):
        ...

    def handle_mode_id_write(self, *args):
        game = self._data.games_metadata.get_game(self._data.mode_id.get())
        self.mode_name_label.configure(text=game.display_name)
        self.mode_description_label.configure(text=game.description)

    def handle_players_write(self, *args):
        self.update_players_view()

    def update_players_view(self):
        for item in self.players_view.get_children():
            self.players_view.delete(item)
        for position, player in enumerate(self._data.players.get(), start=1):
            self.players_view.insert(
                parent="", index=tk.END, text=position, values=(player,)
            )

    def toggle_start(self):
        if not self._data.mode_id.get() or not self._data.players.get():
            self.start.state(["disabled"])
        else:
            self.start.state(["!disabled"])


class PregameWindow():
    """
    tbc
    """

    # Temporary, to be defined somewhere/-how else once I know a better way.
    TEXTS = {
        "go_to_previous_tab": {
            "title": "< Zurück"
        },
        "go_to_next_tab": {
            "title": "Weiter >"
        }
    }

    def __init__(self, parent = ttk.Frame):
        self.parent = parent
        self.root = ttk.Frame(master=self.parent)
        self._data = Data()

        self.notebook = ttk.Notebook(master=self.root)
        self.modes_tab = ModesTab(parent=self.notebook, data=self._data)
        self.players_tab = PlayersTab(parent=self.notebook, data=self._data)
        self.overview_tab = OverviewTab(parent=self.notebook, data=self._data)

        self.bottom_bar = ttk.Frame(master=self.root)
        self.go_to_previous_tab = ttk.Button(master=self.bottom_bar)
        self.go_to_next_tab = ttk.Button(master=self.bottom_bar)

    def build(self):
        self.build_root()
        self.build_notebook()
        self.modes_tab.build()
        self.players_tab.build()
        self.overview_tab.build()
        self.build_bottom_bar()
        self.build_go_to_previous_tab()
        self.build_go_to_next_tab()

    def build_root(self):
        widget = self.root
        widget.configure(takefocus=0)
        widget.grid(row=0, column=0, sticky="nsew")
        widget.rowconfigure(index=0, weight=1)
        widget.columnconfigure(index=0, weight=1)

    def build_notebook(self):
        widget = self.notebook
        widget.configure(takefocus=0)
        widget.grid(row=0, column=0, sticky="nsew")
        widget.rowconfigure(index=0, weight=1)
        widget.columnconfigure(index=0, weight=1)
    
    def build_bottom_bar(self):
        widget = self.bottom_bar
        widget.configure(padding=5, takefocus=0)
        widget.grid(row=1, column=0, sticky="nsew")
        widget.rowconfigure(index=0, weight=1)
        widget.columnconfigure(index=0, weight=1)
        widget.columnconfigure(index=1, weight=1)

    def build_go_to_previous_tab(self):
        text: str = PregameWindow.TEXTS["go_to_previous_tab"]["title"]
        widget = self.go_to_previous_tab
        widget.configure(text=text)
        widget.grid(row=0, column=0, sticky="nsw")

    def build_go_to_next_tab(self):
        text: str = PregameWindow.TEXTS["go_to_next_tab"]["title"]
        widget = self.go_to_next_tab
        widget.configure(text=text)
        widget.grid(row=0, column=1, sticky="nse")

    def bind(self):
        self.bind_notebook()
        self.modes_tab.bind()
        self.players_tab.bind()
        self.overview_tab.bind()
        self.bind_go_to_previous_tab()
        self.bind_go_to_next_tab()

    def bind_notebook(self):
        self.notebook.bind("<<NotebookTabChanged>>", self.handle_tab_changed)

    def bind_go_to_previous_tab(self):
        widget = self.go_to_previous_tab
        widget.configure(command=self.handle_go_to_previous_tab)

    def bind_go_to_next_tab(self):
        widget = self.go_to_next_tab
        widget.configure(command=self.handle_go_to_next_tab)

    def handle_tab_changed(self, event: tk.Event = None):
        self.toggle_controls()
        for tab in self.get_tabs():
            if tab.is_active():
                tab.handle_change_to_self()
                break

    def handle_go_to_previous_tab(self, event: tk.Event = None):
        self.change_to_previous_tab()

    def handle_go_to_next_tab(self, event: tk.Event = None):
        self.change_to_next_tab()

    def change_to_previous_tab(self) -> None:
        current_index = self.notebook.index("current")
        if current_index == 0 or len(self.notebook.tabs()) == 1:
            return None
        self.change_to_tab(current_index-1)

    def change_to_next_tab(self) -> None:
        current_index = self.notebook.index("current")
        last_index = len(self.notebook.tabs())-1
        if current_index == last_index or last_index == 0:
            return None
        self.change_to_tab(current_index+1)

    def change_to_tab(self, tab_id):
        self.notebook.select(tab_id)

    def toggle_controls(self):
        index = self.notebook.index("current")

        if index == 0:
            self.go_to_previous_tab.state(["disabled"])
        else:
            self.go_to_previous_tab.state(["!disabled"])

        if index == len(self.notebook.winfo_children())-1:
            self.go_to_next_tab.state(["disabled"])
        else:
            self.go_to_next_tab.state(["!disabled"])
        

    def get_tabs(self) -> list[BaseTab]:
        return [var for var in vars(self).values() if isinstance(var, BaseTab)]
