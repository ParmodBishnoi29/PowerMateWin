<div align="center">
  <img src="icon.ico" width="128" height="128">
  <h1>PowerMateWin</h1>
  <p>A powerful, native Windows 11 utility for Griffin PowerMate Bluetooth.</p>
</div>

## ✨ Features
- **Native Windows Notifications:** Receive deep-linked toasts right in your Windows Action Center.
- **Auto-Reconnect Engine:** An ultra-resilient Bluetooth daemon that runs completely invisibly in the background. Connects instantly when you wake your knob up.
- **Custom App Launching:** Map your PowerMate to launch Discord, open Steam, execute custom hotkeys, or visit specific websites.
- **Start With Windows:** Natively writes to the Registry to boot up completely silently right when you log in.
- **Modern UI:** A stunning CustomTkinter control panel accessible right from your system tray.

## 📥 Installation

1. Go to the [Releases](https://github.com/ParmodBishnoi29/PowerMateWin/releases) tab.
2. Download `PowerMateWin_Setup.exe`.
3. Run the installer and launch it from your Start Menu.
4. Right-click the blue PowerMate icon in your system tray and hit **Settings** to bind your keys!

## 🛠️ Building from Source

If you want to compile the code yourself:
1. Clone the repository.
2. Run `pip install -r requirements.txt`.
3. Compile using PyInstaller:
   ```bash
   pyinstaller --noconfirm --onedir --windowed --name PowerMateWin --icon=icon.ico --add-data "icon.ico;." --add-data "path\to\customtkinter;customtkinter" main.py
   ```
4. Build the final installer using Inno Setup Compiler (`ISCC build_installer.iss`).

## 📜 License
This project is licensed under the MIT License.
