import tkinter as tk
from tkinter.filedialog import askdirectory
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.tooltip import ToolTip

from typing import Optional, Callable, Union

from editor.grid_util import *


__all__ = [
    "DirectoryButton",
]


class DirectoryButton:
    def __init__(
        self,
        master:tk.Misc,
        text:str,
        tooltip:str,
        column:Union[int, tuple[int, int]],
        row:Union[int, tuple[int, int]],
        padx:Union[int, tuple[int, int], tuple[tuple[int, int], tuple[int, int]]] = (0, 4),
        pady:Union[int, tuple[int, int], tuple[tuple[int, int], tuple[int, int]]] = (0, 4),
        sticky:Union[str, tuple[str, str]] = (EW, EW),
        callback_update_directory:Optional[Callable[[str], None]] = None,
    ) -> None:
        grid = GridUtil(column=column, row=row, padx=padx, pady=pady, sticky=sticky)

        self.directory_var = ttk.StringVar(master, "")

        label = ttk.Label(master, text=text)
        label.grid(column=grid.column, row=grid.row, padx=grid.padx, pady=grid.pady, sticky=grid.sticky)
        ToolTip(label, text=tooltip, delay=100)

        self.entry = ttk.Entry(master, textvariable=self.directory_var, state=READONLY, width=100)
        self.entry.bind("<Button-1>", self.on_browse)
        self.entry.grid(column=grid.column, row=grid.row, padx=grid.padx, pady=grid.pady, sticky=grid.sticky)

        self.callback_update_directory = callback_update_directory

    @property
    def state(self) -> str:
        """ボタンの状態を取得

        Returns:
            str: ボタンの状態
        """
        return str(self.entry["state"])

    @state.setter
    def state(self, state:str) -> None:
        """ボタンの状態をセット

        Args:
            state (str): ボタンの状態
        """
        self.entry.configure(state=state)

    @property
    def directory(self) -> str:
        """ディレクトリを取得

        Returns:
            str: ディレクトリ
        """
        return self.directory_var.get()

    def on_browse(self, event:tk.Event) -> None:
        if self.state == DISABLED:
            return

        if (directory:=askdirectory(initialdir=self.directory)) != "":
            self.directory_var.set(directory)

            if self.callback_update_directory is not None:
                self.callback_update_directory(directory)
