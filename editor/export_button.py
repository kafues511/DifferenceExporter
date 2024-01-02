import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from typing import Union, Optional, Callable

from editor.grid_util import *


__all__ = [
    "ExportButton",
]


class ExportButton:
    def __init__(
        self,
        master:tk.Misc,
        column:int,
        row:int,
        padx:Union[int, tuple[int, int], tuple[tuple[int, int]]] = (0, 4),
        pady:Union[int, tuple[int, int], tuple[tuple[int, int]]] = (0, 4),
        sticky:str = EW,
        callback_export:Optional[Callable[[], None]] = None,
        *args,
        **kwargs,
    ) -> None:
        grid = GridUtil(column=column, row=row, padx=padx, pady=pady, sticky=sticky)

        self.button = ttk.Button(master, text="Export", state=DISABLED, command=callback_export)
        self.button.grid(column=grid.column, row=grid.row, padx=grid.padx, pady=grid.pady, sticky=grid.sticky)

    @property
    def state(self) -> str:
        """ボタンの状態を取得

        Returns:
            str: ボタンの状態
        """
        return str(self.button["state"])

    @state.setter
    def state(self, state:str) -> None:
        """ボタンの状態をセット

        有効と無効の2値のみ対応しています。

        Args:
            state (str): ボタンの状態
        """
        self.button.configure(state=state)
