import customtkinter as ctk
from tkinter import messagebox


class LoginPage:
    def __init__(self):
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.window = ctk.CTk()
        self.window.title("Login - Mental Health App")
        self.window.geometry("1000x600")
        self.window.configure(fg_color="#FFFFFF")

        self.build_ui()

    def build_ui(self):
        # Container utama untuk centering
        main_container = ctk.CTkFrame(
            self.window,
            fg_color="transparent"
        )
        main_container.place(relx=0.5, rely=0.5, anchor="center")

        # Card login box
        login_card = ctk.CTkFrame(
            main_container,
            fg_color="#ffffff",  # Gunakan hex code
            border_width=2,
            border_color="#E1E6E9",
            corner_radius=15,
            width=450,
            height=500
        )
        login_card.pack(padx=40, pady=40)
        login_card.pack_propagate(False)  # Prevent auto-resize

        # Spacing atas
        ctk.CTkLabel(login_card, text="", height=60).pack()

        # Welcome Back Title
        ctk.CTkLabel(
            login_card,
            text="Welcome Back,",
            font=("Arial Bold", 32),
            text_color="#0e0c0c"
        ).pack(pady=(0, 10))

        # Subtitle
        ctk.CTkLabel(
            login_card,
            text="Log in now to continue",
            font=("Arial Bold", 15),
            text_color="#000000",
        ).pack(pady=(0, 40))

        # Form container dengan padding kiri-kanan
        form_frame = ctk.CTkFrame(login_card, fg_color="transparent")
        form_frame.pack(fill="x", padx=40)

        # Email/Username label
        ctk.CTkLabel(
            form_frame,
            text="Email Address",
            font=("Arial", 12),
            text_color="#333333",
            anchor="w"
        ).pack(anchor="w", pady=(0, 8))

        # Email Entry
        email_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="Silakan masukkan email Anda",
            height=45,
            border_width=1,
            border_color="#d1d5db",
            fg_color="#f9fafb",
            font=("Arial", 13)
        )
        email_entry.pack(fill="x", pady=(0, 20))

        # Password label
        ctk.CTkLabel(
            form_frame,
            text="Password",
            font=("Arial", 12),
            text_color="#333333",
            anchor="w"
        ).pack(anchor="w", pady=(0, 8))

        # Password Entry
        password_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="Silakan masukkan password dari dokter Anda",
            show="●",
            height=45,
            border_width=1,
            border_color="#d1d5db",
            fg_color="#f9fafb",
            font=("Arial", 13)
        )
        password_entry.pack(fill="x", pady=(0, 30))

        # Login Button
        login_btn = ctk.CTkButton(
            form_frame,
            text="Log in",
            height=45,
            font=("Arial Bold", 14),
            fg_color="#2563eb",
            hover_color="#1d4ed8",
            corner_radius=8,
            command=self.login_action
        )
        login_btn.pack(fill="x")

        # Demo credentials text
        ctk.CTkLabel(
            form_frame,
            text="Demo: pasien1 / pasien123",
            font=("Arial", 11),
            text_color="#9ca3af"
        ).pack(pady=(20, 0))

    def login_action(self):
        messagebox.showinfo("Login", "Login berhasil")

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = LoginPage()
    app.run()