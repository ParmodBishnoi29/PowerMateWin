import pygetwindow as gw
import psutil
import ctypes

for w in gw.getAllWindows():
    if not w.title: continue
    hwnd = w._hWnd
    pid = ctypes.c_uint()
    ctypes.windll.user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
    if pid.value > 0:
        try:
            p = psutil.Process(pid.value)
            print(f"Title: {repr(w.title)}, Process: {repr(p.name())}")
        except: pass
