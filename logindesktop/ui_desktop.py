import customtkinter as ctk


class DesktopLoginUIMixin:
    """
    Mixin untuk tampilan UI login desktop.
    Butuh:
      - self.window
      - self.login() (dari logic mixin)
    """

    def create_ui(self):
        # LEFT (biru, judul besar)
        left_frame = ctk.CTkFrame(self.window, fg_color="#3b5998", corner_radius=0)
        left_frame.place(x=0, y=0, relwidth=0.5, relheight=1)

        title_label = ctk.CTkLabel(
            left_frame,
            text="Mental Health\nMonitoring System",
            font=("Arial Bold", 48),
            text_color="white",
            justify="center",
        )
        title_label.place(relx=0.5, rely=0.4, anchor="center")

        subtitle_label = ctk.CTkLabel(
            left_frame,
            text="WHO-5 Well-Being Index\nDaily Check-In System",
            font=("Arial", 18),
            text_color="#e0e0e0",
            justify="center",
        )
        subtitle_label.place(relx=0.5, rely=0.55, anchor="center")

        # RIGHT (form login)
        right_frame = ctk.CTkFrame(self.window, fg_color="white", corner_radius=0)
        right_frame.place(relx=0.5, y=0, relwidth=0.5, relheight=1)

        login_container = ctk.CTkFrame(right_frame, fg_color="white")
        login_container.place(relx=0.5, rely=0.5, anchor="center")

        welcome_label = ctk.CTkLabel(
            login_container,
            text="Welcome Back",
            font=("Arial Bold", 36),
            text_color="#000000",
        )
        welcome_label.pack(pady=(0, 10))

        subtitle_login = ctk.CTkLabel(
            login_container,
            text="Please login to continue",
            font=("Arial", 16),
            text_color="#666666",
        )
        subtitle_login.pack(pady=(0, 40))

        # Username
        username_label = ctk.CTkLabel(
            login_container,
            text="Username",
            font=("Arial Medium", 14),
            text_color="#333333",
            anchor="w",
        )
        username_label.pack(anchor="w", pady=(0, 8))

        self.username_entry = ctk.CTkEntry(
            login_container,
            width=400,
            height=50,
            placeholder_text="Enter your username",
            font=("Arial", 14),
            fg_color="#f5f5f5",
            border_width=0,
            corner_radius=8,
        )
        self.username_entry.pack(pady=(0, 20))

        # Password
        password_label = ctk.CTkLabel(
            login_container,
            text="Password",
            font=("Arial Medium", 14),
            text_color="#333333",
            anchor="w",
        )
        password_label.pack(anchor="w", pady=(0, 8))

        self.password_entry = ctk.CTkEntry(
            login_container,
            width=400,
            height=50,
            placeholder_text="Enter your password",
            font=("Arial", 14),
            show="*",
            fg_color="#f5f5f5",
            border_width=0,
            corner_radius=8,
        )
        self.password_entry.pack(pady=(0, 30))

        # Tombol login
        login_button = ctk.CTkButton(
            login_container,
            text="Login",
            width=400,
            height=50,
            font=("Arial Bold", 16),
            fg_color="#2d4373",
            hover_color="#2d4373",
            corner_radius=8,
            command=self.login,  # dari logic mixin
        )
        login_button.pack(pady=(0, 20))

        info_label = ctk.CTkLabel(
            login_container,
            text="Demo: pasien1 / pasien123",
            font=("Arial", 12),
            text_color="#999999",
        )
        info_label.pack(pady=(10, 0))

        # Enter key binding
        self.username_entry.bind("<Return>", lambda e: self.password_entry.focus())
        self.password_entry.bind("<Return>", lambda e: self.login())
