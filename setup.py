import sys
import os
import platform
import subprocess

# if cx_Freeze not installed 
try:
    from cx_Freeze import setup, Executable
except ImportError:
    if platform.system() == "Windows":
        s = subprocess.Popen("pip install cx_Freeze")
        s.kill()
    elif platform.system() == "Linux":
        s = subprocess.Popen("pip3 install cx_Freeze",shell=True)
        s.kill()
# get python dir
python_path = sys.executable
python_dir = python_path[:python_path.rfind(os.sep)]

# get own module
datadir = os.path.dirname(__file__) + os.sep + "src"
sys.path.append(datadir)

if platform.system() == "Windows":
    os.environ['TCL_LIBRARY'] = python_dir + "\\tcl\\tcl8.6"
    os.environ['TK_LIBRARY'] = python_dir + "\\tcl\\tk8.6"
    include_files = [python_dir + "\\DLLs\\tcl86t.dll", python_dir + "\\DLLs\\tk86t.dll"]
    execute_base = "Win32GUI"
elif platforms.system() == "Linux":
    os.environ['TCL_LIBRARY'] = python_dir + "/tcl/tcl8.6"
    os.environ['TK_LIBRARY'] = python_dir + "/tcl/tk8.6"
    include_files = [python_dir + "/DLLs/tcl86t.dll", python_dir + "/DLLs/tk86t.dll"]
    execute_base = None

setup(
    name = "MIPS assembler",
    version = "1.0",
    description = "A MIPS assembler / disassembler ",
    options = {"build_exe": {"include_files": include_files}},
    executables = [Executable("src"+os.sep+"graphics.py", base = execute_base)])