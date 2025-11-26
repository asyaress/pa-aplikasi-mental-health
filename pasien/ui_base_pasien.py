import customtkinter as ctk


class BaseLayoutMixin:
    """Layout dasar: header, area card, bagian bawah."""

    def build_base_layout(self):
        main_container = ctk.CTkFrame(self.window, fg_color="#f8f9fa")
        main_container.pack(fill="both", expand=True)

        # ----- HEADER -----
        header_frame = ctk.CTkFrame(
            main_container, fg_color="white", corner_radius=0, height=190
        )
        header_frame.pack(fill="x", padx=0, pady=0)
        header_frame.pack_propagate(False)

        header_content = ctk.CTkFrame(header_frame, fg_color="transparent")
        header_content.pack(fill="both", padx=18, pady=14)

        top_row = ctk.CTkFrame(header_content, fg_color="transparent")
        top_row.pack(fill="x")

        nama_depan = self.nama_pasien.split()[0] if self.nama_pasien else "Pasien"

        self.greeting_label = ctk.CTkLabel(
            top_row,
            text=f"Hai, {nama_depan}",
            font=("Arial", 16),
            text_color="#333333",
            anchor="w",
        )
        self.greeting_label.pack(side="left")

        profile_button = ctk.CTkButton(
            top_row,
            text="Profile",
            width=70,
            height=28,
            fg_color="transparent",
            hover_color="#e0e0e0",
            text_color="#333333",
            font=("Arial", 11),
            corner_radius=14,
        )
        profile_button.pack(side="right")

        self.title_label = ctk.CTkLabel(
            header_content,
            text="Ayo mulai sesi\nhari ini",
            font=("Arial Bold", 22),
            text_color="#000000",
            anchor="w",
            justify="left",
        )
        self.title_label.pack(anchor="w", pady=(6, 2))

        self.subtitle_label = ctk.CTkLabel(
            header_content,
            text="WHO-5 Well-Being Index\n(2 minggu terakhir)",
            font=("Arial", 11),
            text_color="#777777",
            anchor="w",
            justify="left",
        )
        self.subtitle_label.pack(anchor="w")

        # ----- AREA TENGAH (CARD) -----
        self.card_container = ctk.CTkFrame(main_container, fg_color="transparent")
        self.card_container.pack(fill="both", expand=True, padx=16, pady=(8, 8))

        # ----- BAGIAN BAWAH -----
        bottom_container = ctk.CTkFrame(
            main_container, fg_color="transparent", height=150
        )
        bottom_container.pack(fill="x", padx=18, pady=(0, 18))
        bottom_container.pack_propagate(False)

        self.progress_label = ctk.CTkLabel(
            bottom_container,
            text="Progress 2 minggu: 0/14",
            font=("Arial", 11),
            text_color="#333333",
            anchor="w",
        )
        self.progress_label.pack(anchor="w", pady=(0, 4))

        self.week_progress_bar = ctk.CTkProgressBar(
            bottom_container,
            height=8,
            corner_radius=4,
            fg_color="#e0e0e0",
            progress_color="#3b5998",
        )
        self.week_progress_bar.pack(fill="x", pady=(0, 8))

        self.consult_label = ctk.CTkLabel(
            bottom_container,
            text="Jadwal Konsul: -",
            font=("Arial", 11),
            text_color="#555555",
            anchor="w",
        )
        self.consult_label.pack(anchor="w", pady=(2, 10))

        self.nav_frame = ctk.CTkFrame(bottom_container, fg_color="transparent")
        self.nav_frame.pack(pady=(4, 0))

        self.prev_button = ctk.CTkButton(
            self.nav_frame,
            text="Kembali",
            width=118,
            height=44,
            font=("Arial Bold", 13),
            fg_color="#3b5998",
            hover_color="#2d4373",
            corner_radius=10,
            command=self.previous_question,
            state="disabled",
        )
        self.prev_button.pack(side="left", padx=6)

        self.next_button = ctk.CTkButton(
            self.nav_frame,
            text="Lanjut",
            width=118,
            height=44,
            font=("Arial Bold", 13),
            fg_color="#3b5998",
            hover_color="#2d4373",
            corner_radius=10,
            command=self.next_question,
        )
        self.next_button.pack(side="left", padx=6)

    def update_week_progress_ui(self):
        selesai = min(self.total_checkin, 14)
        self.progress_label.configure(text=f"Progress 2 minggu: {selesai}/14")

        if selesai <= 0:
            self.week_progress_bar.set(0)
        else:
            self.week_progress_bar.set(selesai / 14)

        if selesai >= 14:
            if self.tanggal_konsul:
                teks = f"Jadwal Konsul: {self.tanggal_konsul}"
            else:
                teks = "Jadwal Konsul: belum ditentukan"
        else:
            teks = "Jadwal Konsul: -"

        self.consult_label.configure(text=teks)
