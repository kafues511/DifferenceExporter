import time
import sys
import threading as th
import argparse

from runtime import *


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
