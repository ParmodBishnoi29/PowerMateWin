import pystray
from PIL import Image
import threading
import sys
import os
import gui
import pygetwindow as gw

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ICON_PATH = os.path.join(BASE_DIR, "icon.ico")

gui_thread = None

def create_image():
    if os.path.exists(ICON_PATH):
        return Image.open(ICON_PATH)
    # Fallback if missing
    image = Image.new('RGB', (64, 64), color=(31, 83, 141))
    return image

def on_open_settings(icon, item):
    global gui_thread
    if gui_thread and gui_thread.is_alive():
        try:
            windows = gw.getWindowsWithTitle("PowerMateWin Settings")
            for w in windows:
                if w.isMinimized: w.restore()
                w.activate()
        except: pass
        return
        
    gui_thread = threading.Thread(target=gui.show_gui, daemon=True)
    gui_thread.start()

def on_quit(icon, item):
    icon.stop()
    sys.exit(0)
    
def setup_icon(icon):
    import config_manager
    config_manager.TRAY_ICON = icon
    icon.visible = True

def start_tray():
    icon = pystray.Icon("PowerMateWin", create_image(), "PowerMateWin")
    icon.menu = pystray.Menu(
        pystray.MenuItem("Settings", on_open_settings, default=True),
        pystray.MenuItem("Quit", on_quit)
    )
    icon.run(setup=setup_icon)
