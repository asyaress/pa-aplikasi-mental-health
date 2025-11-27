import customtkinter as ctk
from tkinter import messagebox


class PatientTableMixin:
    """
    Mixin untuk:
    - build_ui (sidebar + main_content + table frame)
    - render_table
    - search, handler tombol
    """

    def build_ui(self):
        # Sidebar
        self.sidebar = ctk.CTkFrame(
            self.window, fg_color="#ffffff", width=65, corner_radius=0
        )
        self.sidebar.pack(side="left", fill="y", padx=0, pady=0)

        ctk.CTkLabel(
            self.sidebar, text="♾️", font=("Arial", 30), text_color="#007bff"
        ).pack(pady=(30, 20))

        ctk.CTkButton(
            self.sidebar,
            text="➕",
            width=50,
            height=50,
            text_color="#000000",
            fg_color="#ffffff",
            hover_color="#0e98f5",
            corner_radius=10,
            command=self.open_create_patient_window,
        ).pack(pady=10)

        self.logout_button = ctk.CTkButton(
            self.sidebar,
            text="Logout",
            width=60,
            height=32,
            fg_color="#fecaca",
            text_color="#b91c1c",
            hover_color="#fca5a5",
            corner_radius=10,
            command=self.logout,
        )
        self.logout_button.pack(side="bottom", pady=20)

        # Main content
        self.main_content = ctk.CTkFrame(self.window, fg_color="#f8f9fa")
        self.main_content.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        # Scrollable frame untuk tabel
        self.table_scroll_frame = ctk.CTkScrollableFrame(
            self.main_content, fg_color="#ffffff", corner_radius=10
        )
        self.table_scroll_frame.pack(side="top", fill="both", expand=True, pady=(0, 0))

        # Render awal
        self.render_table(self.patients_data)

    # ----- Helper handler -----
    def create_detail_handler(self, row_data):
        def handler():
            self.view_detail(row_data)

        return handler

    def create_edit_handler(self, row_data):
        def handler():
            self.open_edit_patient_window(row_data)

        return handler

    def create_set_konsul_handler(self, row_data):
        def handler():
            self.open_set_konsul_window(row_data)

        return handler

    # ----- Tabel -----
    def render_table(self, data):
        for widget in self.table_scroll_frame.winfo_children():
            widget.destroy()

        header_row = ctk.CTkFrame(
            self.table_scroll_frame, fg_color="#f1f1f1", height=40
        )
        header_row.pack(fill="x")

        headers = [
            "Nama Pasien",
            "Diagnosa",
            "Jenis",
            "Kategori",
            "Progress 2 Minggu",
            "Tanggal Konsul",
            "Aksi",
        ]
        col_widths = [200, 250, 150, 150, 170, 130, 120]  # px

        for i, h in enumerate(headers):
            label = ctk.CTkLabel(
                header_row,
                text=h,
                font=("Arial bold", 13),
                text_color="black",
                width=col_widths[i],
                anchor="center",
            )
            label.pack(side="left", padx=(0), pady=5)

        for row_data in data:
            row_frame = ctk.CTkFrame(
                self.table_scroll_frame, fg_color="#ffffff", height=45
            )
            row_frame.pack(fill="x", pady=1)

            nama = row_data.get("nama", "-")
            diagnosa = row_data.get("diagnosa", "-")
            jenis = row_data.get("jenis", "-")
            kategori = row_data.get("kategori", "-")
            progress_label = row_data.get("progress_label", "-")
            selesai_2minggu = row_data.get("selesai_2minggu", False)
            tanggal_konsul = row_data.get("tanggal_konsul") or ""

            # Nama
            ctk.CTkLabel(
                row_frame,
                text=nama,
                font=("Arial Bold", 13),
                anchor="w",
                width=col_widths[0],
            ).pack(side="left", padx=(0))

            # Diagnosa
            ctk.CTkLabel(
                row_frame,
                text=diagnosa,
                width=col_widths[1],
                anchor="w",
                font=("Arial", 13),
            ).pack(side="left", padx=(0))

            # Jenis
            ctk.CTkLabel(
                row_frame,
                text=jenis,
                width=col_widths[2],
                anchor="w",
                font=("Arial", 13),
            ).pack(side="left", padx=(0))

            # Kategori WHO-5
            badge_color = self.badge_colour(kategori)
            ctk.CTkLabel(
                row_frame,
                text=kategori,
                width=col_widths[3] - 20,
                fg_color=badge_color,
                corner_radius=6,
                font=("Arial Bold", 13),
                text_color="black",
            ).pack(side="left", padx=10)

            # Progress 2 minggu
            progress_bg = "#bbf7d0" if selesai_2minggu else "#e5e7eb"
            ctk.CTkLabel(
                row_frame,
                text=progress_label,
                width=col_widths[4] - 20,
                fg_color=progress_bg,
                corner_radius=6,
                font=("Arial Bold", 13),
                text_color="#111827",
            ).pack(side="left", padx=(10))

            # Tanggal konsul
            if tanggal_konsul:
                konsul_text = tanggal_konsul
                konsul_bg = "#bfdbfe"
            else:
                konsul_text = "-"
                konsul_bg = "#e5e7eb"

            ctk.CTkLabel(
                row_frame,
                text=konsul_text,
                width=col_widths[5],
                fg_color=konsul_bg,
                corner_radius=6,
                font=("Arial", 13),
                text_color="#111827",
            ).pack(side="left", padx=(10))

            # Aksi
            action_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
            action_frame.pack(side="left", padx=(5, 5))

            ctk.CTkButton(
                action_frame,
                text="👁",
                text_color="#01030E",
                width=32,
                height=32,
                fg_color="transparent",
                hover_color="#3B8ED0",
                command=self.create_detail_handler(row_data),
            ).pack(side="left", padx=2)

            ctk.CTkButton(
                action_frame,
                text="✏️",
                text_color="#01030E",
                width=32,
                height=32,
                fg_color="transparent",
                hover_color="#22c55e",
                command=self.create_edit_handler(row_data),
            ).pack(side="left", padx=2)

            # tombol 📅 hanya kalau sudah 14/14 dan belum ada tanggal_konsul
            if (
                selesai_2minggu and not tanggal_konsul
            ):  # selesai2minnggu true, tanggal konsul belum ada flase -> true
                ctk.CTkButton(
                    action_frame,
                    text="📅",
                    text_color="#01030E",
                    width=32,
                    height=32,
                    fg_color="transparent",
                    hover_color="#f97316",
                    command=self.create_set_konsul_handler(row_data),
                ).pack(side="left", padx=2)

    # ----- Badge warna kategori -----
    def badge_colour(self, kategori):
        k = (kategori or "").lower()

        if k in ["memadai", "hijau"]:
            return "#bbf7d0"

        if k in ["rendah", "kuning", "orange"]:
            return "#fef08a"

        if k in ["berisiko", "merah"]:
            return "#fecaca"

        return "#e5e7eb"
