import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.tooltip import ToolTip

from typing import Union

from editor.grid_util import *


__all__ = [
    "ExportProgress",
]


class ExportProgress:
    def __init__(
        self,
        master:tk.Misc,
        column:Union[int, tuple[int, int]],
        row:Union[int, tuple[int, int]],
        padx:Union[int, tuple[int, int], tuple[tuple[int, int], tuple[int, int]]] = (0, 4),
        pady:Union[int, tuple[int, int], tuple[tuple[int, int], tuple[int, int]]] = (0, 4),
        sticky:Union[str, tuple[str, str]] = (EW, EW),
        *args,
        **kwargs,
    ) -> None:
        grid = GridUtil(column=column, row=row, padx=padx, pady=pady, sticky=sticky)

        label = ttk.Label(master, text="Export progress")
        label.grid(column=grid.column, row=grid.row, padx=grid.padx, pady=grid.pady, sticky=grid.sticky)
        ToolTip(label, text="")

        self.progressbar = ttk.Progressbar(master, mode=DETERMINATE, bootstyle=(STRIPED, PRIMARY))
        self.progressbar.grid(column=grid.column, row=grid.row, padx=grid.padx, pady=grid.pady, sticky=grid.sticky)

    def start(self) -> None:
        """出力開始
        """
        self.progressbar.start()

    def end(self) -> None:
        """出力終了
        """
        self.progressbar.stop()
