import customtkinter as ctk
from auth import AuthBackend

from .ui_mobile import LoginUIMixin
from .logic_mobile import LoginLogicMixin


class MobileLoginAppFlexible(LoginLogicMixin, LoginUIMixin):
    """
    Aplikasi login mobile:
    - setup window
    - inisialisasi AuthBackend
    - bangun UI (dari LoginUIMixin)
    - logika login & redirect (dari LoginLogicMixin)
    """

    def __init__(self):
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        width, height = 393, 852

        self.window = ctk.CTk()
        self.window.title("Login - Mental Health App")
        self.window.geometry(f"{width}x{height}")
        self.window.resizable(False, False)
        self.window.configure(fg_color="white")

        self.width = width
        self.height = height

        # backend autentikasi
        self.auth = AuthBackend()

        # bangun tampilan
        self.create_ui()

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    app = MobileLoginAppFlexible()
    app.run()
