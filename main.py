import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from pathlib import Path
import os
from typing import Optional

from editor import *
from runtime import *
#from icondata import ICONDATA


class DifferenceExporterApplication(ttk.Window):
    def __init__(self) -> None:
        super().__init__("Difference Exporter", iconphoto=None)

        #self.iconphoto(True, tk.PhotoImage(data=ICONDATA))

        self.diff_exporter = DifferenceExporter()

        self.tk_input_directory = DirectoryButton(self, text="Input directory", tooltip="コピー元のディレクトリを指定します。", column=(0, 1), row=0, padx=((10, 10), (0, 10)), pady=((10, 0), (10, 0)), callback_update_directory=self.update_input_directory)
        self.tk_output_directory = DirectoryButton(self, text="Output directory", tooltip="コピー先のディレクトリを指定します。", column=(0, 1), row=1, padx=((10, 10), (0, 10)), pady=10, callback_update_directory=self.update_output_directory)
        self.tk_search_content_entry = SearchContentEntry(self, column=(0, 1), row=2, padx=((10, 10), (0, 10)), pady=0, callback_update_content=self.update_search_content)
        self.tk_export_progress = ExportProgress(self, column=(0, 1), row=3, padx=((10, 10), (0, 0)), pady=10)
        self.tk_export_button = ExportButton(self, column=1, row=4, padx=((0, 10), ), pady=((0, 10), ), callback_export=self.start_diff_export)

        # 最小サイズが決定したのでウィンドウサイズを固定
        self.resizable(width=False, height=False)

    @property
    def input_dir(self) -> str:
        """入力・コピー元ディレクトリを取得

        Returns:
            str: 入力・コピー元ディレクトリ
        """
        return self.tk_input_directory.directory

    @property
    def output_dir(self) -> str:
        """出力・コピー先ディレクトリを取得

        Returns:
            str: 出力・コピー先ディレクトリ
        """
        return self.tk_output_directory.directory

    @property
    def search_content(self) -> str:
        """検索内容を取得

        Returns:
            str: 検索内容
        """
        return self.tk_search_content_entry.content

    def update_input_directory(self, directory:str) -> None:
        """入力ディレクトリの更新

        Args:
            directory (str): 入力ディレクトリ
        """
        self.update_export_button_state(input_directory=directory)

    def update_output_directory(self, directory:str) -> None:
        """出力ディレクトリの更新

        Args:
            directory (str): 出力ディレクトリ
        """
        self.update_export_button_state(output_directory=directory)

    def update_search_content(self, content:str) -> None:
        """検索内容の更新

        Args:
            content (str): 検索内容
        """
        self.update_export_button_state(search_content=content)

    def update_export_button_state(
        self,
        input_directory:Optional[str] = None,
        output_directory:Optional[str] = None,
        search_content:Optional[str] = None,
    ) -> None:
        """出力ボタンの状態の更新

        Args:
            input_directory (Optional[str], optional): 入力ディレクトリ. Defaults to None.
            output_directory (Optional[str], optional): 出力ディレクトリ. Defaults to None.
            search_content (Optional[str], optional): 検索内容. Defaults to None.
        """
        if input_directory is None:
            input_directory = self.input_dir
        if output_directory is None:
            output_directory = self.output_dir
        if search_content is None:
            search_content = self.search_content

        input_directory:Path = Path(input_directory)
        output_directory:Path = Path(output_directory)

        # 同一ディレクトリは寝ぼけているだろう
        if input_directory.absolute() == output_directory.absolute():
            state = False
        # 不正な検索内容
        elif not self.is_valid_search_content(search_content):
            state = False
        else:
            state = self.is_valid_directory(input_directory) and self.is_valid_directory(output_directory)

        # ボタンの状態を入力、出力ディレクトリと検索内容の有効性に沿って更新
        self.tk_export_button.state = NORMAL if state else DISABLED

    def is_valid_directory(self, directory:str) -> bool:
        """有効なディレクトリか判定

        Args:
            directory (str): ディレクトリ

        Returns:
            bool: 有効な場合はTrueを返します。
        """
        return DifferenceExporter.is_valid_directory(directory)

    def is_valid_search_content(self, content:str) -> bool:
        """検索内容の有効性を判定

        Args:
            content (str): 検索内容

        Returns:
            bool: 有効な場合はTrueを返します。
        """
        return True if isinstance(content, str) and content != "" else False

    def start_diff_export(self) -> None:
        """差分ファイルの出力を開始
        """
        if not self.is_valid_directory((input_dir:=self.input_dir)):
            return

        if not self.is_valid_directory((output_dir:=self.output_dir)):
            return

        if not self.is_valid_search_content((content:=self.search_content)):
            return

        ret = self.diff_exporter.export(
            input_dir,
            output_dir,
            content,
            os.cpu_count(),
            self.end_diff_export,
        )

        if ret:
            self.tk_export_progress.start()
            self.tk_input_directory.state = DISABLED
            self.tk_output_directory.state = DISABLED
            self.tk_search_content_entry.state = DISABLED
            self.tk_export_button.state = DISABLED

    def end_diff_export(self) -> None:
        """差分ファイルの出力を終了
        """
        self.tk_export_progress.end()
        self.tk_input_directory.state = READONLY
        self.tk_output_directory.state = READONLY
        self.tk_search_content_entry.state = NORMAL
        self.tk_export_button.state = NORMAL


if __name__ == "__main__":
    app = DifferenceExporterApplication()
    app.mainloop()
