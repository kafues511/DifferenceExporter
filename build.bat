rem copy resources\icon.ico icon.ico

call .venv\scripts\activate.bat

py -m setup.py build

rem del icon.ico

rem pause
