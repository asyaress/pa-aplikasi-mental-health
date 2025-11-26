import customtkinter as ctk
from auth import AuthBackend

from .ui_desktop import DesktopLoginUIMixin
from .logic_desktop import DesktopLoginLogicMixin


class DesktopLoginApp(DesktopLoginLogicMixin, DesktopLoginUIMixin):
    """
    Aplikasi login desktop:
    - setup window
    - inisialisasi AuthBackend
    - bangun UI (DesktopLoginUIMixin)
    - logika login & redirect (DesktopLoginLogicMixin)
    """

    def __init__(self):
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.window = ctk.CTk()
        self.window.title("Mental Health Monitoring System - Login")

        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        window_width = 1200
        window_height = 700

        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        self.window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.window.resizable(True, True)
        self.window.configure(fg_color="white")

        # backend auth
        self.auth = AuthBackend()

        # bangun UI
        self.create_ui()

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    app = DesktopLoginApp()
    app.run()
