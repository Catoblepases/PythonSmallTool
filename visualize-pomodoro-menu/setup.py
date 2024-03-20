import sys
from cx_Freeze import setup, Executable

build_exe_options = {"packages": [], "excludes": []}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(name="vpomodoro",
      version="1.0",
      description="My App Description",
      options={"build_exe": build_exe_options},
      executables=[Executable("main.py", base=base)])
