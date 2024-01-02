import sys
from cx_Freeze import setup, Executable


# ttkbootstrapは循環で引っかかるので指定
build_exe_options = {
    "packages": ["ttkbootstrap"],
    "includes": [],
    "excludes": [],
}

# base="Win32GUI" should be used only for Windows GUI app
base = "Win32GUI" if sys.platform == "win32" else None

exe = Executable(
    script="main.py",
    base=base,
    target_name="DifferenceExporter",
    #icon="icon.ico",
)

setup(
    name="DifferenceExporter",
    version="0.1.0",
    description="",
    options={
        "build_exe": build_exe_options,
    },
    executables=[exe],
)
