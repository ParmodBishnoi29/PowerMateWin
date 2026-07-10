import asyncio
import time
import keyboard
import ctypes
from bleak import BleakScanner, BleakClient
import config_manager

INPUT_CHAR_UUID = "9cf53570-ddd9-47f3-ba63-09acefc60415"

last_action_time = 0

import pygetwindow as gw

def bring_window_to_front(window_title):
    try:
        windows = gw.getWindowsWithTitle(window_title)
        for w in windows:
            if window_title.lower() in w.title.lower():
                if w.isMinimized:
                    w.restore()
                w.activate()
                return True
    except Exception as e:
        print(f"Window activation error: {e}")
    return False

def bring_app_to_front(target_path):
    import os
    import psutil
    import ctypes
    
    target_exe_base = os.path.basename(target_path).replace(".exe", "").replace(".lnk", "").lower()
    
    target_pids = set()
    for p in psutil.process_iter(['pid', 'name']):
        try:
            if p.info['name'] and p.info['name'].lower().replace(".exe", "") == target_exe_base:
                target_pids.add(p.info['pid'])
        except:
            pass
            
    if not target_pids:
        return False
        
    try:
        for w in gw.getAllWindows():
            if not w.title:
                continue
                
            try:
                hwnd = w._hWnd
                pid = ctypes.c_uint()
                ctypes.windll.user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
                
                if pid.value in target_pids:
                    if w.isMinimized:
                        w.restore()
                    w.activate()
                    return True
            except:
                continue
    except Exception as e:
        print(f"App activation error: {e}")
        
    return False

def notification_handler(sender, data):
    global last_action_time
    if len(data) > 0:
        value = hex(data[0])
        config = config_manager.load_config()
        
        if value in config:
            action = config[value]
            if isinstance(action, str):
                action = {"type": "hotkey", "target": action}
                
            action_type = action.get("type", "hotkey")
            target = action.get("target", "")
            
            if not target or target == "Unbound" or target == "Not Set":
                return
                
            current_time = time.time()
            
            # Throttle the inputs to prevent freezing
            if current_time - last_action_time > 0.05:
                print(f"Detected: {value} -> Triggering {action_type}: {target}")
                last_action_time = current_time
                
                try:
                    if action_type == "hotkey":
                        if target.lower() in ["calculator", "launch app 2"]:
                            if bring_window_to_front("Calculator"):
                                return
                        keyboard.send(target)
                    elif action_type == "app":
                        import os
                        if not bring_app_to_front(target):
                            os.startfile(target)
                    elif action_type == "website":
                        import webbrowser
                        webbrowser.open(target)
                except Exception as e:
                    print(f"Error executing action: {e}")

def update_status(msg, notify=False):
    config_manager.CONNECTION_STATUS = msg
    print(msg)
    if notify:
        try:
            from winotify import Notification
            import os
            BASE_DIR = os.path.dirname(os.path.abspath(__file__))
            icon_path = os.path.join(BASE_DIR, "icon.ico")
            toast = Notification(app_id="powermate.win.bridge",
                                 title="PowerMateWin",
                                 msg=msg,
                                 icon=icon_path,
                                 launch="ms-settings:notifications")
            toast.show()
        except Exception as e: 
            print(f"Notification error: {e}")

async def run_ble():
    while True:
        config = config_manager.load_config()
        target_mac = config.get("mac_address", "")
        
        device = None
        try:
            if target_mac:
                update_status(f"Scanning for known PowerMate...")
                device = await BleakScanner.find_device_by_address(target_mac)
            
            if not device:
                update_status("Discovering new PowerMate device...", notify=False)
                devices = await BleakScanner.discover(timeout=5.0)
                for d in devices:
                    if d.name and "powermate" in d.name.lower():
                        device = d
                        update_status(f"Found {device.name}! Saving MAC.")
                        config["mac_address"] = device.address
                        config_manager.save_config(config)
                        break
        except Exception as e:
            notify = ("Bluetooth is OFF" not in config_manager.CONNECTION_STATUS)
            update_status("Bluetooth is OFF or unavailable! Please turn it on.", notify=notify)
            await asyncio.sleep(5)
            continue
                    
        if not device:
            for i in range(5, 0, -1):
                update_status(f"PowerMate not found! Auto-rescanning in {i}s...", notify=False)
                await asyncio.sleep(1)
            continue

        device_name = device.name if device.name else "PowerMate"
        update_status(f"Connecting to {device_name}...")
        was_connected = False
        try:
            async with BleakClient(device) as client:
                update_status("Connected! Listening for inputs...", notify=True)
                was_connected = True
                await client.start_notify(INPUT_CHAR_UUID, notification_handler)
                
                while True:
                    # Check connection state periodically
                    if not client.is_connected:
                        break
                    await asyncio.sleep(1)
        except Exception as e:
            if was_connected:
                update_status(f"Connection lost. Retrying...", notify=True)
            else:
                update_status(f"Failed to connect. Retrying...", notify=False)
            await asyncio.sleep(2)

def start_engine_sync():
    try:
        asyncio.run(run_ble())
    except KeyboardInterrupt:
        print("Exiting BLE engine...")
    except Exception as e:
        print(f"BLE Engine Error: {e}")
