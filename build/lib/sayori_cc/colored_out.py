# Code by NDRAEY (c) 2023

from colorama import Fore

quiet = False

def _fore(c, v):
    return c + v + Fore.RESET

def success(*args, **kwargs):
    if quiet: return
    print("[" + _fore(Fore.LIGHTGREEN_EX, " + ") + "]", *args, **kwargs)

def warn(*args, **kwargs):
    if quiet: return
    print("[" + _fore(Fore.LIGHTYELLOW_EX, " * ") + "]", *args, **kwargs)

def check(*args, **kwargs):
    if quiet: return
    print("[" + _fore(Fore.LIGHTBLUE_EX, "~~~") + "]", *args, **kwargs)

def error(*args, **kwargs):
    print("[" + _fore(Fore.LIGHTRED_EX, "!!!") + "]", *args, **kwargs)

def info(*args, **kwargs):
    print("[---]", *args, **kwargs)
