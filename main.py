import re
from pathlib import Path
import time
import os
import sys
import shutil
import threading as th
import queue
from typing import Optional, Callable
import argparse
from dataclasses import dataclass


@dataclass
class DiffExportInfo:
    """差分出力情報
    """
    input_dir:Path
    output_dir:Path
    tag:str
    num_workers:int

    def __post_init__(self) -> None:
        if isinstance(self.input_dir, str):
            self.input_dir = Path(self.input_dir)

        if isinstance(self.output_dir, str):
            self.output_dir = Path(self.output_dir)

        self.num_workers = min(max(1, self.num_workers), os.cpu_count())


class DifferenceExporter:
    WAIT_TIME = 1 / 30

    """差分ファイルの出力
    """
    def __init__(self) -> None:
        """コンストラクタ
        """
        # GIF変換と出力を行うスレッド
        self.thread:th.Thread = None

    def is_thread_ready(self) -> bool:
        """スレッドの立ち上げ準備が整っているかを取得します。

        Returns:
            bool: スレッドを立ち上げられる場合はTrueを返します。
        """
        # スレッドが生きている場合は準備完了していません。
        return True if self.thread is None else not self.thread.is_alive()

    def export(
        self,
        input_dir:str,
        output_dir:str,
        tag:str,
        num_workers:int,
        callback_progress:Optional[Callable[[int, int], None]] = None,
        callback_exported:Optional[Callable[[bool, str], None]] = None,
    ) -> bool:
        # 前回実行した差分出力が完了していない
        if not self.is_thread_ready():
            return False

        # コピー元の有効性を判定
        if not DifferenceExporter.is_valid_directory(input_dir):
            return False

        # コピー先の有効性を判定
        if not DifferenceExporter.is_valid_directory(output_dir):
            return False

        # srcとdstが同じディレクトリの場合は破壊するのでダメ
        if Path(input_dir).absolute() == Path(output_dir).absolute():
            return False

        # スレッド立ち上げ
        self.thread = th.Thread(
            target=self.thread_export,
            args=(
                DiffExportInfo(
                    input_dir,
                    output_dir,
                    tag,
                    num_workers,
                ),
                callback_progress,
                callback_exported,
            ),
            daemon=True,
        )
        self.thread.start()

        return True

    def thread_export(
        self,
        info:DiffExportInfo,
        callback_progress:Optional[Callable[[int, int], None]] = None,
        callback_exported:Optional[Callable[[bool, str], None]] = None,
    ) -> None:
        input_queue = queue.Queue()

        threads:list[th.Thread] = []
        for _ in range(info.num_workers):
            thread = th.Thread(
                target=DifferenceExporter.file_copy_worker,
                args=(
                    input_queue,
                    info.input_dir,
                    info.output_dir,
                    info.tag,
                ),
                daemon=True,
            )
            thread.start()
            threads.append(thread)

        total_file_num = 0

        # 再帰的
        for path in info.input_dir.glob("**/*"):
            input_queue.put(path)
            total_file_num += 1

        while True:
            time.sleep(self.WAIT_TIME)

            total_file_left_num = input_queue.qsize()

            if callback_progress is not None:
                callback_progress(total_file_num, total_file_left_num)

            if total_file_left_num == 0:  # whileの判定にqsize()を直に使うと偶に怪しい挙動を見せるため
                break

        # 雑に殺すためにNoneを大量投下
        for _ in range(len(threads) * 10):
            input_queue.put(None)

        if callback_exported is not None:
            callback_exported()

    @staticmethod
    def is_valid_directory(directory:str) -> bool:
        """有効なディレクトリか判定

        Args:
            directory (str): ディレクトリ

        Returns:
            bool: 有効な場合はTrueを返します。
        """
        if isinstance(directory, str) and directory != "":
            directory:Path = Path(directory)
        elif isinstance(directory, Path) and directory == Path(""):
            return False
        elif not isinstance(directory, Path):
            return False

        return directory.is_dir()

    @staticmethod
    def is_edited_file(path:Path, tag:str, encoding:Optional[str] = None) -> bool:
        try:
            with open(str(path), mode="r", encoding=encoding) as f:
                if f.read().find(tag) != -1:
                    return True
        except UnicodeDecodeError as e:
            if encoding is None:
                return DifferenceExporter.is_edited_file(path, tag, "utf-8")
        except Exception as e:
            pass
        return False

    @staticmethod
    def file_copy_worker(input_queue:queue.Queue, input_dir:Path,output_dir:Path, tag:str) -> None:
        pattern = re.compile("\.(h|cpp|ush|usf|ini|md|hlsl|glsl|cs)$")

        input_dir:Path = Path(input_dir)
        input_dir_parts = input_dir.parts
        input_dir_parts_length = len(input_dir_parts)

        while True:
            if isinstance((path:=input_queue.get()), Path):
                # 対象の拡張子 && ファイル名に1つの拡張子(.gen.xxxを省きたい) && 編集したファイル
                if pattern.search(str(path)) and len(path.suffixes) == 1 and DifferenceExporter.is_edited_file(path, tag):
                    input_path = path
                    output_path = output_dir / os.path.join(*path.parts[input_dir_parts_length-1:-1])

                    output_path.mkdir(parents=True, exist_ok=True)

                    shutil.copy(str(input_path), str(output_path))
            else:
                break


lock = th.Lock()
is_finish = False


def show_progress(total_file_num:int, total_file_left_num:int) -> None:
    print(f"{total_file_left_num}/{total_file_num}")


def show_complete() -> None:
    global is_finish
    with lock:
        is_finish = True


def get_is_finish() -> bool:
    global is_finish
    if not lock.acquire(True, 0.0):
        return False
    else:
        is_ret = is_finish
        lock.release()
        return is_ret


def my_app(input_dir:str, output_dir:str, tag:str, show_process_time:bool) -> None:
    app = DifferenceExporter()

    if not app.export(input_dir, output_dir, tag, 2, show_progress, show_complete):
        return

    while not get_is_finish():
        time.sleep(1 / 60)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_dir", type=str, required=True)
    parser.add_argument("--output_dir", type=str, required=True)
    parser.add_argument("--tag", type=str, required=True)
    parser.add_argument("--show_process_time", default=False, action="store_true")

    args = parser.parse_args(sys.argv[1:])

    my_app(args.input_dir, args.output_dir, args.tag, args.show_process_time)
