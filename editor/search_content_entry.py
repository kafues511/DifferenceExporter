import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.tooltip import ToolTip

from typing import Union, Optional, Callable

from editor.grid_util import *


__all__ = [
    "SearchContentEntry",
]


class SearchContentEntry:
    def __init__(
        self,
        master:tk.Misc,
        column:Union[int, tuple[int, int]],
        row:Union[int, tuple[int, int]],
        padx:Union[int, tuple[int, int], tuple[tuple[int, int], tuple[int, int]]] = (0, 4),
        pady:Union[int, tuple[int, int], tuple[tuple[int, int], tuple[int, int]]] = (0, 4),
        sticky:Union[str, tuple[str, str]] = (EW, EW),
        callback_update_content:Optional[Callable[[str], None]] = None,
        *args,
        **kwargs,
    ) -> None:
        grid = GridUtil(column=column, row=row, padx=padx, pady=pady, sticky=sticky)

        self.content_var = ttk.StringVar(value="")

        label = ttk.Label(master, text="Find in files")
        label.grid(column=grid.column, row=grid.row, padx=grid.padx, pady=grid.pady, sticky=grid.sticky)
        ToolTip(label, text="検索内容を指定します。")

        self.entry = ttk.Entry(master, textvariable=self.content_var, validate="all", validatecommand=(master.register(self.is_valid_content), "%P"))
        self.entry.grid(column=grid.column, row=grid.row, padx=grid.padx, pady=grid.pady, sticky=grid.sticky)

        self.callback_update_content = callback_update_content

    @property
    def state(self) -> str:
        return str(self.entry["state"])

    @state.setter
    def state(self, state:str) -> None:
        self.entry.configure(state=state)

    @property
    def content(self) -> str:
        """入力内容・テキストを取得

        Returns:
            str: 入力内容・テキスト
        """
        return self.content_var.get()

    def is_valid_content(self, new_content:str) -> bool:
        """入力内容が反映可能か判定

        実際には判定せずに更新検知しているだけ。

        Args:
            new_content (str): 新しい入力内容

        Returns:
            bool: True固定
        """
        if self.callback_update_content is not None:
            self.callback_update_content(new_content)
        return True
