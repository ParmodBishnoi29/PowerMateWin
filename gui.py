import customtkinter as ctk
import config_manager
import keyboard
import threading
import ctypes

try:
    myappid = 'powermate.win.bridge'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except Exception:
    pass

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class PowerMateApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("PowerMateWin Settings")
        self.geometry("450x500")
        self.resizable(False, False)
        
        try:
            import os
            base_dir = os.path.dirname(os.path.abspath(__file__))
            self.iconbitmap(os.path.join(base_dir, "icon.ico"))
        except Exception as e:
            print(f"Icon error: {e}")
        
        self.config_data = config_manager.load_config()
        
        self.action_labels = {
            "0x65": "Click (Press)",
            "0x67": "Spin Left",
            "0x68": "Spin Right",
            "0x69": "Press + Spin Left",
            "0x70": "Press + Spin Right"
        }
        
        self.action_types = ["Keyboard Hotkey", "Launch App", "Open Website"]
        self.action_mapping = {"Keyboard Hotkey": "hotkey", "Launch App": "app", "Open Website": "website"}
        self.reverse_mapping = {v: k for k, v in self.action_mapping.items()}
        
        self.dropdowns = {}
        self.buttons = {}
        
        # Build UI
        self.title_lbl = ctk.CTkLabel(self, text="PowerMate Shortcuts", font=("Arial", 22, "bold"))
        self.title_lbl.pack(pady=(20, 5))
        
        # Status Label
        self.status_lbl = ctk.CTkLabel(self, text=config_manager.CONNECTION_STATUS, font=("Arial", 12), text_color="#AAB7B8")
        self.status_lbl.pack(pady=(0, 15))
        self.update_status_loop()
        
        for hex_code, label_text in self.action_labels.items():
            frame = ctk.CTkFrame(self, fg_color="transparent")
            frame.pack(fill="x", padx=30, pady=8)
            
            lbl = ctk.CTkLabel(frame, text=label_text, width=120, anchor="w", font=("Arial", 14))
            lbl.pack(side="left", padx=5)
            
            current_bind = self.config_data.get(hex_code, {"type": "hotkey", "target": "Unbound"})
            
            # Action Type Dropdown
            opt = ctk.CTkOptionMenu(frame, values=self.action_types, width=130, command=lambda val, h=hex_code: self.change_action_type(h, val))
            opt.set(self.reverse_mapping.get(current_bind.get("type", "hotkey"), "Keyboard Hotkey"))
            opt.pack(side="left", padx=5)
            
            # Action Target Button
            target_str = current_bind.get("target", "Unbound")
            if current_bind.get("type") == "app":
                import os
                target_str = os.path.basename(target_str)
            elif current_bind.get("type") == "website":
                target_str = target_str[:20] + "..." if len(target_str) > 20 else target_str
                
            btn = ctk.CTkButton(frame, text=target_str, width=130, 
                                command=lambda h=hex_code: self.trigger_action_input(h))
            btn.pack(side="right", padx=5)
            
            self.dropdowns[hex_code] = opt
            self.buttons[hex_code] = btn
            
        # Startup Toggle
        startup_state = config_manager.check_run_on_startup()
        self.startup_var = ctk.BooleanVar(value=startup_state)
        self.startup_switch = ctk.CTkSwitch(self, text="Start with Windows", variable=self.startup_var, command=self.toggle_startup, onvalue=True, offvalue=False)
        self.startup_switch.pack(pady=(10, 5))
            
        # Add Reset to Defaults button
        reset_btn = ctk.CTkButton(self, text="Reset to Defaults", width=200, fg_color="#8E44AD", hover_color="#732D91", command=self.reset_defaults)
        reset_btn.pack(pady=(5, 15))
            
    def toggle_startup(self):
        config_manager.set_run_on_startup(self.startup_var.get())
        
    def update_status_loop(self):
        self.status_lbl.configure(text=config_manager.CONNECTION_STATUS)
        self.after(1000, self.update_status_loop)
            
    def reset_defaults(self):
        self.config_data = config_manager.DEFAULT_CONFIG.copy()
        config_manager.save_config(self.config_data)
        for hex_code, btn in self.buttons.items():
            entry = self.config_data.get(hex_code, {"type": "hotkey", "target": "Unbound"})
            btn.configure(text=entry.get("target", "Unbound"))
            self.dropdowns[hex_code].set(self.reverse_mapping.get(entry.get("type", "hotkey"), "Keyboard Hotkey"))

    def change_action_type(self, hex_code, display_type):
        action_type = self.action_mapping[display_type]
        self.config_data[hex_code] = {"type": action_type, "target": "Not Set"}
        config_manager.save_config(self.config_data)
        self.buttons[hex_code].configure(text="Not Set")

    def trigger_action_input(self, hex_code):
        action_type = self.config_data.get(hex_code, {}).get("type", "hotkey")
        
        if action_type == "hotkey":
            self.record_shortcut(hex_code)
        elif action_type == "app":
            from customtkinter import filedialog
            filepath = filedialog.askopenfilename(title="Select Application", filetypes=[("Executables", "*.exe"), ("All Files", "*.*")])
            if filepath:
                self.config_data[hex_code] = {"type": "app", "target": filepath}
                config_manager.save_config(self.config_data)
                import os
                self.buttons[hex_code].configure(text=os.path.basename(filepath))
        elif action_type == "website":
            dialog = ctk.CTkInputDialog(text="Enter Website URL:", title="Open Website")
            url = dialog.get_input()
            if url:
                if not url.startswith("http"):
                    url = "https://" + url
                self.config_data[hex_code] = {"type": "website", "target": url}
                config_manager.save_config(self.config_data)
                self.buttons[hex_code].configure(text=url[:20] + "..." if len(url) > 20 else url)

    def record_shortcut(self, hex_code):
        btn = self.buttons[hex_code]
        btn.configure(text="Press keys now...", fg_color="#C0392B", hover_color="#E74C3C")
        self.update()
        
        def listener():
            try:
                hotkey = keyboard.read_hotkey(suppress=False)
                self.config_data[hex_code] = {"type": "hotkey", "target": hotkey}
                config_manager.save_config(self.config_data)
                self.after(0, lambda: btn.configure(text=hotkey, fg_color=["#3a7ebf", "#1f538d"], hover_color=["#325882", "#14375e"]))
            except Exception as e:
                print(e)
                self.after(0, lambda: btn.configure(text="Error", fg_color=["#3a7ebf", "#1f538d"]))

        threading.Thread(target=listener, daemon=True).start()

def show_gui():
    app = PowerMateApp()
    app.mainloop()

if __name__ == "__main__":
    show_gui()
