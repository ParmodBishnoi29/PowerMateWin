import threading
import ble_engine
import tray
import os
import ctypes
import sys
import socket

try:
    myappid = 'powermate.win.bridge'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except Exception:
    pass

PORT = 49152

def main():
    is_startup = "--startup" in sys.argv
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    try:
        sock.bind(("127.0.0.1", PORT))
    except OSError:
        if not is_startup:
            client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            client.sendto(b"OPEN_GUI", ("127.0.0.1", PORT))
        sys.exit(0)
        
    print("Starting PowerMateWin...")
    
    def listen_commands():
        while True:
            try:
                data, _ = sock.recvfrom(1024)
                if data == b"OPEN_GUI":
                    tray.on_open_settings(None, None)
            except:
                break
    threading.Thread(target=listen_commands, daemon=True).start()
    
    if not is_startup:
        tray.on_open_settings(None, None)
    
    # Run BLE engine in a background daemon thread
    ble_thread = threading.Thread(target=ble_engine.start_engine_sync, daemon=True)
    ble_thread.start()
    
    # Run System Tray in the main thread (blocking)
    print("Starting system tray icon...")
    tray.start_tray()

if __name__ == "__main__":
    main()
