import customtkinter as ctk


class LoginUIMixin:
    """Mixin: bikin tampilan layar login mobile."""

    def create_ui(self):
        main_container = ctk.CTkFrame(self.window, fg_color="white")
        main_container.pack(fill="both", expand=True)

        # ------- BAGIAN ATAS (BACKGROUND BULAT) -------
        canvas_height = int(self.height * 0.35)
        canvas = ctk.CTkCanvas(
            main_container,
            width=self.width,
            height=canvas_height,
            bg="white",
            highlightthickness=0,
        )
        canvas.pack(side="top", fill="x")

        circle1_size = int(self.width * 0.95)
        canvas.create_oval(
            -int(self.width * 0.2),
            int(canvas_height * 0.15),
            circle1_size - int(self.width * 0.2),
            canvas_height + int(canvas_height * 0.35),
            fill="#3b5998",
            outline="",
        )

        circle2_size = int(self.width * 0.9)
        canvas.create_oval(
            int(self.width * 0.48),
            -int(canvas_height * 0.4),
            int(self.width * 0.48) + circle2_size,
            int(canvas_height * 0.73),
            fill="#8b9dc3",
            outline="",
        )

        # ------- KONTEN UTAMA -------
        content = ctk.CTkFrame(main_container, fg_color="white")
        content.pack(fill="both", expand=True, padx=30, pady=10)

        welcome_label = ctk.CTkLabel(
            content,
            text="Welcome Back,",
            font=("Arial Bold", 26),
            text_color="#000000",
            anchor="w",
        )
        welcome_label.pack(anchor="w", pady=(10, 3))

        subtitle_label = ctk.CTkLabel(
            content,
            text="Log in now to continue",
            font=("Arial", 13),
            text_color="#666666",
            anchor="w",
        )
        subtitle_label.pack(anchor="w", pady=(0, 25))

        # ------- USERNAME -------
        email_label = ctk.CTkLabel(
            content,
            text="Username",
            font=("Arial Medium", 12),
            text_color="#333333",
            anchor="w",
        )
        email_label.pack(anchor="w", pady=(0, 6))

        email_frame = ctk.CTkFrame(
            content, fg_color="#f5f5f5", corner_radius=8, height=48
        )
        email_frame.pack(fill="x", pady=(0, 18))
        email_frame.pack_propagate(False)

        email_icon_label = ctk.CTkLabel(email_frame, text="👤", font=("Arial", 14))
        email_icon_label.pack(side="left", padx=(12, 8))

        self.email_entry = ctk.CTkEntry(
            email_frame,
            placeholder_text="Masukkan username",
            font=("Arial", 12),
            fg_color="transparent",
            border_width=0,
            text_color="#333333",
            placeholder_text_color="#999999",
        )
        self.email_entry.pack(side="left", fill="both", expand=True, padx=(0, 12))

        # ------- PASSWORD -------
        password_label = ctk.CTkLabel(
            content,
            text="Password",
            font=("Arial Medium", 12),
            text_color="#333333",
            anchor="w",
        )
        password_label.pack(anchor="w", pady=(0, 6))

        password_frame = ctk.CTkFrame(
            content, fg_color="#f5f5f5", corner_radius=8, height=48
        )
        password_frame.pack(fill="x", pady=(0, 25))
        password_frame.pack_propagate(False)

        lock_icon_label = ctk.CTkLabel(password_frame, text="🔒", font=("Arial", 14))
        lock_icon_label.pack(side="left", padx=(12, 8))

        self.password_entry = ctk.CTkEntry(
            password_frame,
            placeholder_text="Masukkan password",
            font=("Arial", 12),
            show="●",
            fg_color="transparent",
            border_width=0,
            text_color="#333333",
            placeholder_text_color="#999999",
        )
        self.password_entry.pack(side="left", fill="both", expand=True, padx=(0, 12))

        # ------- TOMBOL LOGIN -------
        login_button = ctk.CTkButton(
            content,
            text="Log in",
            font=("Arial Bold", 14),
            height=48,
            fg_color="#3b5998",
            hover_color="#2d4373",
            corner_radius=8,
            command=self.login,  # method dari LoginLogicMixin
        )
        login_button.pack(fill="x", pady=(0, 15))

        info_label = ctk.CTkLabel(
            content,
            text="Demo: pasien1 / pasien123",
            font=("Arial", 10),
            text_color="#999999",
        )
        info_label.pack(pady=(10, 0))
