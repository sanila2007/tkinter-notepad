# Copyright ©️ 2023 Sanila Ranatunga. All Rights Reserved

import sys
from cx_Freeze import setup, Executable


build_exe_options = {
    "excludes": ["unittest"],
    "zip_include_packages": ["encodings", "PySide6"],
}

# base="Win32GUI" should be used only for Windows GUI app
base = "Win32GUI" if sys.platform == "win32" else None

setup(
    name="Notepad",
    version="0.2.0",
    description="Write, organize, and collaborate effortlessly.",
    options={"build_exe": build_exe_options},
    executables=[Executable("Notepad.py", base=base, icon="images/notepad_ico.ico")],
)