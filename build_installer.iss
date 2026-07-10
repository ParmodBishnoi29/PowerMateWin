[Setup]
AppName=PowerMateWin
AppVersion=1.0
DefaultDirName={userappdata}\PowerMateWin
DefaultGroupName=PowerMateWin
OutputDir=Output
OutputBaseFilename=PowerMateWin_Setup
Compression=lzma
SolidCompression=yes
PrivilegesRequired=lowest
SetupIconFile=icon.ico
UninstallDisplayIcon={app}\PowerMateWin.exe

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"

[Files]
Source: "dist\PowerMateWin\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "icon.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\PowerMateWin"; Filename: "{app}\PowerMateWin.exe"; IconFilename: "{app}\icon.ico"; AppUserModelID: "powermate.win.bridge"
Name: "{userdesktop}\PowerMateWin"; Filename: "{app}\PowerMateWin.exe"; IconFilename: "{app}\icon.ico"; Tasks: desktopicon; AppUserModelID: "powermate.win.bridge"

[Run]
Filename: "{app}\PowerMateWin.exe"; Description: "{cm:LaunchProgram,PowerMateWin}"; Flags: nowait postinstall skipifsilent
