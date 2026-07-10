from winotify import Notification
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
toast = Notification(app_id="powermate.win.bridge",
                     title="Test",
                     msg="Click me to open notifications",
                     icon=os.path.join(BASE_DIR, "icon.ico"),
                     launch="ms-settings:notifications")
toast.show()
