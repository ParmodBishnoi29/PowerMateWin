import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(BASE_DIR, "settings.json")

DEFAULT_CONFIG = {
    "mac_address": "",
    "0x65": {"type": "hotkey", "target": "volume mute"},
    "0x67": {"type": "hotkey", "target": "volume down"},
    "0x68": {"type": "hotkey", "target": "volume up"},
    "0x69": {"type": "hotkey", "target": "previous track"},
    "0x70": {"type": "hotkey", "target": "next track"}
}

# Global state for UI updates
CONNECTION_STATUS = "Initializing..."
TRAY_ICON = None

def load_config():
    if not os.path.exists(CONFIG_FILE):
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG.copy()
    try:
        with open(CONFIG_FILE, "r") as f:
            data = json.load(f)
            
            # Migration from old string schema to new dict schema
            migrated = False
            for k, v in data.items():
                if k.startswith("0x") and isinstance(v, str):
                    data[k] = {"type": "hotkey", "target": v}
                    migrated = True
            
            if migrated:
                save_config(data)
                
            return data
    except Exception as e:
        print(f"Error loading config: {e}")
        return DEFAULT_CONFIG.copy()

def save_config(config_data):
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(config_data, f, indent=4)
    except Exception as e:
        print(f"Error saving config: {e}")

import sys
import winreg

def set_run_on_startup(enable=True):
    exe_path = sys.executable if getattr(sys, 'frozen', False) else os.path.abspath(sys.argv[0])
    command_str = f'"{exe_path}" --startup'
    key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    app_name = "PowerMateWin"
    
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_ALL_ACCESS)
        if enable:
            winreg.SetValueEx(key, app_name, 0, winreg.REG_SZ, command_str)
        else:
            try:
                winreg.DeleteValue(key, app_name)
            except FileNotFoundError:
                pass
        winreg.CloseKey(key)
        return True
    except Exception as e:
        print(f"Startup Registry Error: {e}")
        return False

def check_run_on_startup():
    key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    app_name = "PowerMateWin"
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_READ)
        winreg.QueryValueEx(key, app_name)
        winreg.CloseKey(key)
        return True
    except FileNotFoundError:
        return False
