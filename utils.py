import subprocess
import re
import sys
import os
from tkinter import messagebox, Tk

import win32process


def get_executable(hwnd):
    # Get the windows process ID
    _, process_id = win32process.GetWindowThreadProcessId(hwnd)
    # Loop over running processes to find the one with the same process ID
    for process in get_running_processes():
        if int(process["pid"]) == process_id:
            return process["image"]


def get_running_processes() -> list[dict]:
    tasks_output = subprocess.check_output(['tasklist']).splitlines()
    # Convert from bytes object to string for rejex and remove the b' part from the start
    tasks = [str(task)[2::] for task in tasks_output]
    processes = []
    for task in tasks:
        matches = re.match("(.+?) +(\d+) (.+?) +(\d+) +(\d+.* K).*", task)
        if matches is not None:
            processes.append({"image": matches.group(1), "pid": matches.group(2), "session_name": matches.group(3),
                              "session_num": matches.group(4), "mem_usage": matches.group(5)})
    return processes


def import_lib(library: str):
    os.system(sys.executable + " -m pip3 install " + library)


def popup(window_name: str):
    # Create a popup window
    root = Tk()
    root.withdraw()
    messagebox.showinfo("Focus Enforcer", f"You're supposed to be focusing! Instead, you tried to open {window_name}",
                        detail="Get back to work!", icon=messagebox.WARNING)
    root.destroy()
