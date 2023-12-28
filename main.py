import re
from pathlib import Path
import time
import os
import sys
import shutil
import threading as th
import queue
from typing import Optional
import argparse


def is_edited_file(path:Path, tag:str) -> bool:
    try:
        with open(str(path), mode="r") as f:
            if f.read().find(tag) != -1:
                return True
    except Exception as e:
        pass
    return False


def file_copy_worker(input_queue:queue.Queue, input_dir:Path,output_dir:Path, tag:str) -> None:
    pattern = re.compile("\.(h|cpp|ush|usf|ini|md|hlsl|glsl|cs)$")

    input_dir:Path = Path(input_dir)
    input_dir_parts = input_dir.parts
    input_dir_parts_length = len(input_dir_parts)

    while True:
        if isinstance(path:=input_queue.get(), Path):
            # 対象の拡張子 && ファイル名に1つの拡張子(.gen.xxxを省きたい) && 編集したファイル
            if pattern.search(str(path)) and len(path.suffixes) == 1 and is_edited_file(path, tag):
                input_path = path
                output_path = output_dir / os.path.join(*path.parts[input_dir_parts_length-1:-1])

                output_path.mkdir(parents=True, exist_ok=True)

                shutil.copy(str(input_path), str(output_path))
        else:
            break


def my_app(input_dir:str, output_dir:str, tag:str, show_process_time:bool) -> None:
    if show_process_time:
        start = time.perf_counter()

    input_dir:Path = Path(input_dir)
    output_dir:Path = Path(output_dir)

    input_queue = queue.Queue()

    threads:list[th.Thread] = []
    for _ in range(os.cpu_count()):
        thread = th.Thread(target=file_copy_worker, args=(input_queue, input_dir, output_dir, tag))
        thread.start()
        threads.append(thread)

    for path in input_dir.glob("**/*"):
        input_queue.put(path)

    while True:
        time.sleep(1 / 30)
        if input_queue.qsize() == 0:
            break

    # Event管理が面倒なので雑にNone大量投下でスレッドを殺す
    # デーモン化はtkinterと相性あんまり良くないので好きじゃない
    for _ in range(len(threads) * 10):
        input_queue.put(None)

    # 全て殺したら完了
    for thread in threads:
        thread.join()

    if show_process_time:
        # 参考程度の処理時間を表示
        end = time.perf_counter()
        print(end - start)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_dir", type=str, required=True)
    parser.add_argument("--output_dir", type=str, required=True)
    parser.add_argument("--tag", type=str, required=True)
    parser.add_argument("--show_process_time", default=False, action="store_true")

    args = parser.parse_args(sys.argv[1:])

    my_app(args.input_dir, args.output_dir, args.tag, args.show_process_time)
